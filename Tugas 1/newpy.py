import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/dicom/Daikon-master/tests/data/volume"
# dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/Phantoms/Phantom Test 02/A"
dicom_dir = r"D:/SEMESTER 5/Rekayasa Sistem Berbasis Pengetahuan/Phantoms/Phantom Test 01/A"


dicom_files = []

# Membaca file DICOM dan mendapatkan InstanceNumber
for filename in os.listdir(dicom_dir):
    file_path = os.path.join(dicom_dir, filename)
    try:
        ds = pydicom.dcmread(file_path)
        
        # Periksa jika InstanceNumber ada dalam atribut DICOM
        if hasattr(ds, "InstanceNumber"):
            dicom_files.append((ds, int(ds.InstanceNumber)))
        else:
            # Jika InstanceNumber tidak ada, tambahkan nomor instansi ke nama file
            new_filename = f"{filename}_001"
            os.rename(file_path, os.path.join(dicom_dir, new_filename))
            ds.InstanceNumber = "1"
            dicom_files.append((ds, 1))
    except pydicom.errors.InvalidDicomError:
        pass

# Urutkan file DICOM berdasarkan InstanceNumber
dicom_files.sort(key=lambda x: x[1])

current_image_index = 0

def update(frame):
    plt.clf()
    plt.imshow(dicom_files[frame][0].pixel_array, cmap='gray')
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
