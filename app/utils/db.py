import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'hemo_sync_mirror.db')

class DatabaseManager:
    _connection = None

    @classmethod
    def get_connection(cls):
        """Initializes and returns the SQLite connection."""
        if cls._connection is None:
            cls._connection = sqlite3.connect(DB_PATH, check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
            cls.initialize_schema()
        return cls._connection

    @classmethod
    def is_connected(cls):
        """Checks if the SQLite database is reachable (always True for local file)."""
        try:
            cls.get_connection()
            return True
        except:
            return False

    @staticmethod
    def _translate_query(query):
        """Translates MySQL %s placeholders to SQLite ? placeholders."""
        # Simple replacement; avoid replacing within strings if possible, but safe enough for our standard queries
        return query.replace('%s', '?')

    @classmethod
    def execute_query(cls, query, params=None, fetch_all=True):
        """Executes a SELECT query and securely returns results as dictionaries."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            query = cls._translate_query(query)
            cursor.execute(query, params or ())
            
            # Convert sqlite3.Row to dict to match MySQL Connector dictionary cursor behavior
            if fetch_all:
                rows = cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
            else:
                row = cursor.fetchone()
                return dict(row) if row else None
        finally:
            cursor.close()

    @classmethod
    def execute_modify(cls, query, params=None):
        """Executes an INSERT, UPDATE, or DELETE query and commits."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            query = cls._translate_query(query)
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    @classmethod
    def initialize_schema(cls):
        """Creates tables if they don't exist for the mirrored SQLite database."""
        conn = cls._connection
        cursor = conn.cursor()
        
        # User Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'viewer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Patient Registry
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                current_hb REAL NOT NULL,
                city TEXT NOT NULL,
                priority_level TEXT DEFAULT 'stable',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inventory Stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_group TEXT UNIQUE NOT NULL,
                units_available INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Requisitions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_group TEXT NOT NULL,
                units_required INTEGER NOT NULL,
                city TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Donors
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                contact TEXT NOT NULL,
                city TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()

