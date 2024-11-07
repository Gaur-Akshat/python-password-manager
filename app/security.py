# app/security.py
from cryptography.fernet import Fernet
import os

key = os.getenv('ENCRYPTION_KEY', 'fSsPqQ3Hf7hK9Av8GfyMaDjw6y2X3y4E0u9yGvDJuTw=').encode()
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()
