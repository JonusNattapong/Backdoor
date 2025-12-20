"""
Encryption and decryption utilities using AES-256-CBC.
"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from config import Config


class CryptoManager:
    """AES encryption with unique session keys"""

    @staticmethod
    def generate_key() -> bytes:
        """Generate random AES key"""
        return os.urandom(32)

    @staticmethod
    def encrypt(data: bytes, key: bytes = None) -> bytes:
        """Encrypt data with AES-256-CBC"""
        if key is None:
            key = Config.MASTER_KEY

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # Pad the data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return iv + encrypted

    @staticmethod
    def decrypt(data: bytes, key: bytes = None) -> bytes:
        """Decrypt AES-256-CBC data"""
        if key is None:
            key = Config.MASTER_KEY

        iv = data[:16]
        encrypted = data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(encrypted) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()