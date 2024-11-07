# main.py
from app.database import initialize_database
from app.gui import run_app

if __name__ == "__main__":
    initialize_database()  # Create table if it doesn't exist
    run_app()
