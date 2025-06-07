# update crd to latest version
https://github.com/argoproj/argo-cd/blob/master/manifests/install.yaml

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d