import os
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np

folder_path = "./Phantoms/Phantom Test 01/A"

dicom_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]

if not dicom_files:
    print("No files found in the folder.")
    exit()

dicom_images = []
for file_path in dicom_files:
    try:
        dicom_image = dicom.dcmread(file_path)
        dicom_images.append(dicom_image)
    except Exception as e:
        print(f"Error loading DICOM file {file_path}: {str(e)}")

if not dicom_images:
    print("No valid DICOM images found in the folder.")
    exit()

pixel_arrays = [x.pixel_array for x in dicom_images]

orientation = dicom_images[20].ImageOrientationPatient

plt.figure(figsize=(12, 4))


plt.show()
