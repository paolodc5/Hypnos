# This is a file that defines the database schema for the application.
# It creates the tables and .db file if they do not exist.

import sqlite3
from db.connection import get_connection



def create_tables(conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()

    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            PatID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            DateOfBirth TEXT,
            Gender TEXT,
            FiscalCode TEXT UNIQUE,
            Age INTEGER,
            PhoneNumber TEXT,
            DocID INTEGER,
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID)
        );
    """)

    # Therapist table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Therapist (
            DocID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            Specialty TEXT
        );
    """)

    # Prescriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prescriptions (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatID INTEGER,
            Type TEXT,
            PrescrID TEXT,
            Content TEXT,
            DocID INTEGER,
            PrescrDate TEXT,
            FOREIGN KEY (PatID) REFERENCES Patients(PatID),
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID)
        );
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes (
            NoteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Content TEXT,
            PatID INTEGER,
            DocID INTEGER,
            FOREIGN KEY (PatID) REFERENCES Patients(PatID),
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID)
        );
    """)

    # WearableDevice table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WearableDevice (
            ID INTEGER PRIMARY KEY,
            Model TEXT,
            PatID INTEGER,
            FOREIGN KEY (PatID) REFERENCES Patients(PatID)
        );
    """)

    # SleepRecords table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SleepRecords (
            Date TEXT,
            PatID INTEGER,
            DevID INTEGER,
            Hr INTEGER,
            SpO2 REAL,
            MovementIdx REAL,
            SleepCycles TEXT,
            PRIMARY KEY (Date, PatID, DevID),
            FOREIGN KEY (PatID) REFERENCES Patients(PatID),
            FOREIGN KEY (DevID) REFERENCES WearableDevice(ID)
        );
    """)

    # Questionnaires table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questionnaires (
            Date TEXT,
            Score INTEGER,
            PatID INTEGER,
            DocID INTEGER,
            PRIMARY KEY (Date, PatID),
            FOREIGN KEY (PatID) REFERENCES Patients(PatID),
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID)
        );
    """)

    # QuestionnaireAnswers table (complex attribute)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS QuestionnaireAnswers (
            AnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatID INTEGER,
            Date TEXT,
            Question TEXT,
            Answer TEXT,
            FOREIGN KEY (PatID, Date) REFERENCES Questionnaires(PatID, Date)
        );
    """)

    # AppointmentSlot table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AppointmentSlot (
            ID TEXT PRIMARY KEY,
            DocID INTEGER,
            datetime TEXT,
            isBooked BOOLEAN,
            selected_by_PatID INTEGER,
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID),
            FOREIGN KEY (selected_by_PatID) REFERENCES Patients(PatID)
        );
    """)

    # Appointment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Appointment (
            ID INTEGER PRIMARY KEY,
            SlotID TEXT,
            DocID INTEGER,
            PatID INTEGER,
            Status TEXT,
            Notes TEXT,
            FOREIGN KEY (SlotID) REFERENCES AppointmentSlot(ID),
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID),
            FOREIGN KEY (PatID) REFERENCES Patients(PatID)
        );
    """)

    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    print("Connected to the database.")
    if conn is not None:
        create_tables(conn)
        print("Tables created successfully.")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
