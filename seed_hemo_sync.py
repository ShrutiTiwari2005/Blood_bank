from flask_bcrypt import Bcrypt
from app.utils.db import DatabaseManager

bcrypt = Bcrypt()

def seed_database():
    """Seeds the Hemo-Sync database with realistic clinical data for the cinematic audit."""
    print("Initiating Hemo-Sync Database Mirror...")
    
    # Wait, DatabaseManager might need app context if it imports config? No, it imports Config directly.
    # Instantiate connection and schema
    DatabaseManager.get_connection()

    print("Seeding Institutional Personnel Hub...")
    try:
        # Create an admin user if it doesn't exist
        hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
        user_query = "INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)"
        DatabaseManager.execute_modify(user_query, ("admin", "admin@hemosync.io", hashed_pw, 'admin'))
    except Exception as e:
        print(f"User seed error: {e}")

    print("Seeding Regional Inventory Stock...")
    blood_groups = [
        ("A+", 45), ("A-", 12), ("B+", 38), ("B-", 8),
        ("O+", 60), ("O-", 18), ("AB+", 15), ("AB-", 5)
    ]
    for bg, count in blood_groups:
        stock_query = "INSERT OR REPLACE INTO stock (blood_group, units_available) VALUES (?, ?)"
        DatabaseManager.execute_modify(stock_query, (bg, count))

    print("Seeding Patient Registry...")
    patients = [
        ("Elena Vance", "A-", 7.2, "Metro Hub", "critical"),
        ("Marcus Pierce", "O+", 12.1, "North Node", "stable"),
        ("Sofia Rostova", "AB-", 9.5, "Central Facility", "high"),
        ("David Chen", "B+", 8.4, "East Wing", "high"),
        ("Aisha Khan", "O-", 6.8, "Trauma Center", "critical"),
        ("Robert Ford", "A+", 14.2, "West Clinic", "stable"),
    ]
    # Clear patients first for a fresh run
    DatabaseManager.execute_modify("DELETE FROM patients")
    for name, bg, hb, city, priority in patients:
        pat_query = "INSERT INTO patients (name, blood_group, current_hb, city, priority_level) VALUES (?, ?, ?, ?, ?)"
        DatabaseManager.execute_modify(pat_query, (name, bg, hb, city, priority))

    print("Seeding Recent Requisitions...")
    requests = [
        ("O-", 4, "Trauma Center", "pending"),
        ("A-", 2, "Metro Hub", "pending"),
        ("B+", 5, "East Wing", "fulfilled"),
        ("AB+", 1, "Central Facility", "fulfilled"),
    ]
    DatabaseManager.execute_modify("DELETE FROM requests")
    for bg, units, city, status in requests:
        req_query = "INSERT INTO requests (blood_group, units_required, city, status) VALUES (?, ?, ?, ?)"
        DatabaseManager.execute_modify(req_query, (bg, units, city, status))
        
    print("Seeding Donor Pool...")
    donors = [
        ("James Holden", "O-", "+1 555-0100", "Trauma Center", "active"),
        ("Naomi Nagata", "A+", "+1 555-0101", "West Clinic", "active"),
        ("Amos Burton", "AB+", "+1 555-0102", "East Wing", "active"),
    ]
    DatabaseManager.execute_modify("DELETE FROM donors")
    for name, bg, contact, city, status in donors:
        donor_query = "INSERT INTO donors (name, blood_group, contact, city, status) VALUES (?, ?, ?, ?, ?)"
        DatabaseManager.execute_modify(donor_query, (name, bg, contact, city, status))

    print("Hemo-Sync Diagnostic Data Seeded Successfully!")

if __name__ == "__main__":
    seed_database()
