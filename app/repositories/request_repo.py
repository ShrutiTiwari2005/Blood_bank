from app.utils.db import DatabaseManager

class RequestRepository:
    @staticmethod
    def create_blood_request(city, blood_group, units):
        query = """
        INSERT INTO blood_requests (city, blood_group, units_required)
        VALUES (%s, %s, %s)
        """
        return DatabaseManager.execute_modify(query, (city, blood_group, units))

    @staticmethod
    def get_all_requests():
        query = "SELECT * FROM blood_requests"
        return DatabaseManager.execute_query(query)
