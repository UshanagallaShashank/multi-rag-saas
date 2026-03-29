from cryptography.fernet import Fernet

from ..config import settings

def _fernet() -> Fernet:
    # Build Fernet instance from config key
    return Fernet(settings.encryption_key.encode())

def encrypt(value: str) -> str:
    # Encrypt plaintext string, return ciphertext string
    return _fernet().encrypt(value.encode()).decode()

def decrypt(token: str) -> str:
    # Decrypt ciphertext string, return plaintext string
    return _fernet().decrypt(token.encode()).decode()
