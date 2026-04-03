import pandas as pd
import matplotlib.pyplot as plt

# ---------- LOAD DATA ----------
df = pd.read_csv("blood_bank_dataset.csv")

print(df.head())
print(df.info())
print(df.describe())

# ---------- DATE CLEAN ----------
df['date'] = pd.to_datetime(df['date'])

print("Missing values:\n", df.isnull().sum())

# ---------- CITY STOCK ----------
city_stock = df.groupby('city')['units_available'].sum()

city_stock.plot(kind='bar')
plt.title("City-wise Blood Availability")
plt.ylabel("Total Units")
plt.xticks(rotation=45)

# ---------- RARE BLOOD GROUPS ----------
rare_groups = df.groupby('blood_group')['units_available'].mean().sort_values().head(3)

print("Most critical blood groups:")
print(rare_groups)

plt.show()

# ---------- SHORTAGE HOTSPOTS ----------
LOW_STOCK_THRESHOLD = 10

city_shortage = df[df['units_available'] < LOW_STOCK_THRESHOLD] \
                    .groupby('city').size() \
                    .sort_values(ascending=False)

print("\nCity-wise shortage cases:")
print(city_shortage)

city_shortage.plot(kind='bar')
plt.title("City-wise Shortage Hotspots")
plt.ylabel("Number of Shortage Cases")
plt.xticks(rotation=45)
plt.show()

# ---------- TARGET PREPARATION (allowed in EDA) ----------
df['shortage_label'] = (df['units_available'] < LOW_STOCK_THRESHOLD).astype(int)

print("\nShortage label distribution:")
print(df['shortage_label'].value_counts())





df = pd.read_csv("blood_bank_dataset.csv")

# ---------- City shortage chart ----------
LOW_STOCK_THRESHOLD = 10

city_shortage = df[df['units_available'] < LOW_STOCK_THRESHOLD] \
                    .groupby('city').size() \
                    .sort_values(ascending=False)

plt.figure()
city_shortage.plot(kind='bar')
plt.title("City-wise Blood Shortage")
plt.ylabel("Number of Cases")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("static/city_shortage.png")
plt.close()


# ---------- Blood group availability ----------
blood_group_stock = df.groupby("blood_group")["units_available"].mean()

plt.figure()
blood_group_stock.plot(kind="bar")
plt.title("Average Blood Availability by Group")
plt.ylabel("Average Units")

plt.tight_layout()
plt.savefig("static/blood_group_stock.png")
plt.close()

print("Charts generated successfully!")