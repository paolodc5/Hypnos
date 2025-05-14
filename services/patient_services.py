from db.connection import get_connection
# from models.patient import Patient
import sqlite3
from typing import List

def get_prescriptions(pat_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Prescriptions
        WHERE PatID = ?
        ORDER BY rowid DESC
    """, (pat_id,))
    prescriptions = cursor.fetchall()

    conn.close()
    return prescriptions


def get_notes(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Notes
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    notes = cursor.fetchall()

    conn.close()
    return notes


def get_sleep_data(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM SleepRecords
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    records = cursor.fetchall()

    conn.close()
    return records


def get_patients_by_doctor(doc_id: int):
    from models.patient import Patient
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Patients WHERE DocID = ? ORDER BY Surname, Name
    """, (doc_id,))
    rows = cursor.fetchall()
    conn.close()

    patients = []
    for row in rows:
        patient = Patient(
            patient_id=row["PatID"],
            name=row["Name"],
            surname=row["Surname"],
            birth_date=row["DateOfBirth"],
            gender=row["Gender"],
            fiscal_code=row["FiscalCode"],
            age=row["Age"],
            phone_number=row["PhoneNumber"],
            doctor_id=row["DocID"],
        )
        patients.append(patient)

    return patients