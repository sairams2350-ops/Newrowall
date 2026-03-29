# NeuroWall Agent Setup Guide

## Overview

NeuroWall agents run on endpoints (Windows/Linux) and provide kernel-level packet filtering. This guide covers installation, configuration, and operation.

## Windows Agent

### Prerequisites

- Windows 10/11 or Windows Server 2016+
- Administrator privileges
- Rust toolchain (for building from source)
- Or use pre-built binaries

### Installation

#### Option 1: Pre-built Binary

1. Download the Windows agent binary
2. Extract to `C:\Program Files\NeuroWall\`
3. Create configuration file (see below)

#### Option 2: Build from Source

```powershell
# Install Rust
# Download from https://rustup.rs/

# Clone repository
git clone <repository-url>
cd neurowall/agent/windows

# Build
cargo build --release

# Binary will be at: target\release\neurowall-agent-windows.exe
```

### Configuration

Create `config.json` in the agent directory:

```json
{
  "device_id": "windows-workstation-001",
  "server_url": "http://localhost:8000",
  "grpc_endpoint": "http://localhost:50051",
  "api_endpoint": "http://localhost:8000/api/v1",
  "policy_cache_path": "C:\\ProgramData\\NeuroWall\\policy_cache.json",
  "log_level": "info",
  "heartbeat_interval_secs": 30,
  "telemetry_batch_size": 100,
  "telemetry_flush_interval_secs": 5
}
```

### Running as Service

#### Using NSSM (Non-Sucking Service Manager)

1. Download NSSM from https://nssm.cc/
2. Install service:
```powershell
nssm install NeuroWallAgent "C:\Program Files\NeuroWall\neurowall-agent-windows.exe"
nssm set NeuroWallAgent AppDirectory "C:\Program Files\NeuroWall"
nssm set NeuroWallAgent AppStdout "C:\Program Files\NeuroWall\stdout.log"
nssm set NeuroWallAgent AppStderr "C:\Program Files\NeuroWall\stderr.log"
nssm start NeuroWallAgent
```

#### Using Windows Service (PowerShell)

```powershell
$service = New-Service -Name "NeuroWallAgent" `
  -BinaryPathName "C:\Program Files\NeuroWall\neurowall-agent-windows.exe" `
  -DisplayName "NeuroWall Agent" `
  -StartupType Automatic

Start-Service NeuroWallAgent
```

### Windows Filtering Platform (WFP)

The agent uses WFP for kernel-level filtering:

- **Callouts**: Custom packet inspection
- **Filters**: Rule-based filtering
- **Layers**: Network and transport layers

**Requirements:**
- Administrator privileges
- WFP driver support
- Network adapter access

### Troubleshooting

1. **Agent won't start:**
   - Check administrator privileges
   - Verify WFP is available
   - Check logs in `stdout.log` and `stderr.log`

2. **No policy updates:**
   - Verify gRPC connectivity
   - Check backend is running
   - Verify device registration

3. **High CPU usage:**
   - Review telemetry batch size
   - Check network activity
   - Optimize rule count

## Linux Agent

### Prerequisites

- Linux kernel 5.8+ (for eBPF features)
- Root/sudo privileges
- Rust toolchain (for building)
- eBPF tools (bpftool, etc.)

### Installation

#### Option 1: Pre-built Binary

1. Download Linux agent binary
2. Extract to `/usr/local/bin/`
3. Create configuration (see below)

#### Option 2: Build from Source

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone repository
git clone <repository-url>
cd neurowall/agent/linux

# Build
cargo build --release

# Install
sudo cp target/release/neurowall-agent-linux /usr/local/bin/
sudo chmod +x /usr/local/bin/neurowall-agent-linux
```

### Configuration

Create `/etc/neurowall/config.json`:

```json
{
  "device_id": "linux-server-001",
  "server_url": "http://localhost:8000",
  "grpc_endpoint": "http://localhost:50051",
  "api_endpoint": "http://localhost:8000/api/v1",
  "policy_cache_path": "/var/lib/neurowall/policy_cache.json",
  "log_level": "info",
  "heartbeat_interval_secs": 30,
  "telemetry_batch_size": 100,
  "telemetry_flush_interval_secs": 5
}
```

Create directories:
```bash
sudo mkdir -p /etc/neurowall /var/lib/neurowall
sudo chmod 755 /etc/neurowall /var/lib/neurowall
```

### Systemd Service

Create `/etc/systemd/system/neurowall-agent.service`:

```ini
[Unit]
Description=NeuroWall Agent
Documentation=https://github.com/yourorg/neurowall
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/neurowall-agent-linux
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable neurowall-agent
sudo systemctl start neurowall-agent

# Check status
sudo systemctl status neurowall-agent

# View logs
sudo journalctl -u neurowall-agent -f
```

### eBPF Integration

The Linux agent uses eBPF for packet filtering:

- **XDP**: Fast packet processing
- **TC (Traffic Control)**: Network filtering
- **Netlink**: Connection monitoring

**Requirements:**
- Kernel 5.8+ with eBPF support
- Root privileges
- eBPF programs loaded into kernel

### Troubleshooting

1. **Agent won't start:**
   - Check kernel version: `uname -r`
   - Verify eBPF support: `ls /sys/fs/bpf/`
   - Check logs: `journalctl -u neurowall-agent`

2. **eBPF program errors:**
   - Verify kernel supports required features
   - Check `/sys/kernel/debug/tracing/`
   - Review eBPF verifier logs

3. **Network issues:**
   - Verify Netlink socket permissions
   - Check firewall rules
   - Review network interface configuration

## Common Configuration

### Device ID

The `device_id` uniquely identifies the endpoint:
- Auto-generated UUID (default)
- Custom identifier (recommended for production)
- Format: alphanumeric with hyphens

### Policy Cache

The policy cache stores rules locally:
- JSON format
- Updated on heartbeat
- Verified with signature
- Location: Configurable via `policy_cache_path`

### Telemetry Batching

Telemetry is batched for efficiency:
- **Batch Size**: Number of entries before sending (default: 100)
- **Flush Interval**: Time-based flush (default: 5 seconds)
- **Network Efficiency**: Reduces API calls

### Heartbeat

Agents send heartbeats to backend:
- **Interval**: Default 30 seconds
- **Purpose**: Device status, policy updates
- **Failure**: Agent retries connection

## Security Considerations

### Agent Authentication

- Device registration required
- gRPC mutual TLS (production)
- Policy signature verification

### Policy Security

- HMAC-SHA256 signatures
- Signature verification on receipt
- Reject invalid policies

### Network Security

- Use TLS for production
- VPN for agent communication (optional)
- Firewall rules for backend access

## Performance Tuning

### CPU Usage

- Reduce telemetry batch size if needed
- Optimize rule count
- Review network activity

### Memory Usage

- Policy cache size (typically < 1MB)
- Telemetry buffer (configurable)
- Baseline storage (ML engine)

### Network Usage

- Adjust batch size and flush interval
- Compress telemetry (future enhancement)
- Use efficient serialization

## Monitoring

### Agent Health

- Heartbeat status in dashboard
- Last seen timestamp
- Connection status

### Logs

- Windows: Check service logs
- Linux: `journalctl -u neurowall-agent`
- Log levels: debug, info, warn, error

### Metrics

Monitor:
- CPU usage
- Memory usage
- Network traffic
- Policy update frequency
- Telemetry send rate

## Updating Agents

1. Stop the agent service
2. Backup configuration
3. Replace binary
4. Restart service
5. Verify connectivity

## Uninstallation

### Windows

```powershell
# Stop service
Stop-Service NeuroWallAgent

# Remove service
nssm remove NeuroWallAgent confirm

# Or using sc
sc delete NeuroWallAgent

# Remove files
Remove-Item "C:\Program Files\NeuroWall" -Recurse
```

### Linux

```bash
# Stop service
sudo systemctl stop neurowall-agent

# Disable service
sudo systemctl disable neurowall-agent

# Remove service file
sudo rm /etc/systemd/system/neurowall-agent.service
sudo systemctl daemon-reload

# Remove binary
sudo rm /usr/local/bin/neurowall-agent-linux

# Remove configuration (optional)
sudo rm -rf /etc/neurowall /var/lib/neurowall
```

---

**Last Updated:** 2024

