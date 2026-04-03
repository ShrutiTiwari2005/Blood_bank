from app.utils.db import DatabaseManager
import mysql.connector

class PatientRepo:
    """Institutional Patient Data Access Node v4.4"""

    @staticmethod
    def get_all_patients():
        """Fetches the global patient registry."""
        conn = DatabaseManager.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients ORDER BY priority_level ASC, created_at DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def create_patient(data):
        """Registers a new high-risk patient with prioritized health metrics."""
        conn = DatabaseManager.get_connection()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO patients (name, age, blood_group, current_hb, condition_status, priority_level, city, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['name'], data['age'], data['blood_group'], 
                data['current_hb'], data['condition_status'], 
                data['priority_level'], data['city'], data['phone']
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def update_hb(patient_id, new_hb, priority_level):
        """Updates clinical Hb levels and resets priority status."""
        conn = DatabaseManager.get_connection()
        try:
            cursor = conn.cursor()
            query = "UPDATE patients SET current_hb = %s, priority_level = %s WHERE id = %s"
            cursor.execute(query, (new_hb, priority_level, patient_id))
            conn.commit()
        finally:
            conn.close()
