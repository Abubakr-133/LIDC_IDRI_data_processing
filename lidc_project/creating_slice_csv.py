import os
import pandas as pd

PROCESSED_PATH = "processed_data"

# Load nodule-level metadata with split info
df = pd.read_csv(os.path.join(PROCESSED_PATH, "metadata_with_split.csv"))

slice_rows = []

for _, row in df.iterrows():
    series_id = row["series_id"]
    nodule_id = row["nodule_id"]
    label = row["label"]
    patient_id = row["patient_id"]
    split = row["split"]

    folder_name = f"series_{series_id}_nodule_{nodule_id}"
    folder_path = os.path.join(PROCESSED_PATH, folder_name)

    if not os.path.exists(folder_path):
        continue

    for file in os.listdir(folder_path):
        if file.endswith(".png"):
            image_path = os.path.join(folder_name, file)

            slice_rows.append([
                image_path,
                label,
                patient_id,
                split
            ])

slice_df = pd.DataFrame(
    slice_rows,
    columns=["image_path", "label", "patient_id", "split"]
)

slice_df.to_csv(os.path.join(PROCESSED_PATH, "slice_level.csv"), index=False)

print("Slice-level CSV created.")
print("Total slices:", len(slice_df))

print("\nSplit distribution (slices):")
print(slice_df["split"].value_counts())

print("\nClass distribution (slices):")
print(pd.crosstab(slice_df["split"], slice_df["label"]))