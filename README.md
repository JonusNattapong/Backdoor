# backdoor-cassandra Framework

A comprehensive, multi-protocol backdoor-cassandra implementation for research and educational purposes. This framework demonstrates persistence, stealth, and communication techniques used in modern malware.

> **⚠️ WARNING: This is for educational and research purposes only. Using this software for malicious activities is illegal and unethical.**

## Features

### Multi-Protocol Communication
- **HTTPS**: Encrypted communication via REST API
- **DNS Tunneling**: Covert data exfiltration through DNS queries
- **Telegram Bot**: Command and control via Telegram messages
- **Discord Webhook**: Real-time notifications and commands
- **Gmail SMTP**: Email-based communication channel

### Cross-Platform Persistence
- **Windows**: Registry keys, scheduled tasks, services, startup folder, WMI
- **Linux**: Cron jobs, systemd services, rc.local, profile scripts, SSH keys
- **macOS**: Launch agents, cron, login items

### Stealth and Anti-Analysis
- Environment detection (debuggers, virtual machines, sandboxes)
- Process hiding capabilities
- Encrypted communications
- Data compression
- Timing-based evasion techniques

### Modular Architecture
- **Shell Module**: Execute system commands
- **File Manager**: Upload/download/delete files
- **Keylogger**: Capture keystrokes
- **Screenshot**: Capture screen images
- **Browser Stealer**: Extract browser data (passwords, cookies, history)
- **Password Dumper**: Extract system credentials
- **Network Scanner**: Discover hosts and open ports
- **Privilege Escalation**: Attempt to gain higher privileges
- **Lateral Movement**: Spread to other systems
- **Ransomware**: File encryption/decryption (educational only)

## Building

```bash
cargo build --release
```

## Running

```bash
cargo run
```

## Configuration

The backdoor-cassandra is configured via `config.toml` file in the project root.

### Configuration File

Create a `config.toml` file with your settings:

```toml
[beacon]
interval = 30
jitter = 0.3

[communication.https]
host = "c2.example.com"
port = 443
path = "/api/beacon"

[communication.telegram]
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_TELEGRAM_CHAT_ID"

[communication.discord]
webhook_url = "https://discord.com/api/webhooks/xxx"

[communication.gmail]
email = "backdoor-cassandra.receiver@gmail.com"
app_password = "YOUR_GMAIL_APP_PASSWORD"

[security]
encrypt_comms = true
compress_data = true
hide_process = true

[modules]
enabled = ["shell", "file_manager", "keylogger", "screenshot"]
```

## Disclaimer

This software is provided for educational and research purposes only. The authors are not responsible for any misuse or illegal activities performed with this software.
