# Secrets Handling

- `.secrets/` is gitignored and never leaves your machine. `build.py` creates it (and the files in it) with `0700`/`0600` permissions.
- `.secrets/cloud-init.yaml` contains your **password hash**. Cloud providers expose user-data verbatim through their instance metadata service to anyone with access to the running VM — don't upload it anywhere but the provider's own server-creation flow, and delete it (`rm .secrets/cloud-init.yaml`) once the server is up if you don't need to re-provision.
- Provisioning from a shared/CI machine instead of your own laptop? Pull `credentials.yaml`'s values from a real secrets manager (Vault, `sops`+`age`, your cloud provider's secret store) instead of writing them to disk.
- [AGENTS.md](../AGENTS.md) tells AI coding agents not to read `.secrets/`. That's a convention an agent can choose to honor, not an access control — a complement to the permissions above, not a substitute.
