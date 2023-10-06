import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# dicom_dir = r"C:\Users\HP\Documents\kuliah\SEMESTER 5\RSBP\Asistensi\Tugas 1\2_skull_ct\DICOM"
# dicom_dir = r"C:\Users\HP\Documents\kuliah\SEMESTER 5\RSBP\Asistensi\Tugas 1\Phantoms\Manekin-01\A"
# dicom_dir = r"C:\Users\HP\Documents\kuliah\SEMESTER 5\RSBP\Asistensi\Tugas 1\Phantoms\Phantom Test 01\A"
dicom_dir = r"C:\Users\HP\Documents\kuliah\SEMESTER 5\RSBP\Asistensi\Tugas 2\Tugas 2\data\volume"

dicom_files = []

for filename in os.listdir(dicom_dir):
    file_path = os.path.join(dicom_dir, filename)
    try:
        ds = pydicom.dcmread(file_path)
        dicom_files.append(ds)
    except pydicom.errors.InvalidDicomError:
        pass

current_image_index = 0

def update(frame):
    plt.clf()
    plt.imshow(dicom_files[frame].pixel_array, cmap="gray")
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