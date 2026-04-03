import pandas as pd
import random
from datetime import datetime, timedelta

# ---------- CONFIG ----------
cities = ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar"]
blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
blood_banks = [
    "Red Cross Blood Bank",
    "City Care Blood Bank",
    "LifeLine Blood Center",
    "Hope Blood Bank",
    "Metro Blood Bank"
]

# ⭐ NEW: city demand factor (realism boost)
city_factor = {
    "Bhopal": 1.25,
    "Indore": 1.20,
    "Jabalpur": 0.95,
    "Gwalior": 1.00,
    "Ujjain": 0.80,
    "Sagar": 0.85
}

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 6, 30)

# ---------- DATA GENERATION ----------
data = []

current_date = start_date
while current_date <= end_date:
    for city in cities:
        for bank in blood_banks:
            for group in blood_groups:

                # base stock logic
                if group in ["O-", "AB-"]:
                    units = random.randint(0, 20)
                elif group in ["A-", "B-"]:
                    units = random.randint(5, 30)
                else:
                    units = random.randint(10, 100)

                # ⭐ APPLY CITY FACTOR
                units = int(units * city_factor[city])

                thalassemia_units_required = random.randint(0, 10)

                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "city": city,
                    "blood_bank": bank,
                    "blood_group": group,
                    "units_available": units,
                    "thalassemia_units_required": thalassemia_units_required
                })

    current_date += timedelta(days=1)

# ---------- SAVE ----------
df = pd.DataFrame(data)
df.to_csv("blood_bank_dataset.csv", index=False)

print("✅ Improved dataset generated!")
print("Total rows:", len(df))