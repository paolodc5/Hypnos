# services/auth_service.py
from db.connection import get_connection
from models.patient import Patient
import sqlite3

def authenticate_patient(email: str, password: str) -> Patient | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patients WHERE Email = ? AND Password = ?", (email, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Patient(patient_id=row["PatID"], name=row["Name"], surname=row['Surname'], email=row["Email"], password=row["Password"])
    return None