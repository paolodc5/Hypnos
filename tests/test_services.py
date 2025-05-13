import unittest
import sqlite3
from services.doctor_services import write_prescription
from services.patient_services import get_prescriptions
from db.schema import create_tables


class TestPrescriptionServices(unittest.TestCase):

    def setUp(self):
        # Create in-memory DB
        print("Setting up in-memory database for testing...")
        self.conn = sqlite3.connect(':memory:')
        create_tables(self.conn)
        print("Database and tables created in memory.")

        # Insert dummy patient and doctor
        print("Inserting dummy data into the database...")
        cur = self.conn.cursor()
        cur.execute("INSERT INTO Patients (PatID, Name) VALUES (?, ?)", (1, "Test Patient"))
        cur.execute("INSERT INTO Therapist (DocID, Name, Email) VALUES (?, ?, ?)", (101, "Dr. Who", "who@tardis.com"))
        self.conn.commit()
        print("Dummy data inserted.")
        print("Setup complete.")

    def tearDown(self):
        self.conn.close()

    def test_create_and_retrieve_prescription(self):
        write_prescription(self.conn, pat_id=1, doctor_id=101, treatm_type="Melatonin", prescr_id="RX123", content="Sleep well")
        results = get_prescriptions(self.conn, 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].prescription_id, "RX123")

if __name__ == '__main__':
    unittest.main()