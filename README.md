# Hardened Cloud Server Configuration

Secure cloud-init configuration for Debian servers on any cloud provider, focused on security automation.

**Tested on:** AWS EC2, Azure, Hetzner Cloud, DigitalOcean, Linode, Vultr

- **Security:** SSH key-only auth, UFW firewall, Fail2Ban, kernel hardening, auto-updates
- **Docker:** pre-hardened daemon (no-new-privileges, ICC disabled)
- **Automation:** fully set up via cloud-init, no manual steps after boot

## Quick Start

```bash
python3 build.py                    # 1st run: creates .secrets/credentials.yaml
nano .secrets/credentials.yaml      # fill in SSH key + password hash
python3 build.py                    # 2nd run: writes .secrets/cloud-init.yaml

hcloud server create --name my-server --type cx11 --image debian-12 \
  --location nbg1 --user-data-from-file .secrets/cloud-init.yaml

ssh oliver@<server-ip>
```

Root login is disabled; only `oliver` (SSH key-only) can log in, sudo still asks for a password.

→ **[Full deployment guide](docs/deployment.md)** (all providers, verification, troubleshooting)
→ **[Security hardening details](docs/security.md)** (what's locked down and why)
→ **[Secrets handling](docs/secrets.md)** (where credentials live, permissions, AI-agent access)

## Project Structure

```
cloud-hetzner/
├── build.py                       # generates the deployable config
├── templates/
│   ├── cloud-init.template.yaml       # tracked template ({{PLACEHOLDER}}s only)
│   └── credentials.example.yaml
├── docs/                          # deployment.md, security.md, secrets.md, hetzner-locations.md
└── .secrets/                      # gitignored, created by build.py
    ├── credentials.yaml
    └── cloud-init.yaml
```

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2025 Oliver Lux
