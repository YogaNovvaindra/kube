# How to Manually Delete Provisioned Alerts from Grafana Database

If alerts are "stuck" in the Grafana UI labeled as **Provisioned** even after the YAML source file is removed, they are orphaned in the internal database. This guide explains how to purge them.

## 1. Prerequisites

- Access to the `grafana.db` file (SQLite).
- `sqlite3` CLI installed on your machine.

## 2. Identify the Target UIDs

List all alerts with their UIDs to find the ones you want to delete:

```bash
sqlite3 grafana.db "SELECT uid, title FROM alert_rule;"
```

## 3. Verify Provenance

Provisioned alerts are usually locked with a `file` provenance, which prevents deletion via the API.

```bash
sqlite3 grafana.db "SELECT * FROM provenance_type WHERE record_key = 'YOUR_ALERT_UID_HERE';"
```

## 4. Execute Deletion (Transactional)

To maintain database integrity, delete the alert from all related tables in a single transaction.

> [!CAUTION]
> Always backup your `grafana.db` before running destructive queries.

```sql
-- Replace 'UID1', 'UID2' with your target UIDs
BEGIN TRANSACTION;

DELETE FROM provenance_type WHERE record_type = 'alertRule' AND record_key IN ('UID1', 'UID2');
DELETE FROM alert_rule WHERE uid IN ('UID1', 'UID2');
DELETE FROM alert_instance WHERE rule_uid IN ('UID1', 'UID2');
DELETE FROM alert_rule_version WHERE rule_uid IN ('UID1', 'UID2');
DELETE FROM alert_rule_state WHERE rule_uid IN ('UID1', 'UID2');

COMMIT;
```

## 5. Sync Grafana

After modifying the database:

1.  **Restart Grafana**: This forces the scheduler and cache to reload from the database.
    ```bash
    kubectl rollout restart deployment grafana -n monitoring
    ```
2.  (Optional) **Trigger Reload via API**:
    ```bash
    curl -X POST -u user:pass http://grafana-url/api/admin/provisioning/alerting/reload
    ```
