import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/dicom/Daikon-master/tests/data/volume"
dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/Phantoms/Phantom Test 02/A"
# dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/Phantoms/Phantom Test 01/A"

dicom_files = []

for filename in os.listdir(dicom_dir):
    file_path = os.path.join(dicom_dir, filename)
    try:
        ds = pydicom.dcmread(file_path)
        
        if hasattr(ds, "InstanceNumber"):
            dicom_files.append((ds, int(ds.InstanceNumber)))
        else:
            new_filename = f"{filename}_001"
            os.rename(file_path, os.path.join(dicom_dir, new_filename))
            ds.InstanceNumber = "1"
            dicom_files.append((ds, 1))
    except pydicom.errors.InvalidDicomError:
        pass

dicom_files.sort(key=lambda x: x[1])

current_image_index = 0

def window_image(image, window_center, window_width):
    # np.zeros((512,512))
    window_image = np.zeros((512,512))
    for i in range(512):
        for j in range(512):
            new_value = ((image[j,i] - (window_center - 0.5)) / window_width + 0.5) * 255.0
            if new_value > 255.0 or new_value < 0.0:
                window_image[j,i] = 0.0
            else:
                window_image[j,i] = new_value
    # img_min = window_center - window_width / 2
    # img_max = window_center + window_width / 2
    # windowed_image = np.clip(image, img_min, img_max)
    return window_image

def update(frame):
    plt.clf()
    dicom_image = dicom_files[frame][0].pixel_array
    print(np.shape(dicom_image)) 
    ww = 2800
    wc = 600
    windowed_image = window_image(dicom_image, wc, ww)
    plt.imshow(windowed_image, cmap='gray')
    plt.title(f"DICOM Image {frame + 1}")

fig, ax = plt.subplots()

def on_mouse(event):
    global current_image_index
    if event.button == 'up':
        current_image_index = min(current_image_index + 1, len(dicom_files) - 1)
    elif event.button == 'down':
        current_image_index = max(current_image_index - 1, 0)
    update(current_image_index)
    fig.canvas.draw()

def on_key(event):
    global current_image_index
    if event.key == 'right':
        current_image_index = min(current_image_index + 1, len(dicom_files) - 1)
    elif event.key == 'left':
        current_image_index = max(current_image_index - 1, 0)
    update(current_image_index)
    fig.canvas.draw()

fig.canvas.mpl_connect('scroll_event', on_mouse)

fig.canvas.mpl_connect('key_press_event', on_key)

update(current_image_index)

plt.show()
