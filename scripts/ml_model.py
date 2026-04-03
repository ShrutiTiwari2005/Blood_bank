import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ---------- LOAD DATA ----------
df = pd.read_csv("blood_bank_dataset.csv")

LOW_STOCK_THRESHOLD = 10
df['shortage_label'] = (df['units_available'] < LOW_STOCK_THRESHOLD).astype(int)

# ---------- FEATURES ----------
features = df[['city', 'blood_group', 'thalassemia_units_required']].copy()
target = df['shortage_label']

# ---------- ENCODING ----------
le_city = LabelEncoder()
le_group = LabelEncoder()

features['city'] = le_city.fit_transform(features['city'])
features['blood_group'] = le_group.fit_transform(features['blood_group'])

# ---------- TRAIN TEST SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)

# ---------- MODEL ----------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ---------- EVALUATION ----------
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
print("✅ Model Accuracy:", acc)

print("\nClassification Report:\n")
print(classification_report(y_test, preds))

# ---------- SAVE MODEL ----------
joblib.dump(model, "shortage_model.pkl")
joblib.dump(le_city, "le_city.pkl")
joblib.dump(le_group, "le_group.pkl")

print("\n✅ Model and encoders saved successfully!")