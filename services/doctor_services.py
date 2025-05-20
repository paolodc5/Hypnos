# services/doctor_services.py
import sqlite3
from db.connection import get_connection
from datetime import datetime
from models.appointment_slot import AppointmentSlot
# from models.appointment import Appointment
# from models.doctor import Doctor

def get_prescription_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TypeID, TypeName FROM PrescriptionTypes")
    types = cursor.fetchall()
    conn.close()
    return types  # List of (TypeID, TypeName)

def write_prescription(pat_id, doctor_id, type_id, content, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    prescr_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO Prescriptions (PatID, TypeID, Content, DocID, PrescrDate)
        VALUES (?, ?, ?, ?, ?)
    """, (pat_id, type_id, content, doctor_id, prescr_date))
    conn.commit()
    conn.close()

def update_prescription(prescription_id, type_id, content, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    prescr_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "UPDATE Prescriptions SET TypeID = ?, Content = ?, PrescrDate = ? WHERE PrescrID = ?",
        (type_id, content, prescr_date, prescription_id)
    )
    conn.commit()
    conn.close()

def delete_prescription(prescription_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Prescriptions WHERE PrescrID = ?", (prescription_id,))
    conn.commit()
    conn.close()

# Get all notes for a patient (both doctor and patient notes)
def get_notes_for_patient(pat_id, doctor_id=None):
    from models.note import Note
    conn = get_connection()
    cursor = conn.cursor()
    if doctor_id is not None:
        cursor.execute("""
            SELECT NoteID, Date, Content, PatID, DocID
            FROM Notes
            WHERE PatID = ? AND (DocID IS NULL OR DocID = ?)
            ORDER BY Date DESC
        """, (pat_id, doctor_id))
    else:
        cursor.execute("""
            SELECT NoteID, Date, Content, PatID, DocID
            FROM Notes
            WHERE PatID = ?
            ORDER BY Date DESC
        """, (pat_id,))
    notes = [Note(note_id=row[0], date=row[1], content=row[2], patient_id=row[3], doctor_id=row[4]) for row in cursor.fetchall()]
    conn.close()
    return notes

def write_note(pat_id, doctor_id, content, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO Notes (Date, Content, PatID, DocID)
        VALUES (?, ?, ?, ?)
    """, (date, content, pat_id, doctor_id))
    conn.commit()
    conn.close()

def update_note(note_id, new_content, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Notes SET Content = ?, Date = ? WHERE NoteID = ?", (new_content, date, note_id))
    conn.commit()
    conn.close()

def delete_note(note_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Notes WHERE NoteID = ?", (note_id,))
    conn.commit()
    conn.close()

def add_appointment_slot(doctor_id, start_time, conn=None):
    if conn is None:
        from db.connection import get_connection
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO AppointmentSlot (DocID, datetime, isBooked) VALUES (?, ?, 0)",
        (doctor_id, start_time)
    )
    conn.commit()
    conn.close()

def load_appointment_slots_by_doctor(doc_id, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, DocID, datetime, isBooked, selected_by_PatID
        FROM AppointmentSlot
        WHERE DocID = ?
        ORDER BY datetime DESC
    """, (doc_id,))
    slots = []
    for row in cursor.fetchall():
        slot = AppointmentSlot(
            slot_id=row[0],
            doctor_id=row[1],
            start_time=row[2],
            end_time=row[2],  # Assuming start_time and end_time are the same for simplicity
        )
        slot.is_booked = row[3]
        slot.selected_by = row[4]
        slots.append(slot)
    conn.close()
    return slots

def load_appointments_by_doctor(doc_id, conn=None):
    from models.appointment_slot import AppointmentSlot  # Avoid circular import
    from models.appointment import Appointment

    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    
    # Fetch appointments for the given doctor
    print(f"Loading appointments for doctor ID: {doc_id}")
    cursor.execute("""
        SELECT ID, SlotID, DocID, PatID, Status, Notes
        FROM Appointment
        WHERE DocID = ?
        ORDER BY ID DESC
    """, (doc_id,))
    appointments = []

    for row in cursor.fetchall():
        # print(f"Processing appointment row: {row}")
        # Retrieve the AppointmentSlot for this appointment
        cursor.execute("""
            SELECT ID, DocID, datetime, isBooked, selected_by_PatID
            FROM AppointmentSlot
            WHERE ID = ?
        """, (row[1],))
        slot_row = cursor.fetchone()
        if slot_row is None:
            continue  # Skip if slot not found

        slot = AppointmentSlot(
            slot_id=slot_row[0],
            doctor_id=slot_row[1],
            start_time=slot_row[2],
            end_time=slot_row[2],  # Assuming start_time and end_time are the same for simplicity
        )
        slot.is_booked = slot_row[3]
        slot.selected_by = slot_row[4]

        appointment = Appointment(
            appointment_id=row[0],
            slot=slot,
            patient_id=row[3],
            doctor_id=row[2],
            confirmed=(row[4] == "confirmed")  # or adjust based on your schema
        )
        appointments.append(appointment)
    conn.close()
    return appointments

def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DocID, Name, Surname, Email, Specialty FROM Therapist")
    doctors = []
    for row in cursor.fetchall():
        doctors.append({
            "doctor_id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "specialty": row[4]
        })
    conn.close()
    return doctors

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