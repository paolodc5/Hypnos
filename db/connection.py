# This is a file that defines the database connection for the application.
# It creates the connection to the database and provides a function to get the connection.

import sqlite3
from sqlite3 import Connection
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "sleep_monitoring.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    # conn.row_factory = sqlite3.Row  # Optional: allows dict-like access
    return conn