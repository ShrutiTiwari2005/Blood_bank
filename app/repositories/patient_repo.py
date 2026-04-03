from app.utils.db import DatabaseManager
import mysql.connector

class PatientRepo:
    """Institutional Patient Data Access Node v4.4"""

    @staticmethod
    def get_all_patients():
        """Fetches the global patient registry with priority-level sorting."""
        query = "SELECT * FROM patients ORDER BY priority_level ASC, created_at DESC"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def create_patient(data):
        """Registers a new high-risk patient with prioritized health metrics."""
        query = """
            INSERT INTO patients (name, age, blood_group, current_hb, condition_status, priority_level, city, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['name'], data['age'], data['blood_group'], 
            data['current_hb'], data['condition_status'], 
            data['priority_level'], data['city'], data['phone']
        )
        return DatabaseManager.execute_modify(query, params)

    @staticmethod
    def update_hb(patient_id, new_hb, priority_level):
        """Updates clinical Hb levels and resets institutional priority status."""
        query = "UPDATE patients SET current_hb = %s, priority_level = %s WHERE id = %s"
        return DatabaseManager.execute_modify(query, (new_hb, priority_level, patient_id))
