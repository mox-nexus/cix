# Linux Setup

## Prerequisites

| Tool | Debian/Ubuntu | Fedora | Arch |
|------|---------------|--------|------|
| bubblewrap | `apt install bubblewrap` | `dnf install bubblewrap` | `pacman -S bubblewrap` |
| socat | `apt install socat` | `dnf install socat` | `pacman -S socat` |
| Node.js 22+ | NodeSource/nvm | dnf module | `pacman -S nodejs` |

## Kernel Requirement

```bash
# Check
cat /proc/sys/kernel/unprivileged_userns_clone

# Enable if 0
sudo sysctl -w kernel.unprivileged_userns_clone=1
echo 'kernel.unprivileged_userns_clone=1' | sudo tee /etc/sysctl.d/99-userns.conf
```

## Steps

### 1. SRT Config

Same as macOS: `cp template to ~/.srt-settings.json`

### 2. Install Daemon

```bash
openclaw daemon install
cat ~/.config/systemd/user/openclaw-gateway.service
```

### 3. Modify Service

```bash
systemctl --user stop openclaw-gateway
nano ~/.config/systemd/user/openclaw-gateway.service
```

Change `ExecStart`:
```ini
ExecStart=/usr/local/bin/srt --settings /home/USER/.srt-settings.json -- /usr/bin/node ... gateway --port 18789
```

### 4. Start

```bash
systemctl --user daemon-reload
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway
```

### 5. Enable Linger (for always-on)

```bash
loginctl enable-linger $USER
```

## Service Commands

| Task | Command |
|------|---------|
| Status | `systemctl --user status openclaw-gateway` |
| Restart | `systemctl --user restart openclaw-gateway` |
| Logs | `journalctl --user -u openclaw-gateway -f` |

## Linux vs macOS

| Aspect | macOS | Linux |
|--------|-------|-------|
| Service | launchd | systemd |
| Sandbox | sandbox-exec | bubblewrap |
| Network | Proxy only | Network namespace + proxy |
| Always-on | Default | Requires linger |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Permission denied | `sudo sysctl -w kernel.unprivileged_userns_clone=1` |
| Service stops on logout | `loginctl enable-linger $USER` |
| Missing socat | `apt install socat` |
