import os
import xml.etree.ElementTree as ET

RAW_DATA_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data"

total_unblinded = 0
has_characteristics = 0

char_fields = [
    "subtlety",
    "sphericity",
    "margin",
    "lobulation",
    "spiculation",
    "texture",
    "malignancy"
]

char_counts = {field: 0 for field in char_fields}

for root_dir, dirs, files in os.walk(RAW_DATA_PATH):
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
                total_unblinded += 1

                characteristics = nodule.find(".//ns:characteristics", namespace)

                if characteristics is not None:
                    has_characteristics += 1

                    for field in char_fields:
                        tag = characteristics.find(f".//ns:{field}", namespace)
                        if tag is not None:
                            char_counts[field] += 1

    except Exception as e:
        continue

print("\nTotal unblindedReadNodule:", total_unblinded)
print("With characteristics block:", has_characteristics)
print("Percentage:", round((has_characteristics / total_unblinded) * 100, 2), "%")

print("\nIndividual Characteristic Availability:")
for field in char_fields:
    print(f"{field}: {char_counts[field]}")