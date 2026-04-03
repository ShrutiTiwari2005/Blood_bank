import pandas as pd
import mysql.connector

# CSV load
df = pd.read_csv("data/blood_bank_dataset.csv")

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shruti@2005",
    database="blood_bank"
)

cursor = db.cursor()

# Insert data
for index, row in df.iterrows():

    sql = """
    INSERT INTO blood_stock
    (date, city, blood_bank, blood_group, units_available, thalassemia_units_required)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        row["date"],
        row["city"],
        row["blood_bank"],
        row["blood_group"],
        row["units_available"],
        row["thalassemia_units_required"]
    )

    cursor.execute(sql, values)

db.commit()

print("CSV data inserted successfully!")