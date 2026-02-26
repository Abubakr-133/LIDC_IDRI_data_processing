# import pydicom
# import matplotlib.pyplot as plt
# import numpy as np
#
# dicom_path = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data\3000566.000000-NA-03192\1-001.dcm"
#
# ds = pydicom.dcmread(dicom_path)
#
# # Convert to HU
# image = ds.pixel_array.astype(np.int16)
#
# intercept = ds.RescaleIntercept
# slope = ds.RescaleSlope
#
# hu_image = image * slope + intercept
#
# print("HU range:", np.min(hu_image), np.max(hu_image))
# # Lung window parameters
# window_center = -600
# window_width = 1500
#
# lower = window_center - window_width // 2
# upper = window_center + window_width // 2
#
# windowed_image = np.clip(hu_image, lower, upper)
# #normalized to [0,1]
# normalized_image = (windowed_image - lower) / (upper - lower)
# normalized_image = np.clip(normalized_image, 0, 1)
# normalized_image = normalized_image.astype(np.float32)
#
# plt.imshow(normalized_image, cmap="gray")
# plt.title("Normalized Slice")
# plt.show()
#
#
# import os
# import pydicom
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Folder containing DICOM slices
# folder_path = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data\3000566.000000-NA-03192"
#
# # Load all DICOM files
# slices = []
# for file in os.listdir(folder_path):
#     if file.endswith(".dcm"):
#         ds = pydicom.dcmread(os.path.join(folder_path, file))
#         slices.append(ds)
#
# print("Total slices loaded:", len(slices))
#
# # Sort slices by Z position
# try:
#     slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
#     print("Sorted using ImagePositionPatient")
# except:
#     slices.sort(key=lambda x: int(x.InstanceNumber))
#     print("Sorted using InstanceNumber")
#
# # Extract slice Z positions
# dicom_z_positions = [float(ds.ImagePositionPatient[2]) for ds in slices]
# print("First 5 DICOM Z positions:", dicom_z_positions[:5])
#
# # Convert to HU and stack
# volume = []
#
# for ds in slices:
#     image = ds.pixel_array.astype(np.int16)
#     intercept = ds.RescaleIntercept
#     slope = ds.RescaleSlope
#     hu_image = image * slope + intercept
#     volume.append(hu_image)
#
# volume = np.stack(volume)
#
# print("Volume shape:", volume.shape)
#
# # Lung window parameters
# window_center = -600
# window_width = 1500
#
# lower = window_center - window_width // 2
# upper = window_center + window_width // 2
#
# # Apply window to whole volume
# volume_windowed = np.clip(volume, lower, upper)
#
# # Normalize to [0,1]
# volume_normalized = (volume_windowed - lower) / (upper - lower)
# volume_normalized = np.clip(volume_normalized, 0, 1).astype(np.float32)
#
# print("Normalized volume shape:", volume_normalized.shape)
# print("Value range:", volume_normalized.min(), volume_normalized.max())
#
# #xml
# import xml.etree.ElementTree as ET
#
# xml_path = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\raw_data\3000566.000000-NA-03192\069.xml"
#
# tree = ET.parse(xml_path)
# root = tree.getroot()
#
# namespace = {'ns': root.tag.split('}')[0].strip('{')}
#
# reading_sessions = root.findall(".//ns:readingSession", namespace)
#
# print("Total radiologists:", len(reading_sessions))
#
# for i, session in enumerate(reading_sessions):
#     nodules = session.findall(".//ns:unblindedReadNodule", namespace)
#     print(f"\nRadiologist {i+1}:")
#
#     for nodule in nodules:
#         malignancy = nodule.find(".//ns:malignancy", namespace)
#         if malignancy is not None:
#             print("Malignancy score:", malignancy.text)
#
#
# for i, session in enumerate(reading_sessions):
#     nodules = session.findall(".//ns:unblindedReadNodule", namespace)
#
#     print(f"\nRadiologist {i+1}:")
#
#     for nodule in nodules:
#         malignancy = nodule.find(".//ns:malignancy", namespace)
#
#         if malignancy is None:
#             print("Skipping nodule (no malignancy score)")
#             continue
#
#         print("Malignancy score:", malignancy.text)
#
#         rois = nodule.findall(".//ns:roi", namespace)
#         print("Number of ROI slices:", len(rois))
#
#         z_positions = []
#         for roi in rois:
#             z = roi.find(".//ns:imageZposition", namespace)
#             if z is not None:
#                 z_positions.append(float(z.text.strip()))
#
#         print("Z positions:", z_positions[:5], "...")
#
#
# all_z_positions = []
#
# for session in reading_sessions:
#     nodules = session.findall(".//ns:unblindedReadNodule", namespace)
#
#     for nodule in nodules:
#         malignancy = nodule.find(".//ns:malignancy", namespace)
#
#         if malignancy is None:
#             continue
#
#         rois = nodule.findall(".//ns:roi", namespace)
#
#         for roi in rois:
#             z = roi.find(".//ns:imageZposition", namespace)
#             if z is not None:
#                 all_z_positions.append(float(z.text.strip()))
#
# # Remove duplicates and sort
# all_z_positions = sorted(list(set(all_z_positions)))
#
# print("Merged Z positions:", all_z_positions)
# print("Total slices covering nodule:", len(all_z_positions))
#
# nodule_slice_indices = []
#
# for z in all_z_positions:
#     closest_index = min(
#         range(len(dicom_z_positions)),
#         key=lambda i: abs(dicom_z_positions[i] - z)
#     )
#     nodule_slice_indices.append(closest_index)
#
# # Sort and remove duplicates
# nodule_slice_indices = sorted(list(set(nodule_slice_indices)))
#
# print("Nodule slice indices:", nodule_slice_indices)
# print("Number of slices extracted:", len(nodule_slice_indices))
#
# nodule_volume = volume_normalized[nodule_slice_indices]
# print("Nodule volume shape:", nodule_volume.shape)

#  pipeline:
# DICOM folder
#  Sorted 3D volume
#  HU conversion
#  Lung window
# Normalize
# Parse XML
#  Merge radiologists
#  Map Z --> slice index
#  Extract 3D nodule
import pandas as pd
df = pd.read_csv("processed_data/metadata.csv")
print(len(df))
print(df.head())
print("Benign:", sum(df["label"] == 0))
print("indetermine:", sum(df["label"] == 1))
print("Malignant:",sum(df["label"]==2))