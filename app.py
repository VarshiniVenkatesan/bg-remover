import os
import tkinter as tk
from tkinter import filedialog
from rembg import remove

def remove_background(input_path, output_path):
    """Removes background from an image and saves the output."""
    try:
        with open(input_path, "rb") as inp_file:
            input_image = inp_file.read()
            output_image = remove(input_image)

        with open(output_path, "wb") as out_file:
            out_file.write(output_image)

        print(f"✅ Background removed successfully! Output saved at: {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Initialize Tkinter and hide the root window
root = tk.Tk()
root.withdraw()

# Open file dialog to select an image
input_image_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
)

# Check if the user selected a file
if not input_image_path:
    print("❌ No file selected. Exiting...")
    exit()

# Ask the user for an output filename
output_image_path = filedialog.asksaveasfilename(
    title="Save Output Image",
    defaultextension=".png",
    filetypes=[("PNG Files", "*.png")]
)

# Ensure the output filename ends with .png
if not output_image_path.endswith(".png"):
    output_image_path += ".png"

# Run background removal
remove_background(input_image_path, output_image_path)