
import os
from models.doctor import Doctor

# test_doctor = Doctor(
#     doctor_id=3,
#     name="Cheyenne",
#     surname="Walter",
#     specialty="Careers adviser",
#     email="danielle54@example.org",
#     password="testpassword"
# )

# print(test_doctor)

# test_doctor.load_appointment_slots()
# test_doctor.load_appointments()
# test_doctor.load_patients()

# print("Appointment Slots:")
# for slot in test_doctor.appointment_slots:
#     print(slot.selected_by, slot.start_time, slot.end_time)

# print("Appointments:")
# for appointment in test_doctor.appointments:
#     print(appointment.patient_id, appointment.confirmed)

# print("Patients:")
# for patient in test_doctor.patients:
#     print(patient.name, patient.surname, patient.patient_id)
from models.patient import Patient

# Example patient (adjust IDs and fields as needed)
test_patient = Patient(
    patient_id=1,
    name="Mario",
    surname="Rossi",
    birth_date="1980-01-01",
    age=44,
    gender="M",
    phone_number="1234567890",
    fiscal_code="RSSMRA80A01H501U",
    doctor_id=1
)

# Load related data
test_patient.load_prescriptions()
test_patient.load_notes()
test_patient.load_sleep_records()

print("Prescriptions:")
for prescription in test_patient.prescriptions:
    print(vars(prescription))

print("\nNotes:")
for note in test_patient.notes:
    print(vars(note))

print("\nSleep Records:")
for record in test_patient.sleep_records:
    print(vars(record))