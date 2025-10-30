# Hardened Cloud Server Configuration

Secure cloud-init configuration for Debian servers on any cloud provider with focus on security automation and best practices.

**Tested on:** AWS EC2, Azure, Hetzner Cloud, DigitalOcean, Linode, Vultr

## Features

- **Security:** SSH key-only auth, UFW firewall, Fail2Ban, kernel hardening, auto-updates
- **Docker:** Pre-configured with security settings (no-new-privileges, ICC disabled)
- **Automation:** Fully automated setup via cloud-init
- **Minimal:** Clean Debian base with essential tools only
- **Universal:** Works on any cloud provider supporting cloud-init

## Quick Start

### 1. Setup Secrets

```bash
# Run build script (auto-creates credentials file on first run)
python3 build_config.py

# Edit credentials
nano .private/credentials.yaml
```

**Generate SSH Key:**
```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub  # Copy this to credentials.yaml
```

**Generate Password Hash:**
```bash
mkpasswd -m sha-512
# Or with Python:
python3 -c "import crypt; print(crypt.crypt('YOUR_PASSWORD', crypt.mksalt(crypt.METHOD_SHA512)))"
```

### 2. Build Configuration

```bash
python3 build_config.py
# Output: .private/cloud-config-ready.yaml
```

### 3. Deploy to Cloud Provider

#### Hetzner Cloud

```bash
# Via Hetzner CLI
hcloud server create \
  --name my-server \
  --type cx11 \
  --image debian-12 \
  --location nbg1 \
  --user-data-from-file .private/cloud-config-ready.yaml
```

**Web UI:**
1. Create new server at [Hetzner Cloud Console](https://console.hetzner.cloud)
2. Under "Cloud config" paste contents of `.private/cloud-config-ready.yaml`
3. **Important:** Do NOT select SSH key in provider UI (already in cloud-config)
4. Create server

#### AWS EC2

```bash
# Via AWS CLI
aws ec2 run-instances \
  --image-id ami-0123456789 \
  --instance-type t3.micro \
  --key-name my-key \
  --user-data file://.private/cloud-config-ready.yaml
```

#### Azure

```bash
# Via Azure CLI
az vm create \
  --name my-server \
  --resource-group my-rg \
  --image Debian11 \
  --size Standard_B1s \
  --custom-data .private/cloud-config-ready.yaml
```

#### DigitalOcean

```bash
# Via doctl
doctl compute droplet create my-server \
  --image debian-12-x64 \
  --size s-1vcpu-1gb \
  --region nyc1 \
  --user-data-file .private/cloud-config-ready.yaml
```

#### Universal (Web Interface)

Most cloud providers support cloud-init user-data:
1. Create new server/VM/droplet
2. Look for "User Data", "Cloud Config", or "Custom Data" option
3. Paste contents of `.private/cloud-config-ready.yaml`
4. **Important:** Do NOT select SSH key in UI if option exists (already in cloud-config)
5. Create server

### 4. Connect

```bash
ssh oliver@<server-ip>
```

## Critical Security Configuration

### User Setup (cloud-config.yaml Lines 8-17)

```yaml
users:
  - name: oliver
    sudo: ALL=(ALL) ALL          # sudo requires password
    lock_passwd: false           # password for sudo only
    hashed_passwd: "{{...}}"     # password hash required
    ssh_authorized_keys: [...]   # SSH key-only login
```

**⚠️ Critical:**
- Root user is DISABLED (no direct root login)
- SSH login: Key-only (password disabled via `ssh_pwauth: false`)
- sudo: Requires password authentication (security layer)
- Emergency access: Cloud provider console (VNC/Serial)

### SSH Hardening (Lines 22-33)

```yaml
PasswordAuthentication no        # No password SSH login
PermitRootLogin prohibit-password  # Root cannot login via SSH
PubkeyAuthentication yes
MaxAuthTries 3                   # Only 3 login attempts
```

### Fail2Ban (Lines 35-40)

```yaml
maxretry: 3      # Ban after 3 failed attempts
bantime: 1h      # Ban duration: 1 hour
findtime: 10m    # Time window (default)
```

### Auto-Reboot for Updates (Lines 42-47)

```yaml
Unattended-Upgrade::Automatic-Reboot "true"
Unattended-Upgrade::Automatic-Reboot-Time "03:00"  # 3 AM
```

**⚠️ Warning:** Server reboots automatically at 3 AM if kernel updates require it!

### Kernel Hardening (Lines 49-60)

- SYN flood protection
- IP spoofing protection
- ICMP redirects blocked
- Kernel pointers hidden

### Docker Security (Lines 62-71)

```yaml
"no-new-privileges": true     # Containers can't gain privileges
"icc": false                  # Inter-container communication disabled
"userland-proxy": false       # Direct iptables rules
```

## Post-Deployment

### Verify Setup

```bash
# SSH connection works
ssh oliver@<server-ip>

# Check firewall
sudo ufw status verbose

# Check Fail2Ban
sudo fail2ban-client status

# Test Docker
docker ps
docker run hello-world

# Test sudo (requires password)
sudo whoami
```

### Emergency Access

If SSH fails, use your cloud provider's console:

**Hetzner Cloud:** Browser-based VNC via [Cloud Console](https://console.hetzner.cloud)
**AWS EC2:** EC2 Serial Console or Session Manager
**Azure:** Azure Serial Console
**DigitalOcean:** Droplet Console
**Others:** Check provider documentation for console access

Then:
1. Login as `oliver` with your password
2. Debug: `sudo systemctl status ssh`
3. Fix SSH configuration if needed

## File Structure

```
cloud-hetzner/
├── README.md                          # This file
├── cloud-config.yaml                  # Main config template
├── credentials.yaml.example           # Secrets template
├── build_config.py                    # Build script
├── hetzner-data-centers.txt          # Hetzner locations reference
├── .private/
│   ├── credentials.yaml              # Your secrets (gitignored)
│   └── cloud-config-ready.yaml       # Generated config (gitignored)
└── .gitignore                         # Protects secrets
```

## Important Notes

1. **No SSH Key in Provider UI:** Most cloud providers have an SSH key option during server creation. Do NOT select it if your key is already in cloud-config (duplicates can cause issues).
2. **Root is disabled:** Only `oliver` user can login
3. **sudo requires password:** Even with SSH key access
4. **Auto-reboot at 3 AM:** If kernel updates need it
5. **Console Access:** Every major cloud provider offers emergency console access (VNC/Serial)

## Common Issues

**Problem: Can't SSH into server**
- Wait 2-3 minutes for cloud-init to complete
- Check cloud provider console for setup status
- Use console access as fallback

**Problem: Locked out after SSH key change**
- Use provider console to login
- Update `~/.ssh/authorized_keys` manually

**Problem: Fail2Ban banned my IP**
```bash
# Via provider console:
sudo fail2ban-client set sshd unbanip <your-ip>
```

## Cloud Provider Notes

### Hetzner Cloud
- Data center locations: See `hetzner-data-centers.txt`
- Console access: Excellent browser-based VNC
- Cost: CX11 ~€4/month

### AWS EC2
- Region selection important for latency
- Enable EC2 Serial Console in account settings
- Use Debian official AMIs

### Azure
- Use Debian images from marketplace
- Serial Console available by default
- Resource groups required

### DigitalOcean
- "Droplet Console" for emergency access
- Simple pricing, good for testing
- Multiple datacenter options

## License

MIT License - see [LICENSE](LICENSE) file for details

Copyright (c) 2025 Oliver Lux
