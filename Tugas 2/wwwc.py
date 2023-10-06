import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def load_dicom_series(directory):
    dicom_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            try:
                dicom_file = pydicom.dcmread(os.path.join(root, file))
                dicom_files.append(dicom_file)
            except pydicom.errors.InvalidDicomError:
                pass  # Ignore non-DICOM files

    return dicom_files

def trialWWWC(array, WW, WC):
    # Apply WW/WC to the pixel data
    windowed_image = ((array - (WC - 0.5)) / WW + 0.5) * 255.0

    # Clip the values to [0, 255]
    windowed_image = windowed_image.clip(0, 255).astype('uint8')

    return windowed_image

def display_images(dicom_files, wwwc):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    current_index = 0
    num_images = len(dicom_files)
    dicom_file = dicom_files[current_index]
    pixel_data = dicom_file.pixel_array
    ww, wc = wwwc[0], wwwc[1]

    image = trialWWWC(pixel_data, ww, wc)
    imgplot = ax.imshow(image, cmap='gray', vmin=0, vmax=255)
    
    ax_slider = plt.axes([0.1, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Image', 0, num_images - 1, valinit=0, valstep=1)

    def update(val):
        nonlocal current_index
        current_index = int(slider.val)
        dicom_file = dicom_files[current_index]
        pixel_data = dicom_file.pixel_array
        image = trialWWWC(pixel_data, ww, wc)
        imgplot.set_array(image)
        fig.canvas.draw()

    slider.on_changed(update)

    plt.show()

if _name_ == "_main_":
    dicom_directory = 'D:\SEMESTER 5\Rekayasa Sistem Berbasis Pengetahuan\Phantoms\Manekin-01\A'  # Ganti dengan direktori DICOM Anda
    dicom_files = load_dicom_series(dicom_directory)
    wwwc = [1.0, 0.5]  # Sesuaikan parameter WW/WC sesuai kebutuhan

    display_images(dicom_files, wwwc)