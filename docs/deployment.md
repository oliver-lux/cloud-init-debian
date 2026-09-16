# Deployment Guide

## 1. Secrets

```bash
python3 build.py          # first run: creates .secrets/credentials.yaml
nano .secrets/credentials.yaml
python3 build.py          # second run: writes .secrets/cloud-init.yaml
```

```bash
# SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub

# Password hash
mkpasswd -m sha-512
# or: python3 -c "import crypt; print(crypt.crypt('PW', crypt.mksalt(crypt.METHOD_SHA512)))"
```

## 2. Deploy

Paste/pass the contents of `.secrets/cloud-init.yaml` as user-data. **Don't**
also select an SSH key in the provider UI — it's already in the cloud-config.

| Provider | CLI |
|---|---|
| Hetzner | `hcloud server create --name my-server --type cx11 --image debian-12 --location nbg1 --user-data-from-file .secrets/cloud-init.yaml` |
| AWS EC2 | `aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro --key-name my-key --user-data file://.secrets/cloud-init.yaml` |
| Azure | `az vm create --name my-server --resource-group my-rg --image Debian11 --size Standard_B1s --custom-data .secrets/cloud-init.yaml` |
| DigitalOcean | `doctl compute droplet create my-server --image debian-12-x64 --size s-1vcpu-1gb --region nyc1 --user-data-file .secrets/cloud-init.yaml` |
| Other / Web UI | Create server → paste `.secrets/cloud-init.yaml` into "User Data" / "Cloud Config" / "Custom Data" |

Provider notes: Hetzner — best browser VNC console, CX11 ~€4/mo, see
[hetzner-locations.md](hetzner-locations.md). AWS — enable EC2 Serial Console
beforehand, use official Debian AMIs. Azure — Serial Console on by default,
needs a resource group. DigitalOcean — "Droplet Console" for emergency access.

## 3. Connect & verify

```bash
ssh oliver@<server-ip>          # wait 2-3 min for cloud-init on first boot

sudo ufw status verbose
sudo fail2ban-client status
docker run hello-world
sudo whoami                     # sudo should prompt for a password
```

## Troubleshooting

- **Can't SSH:** wait for cloud-init to finish, check the provider's boot/console log.
- **Locked out:** use the provider's console (VNC/Serial), log in as `oliver` with the password, fix `/etc/ssh/sshd_config.d/`.
- **Fail2Ban banned your own IP:** via console, `sudo fail2ban-client set sshd unbanip <your-ip>`.

See [security.md](security.md) for what's actually being hardened.
