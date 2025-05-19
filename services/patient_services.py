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
        SELECT p.PrescrID, p.PatID, p.DocID, t.TypeName, p.PrescrDate, p.Content
        FROM Prescriptions p
        JOIN PrescriptionTypes t ON p.TypeID = t.TypeID
        WHERE p.PatID = ?
        ORDER BY p.PrescrDate DESC
    """, (pat_id,))
    prescriptions = []
    for row in cursor.fetchall():
        prescriptions.append(Prescription(
            prescription_id=row[0],
            patient_id=row[1],
            doctor_id=row[2],
            treatm_type=row[3],  # This is the type name
            prescr_date=row[4],
            content=row[5]
        ))
    conn.close()
    return prescriptions

def get_doctor_notes(patient_id, doctor_id):
    from db.connection import get_connection
    from models.note import Note
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT NoteID, Date, Content, PatID, DocID
        FROM Notes
        WHERE PatID = ? AND DocID = ?
        ORDER BY Date DESC
    """, (patient_id, doctor_id))
    notes = [Note(note_id=row[0], date=row[1], content=row[2], patient_id=row[3], doctor_id=row[4]) for row in cursor.fetchall()]
    conn.close()
    return notes

def get_patient_notes(patient_id):
    from db.connection import get_connection
    from models.note import Note
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT NoteID, Date, Content, PatID, DocID
        FROM Notes
        WHERE PatID = ? AND DocID IS NULL
        ORDER BY Date DESC
    """, (patient_id,))
    notes = [Note(note_id=row[0], date=row[1], content=row[2], patient_id=row[3], doctor_id=row[4]) for row in cursor.fetchall()]
    conn.close()
    return notes

def add_patient_note(patient_id, content):
    from db.connection import get_connection
    import datetime
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute(
        "INSERT INTO Notes (Date, Content, PatID, DocID) VALUES (?, ?, ?, NULL)",
        (today, content, patient_id)
    )
    conn.commit()
    conn.close()

def update_patient_note(note_id, new_content):
    from db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Notes SET Content = ? WHERE NoteID = ? AND DocID IS NULL",
        (new_content, note_id)
    )
    conn.commit()
    conn.close()

def delete_patient_note(note_id):
    from db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM Notes WHERE NoteID = ? AND DocID IS NULL",
        (note_id,)
    )
    conn.commit()
    conn.close()

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

def get_all_doctors():
    from db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DocID, Surname FROM Therapist")
    doctors = [{"DocID": row[0], "Surname": row[1]} for row in cursor.fetchall()]
    conn.close()
    return doctors

def add_patient_to_db(name, surname, age, birth_date, gender, fiscal_code, phone_number, doctor_id, password="12345"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Patients (Name, Surname, Age, DateOfBirth, Gender, FiscalCode, PhoneNumber, DocID, Password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, age, birth_date, gender, fiscal_code, phone_number, doctor_id, password))
    conn.commit()
    conn.close()

def get_doctor_by_id(doctor_id, conn=None):
    from models.doctor import Doctor
    if conn is None:
        from db.connection import get_connection
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DocID, Name, Surname, Specialty, Email, Password
        FROM Therapist
        WHERE DocID = ?
    """, (doctor_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Doctor(
            doctor_id=row[0],
            name=row[1],
            surname=row[2],
            specialty=row[3],
            email=row[4],
            password=row[5]
        )
    return None

def update_patient_profile(patient_id, name, surname, birth_date, age, gender, fiscal_code, email, phone_number):
    from db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Patients SET Name=?, Surname=?, DateOfBirth=?, Age=?, Gender=?, FiscalCode=?, Email=?, PhoneNumber=? WHERE PatID=?""",
        (name, surname, birth_date, age, gender, fiscal_code, email, phone_number, patient_id)
    )
    conn.commit()
    conn.close()

def get_patient_by_id(patient_id):
    from models.patient import Patient
    from db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PatID, Name, Surname, DateOfBirth, Age, Gender, PhoneNumber, FiscalCode, DocID, Email FROM Patients WHERE PatID = ?",
        (patient_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return Patient(
            patient_id=row[0],
            name=row[1],
            surname=row[2],
            birth_date=row[3],
            age=row[4],
            gender=row[5],
            phone_number=row[6],
            fiscal_code=row[7],
            doctor_id=row[8],
            email=row[9]
        )
    return None

def get_questionnaires_patient(patient_id):
    from db.connection import get_connection
    #Returns a dict: {date: {"total_score": int, "severity": str, "responses": [(question, answer), ...]}}
    
    ISI_QUESTIONS = [
        "Difficulty falling asleep",
        "Difficulty staying asleep",
        "Problem waking up early",
        "Sleep dissatisfaction",
        "Interference with daily functioning",
        "Noticeable by others",
        "Worry about current sleep"
    ]

    def isi_severity(score):
        if score <= 7:
            return "No clinically significant insomnia"
        elif score <= 14:
            return "Subthreshold insomnia"
        elif score <= 21:
            return "Moderate insomnia"
        else:
            return "Severe insomnia"

    conn = get_connection()
    cursor = conn.cursor()
    # Get all questionnaires for the patient
    cursor.execute("""
        SELECT Date, Score FROM Questionnaires
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (patient_id,))
    questionnaires = cursor.fetchall()

    result = {}
    for date, score in questionnaires:
        # Get all answers for this date
        cursor.execute("""
            SELECT Question, Answer FROM QuestionnaireAnswers
            WHERE PatID = ? AND Date = ?
            ORDER BY AnswerID ASC
        """, (patient_id, date))
        answers = cursor.fetchall()
        # Ensure answers are in the same order as ISI_QUESTIONS
        responses = []
        for q in ISI_QUESTIONS:
            found = next((int(a[1]) for a in answers if a[0] == q), None)
            responses.append((q, found if found is not None else 0))
        result[date] = {
            "total_score": score,
            "severity": isi_severity(score),
            "responses": responses
        }
    conn.close()
    return result