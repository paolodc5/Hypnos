# services/doctor_services.py
import sqlite3
from db.connection import get_connection
from datetime import datetime

def write_prescription(pat_id, doc_id, treatm_type, content):
    conn = get_connection()
    cursor = conn.cursor()

    prescr_id = f"{pat_id}_{doc_id}_{datetime.now().isoformat()}"
    prescr_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO Prescriptions (PatID, Type, PrescrID, Content, DocID, PrescrDate)
        VALUES (?, ?, ?, ?, ?)
    """, (pat_id, treatm_type, prescr_id, content, doc_id, prescr_date))

    conn.commit()
    conn.close()
    return prescr_id


def edit_prescription_db(prescr_id, new_content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Prescriptions
        SET Content = ?
        WHERE PrescrID = ?
    """, (new_content, prescr_id))

    conn.commit()
    conn.close()


def view_patient_sleep_records(pat_id):
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


def view_patient_questionnaires(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Questionnaires
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    questionnaires = cursor.fetchall()

    conn.close()
    return questionnaires


def write_note(pat_id, doc_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO Notes (Date, Content, PatID, DocID)
        VALUES (?, ?, ?, ?)
    """, (date, content, pat_id, doc_id))

    conn.commit()
    conn.close()


def edit_note_db(note_id, new_content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Notes
        SET Content = ?
        WHERE NoteID = ?
    """, (new_content, note_id))

    conn.commit()
    conn.close()
