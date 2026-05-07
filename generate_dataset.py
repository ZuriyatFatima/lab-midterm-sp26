import pandas as pd
import numpy as np
import json
import os

with open("config.json") as f:
    config = json.load(f)

student_id = config["student_id"]
seed = config["seed"]
noise_level = config["noise_level"]

np.random.seed(seed)
ROWS = 500

f1 = np.random.rand(ROWS)
f2 = np.random.rand(ROWS)
f3 = np.random.rand(ROWS)
f4 = np.random.rand(ROWS)
f5 = np.random.rand(ROWS)

noise = np.random.normal(loc=0, scale=noise_level, size=ROWS)
score = (f1*0.30) + (f2*0.20) + (f3*0.40) + (f4*0.05) + (f5*0.05) + noise
label = (score > 0.5).astype(int)

df = pd.DataFrame({"f1":f1,"f2":f2,"f3":f3,"f4":f4,"f5":f5,"label":label})
os.makedirs("dataset", exist_ok=True)
df.to_csv("dataset/train.csv", index=False)

metadata = {
    "student_id": student_id,
    "seed": seed,
    "noise_level": noise_level,
    "rows": ROWS,
    "dataset_version": config["dataset_version"]
}
with open("dataset/metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("DATASET GENERATED SUCCESSFULLY")
print(f"Student ID: {student_id}")
