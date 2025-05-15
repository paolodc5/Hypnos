# services/doctor_services.py
import sqlite3
from db.connection import get_connection
from datetime import datetime
from models.appointment_slot import AppointmentSlot
from models.appointment import Appointment

# def write_prescription(pat_id, doc_id, treatm_type, content, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     prescr_id = f"{pat_id}_{doc_id}_{datetime.now().isoformat()}"
#     prescr_date = datetime.now().strftime("%Y-%m-%d")

#     cursor.execute("""
#         INSERT INTO Prescriptions (PatID, Type, PrescrID, Content, DocID, PrescrDate)
#         VALUES (?, ?, ?, ?, ?)
#     """, (pat_id, treatm_type, prescr_id, content, doc_id, prescr_date))

#     conn.commit()
#     conn.close()
#     return prescr_id


# def edit_prescription_db(prescr_id, new_content, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         UPDATE Prescriptions
#         SET Content = ?
#         WHERE PrescrID = ?
#     """, (new_content, prescr_id))

#     conn.commit()
#     conn.close()


# def view_patient_sleep_records(pat_id, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT * FROM SleepRecords
#         WHERE PatID = ?
#         ORDER BY Date DESC
#     """, (pat_id,))
#     records = cursor.fetchall()

#     conn.close()
#     return records


# def view_patient_questionnaires(pat_id, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT * FROM Questionnaires
#         WHERE PatID = ?
#         ORDER BY Date DESC
#     """, (pat_id,))
#     questionnaires = cursor.fetchall()

#     conn.close()
#     return questionnaires


# def write_note(pat_id, doc_id, content, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cursor.execute("""
#         INSERT INTO Notes (Date, Content, PatID, DocID)
#         VALUES (?, ?, ?, ?)
#     """, (date, content, pat_id, doc_id))

#     conn.commit()
#     conn.close()


# def edit_note_db(note_id, new_content, conn=None):
#     if conn is None:
#         conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         UPDATE Notes
#         SET Content = ?
#         WHERE NoteID = ?
#     """, (new_content, note_id))

#     conn.commit()
#     conn.close()




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