import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import cv2

PROCESSED_PATH = r"C:\Users\shaik\myProjects\Lung_nodule_diagnosis\lidc_project\processed_data"

df = pd.read_csv(os.path.join(PROCESSED_PATH, "metadata.csv"))

print("Class distribution:")
print(df["label"].value_counts())

# Pick 1 random sample from each class
classes = df["label"].unique()

for c in classes:
    sample = df[df["label"] == c].sample(1)

    series_id = sample.iloc[0]["series_id"]
    nodule_id = sample.iloc[0]["nodule_id"]

    folder = f"series_{series_id}_nodule_{nodule_id}"
    folder_path = os.path.join(PROCESSED_PATH, folder)

    images = [f for f in os.listdir(folder_path) if f.endswith(".png")]
    img_path = os.path.join(folder_path, random.choice(images))

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    plt.figure()
    plt.imshow(img, cmap="gray")
    plt.title(f"Class {c} | {folder}")
    plt.axis("off")

plt.show()