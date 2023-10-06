import pydicom as dicom
import matplotlib.pyplot as plt

path = "C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 2/Tugas 2/data/volume/brain_001.dcm"
x = dicom.dcmread(path)
plt.imshow(x.pixel_array, cmap="gray")
plt.show()
# print(x)