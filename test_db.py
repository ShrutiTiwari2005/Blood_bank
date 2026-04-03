import os
from dotenv import load_dotenv, find_dotenv
import mysql.connector

# SaaS Diagnostic Script v4.6
load_dotenv(find_dotenv())

print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
password = os.getenv("DB_PASSWORD")
print(f"DB_PASS_LEN: {len(password) if password else 'None'}")

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=password,
        database=os.getenv("DB_NAME")
    )
    print("SUCCESS: Connection Protocol Established.")
    conn.close()
except Exception as e:
    print(f"FAILURE: Clinical Synchronization Node Error - {e}")
