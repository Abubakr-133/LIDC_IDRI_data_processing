import os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

RAW_DATA_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data"
PROCESSED_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\processed_data"

metadata = pd.read_csv(os.path.join(PROCESSED_PATH, "metadata_with_split.csv"))

metadata["spiculation_label"] = -1
metadata["margin_label"] = -1
metadata["texture_label"] = -1

# ------------------------------------
# STEP 1: Build patient_id → xml_path map (ONCE)
# ------------------------------------
patient_xml_map = {}

for root_dir, dirs, files in os.walk(RAW_DATA_PATH):
    xml_files = [f for f in files if f.endswith(".xml")]
    if not xml_files:
        continue

    # Extract patient ID from path
    path_parts = root_dir.split(os.sep)
    patient_ids = [p for p in path_parts if p.startswith("LIDC-IDRI-")]

    if len(patient_ids) >= 2:
        patient_id = patient_ids[1]
    elif len(patient_ids) == 1:
        patient_id = patient_ids[0]
    else:
        continue

    if patient_id not in patient_xml_map:
        patient_xml_map[patient_id] = os.path.join(root_dir, xml_files[0])

print("Total patients with XML:", len(patient_xml_map))

# ------------------------------------
# Mapping function
# ------------------------------------
def map_to_3class(avg_score):
    if avg_score <= 2:#benign
        return 0
    elif avg_score == 3:#indeterminate
        return 1
    else:
        return 2

# ------------------------------------
# STEP 2: Process each metadata row
# ------------------------------------
for idx, row in metadata.iterrows():

    patient_id = row["patient_id"]

    if patient_id not in patient_xml_map:
        continue

    xml_path = patient_xml_map[patient_id]

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        namespace = {'ns': root.tag.split('}')[0].strip('{')}

        reading_sessions = root.findall(".//ns:readingSession", namespace)

        sp_scores = []
        margin_scores = []
        texture_scores = []

        for session in reading_sessions:
            nodules = session.findall(".//ns:unblindedReadNodule", namespace)

            for nodule in nodules:
                characteristics = nodule.find(".//ns:characteristics", namespace)
                if characteristics is None:
                    continue

                sp = characteristics.find(".//ns:spiculation", namespace)
                mg = characteristics.find(".//ns:margin", namespace)
                tx = characteristics.find(".//ns:texture", namespace)

                if sp is not None:
                    sp_scores.append(int(sp.text))
                if mg is not None:
                    margin_scores.append(int(mg.text))
                if tx is not None:
                    texture_scores.append(int(tx.text))

        if len(sp_scores) >= 2:
            metadata.at[idx, "spiculation_label"] = map_to_3class(np.mean(sp_scores))

        if len(margin_scores) >= 2:
            metadata.at[idx, "margin_label"] = map_to_3class(np.mean(margin_scores))

        if len(texture_scores) >= 2:
            metadata.at[idx, "texture_label"] = map_to_3class(np.mean(texture_scores))

    except:
        continue

# ------------------------------------
# Save
# ------------------------------------
metadata.to_csv(os.path.join(PROCESSED_PATH, "metadata_multitask.csv"), index=False)

print("\nMultitask metadata created.")
print("\nMissing values count:")
print((metadata[["spiculation_label","margin_label","texture_label"]] == -1).sum())

print("\nDistribution:")
print(metadata["spiculation_label"].value_counts())
print(metadata["margin_label"].value_counts())
print(metadata["texture_label"].value_counts())