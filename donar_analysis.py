import pandas as pd
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv("data/transfusion.csv")

# check columns (important)
print("Columns in dataset:\n", df.columns)

print("\nFirst 5 rows:\n", df.head())

# -------------------- RENAME COLUMNS --------------------
df.rename(columns={
    "Recency (months)": "Recency",
    "Frequency (times)": "Frequency",
    "Monetary (c.c. blood)": "Monetary",
    "Time (months)": "Time",
    "whether he/she donated blood in March 2007": "target"
}, inplace=True)

# -------------------- DONOR DISTRIBUTION --------------------
print("\nDonor Distribution:")
print(df["target"].value_counts())

# -------------------- FREQUENCY ANALYSIS --------------------
plt.figure()
df["Frequency"].hist()
plt.title("Donation Frequency Distribution")
plt.xlabel("Frequency")
plt.ylabel("Count")
plt.show()

# -------------------- RECENCY VS FREQUENCY --------------------
plt.figure()
plt.scatter(df["Recency"], df["Frequency"])
plt.xlabel("Recency (months)")
plt.ylabel("Frequency (times)")
plt.title("Donor Behaviour")
plt.show()