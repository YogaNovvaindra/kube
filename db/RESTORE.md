# PostgreSQL Backup Restore Guide

Restoring from a `pg_basebackup` snapshot taken by the `db-pg-snapshots` CronJob.

## Backup Structure

Each daily backup creates a directory under the CephFS mount:

```
/mnt/cephfs/docker/db/postgres/backup/pg-snapshots/
└── postgres-backup-20260802015023/
    ├── base.tar.gz        ← full data directory (compressed)
    ├── pg_wal.tar.gz      ← WAL segments streamed during backup
    └── backup_manifest    ← checksums + metadata
```

Both `base.tar.gz` and `pg_wal.tar.gz` are required for a consistent restore.

### Reading backup metadata

```bash
tar -xzOf /mnt/cephfs/docker/db/postgres/backup/pg-snapshots/postgres-backup-<TS>/base.tar.gz backup_label
```

Example output:
```
START WAL LOCATION: 15/5C000028 (file 0000000100000015000000C5)
CHECKPOINT LOCATION: 15/5C000080
BACKUP METHOD: streamed
BACKUP FROM: primary
START TIME: 2026-08-02 01:50:05 WIB
```

---

## Option A — In-Place Restore (replaces production data)

> [!CAUTION]
> This destroys the current data directory. Do this during a maintenance window.
> All applications connecting to postgres will be unavailable until step 5 completes.

### 1. Scale down postgres

```bash
kubectl scale statefulset postgres -n db --replicas=0
kubectl get pods -n db -w   # wait until postgres-0 is gone
```

### 2. Clear data directory

```bash
# Spawn a root helper pod with access to the data hostPath
kubectl run restore-helper -n db --rm -it --restart=Never \
  --image=alpine:3.24.1 \
  --overrides='{
    "spec": {
      "nodeSelector": {"kubernetes.io/hperf": "true"},
      "volumes": [{"name":"pgdata","hostPath":{"path":"/mnt/cephfs/docker/db/postgres/data","type":"Directory"}}],
      "containers": [{"name":"h","image":"alpine:3.24.1","command":["sh"],"stdin":true,"tty":true,
        "volumeMounts":[{"name":"pgdata","mountPath":"/pgdata"}]}]
    }
  }'

# Inside the pod — clear contents (not the mountpoint itself):
rm -rf /pgdata/*
```

### 3. Extract the backup

Still inside the restore-helper pod:

```bash
BACKUP_DIR="/mnt/cephfs/docker/db/postgres/backup/pg-snapshots/postgres-backup-<TIMESTAMP>"

# Mount the backup dir too, or use the CephFS path directly if accessible
tar -xzf "${BACKUP_DIR}/base.tar.gz"    -C /pgdata
mkdir -p /pgdata/pg_wal
tar -xzf "${BACKUP_DIR}/pg_wal.tar.gz" -C /pgdata/pg_wal

# Fix ownership and permissions (critical — postgres refuses 0777 dirs)
chown -R 999:999 /pgdata
chmod 0700 /pgdata
```

### 4. Scale postgres back up

```bash
kubectl scale statefulset postgres -n db --replicas=1
kubectl logs -f -n db postgres-0 -c postgres
```

Watch for WAL recovery completing:
```
LOG:  starting backup recovery with redo LSN 15/5C000028 ...
LOG:  redo done at 15/5C0B9CF0
LOG:  database system is ready to accept connections
```

---

## Option B — Isolated Restore (safe, non-destructive)

Use this to verify a backup or inspect data without touching production.
Validated via PoC on 2026-08-02 — all 6 databases and 500+ tables restored successfully.

### 1. Extract to a separate directory

On the node (or via a root pod):

```bash
BACKUP_DIR="/mnt/cephfs/docker/db/postgres/backup/pg-snapshots/postgres-backup-<TIMESTAMP>"
RESTORE_DIR="/mnt/cephfs/docker/db/postgres/restore-test"

mkdir -p "$RESTORE_DIR"
tar -xzf "${BACKUP_DIR}/base.tar.gz"    -C "$RESTORE_DIR"
mkdir -p "$RESTORE_DIR/pg_wal"
tar -xzf "${BACKUP_DIR}/pg_wal.tar.gz" -C "$RESTORE_DIR/pg_wal"
chown -R 999:999 "$RESTORE_DIR"
chmod 0700 "$RESTORE_DIR"    # ← required, postgres rejects world-writable dirs
```

### 2. Launch a restore pod

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: pg-restore-verify
  namespace: db
spec:
  nodeSelector:
    kubernetes.io/hperf: "true"
  restartPolicy: Never
  initContainers:
    - name: fix-perms
      image: reg.ygnv.my.id/docker/alpine:3.24.1
      securityContext:
        runAsUser: 0
      command: ["sh", "-c", "chown -R 999:999 /pgdata && chmod 0700 /pgdata"]
      volumeMounts:
        - name: pgdata
          mountPath: /pgdata
  containers:
    - name: postgres
      image: reg.ygnv.my.id/docker/pgautoupgrade/pgautoupgrade:debian@sha256:6c5e519451fe7ad193678e8ad79bd9b258c8c70bbb43410a55ff3cd1a9ce0a5f
      securityContext:
        runAsUser: 999
        runAsGroup: 999
      command:
        - postgres
        - -D
        - /pgdata
        - -c
        - shared_preload_libraries=pg_stat_statements
        - -c
        - listen_addresses=*
      ports:
        - containerPort: 5432
      volumeMounts:
        - name: pgdata
          mountPath: /pgdata
  volumes:
    - name: pgdata
      hostPath:
        path: /mnt/cephfs/docker/db/postgres/restore-test
        type: Directory
EOF
```

### 3. Verify

```bash
# Wait for it to be ready
kubectl wait pod pg-restore-verify -n db --for=condition=Ready --timeout=60s

# List databases
kubectl exec -n db pg-restore-verify -- psql -U postgres -c "\l"

# Table counts per DB
kubectl exec -n db pg-restore-verify -- psql -U postgres -c "
  SELECT datname, pg_size_pretty(pg_database_size(datname)) AS size
  FROM pg_database WHERE datistemplate=false ORDER BY 2 DESC;"

# WAL position after recovery
kubectl exec -n db pg-restore-verify -- psql -U postgres -c \
  "SELECT pg_current_wal_lsn(), now();"
```

### 4. Cleanup

```bash
kubectl delete pod pg-restore-verify -n db
rm -rf /mnt/cephfs/docker/db/postgres/restore-test
```
