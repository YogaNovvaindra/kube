# 🔐 Kubeseal UI

Web interface for inspecting and sealing Kubernetes SealedSecrets across
namespaces. Reads `bitnami.com/v1alpha1` SealedSecrets cluster-wide and
renders them in a Vue frontend served by nginx.

## 📂 Contents

| File | Kind | Purpose |
| --- | --- | --- |
| `kubeseal-ui.yml` | plain Kubernetes manifests (SA, ClusterRole, ClusterRoleBinding, 2 Services, 2 Deployments) | Live object definitions |
| `ingressroute.yml` | Traefik `IngressRoute` | `sealer.ygnv.my.id` -> UI + `/api` -> API |
| `kubeseal-cred.yml` | `SealedSecret` template | OIDC client secret + GitHub PAT (gitops token) |

Hand-written plain YAML, mirroring the style of `cluster/keel/keel.yml`
(`app:` labels, explicit `namespace: cluster`, Harbor images, credential
mounted from a SealedSecret). The source of truth for this manifest is the
`kubeseal-ui` Helm chart under `charts/` — the chart encodes the security
posture, but this folder commits plain manifests rather than chart
templates.

## 📦 Resources

| Kind | Name | Notes |
| --- | --- | --- |
| `ServiceAccount` | `kubeseal-ui-api` | Identity for the API pod |
| `ClusterRole` | `kubeseal-ui-api` | `get`/`list`/`watch` on `sealedsecrets`; `get`/`list` on `namespaces` |
| `ClusterRoleBinding` | `kubeseal-ui-api` | Binds the role to the API ServiceAccount |
| `Service` | `kubeseal-ui-api` | ClusterIP `:8080` |
| `Service` | `kubeseal-ui` | ClusterIP `:80` (UI) |
| `Deployment` | `kubeseal-ui-api` | `reg.ygnv.my.id/ghcr/kubeseal-ui/api:dev` |
| `Deployment` | `kubeseal-ui` | `reg.ygnv.my.id/ghcr/kubeseal-ui/frontend:dev` |

## 🖼️ Images

Mirrored through Harbor with the moving `dev` tag:

- API: `reg.ygnv.my.id/ghcr/kubeseal-ui/api:dev`
- UI:  `reg.ygnv.my.id/ghcr/kubeseal-ui/frontend:dev`

`imagePullPolicy: IfNotPresent`. Re-render (or replace the tag) with
pinned tags/digests before relying on this in production.

## 🔑 OIDC

- Issuer: `https://auth.ygnv.my.id/application/o/kubeseal-ui/` (Authentik)
- Client id: `kubeseal-ui`
- Client secret: mounted from the `kubeseal-cred` Secret (see below)

## 🔐 Credential (`kubeseal-cred`)

`kubeseal-cred.yml` is a **SealedSecret template** holding two keys:

| Key | Purpose |
| --- | --- |
| `OIDC_CLIENT_SECRET` | Authentik confidential client secret — consumed as env `valueFrom.secretKeyRef` |
| `token` | GitHub PAT — mounted at `/var/run/secrets/git/platform/token` for GitOps push |

The API consumes them as:

```yaml
env:
  - name: OIDC_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: kubeseal-cred
        key: OIDC_CLIENT_SECRET
```

```yaml
volumeMounts:
  - name: git-credentials
    mountPath: /var/run/secrets/git/platform
    readOnly: true
volumes:
  - name: git-credentials
    secret:
      secretName: kubeseal-cred
```

It is intentionally **not** listed in the parent `cluster/kustomization.yaml`
`resources:` so it is never applied with placeholder bytes. To activate:

```bash
kubectl create secret generic kubeseal-cred \
  --namespace cluster \
  --from-literal=OIDC_CLIENT_SECRET='<authentik-application-client-secret>' \
  --from-literal=token='<github-personal-access-token>' \
  --dry-run=client -o json \
  | kubeseal --format yaml --namespace cluster > cluster/kubeseal-ui/kubeseal-cred.yml
```

Then add `- kubeseal-ui/kubeseal-cred.yml` to the parent `cluster/kustomization.yaml` `resources:` and commit.

`ENABLE_DECRYPT` is `true` (decrypt enabled, reads controller key from `cluster` namespace) and `GITOPS_ENABLED`
is `true` (Git push enabled for `cluster` namespace → `YogaNovvaindra/kube:main` at `cluster/sealed-secrets/{name}.yaml`).

## 📁 Target Directory Selection (Namespace-Based)

The UI supports selecting the target directory when creating new sealed secrets. Access is controlled **by namespace** — if a user has `gitops:push` capability in a namespace, they can write to **any path that namespace's mapping allows**.

### Configuration (in `values.cluster.gitops.yaml`)

```yaml
api:
  gitops:
    namespaces:
      - namespace: cluster
        pathTemplate: cluster/sealed-secrets/{name}.yaml
        allowedPaths:           # ALL valid paths for this namespace
          - cluster/sealed-secrets/
          - cluster/kubeseal-ui/
          - cluster/sealed-secret/
        authRef: github
        mode: direct
      - namespace: payments
        pathTemplate: clusters/payments/{name}.yaml
        allowedPaths:
          - clusters/payments/
        authRef: github
        mode: direct
```

### How it works

| User has `gitops:push` in namespace | Can write to paths |
|---|---|
| `cluster` | `cluster/sealed-secrets/`, `cluster/kubeseal-ui/`, `cluster/sealed-secret/` |
| `payments` | `clusters/payments/` |

### Runtime behavior

1. **`GET /api/v1/gitops/paths`** → returns `allowed_paths` for **all namespaces** (user's namespace access is controlled by RBAC on the secret itself)
2. **UI** shows a **Target directory** dropdown with the `allowedPaths` from the selected secret's namespace
3. **Server validates** `target_path` against that namespace's `allowedPaths` via `IsPathAllowed()`
4. **Admin onboarding**: Admin adds namespace mapping with `allowedPaths`, then grants users `gitops:push` capability for that namespace via Authentik groups → kube RBAC

### Frontend

The "Create new SealedSecret" panel shows a **Target directory** dropdown populated from `/gitops/paths` for the current namespace. The selected `target_path` is sent with encrypt/dry-run/deliver requests and validated server-side against that namespace's `allowedPaths`.

## 🚀 Activation

This folder is already referenced by the parent `cluster/kustomization.yaml`:

```yaml
resources:
  - sealed-secret
  - kubeseal-ui/kubeseal-ui.yml
  - kubeseal-ui/ingressroute.yml
  - reloader
  - keel/keel.yml
  - keel/keel-cred.yml
  - keel/notification.yml
```

The `cluster` ArgoCD app (`gitops/cluster.yml`) syncs `cluster/` with
`automated + prune + selfHeal`, so committing this folder deploys it.

> ⚠️ `kubeseal-cred.yml` is a **template** with placeholder `encryptedData`.
> It is intentionally **not** listed in the parent `resources:` so it won't
> be applied with placeholder bytes. After you seal the real credentials,
> add `- kubeseal-ui/kubeseal-cred.yml` to the parent `resources:` list.