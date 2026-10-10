import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("crop.csv")
df.columns = df.columns.str.strip()

X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Crop model accuracy:", round(accuracy_score(y_test, model.predict(X_test)) * 100, 2), "%")

with open("crop_model.pkl", "wb") as f:
    pickle.dump(model, f)
