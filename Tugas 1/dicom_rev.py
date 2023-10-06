import pydicom
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import median_filter

class DICOMViewer:
    def __init__(self, root, dicom_directory):
        self.root = root
        self.dicom_directory = dicom_directory
        self.dicom_files = self.load_dicom_series(self.dicom_directory)
        self.current_index = 0

        self.create_gui()
        self.load_image(self.current_index)
        
        # Bind keyboard and mouse events
        self.root.bind("<Left>", self.previous_image)
        self.root.bind("<Right>", self.next_image)

    def load_dicom_series(self, directory):
        dicom_files = []

        for root, _, files in os.walk(directory):
            for file in files:
                try:
                    dicom_file = pydicom.dcmread(os.path.join(root, file))
                    dicom_files.append(dicom_file)
                except pydicom.errors.InvalidDicomError:
                    pass  # Ignore non-DICOM files

        dicom_files.sort(key=lambda x: int(x.InstanceNumber))
        return dicom_files

    def create_gui(self):
        self.canvas = tk.Canvas(self.root, width=512, height=512)
        self.canvas.pack()

        self.label = ttk.Label(self.root, text="DICOM Viewer")
        self.label.pack()

        self.prev_button = ttk.Button(self.root, text="Previous", command=self.previous_image)
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack(side="right")

    def load_image(self, index):
        if 0 <= index < len(self.dicom_files):
            dicom_file = self.dicom_files[index]
            image_data = dicom_file.pixel_array

            # Apply a median filter to reduce noise
            filtered_image_data = median_filter(image_data, size=3)

            image = Image.fromarray(filtered_image_data)
            image = ImageTk.PhotoImage(image)

            self.canvas.create_image(0, 0, anchor="nw", image=image)
            self.canvas.image = image
            self.label.config(text=f"Slice {index + 1}/{len(self.dicom_files)}")


    def previous_image(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image(self.current_index)

    def next_image(self, event=None):
        if self.current_index < len(self.dicom_files) - 1:
            self.current_index += 1
            self.load_image(self.current_index)


if __name__ == "__main__":
    # dicom_directory = 'C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 1/Phantoms/Phantom Test 01/A'
    dicom_directory = 'C:/Users/HP/Downloads/Daikon-master/Daikon-master/tests/data/volume'

    root = tk.Tk()
    viewer = DICOMViewer(root, dicom_directory)
    root.mainloop()
