import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

with open("config.json") as f:
    config = json.load(f)

student_id = config["student_id"]
dataset_version = config["dataset_version"]
model_type = config["model_type"]

df = pd.read_csv("dataset/train.csv")
X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

if model_type == "logistic_regression":
    model = LogisticRegression()
elif model_type == "random_forest":
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
elif model_type == "decision_tree":
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
else:
    raise Exception(f"Unsupported model_type: {model_type}")

model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

joblib.dump(model, "model.pkl")

metrics = {
    "student_id": student_id,
    "dataset_version": dataset_version,
    "model_type": model_type,
    "accuracy": round(float(accuracy), 4),
    "samples": len(df)
}
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("MODEL TRAINING COMPLETE")
print(f"Accuracy: {accuracy:.4f}")
