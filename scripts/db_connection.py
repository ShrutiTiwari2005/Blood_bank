import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shruti@2005",
    database="blood_bank"
)

cursor = db.cursor()
print("connected to databse successfully")