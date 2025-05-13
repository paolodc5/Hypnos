from db.connection import get_connection

def get_prescriptions(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Prescriptions
        WHERE PatID = ?
        ORDER BY rowid DESC
    """, (pat_id,))
    prescriptions = cursor.fetchall()

    conn.close()
    return prescriptions


def get_notes(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Notes
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    notes = cursor.fetchall()

    conn.close()
    return notes


def get_sleep_data(pat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM SleepRecords
        WHERE PatID = ?
        ORDER BY Date DESC
    """, (pat_id,))
    records = cursor.fetchall()

    conn.close()
    return records
