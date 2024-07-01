import os
import pydicom
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def dcm2png(dcm_file_path, output_png_path):
    dicom = pydicom.dcmread(dcm_file_path)
    pixel_array = dicom.pixel_array
    pixel_array = ((pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array)) * 255).astype(np.uint8)
    image = Image.fromarray(pixel_array)
    image.save(output_png_path)

def convert_dcom_in_folders(base_folder, progress, status_label, percentage_label, root):
    file_list = []
    for root_dir, _, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(".dcm"):
                file_list.append(os.path.join(root_dir, file))

    total_files = len(file_list)
    converted_count = 0

    for dicom_file_path in file_list:
        output_png_path = os.path.splitext(dicom_file_path)[0] + '.png'
        dcm2png(dicom_file_path, output_png_path)
        os.remove(dicom_file_path)
        converted_count += 1
        progress['value'] = (converted_count / total_files) * 100
        percentage_label.config(text=f"%{int(progress['value'])}")
        status_label.config(text=f"Dönüştürülen dosya: {output_png_path}")
        root.update_idletasks()

    messagebox.showinfo("Tamamlandı", "Dönüştürme işlemi tamamlandı.")

def start_conversion():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        progress['value'] = 0
        percentage_label.config(text="%0")
        status_label.config(text="Dönüştürme başlıyor...")
        root.update_idletasks()
        threading.Thread(target=convert_dcom_in_folders, args=(folder_selected, progress, status_label, percentage_label, root)).start()

def on_enter(e):
    e.widget.config(cursor="hand2")

def on_leave(e):
    e.widget.config(cursor="")

root = tk.Tk()
root.title("DICOM to PNG Converter")

frame = tk.Frame(root, width=500, height=300)
frame.pack_propagate(False)  
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Klasör Seç", command=start_conversion)
select_button.pack(pady=50)
select_button.bind("<Enter>", on_enter)
select_button.bind("<Leave>", on_leave)

progress_frame = tk.Frame(frame)
progress_frame.pack(pady=5)

progress = ttk.Progressbar(progress_frame, orient="horizontal", length=350, mode="determinate")
progress.pack(side="left")

percentage_label = tk.Label(progress_frame, text="%0", width=5)
percentage_label.pack(side="left", padx=10)

status_label = tk.Label(frame, text="", wraplength=480, anchor="w")
status_label.pack(pady=5)

root.mainloop()
