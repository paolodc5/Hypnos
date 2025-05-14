# seed_data.py
import sqlite3
from db.connection import get_connection

def insert_fake_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    doctors = [
        (1, "Alice","Carrol", "alice@hypnos.com", "Neurologist", "pass123"),
        (2, "Bob","Blues", "bob@hypnos.com", "Psychiatrist", "bobpass"),
        (3, "Carol", "Smith", "carol@hypnos.com", "Pulmonologist", "carol123"),
    ]

    for doc in doctors:
        try:
            cursor.execute("""
                INSERT INTO Therapist (DocID, Name, Surname, Email, Specialty, Password)
                VALUES (?, ?, ?, ?, ?, ?)
            """, doc)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists

    conn.commit()
    conn.close()

def insert_fake_patients():
    conn = get_connection()
    cursor = conn.cursor()

    patients = [
        (101, "John","Doe", "1988-03-12", "M", "JHNDOE88", 36, "1234567890", 1),
        (102, "Maria","Rossi", "1995-07-05", "F", "MRARSS95", 29, "0987654321", 1),
        (103, "Karl", "Zimmer", "1980-11-21", "M", "KRZMMR80", 43, "2223334444", 2),
    ]

    for pat in patients:
        try:
            cursor.execute("""
                INSERT INTO Patients (PatID, Name, Surname, DateOfBirth, Gender, FiscalCode, Age, PhoneNumber, DocID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, pat)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Seeding database with test doctors and patients...")
    insert_fake_doctors()
    insert_fake_patients()
    print("Done!")
