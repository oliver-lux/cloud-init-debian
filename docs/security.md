# Security Hardening Details

What `templates/cloud-init.template.yaml` locks down, and why. Line numbers refer
to that file.

## User Setup (Lines 14-22)

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

## SSH Hardening (Lines 51-68)

```yaml
PasswordAuthentication no        # No password SSH login
PermitRootLogin prohibit-password  # Root cannot login via SSH
PubkeyAuthentication yes
MaxAuthTries 3                   # Only 3 login attempts
```

## Fail2Ban (Lines 71-84)

```yaml
maxretry: 3      # Ban after 3 failed attempts
bantime: 1h      # Ban duration: 1 hour
findtime: 10m    # Time window (default)
```

Unban an IP from the provider console if you get locked out:

```bash
sudo fail2ban-client set sshd unbanip <your-ip>
```

## Auto-Reboot for Updates (Lines 88-100)

```yaml
Unattended-Upgrade::Automatic-Reboot "true"
Unattended-Upgrade::Automatic-Reboot-Time "03:00"  # 3 AM
```

**⚠️ Warning:** Server reboots automatically at 3 AM if kernel updates require it!

## Kernel Hardening (Lines 110-138)

- SYN flood protection
- IP spoofing protection
- ICMP redirects blocked
- Kernel pointers hidden

## Docker Security (Lines 141-155)

```yaml
"no-new-privileges": true     # Containers can't gain privileges
"icc": false                  # Inter-container communication disabled
"userland-proxy": false       # Direct iptables rules
```

## Summary

1. **No SSH Key in Provider UI:** Most cloud providers offer an SSH key option during server creation. Do NOT select it if your key is already in cloud-config (duplicates can cause issues).
2. **Root is disabled:** Only `oliver` can log in.
3. **sudo requires password:** Even with SSH key access.
4. **Auto-reboot at 3 AM:** If kernel updates need it.
5. **Console access:** Every major cloud provider offers emergency console access (VNC/Serial) if SSH breaks.
