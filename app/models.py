# app/models.py
from app.database import get_app_db_connection, close_db_connection

class PasswordEntry:
    def __init__(self, service_name, username, password):
        self.service_name = service_name
        self.username = username
        self.password = password

    @staticmethod
    def add_entry(service_name, username, password):
        conn = get_app_db_connection()  # Use the function that connects to the specific database
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO password_entries (service_name, username, password) VALUES (%s, %s, %s)",
            (service_name, username, password)
        )
        conn.commit()
        close_db_connection(conn)

    @staticmethod
    def get_entry(service_name):
        conn = get_app_db_connection()  # Use the function that connects to the specific database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, password FROM password_entries WHERE service_name = %s",
            (service_name,)
        )
        result = cursor.fetchone()
        close_db_connection(conn)
        return result if result else None

    @staticmethod
    def get_all_entries():
        conn = get_app_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, service_name, username, password FROM password_entries")
        results = cursor.fetchall()
        close_db_connection(conn)
        return results

    @staticmethod
    def get_entry_by_id(entry_id):
        conn = get_app_db_connection()
        cursor = conn.cursor()
        # Select ID, Encrypted Password, Service Name, and Username from the table
        cursor.execute("SELECT id, password, service_name, username FROM password_entries WHERE id = %s", (entry_id,))
        result = cursor.fetchone()
        close_db_connection(conn)
        return result  # Returns a tuple: (ID, Encrypted Password, Service Name, Username)
    
    @staticmethod
    def delete_entry_by_id(entry_id):
        conn = get_app_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM password_entries WHERE id = %s", (entry_id,))
        conn.commit()
        close_db_connection(conn)
