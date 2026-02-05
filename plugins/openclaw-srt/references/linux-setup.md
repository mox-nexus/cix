# Linux Setup

OpenClaw + SRT on Linux using systemd and bubblewrap.

## Prerequisites

```bash
# Install bubblewrap and socat (required for SRT)
# Debian/Ubuntu:
sudo apt install bubblewrap socat

# Fedora/RHEL:
sudo dnf install bubblewrap socat

# Arch:
sudo pacman -S bubblewrap socat

# Verify
bwrap --version
socat -V
```

## Check Kernel Support

```bash
# bubblewrap needs unprivileged user namespaces
cat /proc/sys/kernel/unprivileged_userns_clone

# If 0, enable it:
sudo sysctl -w kernel.unprivileged_userns_clone=1

# Make permanent:
echo 'kernel.unprivileged_userns_clone=1' | sudo tee /etc/sysctl.d/99-userns.conf
```

## Setup Steps

### 1. Create SRT Config

Same as macOS - copy template to `~/.srt-settings.json`.

### 2. Install OpenClaw Daemon

```bash
# Install daemon (creates systemd user service)
openclaw daemon install

# Check generated service
cat ~/.config/systemd/user/openclaw-gateway.service
```

### 3. Stop and Modify Service

```bash
# Stop
systemctl --user stop openclaw-gateway

# Edit service file
nano ~/.config/systemd/user/openclaw-gateway.service
```

Change `ExecStart` line from:
```ini
ExecStart=/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789
```

To:
```ini
ExecStart=/usr/local/bin/srt --settings /home/youruser/.srt-settings.json -- /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789
```

Also update PATH:
```ini
Environment="PATH=/home/youruser/.local/bin:/usr/local/bin:/usr/bin:/bin"
```

### 4. Reload and Start

```bash
# Reload systemd
systemctl --user daemon-reload

# Enable auto-start
systemctl --user enable openclaw-gateway

# Start
systemctl --user start openclaw-gateway

# Check status
systemctl --user status openclaw-gateway
```

### 5. Enable Linger (for servers)

By default, user services stop when you log out. For always-on:

```bash
# Enable linger
loginctl enable-linger $USER

# Verify
loginctl show-user $USER | grep Linger
```

## Service Commands

```bash
# Status
systemctl --user status openclaw-gateway

# Start/Stop/Restart
systemctl --user start openclaw-gateway
systemctl --user stop openclaw-gateway
systemctl --user restart openclaw-gateway

# View logs
journalctl --user -u openclaw-gateway -f

# Logs since boot
journalctl --user -u openclaw-gateway -b
```

## Linux vs macOS Differences

| Aspect | macOS | Linux |
|--------|-------|-------|
| Service manager | launchd | systemd |
| Config location | `~/Library/LaunchAgents/*.plist` | `~/.config/systemd/user/*.service` |
| Sandbox tool | sandbox-exec | bubblewrap |
| Network isolation | Proxy only | Network namespace + proxy |
| Always-on | Default | Requires `loginctl enable-linger` |

## Troubleshooting

### Service won't start

```bash
# Check logs
journalctl --user -u openclaw-gateway -n 50

# Test SRT manually
srt --settings ~/.srt-settings.json -- echo "sandbox works"
```

### Permission denied from bubblewrap

```bash
# Check user namespaces
cat /proc/sys/kernel/unprivileged_userns_clone

# If 0, enable:
sudo sysctl -w kernel.unprivileged_userns_clone=1
```

### Service stops on logout

```bash
loginctl enable-linger $USER
```

### Missing socat

SRT on Linux requires socat for Unix socket bridging:
```bash
sudo apt install socat
```
