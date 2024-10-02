import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import struct
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Function to draw a rounded rectangle on a canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    canvas.create_oval(x1, y1, x1 + r * 2, y1 + r * 2, **kwargs)
    canvas.create_oval(x2 - r * 2, y1, x2, y1 + r * 2, **kwargs)
    canvas.create_oval(x1, y2 - r * 2, x1 + r * 2, y2, **kwargs)
    canvas.create_oval(x2 - r * 2, y2 - r * 2, x2, y2, **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)

# Create the main window
root = tk.Tk()
root.title("SnapTune")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to be a fraction of the screen size
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Apply the window size and position the window in the center of the screen
root.geometry(f"{window_width}x{window_height}+{int(screen_width * 0.1)}+{int(screen_height * 0.1)}")

# Load the background image and set it as the background of the window
bg_image = Image.open("cute-bg.png")
bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a canvas to draw the rounded frame
canvas = tk.Canvas(root, bg="#7db1ce", highlightthickness=0)
canvas.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Draw the rounded rectangle on the canvas
create_rounded_rectangle(canvas, 0, 0, window_width * 0.8, window_height * 0.8, r=40, fill="#7db1ce", outline="")

# Create a frame to hold the icons inside the canvas
main_frame = tk.Frame(root, bg="#7db1ce", bd=0)
main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Set up grid layout with row and column weights to center the content
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_rowconfigure(0, weight=0)  # Add weight to row above icons to center them vertically
main_frame.grid_rowconfigure(1, weight=1)  # Row containing icons
main_frame.grid_rowconfigure(2, weight=0)  # Add weight to row below icons to center them vertically

# Load images for the icons
viewer_image = Image.open("viewer_icon.png")
snaptune_image = Image.open("snaptune_icon.png")
snaptune_image = snaptune_image.resize(viewer_image.size, Image.LANCZOS)
pcx_inspect_image = Image.open("pcx_inspect.png")
pcx_inspect_image = pcx_inspect_image.resize(viewer_image.size, Image.LANCZOS)

# Convert images to PhotoImage
viewer_icon = ImageTk.PhotoImage(viewer_image)
snaptune_icon = ImageTk.PhotoImage(snaptune_image)
pcx_inspect_icon = ImageTk.PhotoImage(pcx_inspect_image)

# Define the custom font
try:
    custom_font = font.Font(family="HYWenHei-85W", size=12, weight="bold")
except Exception as e:
    print(f"Error loading font: {e}")
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Function to open and display an image file
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.png;*.tiff;*.jpeg;*.bmp")]
    )
    if file_path:
        image = Image.open(file_path)
        image_ratio = image.width / image.height
        frame_ratio = 1070 / 600

        if image_ratio > frame_ratio:
            new_width = 1070
            new_height = int(1070 / image_ratio)
        else:
            new_height = 600
            new_width = int(600 * image_ratio)

        image = image.resize((new_width, new_height), Image.LANCZOS)
        image_photo = ImageTk.PhotoImage(image)

        image_label.config(image=image_photo)
        image_label.image = image_photo  # Prevent garbage collection
        image_label.place(relwidth=1, relheight=1)

        back_button.place(relx=0.05, rely=0.05)

# Function to return to the main screen
def go_back():
    image_label.place_forget()  # Hide the image label
    header_frame.place_forget()  # Hide the header frame
    main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)  # Show the main frame
    back_button.place_forget()  # Hide the back button

# Function to read PCX header information
def read_pcx_header(file_path):
    with open(file_path, "rb") as f:
        header_data = f.read(128)  # PCX header is 128 bytes
        header = struct.unpack("<BxHHHHBBBBHHBBBBBBBB16s", header_data)
        width = header[3] - header[1] + 1
        height = header[4] - header[2] + 1
        bits_per_pixel = header[8]
        color_planes = header[10]
        bytes_per_line = header[11]
        palette_type = header[14]
        return {
            "Width": width,
            "Height": height,
            "Bits per Pixel": bits_per_pixel,
            "Color Planes": color_planes,
            "Bytes per Line": bytes_per_line,
            "Palette Type": palette_type,
        }

# Function to open and display a PCX file
def open_pcx_file():
    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    if not file_path:
        return  # If no file is selected, return

    try:
        with open(file_path, 'rb') as f:
            header = f.read(128)

            pcx_header = struct.unpack('<B B B B H H H H H H 48B B B H H 58B', header)
            manufacturer = pcx_header[0]
            version = pcx_header[1]
            encoding = pcx_header[2]
            bits_per_pixel = pcx_header[3]
            xmin = pcx_header[4]
            ymin = pcx_header[5]
            xmax = pcx_header[6]
            ymax = pcx_header[7]
            hres = pcx_header[8]
            vres = pcx_header[9]
            palette = pcx_header[10:58]
            nplanes = pcx_header[59]
            bytes_per_line = pcx_header[60]
            palette_type = pcx_header[61]

            width = xmax - xmin + 1
            height = ymax - ymin + 1

            if width <= 0 or height <= 0:
                raise ValueError("Invalid PCX file: dimensions are non-positive.")

            header_info = (
                f"Version: {version}\n"
                f"Encoding: {encoding}\n"
                f"Bits Per Pixel: {bits_per_pixel}\n"
                f"Image Dimensions: {xmin} {ymin} {xmax} {ymax}\n" 
                f"Horizontal Resolution (HDPI): {hres}\n"
                f"Vertical Resolution (VDPI): {vres}\n"
                f"Number of Color Planes: {nplanes}\n"
                f"Bytes per Line: {bytes_per_line}\n"
                f"Palette Type: {palette_type}\n"
            )

            main_frame.place_forget()
            header_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

            info_label.config(text=header_info)

            pcx_image = Image.open(file_path)
            pcx_photo = ImageTk.PhotoImage(pcx_image)
            img_label.config(image=pcx_photo)
            img_label.image = pcx_photo
            img_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)

            back_button.place(relx=0.05, rely=0.05)

            # Display the color palette from the PCX file
            display_color_palette(file_path)

    except (FileNotFoundError, struct.error, ValueError) as e:
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

# Function to display the color palette from a PCX file
def display_color_palette(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-769, 2)  # Move to the palette start
        palette_header = f.read(1)
        if palette_header == b'\x0C':  # Ensure it's a valid palette
            palette_data = f.read(768)
            colors = [tuple(palette_data[i:i + 3]) for i in range(0, 768, 3)]

            # Create an image to display the color palette (16x16 grid)
            palette_image = Image.new('RGB', (16, 16))
            palette_image.putdata(colors)
            palette_image = palette_image.resize((128, 128), Image.NEAREST)
            palette_tk = ImageTk.PhotoImage(palette_image)

            # Update the palette label with the image
            palette_label.config(image=palette_tk)
            palette_label.image = palette_tk  # Keep reference to avoid garbage collection

# Create the header frame to display the image and header information
header_frame = tk.Frame(root, bg="#7db1ce", bd=0)
header_frame.place_forget()  # Initially hidden

info_label = tk.Label(header_frame, text="", justify=tk.LEFT, bg="#7db1ce", font=custom_font)
info_label.pack(side=tk.LEFT, padx=(150, 60), pady=10)

img_label = tk.Label(header_frame, bg="#7db1ce")
img_label.pack(side=tk.LEFT, padx=(5, 5), pady=10)

palette_label = tk.Label(header_frame, bg="#7db1ce")
palette_label.pack(side=tk.RIGHT, padx=(60, 150), pady=10)

# Create an image label for the displayed image
image_label = tk.Label(root, bg="#7db1ce")

# Create the back button (initially hidden) with custom styling
back_button = tk.Button(
    root, 
    text="< Back", 
    command=go_back,
    font=custom_font,  # Apply custom font
    bg="#222437",      # Background color to match theme
    fg="white",        # Text color for contrast
    # activebackground="#357ABD",  # Background color when pressed
    # activeforeground="white",    # Text color when pressed
    bd=0,              # Borderless button for a modern look
    padx=10,           # Padding to make the button larger and more clickable
    pady=5             # Vertical padding
)
back_button.place_forget()  # Hide initially

# Add buttons for image viewer, snaptune, and PCX inspection with reduced horizontal padding
button_viewer = tk.Button(
    main_frame, 
    image=viewer_icon, 
    text="Image Viewer", 
    compound=tk.TOP, 
    command=open_image,
    font=custom_font  # Apply the custom font
)
button_viewer.grid(row=1, column=0, padx=25, pady=30)

button_snaptune = tk.Button(
    main_frame, 
    image=snaptune_icon, 
    text="SnapTune", 
    compound=tk.TOP,
    font=custom_font  # Apply the custom font
)
button_snaptune.grid(row=1, column=1, padx=25, pady=30)

button_pcx = tk.Button(
    main_frame, 
    image=pcx_inspect_icon, 
    text="PCX Inspector", 
    compound=tk.TOP, 
    command=open_pcx_file,
    font=custom_font  # Apply the custom font
)
button_pcx.grid(row=1, column=2, padx=25, pady=30)  # Reduced padx from 50 to 20

# Run the main loop
root.mainloop()