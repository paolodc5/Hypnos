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
            Email TEXT,
            DocID INTEGER,
            Password TEXT NOT NULL,
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

    # PrescriptionTypes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PrescriptionTypes (
            TypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            TypeName TEXT UNIQUE NOT NULL
        );
    """)

    # Prescriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prescriptions (
            PrescrID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatID INTEGER,
            TypeID INTEGER,
            Content TEXT,
            DocID INTEGER,
            PrescrDate TEXT,
            FOREIGN KEY (PatID) REFERENCES Patients(PatID),
            FOREIGN KEY (DocID) REFERENCES Therapist(DocID),
            FOREIGN KEY (TypeID) REFERENCES PrescriptionTypes(TypeID)
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
            Duration INTEGER,
            DeepSleepTime REAL,
            LightSleepTime REAL,
            REMTime REAL,
            Latency REAL,
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
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # ForumQuestions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ForumQuestions (
            RequestID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserType TEXT NOT NULL CHECK (UserType IN ('Doctor', 'Patient')),
            UserID INTEGER,
            Request TEXT,
            FillingDate TEXT,
            FillingTime TEXT,
            Taken BOOLEAN DEFAULT 0,
            FOREIGN KEY (UserID) REFERENCES Patients(PatID),
            FOREIGN KEY (UserID) REFERENCES Therapist(DocID)
        );
    """)

    conn.commit()

def insert_prescription_types(conn):
    cursor = conn.cursor()
    types = ["drug", "remedies", "visits"]
    for t in types:
        cursor.execute("INSERT OR IGNORE INTO PrescriptionTypes (TypeName) VALUES (?)", (t,))
    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    print("Connected to the database.")
    if conn is not None:
        create_tables(conn)
        print("Tables created successfully.")
        insert_prescription_types(conn)
        print("Prescription types inserted successfully.")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
