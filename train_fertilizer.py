import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

df = pd.read_csv("fertilizer.csv")
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "Temparature": "Temperature",
    "Phosphorous": "Phosphorus",
    "Humidity ": "Humidity",
})

soil_enc = LabelEncoder().fit(df["Soil Type"])
crop_enc = LabelEncoder().fit(df["Crop Type"])
fert_enc = LabelEncoder().fit(df["Fertilizer Name"])

X = pd.DataFrame({
    "Temperature": df["Temperature"],
    "Humidity": df["Humidity"],
    "Moisture": df["Moisture"],
    "Soil Type": soil_enc.transform(df["Soil Type"]),
    "Crop Type": crop_enc.transform(df["Crop Type"]),
    "Nitrogen": df["Nitrogen"],
    "Potassium": df["Potassium"],
    "Phosphorus": df["Phosphorus"],
})
y = fert_enc.transform(df["Fertilizer Name"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Fertilizer model accuracy:", round(accuracy_score(y_test, model.predict(X_test)) * 100, 2), "%")

with open("fertilizer_model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "soil_encoder": soil_enc,
        "crop_encoder": crop_enc,
        "fertilizer_encoder": fert_enc,
    }, f)
