import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont


def add_watermark():
    # Get input photo path
    input_photo_path = input_photo_entry.get()

    # Get watermark image path
    watermark_image_path = watermark_entry.get()

    # Get output photo path
    output_photo_path = output_photo_entry.get()

    # Get watermark position
    watermark_position = watermark_position_var.get()

    # Open input photo
    base_image = Image.open(input_photo_path)
    width, height = base_image.size

    # Open watermark image
    watermark = Image.open(watermark_image_path)

    # Calculate watermark position
    if watermark_position == "bottom left":
        x, y = 10, height - watermark.height - 10
    elif watermark_position == "bottom right":
        x, y = width - watermark.width - 10, height - watermark.height - 10
    elif watermark_position == "top left":
        x, y = 10, 10
    elif watermark_position == "top right":
        x, y = width - watermark.width - 10, 10
    else:  # center
        x, y = (width - watermark.width) // 2, (height - watermark.height) // 2

    # Add watermark to input photo
    base_image.paste(watermark, (x, y), watermark)

    # Save output photo
    base_image.save(output_photo_path)


# Create main window
root = tk.Tk()
root.title("Photo Watermarker")

# Input photo path
input_photo_label = tk.Label(root, text="Input Photo:")
input_photo_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
input_photo_entry = tk.Entry(root, width=50)
input_photo_entry.grid(row=0, column=1, padx=5, pady=5)
input_photo_button = tk.Button(root, text="Browse",
                               command=lambda: input_photo_entry.insert(tk.END, filedialog.askopenfilename()))
input_photo_button.grid(row=0, column=2, padx=5, pady=5)

# Watermark image path
watermark_label = tk.Label(root, text="Watermark Image:")
watermark_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
watermark_entry = tk.Entry(root, width=50)
watermark_entry.grid(row=1, column=1, padx=5, pady=5)
watermark_button = tk.Button(root, text="Browse",
                             command=lambda: watermark_entry.insert(tk.END, filedialog.askopenfilename()))
watermark_button.grid(row=1, column=2, padx=5, pady=5)

# Output photo path
output_photo_label = tk.Label(root, text="Output Photo:")
output_photo_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_photo_entry = tk.Entry(root, width=50)
output_photo_entry.grid(row=2, column=1, padx=5, pady=5)
output_photo_button = tk.Button(root, text="Browse",
                                command=lambda: output_photo_entry.insert(tk.END, filedialog.asksaveasfilename()))
output_photo_button.grid(row=2, column=2, padx=5, pady=5)

# Watermark position
watermark_position_label = tk.Label(root, text="Watermark Position:")
watermark_position_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
watermark_position_var = tk.StringVar()
watermark_position_var.set("bottom right")  # Default value
watermark_position_listbox = tk.Listbox(root, listvariable=watermark_position_var, height=5, exportselection=False)
watermark_position_listbox.grid(row=3, column=1, padx=5, pady=5)
watermark_positions = ["bottom left", "bottom right", "top left", "top right", "center"]
for position in watermark_positions:
    watermark_position_listbox.insert(tk.END, position)

# Add watermark button
add_watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark)
add_watermark_button.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
