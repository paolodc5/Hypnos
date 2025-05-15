import sqlite3

from db.connection import get_connection
from models.patient import Patient
from models.prescription import Prescription
from models.note import Note
from models.sleep_record import SleepRecord

def get_prescriptions(pat_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PrescrID, PatID, DocID, Type, PrescrDate, Content
        FROM Prescriptions
        WHERE PatID = ?
        ORDER BY rowid DESC
    """, (pat_id,))
    prescriptions = []
    for row in cursor.fetchall():
        prescriptions.append(Prescription(
            prescription_id=row[0],
            patient_id=row[1],
            doctor_id=row[2],
            treatm_type=row[3],
            prescr_date=row[4],
            content=row[5]
        ))
    conn.close()
    return prescriptions

def get_notes(pat_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT NoteID, PatID, DocID, Content, Date
        FROM Notes
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    notes = []
    for row in cursor.fetchall():
        notes.append(Note(
            note_id=row[0],
            patient_id=row[1],
            doctor_id=row[2],
            content=row[3],
            date=row[4]
        ))
    conn.close()
    return notes

def get_sleep_records(pat_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Date, PatID, DevID, Hr, SpO2, MovementIdx, SleepCycles
        FROM SleepRecords
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    records = []
    for row in cursor.fetchall():
        records.append(SleepRecord(
            date=row[0],
            patient_id=row[1],
            device_id=row[2],
            hr=row[3],
            spo2=row[4],
            movement_idx=row[5],
            sleep_cycles=row[6]
        ))
    conn.close()
    return records

def get_patients_by_doctor(doc_id: int):
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