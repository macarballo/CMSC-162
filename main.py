import tkinter as tk
<<<<<<< Updated upstream
from tkinter import font, filedialog
from PIL import Image, ImageTk, ImageDraw
=======
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import struct
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
>>>>>>> Stashed changes

# Function to draw a rounded rectangle on a canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    # Draw the rounded rectangle
    canvas.create_oval(x1, y1, x1 + r * 2, y1 + r * 2, **kwargs)
    canvas.create_oval(x2 - r * 2, y1, x2, y1 + r * 2, **kwargs)
    canvas.create_oval(x1, y2 - r * 2, x1 + r * 2, y2, **kwargs)
    canvas.create_oval(x2 - r * 2, y2 - r * 2, x2, y2, **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)

# Create the main window
root = tk.Tk()
root.title("Home Page")

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

# Draw the rounded rectangle on the canvas with a larger radius
create_rounded_rectangle(canvas, 0, 0, window_width * 0.8, window_height * 0.8, r=40, fill="#7db1ce", outline="")

# Create a frame to hold the icons inside the canvas
frame = tk.Frame(root, bg="#7db1ce", bd=0)
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Load images for the icons
viewer_image = Image.open("viewer_icon.png")
snaptune_image = Image.open("snaptune_icon.png")
snaptune_image = snaptune_image.resize(viewer_image.size, Image.LANCZOS)

# Convert images to PhotoImage
viewer_icon = ImageTk.PhotoImage(viewer_image)
snaptune_icon = ImageTk.PhotoImage(snaptune_image)

# Define the custom font
try:
    custom_font = font.Font(family="HYWenHei-85W", size=12, weight="bold")
except Exception as e:
    print(f"Error loading font: {e}")
    # Fallback to a default font if custom font fails to load
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Calculate icon width as a fraction of the frame width
icon_width_fraction = viewer_icon.width() / window_width

# Function to open and display an image file
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.png;*.tiff;*.jpeg;*.bmp")]
    )
    if file_path:
        image = Image.open(file_path)
        
        #Adjust image size and ratio
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

        frame.place_forget() #Hide frame

        image_label.config(image=image_photo)
        image_label.image = image_photo  # Keep a reference to prevent garbage collection
        image_label.place(relwidth=1, relheight=1)

        # Show the back button
        back_button.place(relx=0.05, rely=0.05)

# Function to return to the main screen
def go_back():
    # Show the main frame
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    
    # Hide the image and back button
    image_label.place_forget()
    back_button.place_forget()

<<<<<<< Updated upstream
    for rect in rectangles:
        canvas.delete(rect)
    rectangles.clear()
=======
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
>>>>>>> Stashed changes


<<<<<<< Updated upstream

# Add the Viewer icon and text
viewer_button = tk.Button(
    frame,
    image=viewer_icon,
    bg="#7db1ce",
    bd=0,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
    command=open_image  # Bind the button click to the open_image function
)
viewer_button.place(relx=0.5 - icon_width_fraction / 2, rely=0.15)
viewer_label = tk.Label(
    frame,
    text="Viewer",
    bg="#7db1ce",
    fg="#222437",
    font=custom_font
)
viewer_label.place(relx=0.520 - icon_width_fraction / 2, rely=0.32)

# Add the SnapTune icon and text
snaptune_button = tk.Button(
    frame,
    image=snaptune_icon,
    bg="#7db1ce",
    bd=0,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
    relief="flat"
)
snaptune_button.place(relx=0.5 - icon_width_fraction / 2, rely=0.40)
snaptune_label = tk.Label(
    frame,
    text="SnapTune",
    bg="#7db1ce",
    fg="#222437",
    font=custom_font
)
snaptune_label.place(relx=0.512 - icon_width_fraction / 2, rely=0.57)
=======
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
info_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)

img_label = tk.Label(header_frame, bg="#7db1ce")
img_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)

palette_label = tk.Label(header_frame, bg="#7db1ce")
palette_label.pack(side=tk.RIGHT, padx=(10, 10), pady=10)
>>>>>>> Stashed changes

# Create an image label for the displayed image
image_label = tk.Label(root, bg="#7db1ce")
<<<<<<< Updated upstream
image_label.place(relx=0.5, rely=0.5, anchor="center")  # Position in the center of the window


# Adding a back button (initially hidden)
back_button = tk.Button(
    root,
    text="Viewer",
    bg="#222437",
    fg="white",
    font=custom_font,
    command=go_back
)
back_button.place_forget()


rectangles = []
=======

# Create the back button (initially hidden)
back_button = tk.Button(root, text="Back", command=go_back)
back_button.place_forget()

# Add buttons for image viewer, snaptune, and PCX inspection
button_viewer = tk.Button(main_frame, image=viewer_icon, text="Image Viewer", compound=tk.TOP, command=open_image)
button_viewer.grid(row=0, column=0, padx=50, pady=30)

button_snaptune = tk.Button(main_frame, image=snaptune_icon, text="SnapTune", compound=tk.TOP)
button_snaptune.grid(row=0, column=1, padx=50, pady=30)

button_pcx = tk.Button(main_frame, image=pcx_inspect_icon, text="PCX Inspector", compound=tk.TOP, command=open_pcx_file)
button_pcx.grid(row=0, column=2, padx=50, pady=30)
>>>>>>> Stashed changes

# Run the main loop
root.mainloop()
