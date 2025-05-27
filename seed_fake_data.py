# seed_data.py
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
from db.connection import get_connection

fake = Faker()

def generate_phone():
    # 8 to 15 digits, no spaces
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def generate_email(name, surname, domain="hypnos.com"):
    # Lowercase, no spaces, unique
    return f"{name.lower()}.{surname.lower()}{random.randint(100,999)}@{domain}"

def generate_fiscal_code():
    # 8 alphanumeric characters
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

def insert_fake_therapists(n=10):
    conn = get_connection()
    cur = conn.cursor()
    specialties = [
        "Neurologist", "Psychiatrist", "Pulmonologist", "General Practitioner",
        "Sleep Medicine Specialist", "Endocrinologist", "Cardiologist", "Otolaryngologist"
    ]
    for i in range(n):
        name = fake.first_name()
        surname = fake.last_name()
        email = generate_email(name, surname)
        specialty = random.choice(specialties)
        password = "12345"
        cur.execute("""
            INSERT INTO Therapist (Name, Surname, Specialty, Email, Password)
            VALUES (?, ?, ?, ?, ?)
        """, (name, surname, specialty, email, password))
    conn.commit()
    conn.close()

def insert_fake_patients(n=20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DocID FROM Therapist")
    doctor_ids = [row[0] for row in cur.fetchall()]
    for i in range(n):
        name = fake.first_name()
        surname = fake.last_name()
        age = random.randint(18, 80)
        birth_date = fake.date_of_birth(minimum_age=age, maximum_age=age).strftime("%Y-%m-%d")
        gender = random.choice(["M", "F"])
        phone = generate_phone()
        fiscal_code = generate_fiscal_code()
        email = generate_email(name, surname)
        doctor_id = random.choice(doctor_ids) if doctor_ids else None
        password = "12345"
        cur.execute("""
            INSERT INTO Patients (Name, Surname, Age, DateOfBirth, Gender, FiscalCode, PhoneNumber, DocID, Email, Password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, surname, age, birth_date, gender, fiscal_code, phone, doctor_id, email, password))
    conn.commit()
    conn.close()

def insert_fake_prescriptions(n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID FROM Patients")
    patient_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DocID FROM Therapist")
    doctor_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT TypeID, TypeName FROM PrescriptionTypes")
    type_map = {row[1]: row[0] for row in cur.fetchall()}
    prescription_examples = {
        "drug": [
            "Melatonin 3mg, 1 tablet before bedtime",
            "Zolpidem 10mg, take one at night as needed",
            "Trazodone 50mg, half tablet at bedtime"
        ],
        "remedies": [
            "Practice sleep hygiene: regular bedtime, no screens 1h before sleep",
            "Use blackout curtains and keep the room cool",
            "Try relaxation techniques before bed"
        ],
        "visits": [
            "Schedule a follow-up sleep study in 3 months",
            "Refer to ENT for evaluation of snoring",
            "Book a consultation with a psychologist"
        ]
    }
    types = list(type_map.keys())
    for i in range(n):
        pat_id = random.choice(patient_ids)
        doc_id = random.choice(doctor_ids)
        type_name = random.choice(types)
        type_id = type_map[type_name]
        content = random.choice(prescription_examples[type_name])
        cur.execute("""
            INSERT INTO Prescriptions (PatID, TypeID, Content, DocID, PrescrDate)
            VALUES (?, ?, ?, ?, ?)
        """, (
            pat_id,
            type_id,
            content,
            doc_id,
            fake.date_this_decade().strftime("%Y-%m-%d")
        ))
    conn.commit()
    conn.close()

def insert_fake_notes(n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID FROM Patients")
    patient_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DocID FROM Therapist")
    doctor_ids = [row[0] for row in cur.fetchall()]
    note_examples = [
        "Patient reports difficulty falling asleep, recommends sleep hygiene.",
        "Observed improvement in sleep duration since last visit.",
        "Patient complains of frequent awakenings, consider sleep study.",
        "Discussed possible side effects of medication.",
        "Patient denies nightmares, but reports daytime fatigue.",
        "Follow-up in two weeks to assess response to therapy.",
        "Patient started melatonin, no adverse effects reported.",
        "Encouraged patient to maintain a sleep diary."
    ]
    for i in range(n):
        cur.execute("""
            INSERT INTO Notes (Date, Content, PatID, DocID)
            VALUES (?, ?, ?, ?)
        """, (
            fake.date_this_year().strftime("%Y-%m-%d"),
            random.choice(note_examples),
            random.choice(patient_ids),
            random.choice(doctor_ids)
        ))
    conn.commit()
    conn.close()

def insert_fake_wearable_devices(n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID FROM Patients")
    patient_ids = [row[0] for row in cur.fetchall()]
    for i in range(n):
        cur.execute("""
            INSERT INTO WearableDevice (ID, Model, PatID)
            VALUES (?, ?, ?)
        """, (
            i+1,
            fake.word() + "-" + fake.bothify(text="##"),
            random.choice(patient_ids)
        ))
    conn.commit()
    conn.close()

def insert_fake_sleep_records(n=100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID FROM Patients")
    patient_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT ID FROM WearableDevice")
    device_ids = [row[0] for row in cur.fetchall()]
    used_keys = set()
    inserted = 0
    while inserted < n:
        date = fake.date_this_year().strftime("%Y-%m-%d")
        pat_id = random.choice(patient_ids)
        dev_id = random.choice(device_ids)
        key = (date, pat_id, dev_id)
        if key in used_keys:
            continue
        duration = random.randint(360, 540)  # minutes (6h to 9h)
        deep_sleep = round(random.uniform(60, 120), 1)  # minutes
        light_sleep = round(random.uniform(120, 240), 1)
        rem_sleep = round(random.uniform(60, 120), 1)
        # Latency: healthy avg ~15min, insomnia avg ~30-60min, randomize with a bias
        if random.random() < 0.7:
            latency = max(2, random.gauss(15, 5))  # healthy
        else:
            latency = max(5, random.gauss(35, 15))  # insomnia
        cur.execute("""
            INSERT INTO SleepRecords (
                Date, PatID, DevID, Hr, SpO2, MovementIdx, SleepCycles,
                Duration, DeepSleepTime, LightSleepTime, REMTime, Latency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date,
            pat_id,
            dev_id,
            random.randint(50, 100),
            round(random.uniform(90, 100), 1),
            round(random.uniform(0, 10), 2),
            str(random.randint(3, 6)),
            duration,
            deep_sleep,
            light_sleep,
            rem_sleep,
            round(latency, 1)
        ))
        used_keys.add(key)
        inserted += 1
    conn.commit()
    conn.close()

def insert_fake_questionnaires(n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID FROM Patients")
    patient_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DocID FROM Therapist")
    doctor_ids = [row[0] for row in cur.fetchall()]
    used_pairs = set()
    inserted = 0
    while inserted < n:
        date = fake.date_this_year().strftime("%Y-%m-%d")
        pat_id = random.choice(patient_ids)
        pair = (date, pat_id)
        if pair in used_pairs:
            continue
        doc_id = random.choice(doctor_ids)
        cur.execute("""
            INSERT INTO Questionnaires (Date, Score, PatID, DocID)
            VALUES (?, ?, ?, ?)
        """, (
            date,
            random.randint(0, 30),
            pat_id,
            doc_id
        ))
        used_pairs.add(pair)
        inserted += 1
    conn.commit()
    conn.close()

def insert_fake_questionnaire_answers(n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatID, Date FROM Questionnaires")
    questionnaire_keys = cur.fetchall()
    questions = ["How do you feel?", "Did you sleep well?", "Any nightmares?", "How many hours?"]
    for i in range(n):
        if not questionnaire_keys:
            break
        pat_id, date = random.choice(questionnaire_keys)
        cur.execute("""
            INSERT INTO QuestionnaireAnswers (PatID, Date, Question, Answer)
            VALUES (?, ?, ?, ?)
        """, (
            pat_id,
            date,
            random.choice(questions),
            fake.sentence(nb_words=6)
        ))
    conn.commit()
    conn.close()

def insert_fake_appointment_slots_and_appointments(n=10):
    """
    Inserts n appointment slots and n appointments, ensuring that each appointment
    is booked by a patient who is actually assigned to the respective doctor.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all doctors
    cur.execute("SELECT DocID FROM Therapist")
    doctor_ids = [row[0] for row in cur.fetchall()]

    slot_patient_pairs = []

    slots_created = 0
    slot_index = 1000

    while slots_created < n:
        doc_id = random.choice(doctor_ids)
        # Get patients for this doctor
        cur.execute("SELECT PatID FROM Patients WHERE DocID = ?", (doc_id,))
        patient_ids = [row[0] for row in cur.fetchall()]
        if not patient_ids:
            continue  # Skip this doctor if they have no patients

        pat_id = random.choice(patient_ids)
        slot_id = f"SLOT{slot_index}"
        slot_index += 1
        dt = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M")
        is_booked = 1
        selected_by = pat_id

        # Insert the appointment slot
        cur.execute("""
            INSERT INTO AppointmentSlot (ID, DocID, datetime, isBooked, selected_by_PatID)
            VALUES (?, ?, ?, ?, ?)
        """, (slot_id, doc_id, dt, is_booked, selected_by))

        slot_patient_pairs.append((slot_id, doc_id, pat_id))
        slots_created += 1

    # Now insert appointments, each linked to the slot and patient
    statuses = ["pending", "confirmed", "cancelled"]
    for slot_id, doc_id, pat_id in slot_patient_pairs:
        status = random.choice(statuses)
        notes = fake.sentence(nb_words=10)
        cur.execute("""
            INSERT INTO Appointment (SlotID, DocID, PatID, Status, Notes)
            VALUES (?, ?, ?, ?, ?)
        """, (slot_id, doc_id, pat_id, status, notes))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Seeding database with fake data...")
    insert_fake_therapists(5)
    insert_fake_patients(20)
    insert_fake_prescriptions(100)
    insert_fake_notes(100)
    insert_fake_wearable_devices()
    insert_fake_sleep_records(100)
    insert_fake_questionnaires(40)
    insert_fake_questionnaire_answers(50)
    insert_fake_appointment_slots_and_appointments(30)
    print("Done!")



