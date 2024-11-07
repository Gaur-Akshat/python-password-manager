# app/manager.py
from app.models import PasswordEntry
from app.security import encrypt_password, decrypt_password

def create_password_entry(service_name, username, password):
    encrypted_password = encrypt_password(password)
    PasswordEntry.add_entry(service_name, username, encrypted_password)

def get_all_entries():
    return PasswordEntry.get_all_entries()

def get_password_by_id(entry_id):
    entry = PasswordEntry.get_entry_by_id(entry_id)
    if entry:
        encrypted_password = entry[1]
        service_name = entry[2]
        username = entry[3]
        decrypted_password = decrypt_password(encrypted_password)
        return entry[0], decrypted_password, service_name, username  # Return ID, decrypted password, service name, and username
    return None

def delete_password_entry(entry_id):
    PasswordEntry.delete_entry_by_id(entry_id)
