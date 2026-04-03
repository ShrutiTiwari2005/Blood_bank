import mysql.connector
from mysql.connector import pooling
from app.config import Config

class DatabaseManager:
    _pool = None

    @classmethod
    def get_pool(cls):
        """Initializes the connection pool if it doesn't exist."""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="blood_bank_prod_pool",
                    pool_size=10,
                    pool_reset_session=True,
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME
                )
            except mysql.connector.Error as err:
                print(f"CRITICAL: Database connection failed: {err}")
                cls._pool = None
        return cls._pool

    @classmethod
    def is_connected(cls):
        """Checks if the database is currently reachable."""
        try:
            pool = cls.get_pool()
            if pool:
                conn = pool.get_connection()
                conn.close()
                return True
        except:
            pass
        return False

    @classmethod
    def get_connection(cls):
        """Fetches a connection from the pool."""
        pool = cls.get_pool()
        if not pool:
            raise mysql.connector.DatabaseError("Database connection pool not initialized.")
        return pool.get_connection()

    @classmethod
    def execute_query(cls, query, params=None, fetch_all=True):
        """
        Executes a SELECT query and safely returns results.
        Ensures the connection is always returned to the pool.
        """
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall() if fetch_all else cursor.fetchone()
            return result
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def execute_modify(cls, query, params=None):
        """
        Executes an INSERT, UPDATE, or DELETE query and commits.
        Ensures the connection is always returned to the pool.
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
