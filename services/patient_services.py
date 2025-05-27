import sqlite3
from datetime import datetime, timedelta

from db.connection import get_connection
from models.patient import Patient
from models.prescription import Prescription
from models.note import Note
from models.sleep_record import SleepRecord
from models.forum_question import ForumQuestion
from models.appointment_slot import AppointmentSlot
from models.appointment import Appointment

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
        SELECT Date, PatID, DevID, Hr, SpO2, MovementIdx, SleepCycles,
               Duration, DeepSleepTime, LightSleepTime, REMTime, Latency
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
            sleep_cycles=row[6],
            duration=row[7],
            deep_sleep_time=row[8],
            light_sleep_time=row[9],
            REM_time=row[10],
            latency=row[11] if len(row) > 11 else 0.0
        ))
    conn.close()
    return records

def add_sleep_record(record: SleepRecord, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO SleepRecords (
            Date, PatID, DevID, Hr, SpO2, MovementIdx, SleepCycles,
            Duration, DeepSleepTime, LightSleepTime, REMTime, Latency
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.date,
        record.patient_id,
        record.device_id,
        record.hr,
        record.spo2,
        record.movement_idx,
        record.sleep_cycles,
        record.duration,
        record.deep_sleep_time,
        record.light_sleep_time,
        record.REM_time,
        record.latency
    ))
    conn.commit()
    conn.close()

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

def add_forum_question(question: ForumQuestion, conn=None) -> int:
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ForumQuestions (UserType, UserID, Request, FillingDate, FillingTime, Taken)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question.user_type, question.user_id, question.request,
          question.filling_date, question.filling_time, question.taken))
    conn.commit()
    request_id = cursor.lastrowid

    if close_conn:
        conn.close()

    return request_id

# Load appointment slots for a specific doctor
def load_appointment_slots_by_doctor(doc_id, selected_date, conn=None):
    if conn is None:
        conn = get_connection()
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, DocID, datetime, isBooked, selected_by_PatID
        FROM AppointmentSlot
        WHERE DocID = ? AND DATE(datetime) = ?
        ORDER BY datetime DESC
    """, (doc_id, selected_date))
    
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

def book_appointment(slot_id: str, patient_id: str, confirm: bool = False) -> bool:
    """
    Book an appointment by selecting an available slot, then confirm the appointment if requested.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the slot details
    cursor.execute("""
        SELECT ID, DocID, datetime, isBooked, selected_by_PatID
        FROM AppointmentSlot
        WHERE ID = ?
    """, (slot_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise ValueError("Slot not found")

    # Create an AppointmentSlot instance
    slot = AppointmentSlot(
        slot_id=row[0],
        doctor_id=row[1],
        start_time=row[2],  # Make sure this is converted to datetime
        end_time=row[2],  # Calculate end_time from start_time or set accordingly
    )
    slot.is_booked = bool(row[3])
    slot.selected_by = row[4] if row[3] else None

    # Check if the slot is already booked
    if slot.is_booked:
        # If the slot is booked but this patient has selected it, confirm the appointment
        if slot.selected_by == patient_id:
            if confirm:
                # Confirm the appointment if the flag is True
                cursor.execute("""
                    UPDATE AppointmentSlot
                    SET isBooked = 1
                    WHERE ID = ?
                """, (slot_id,))
                # Insert the appointment into the Appointment table
                cursor.execute("""
                    INSERT INTO Appointment (SlotID, DocID, PatID, Status)
                    VALUES (?, ?, ?, ?)
                """, (slot_id, slot.doctor_id, patient_id, "Confirmed"))
                conn.commit()
                conn.close()
                return True
            else:
                # Slot is selected but not confirmed
                raise ValueError("Slot already selected by this patient, but not confirmed yet.")
        else:
            # Slot is already booked by another patient
            conn.close()
            raise ValueError("Slot is already booked by another patient.")
    else:
        # If the slot is not booked, allow the patient to select it
        slot.select_slot(patient_id)
        # Update the slot selection in the database
        cursor.execute("""
            UPDATE AppointmentSlot
            SET isBooked = 1, selected_by_PatID = ?
            WHERE ID = ?
        """, (patient_id, slot_id))
        conn.commit()
        conn.close()
        return True

def get_appointments_by_patient(patient_id, conn=None):
    """
    Fetch all appointments for a specific patient along with their appointment slot data.
    """
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, SlotID, DocID, PatID, Status, Notes
        FROM Appointment
        WHERE PatID = ?
        ORDER BY ID DESC
    """, (patient_id,))
    
    rows = cursor.fetchall()
    appointments = []
    
    for row in rows:
        # Create an Appointment object
        appointment = Appointment(
            appointment_id=row[0],
            doctor_id=row[2],  # DocID
            patient_id=row[3],  # PatID
            status=row[4],  # Status (confirmed, pending, or canceled)
            notes=row[5]  # Notes
        )

        # Fetch the AppointmentSlot data using the SlotID from the row
        cursor.execute("""
            SELECT ID, DocID, datetime, isBooked, selected_by_PatID
            FROM AppointmentSlot
            WHERE ID = ?
        """, (row[1],))  # row[1] is the SlotID
        
        slot_row = cursor.fetchone()
        
        # If slot exists, assign it to the appointment
        if slot_row:
            # Convert the 'datetime' field into a datetime object
            start_time = datetime.strptime(slot_row[2], "%Y-%m-%d %H:%M")  # Assuming 'datetime' is stored as 'YYYY-MM-DD HH:MM'
            
            # Assuming the end time is also stored as a string in the same format, we convert it too
            # If end_time is not available, you might want to calculate it based on the start_time and a fixed duration
            end_time = start_time + timedelta(hours=1)  # Example of adding 1 hour for the appointment duration
            
            slot = AppointmentSlot(
                slot_id=slot_row[0],
                doctor_id=slot_row[1],
                start_time=start_time,  # start_time as a datetime object
                end_time=end_time,  # end_time as a datetime object
            )
            appointment.slot = slot  # Add slot to appointment
        
        # Add the appointment to the list
        appointments.append(appointment)

    if close_conn:
        conn.close()

    return appointments

def get_appointmentslot_by_patient(patient_id, conn=None):
    """
    Fetch all appointment slots for a specific patient.
    """
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, DocID, datetime, isBooked, selected_by_PatID
        FROM AppointmentSlot
        WHERE selected_by_PatID = ?
        ORDER BY datetime DESC
    """, (patient_id,))
    
    rows = cursor.fetchall()
    slots = []
    
    for row in rows:
        slot = AppointmentSlot(
            slot_id=row[0],
            doctor_id=row[1],
            start_time=datetime.strptime(row[2], "%Y-%m-%d %H:%M"),  # Convert to datetime object
            end_time=datetime.strptime(row[2], "%Y-%m-%d %H:%M") + timedelta(hours=1),  # Assuming 1 hour duration
        )
        slot.is_booked = row[3]
        slot.selected_by = row[4]
        slots.append(slot)

    if close_conn:
        conn.close()

    return slots

def get_doctor_name(doctor_id, conn=None):
    """
    Fetch the doctor's name from the database using doctor_id.
    """
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    cursor.execute("""
        SELECT Surname
        FROM Therapist
        WHERE DocID = ?
    """, (doctor_id,))

    row = cursor.fetchone()
    doctor_name = row[0] if row else "Unknown Doctor"

    if close_conn:
        conn.close()

    return doctor_name

