from app.utils.db import DatabaseManager

class DonorRepository:
    @staticmethod
    def create(name, age, blood_group, city, phone, last_donation):
        query = """
        INSERT INTO donors (Name, age, blood_group, City, phone, last_donation_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return DatabaseManager.execute_modify(
            query, (name, age, blood_group, city, phone, last_donation)
        )

    @staticmethod
    def find_by_city_and_group(city, blood_group):
        query = """
        SELECT Name, age, blood_group, City, phone
        FROM donors
        WHERE City=%s AND blood_group=%s
        """
        return DatabaseManager.execute_query(query, (city, blood_group))

    @staticmethod
    def get_all():
        query = "SELECT * FROM donors"
        return DatabaseManager.execute_query(query)
