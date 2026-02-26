import os
import pandas as pd
import xml.etree.ElementTree as ET

RAW_DATA_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data"
PROCESSED_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\processed_data"

# Load your final metadata (855 nodules)
metadata = pd.read_csv(os.path.join(PROCESSED_PATH, "metadata.csv"))

total_final_nodules = len(metadata)
nodules_with_characteristics = 0

checked_series = set()

for _, row in metadata.iterrows():

    series_id = row["series_id"]

    # Avoid re-checking same series multiple times
    if series_id in checked_series:
        continue

    checked_series.add(series_id)

    # Find XML file inside raw_data
    for root_dir, dirs, files in os.walk(RAW_DATA_PATH):
        if f"series_{series_id}_" in str(root_dir):
            continue

        xml_files = [f for f in files if f.endswith(".xml")]
        if not xml_files:
            continue

        xml_path = os.path.join(root_dir, xml_files[0])

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            namespace = {'ns': root.tag.split('}')[0].strip('{')}

            reading_sessions = root.findall(".//ns:readingSession", namespace)

            for session in reading_sessions:
                nodules = session.findall(".//ns:unblindedReadNodule", namespace)

                for nodule in nodules:
                    characteristics = nodule.find(".//ns:characteristics", namespace)
                    if characteristics is not None:
                        nodules_with_characteristics += 1

            break

        except:
            continue

print("\nFinal dataset nodules:", total_final_nodules)
print("Nodules with characteristics found (raw count):", nodules_with_characteristics)