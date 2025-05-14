# services/auth_service.py
from db.connection import get_connection
from models.doctor import Doctor
import sqlite3

def authenticate_doctor(surname: str, password: str) -> Doctor | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Therapist WHERE Surname = ? AND Password = ?", (surname, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Doctor(doctor_id=row["DocID"], name=row["Name"], surname=row['Surname'],email=row["Email"], specialty=row["Specialty"], password=row["Password"])
    return None