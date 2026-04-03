from app.utils.db import DatabaseManager

class UserRepository:
    """SaaS User Data Access v4.0"""
    
    @staticmethod
    def create(username, email, password_hash, role='viewer'):
        query = """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        """
        return DatabaseManager.execute_modify(
            query, (username, email, password_hash, role)
        )

    @staticmethod
    def get_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        return DatabaseManager.execute_query(query, (username,), fetch_all=False)

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s"
        return DatabaseManager.execute_query(query, (user_id,), fetch_all=False)

    @staticmethod
    def update_last_login(user_id):
        import datetime
        query = "UPDATE users SET last_login = %s WHERE id = %s"
        return DatabaseManager.execute_modify(query, (datetime.datetime.now(), user_id))
