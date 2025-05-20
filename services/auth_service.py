# services/auth_service.py
from db.connection import get_connection
from models.doctor import Doctor
from models.patient import Patient
import sqlite3

def authenticate_doctor(surname: str, password: str) -> Doctor | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Therapist WHERE Surname = ? AND Password = ?", (surname, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Doctor(doctor_id=row["DocID"], 
                      name=row["Name"], 
                      surname=row['Surname'],
                      email=row["Email"], 
                      specialty=row["Specialty"], 
                      password=row["Password"])
    return None

def authenticate_patient(surname: str, password: str) -> Patient | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patients WHERE Surname = ? AND Password = ?", (surname, password))

    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Patient(patient_id=row["PatID"],
            name=row["Name"],
            surname=row["Surname"],
            birth_date=row["DateOfBirth"],
            age=row["Age"],
            gender=row["Gender"],
            phone_number=row["PhoneNumber"],
            fiscal_code=row["FiscalCode"],
            doctor_id=row["DocID"],
            email=row["Email"])
    return None

def add_doctor_to_db(name: str, surname: str, specialty: str, email: str, password: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Therapist (Name, Surname, Specialty, Email, Password)
        VALUES (?, ?, ?, ?, ?)
    """, (name, surname, specialty, email, password))
    conn.commit()
    conn.close()