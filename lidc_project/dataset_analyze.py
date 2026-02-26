import pandas as pd

df = pd.read_csv("processed_data/metadata.csv")

print("Total nodules:", len(df))
print("Unique patients:", df["patient_id"].nunique())
print("Average nodules per patient:",
      round(len(df) / df["patient_id"].nunique(), 2))

print("\nClass Distribution (nodule level):")
print(df["label"].value_counts())
print(df["label"].value_counts(normalize=True) * 100)

print("\nPatients per class:")
print(df.groupby("label")["patient_id"].nunique())

print("\nSlices per nodule stats:")
print(df["num_slices"].describe())

print("\nTop 10 patients with most nodules:")
print(df["patient_id"].value_counts().head(10))

print("="*50)