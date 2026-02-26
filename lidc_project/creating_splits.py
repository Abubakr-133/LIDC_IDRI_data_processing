import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

PROCESSED_PATH = "processed_data"

# Load metadata
df = pd.read_csv(os.path.join(PROCESSED_PATH, "metadata.csv"))

print("Total nodules:", len(df))
print("Unique patients:", df["patient_id"].nunique())

# --------------------------------
# Step 1: Get unique patients
# --------------------------------
patients = df["patient_id"].unique()

# 70% train, 30% temp
train_patients, temp_patients = train_test_split(
    patients,
    test_size=0.30,
    random_state=42,
    shuffle=True
)

# Split remaining 30% into 15% val and 15% test
val_patients, test_patients = train_test_split(
    temp_patients,
    test_size=0.50,
    random_state=42,
    shuffle=True
)

print("\nPatient Split:")
print("Train patients:", len(train_patients))
print("Val patients:", len(val_patients))
print("Test patients:", len(test_patients))

# --------------------------------
# Step 2: Assign split label
# --------------------------------
df["split"] = "train"

df.loc[df["patient_id"].isin(val_patients), "split"] = "val"
df.loc[df["patient_id"].isin(test_patients), "split"] = "test"

# --------------------------------
# Save split metadata
# --------------------------------
df.to_csv(os.path.join(PROCESSED_PATH, "metadata_with_split.csv"), index=False)

print("\nSplit distribution (nodules):")
print(df["split"].value_counts())

print("\nClass distribution per split:")
print(pd.crosstab(df["split"], df["label"]))