import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import struct

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

# Draw the rounded rectangle on the canvas
create_rounded_rectangle(canvas, 0, 0, window_width * 0.8, window_height * 0.8, r=40, fill="#7db1ce", outline="")

# Create a frame to hold the icons inside the canvas
main_frame = tk.Frame(root, bg="#7db1ce", bd=0)
main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

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
        header_data = f.read(128)  # PCX header is 129 bytes
        header = struct.unpack("<BxHHHHBBBBHHBBBBBBBB16s", header_data)
        # Extract relevant header info
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
            header = f.read(128)  # Read the first 128 bytes of the PCX file (header size)

            if len(header) < 128:
                raise ValueError("Invalid PCX file: header size is incorrect.")

            # Unpack the PCX header based on the provided structure
            pcx_header = struct.unpack('<B B B B H H H H H H 48B B B H H 58B', header)

            # Extract header information
            # REFERENCE: Encyclopedia of Graphics File Formats (2nd ed.)
            # typedef struct _PcxHeader
            # {
            # BYTE	Identifier;        /* PCX Id Number (Always 0x0A) */
            # BYTE	Version;           /* Version Number */
            # BYTE	Encoding;          /* Encoding Format */
            # BYTE	BitsPerPixel;      /* Bits per Pixel */
            # WORD	XStart;            /* Left of image */
            # WORD	YStart;            /* Top of Image */
            # WORD	XEnd;              /* Right of Image
            # WORD	YEnd;              /* Bottom of image */
            # WORD	HorzRes;           /* Horizontal Resolution */
            # WORD	VertRes;           /* Vertical Resolution */
            # BYTE	Palette[48];       /* 16-Color EGA Palette */
            # BYTE	Reserved1;         /* Reserved (Always 0) */
            # BYTE	NumBitPlanes;      /* Number of Bit Planes */
            # WORD	BytesPerLine;      /* Bytes per Scan-line */
            # WORD	PaletteType;       /* Palette Type */
            # WORD	HorzScreenSize;    /* Horizontal Screen Size */
            # WORD	VertScreenSize;    /* Vertical Screen Size */
            # BYTE	Reserved2[54];     /* Reserved (Always 0) */
            # } PCXHEAD;
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
            palette = pcx_header[10:58]  # 48 bytes for the palette
            reserved1 = pcx_header[58]
            nplanes = pcx_header[59]  # Number of color planes
            bytes_per_line = pcx_header[60]
            palette_type = pcx_header[61]
            horizontal_screen_size = pcx_header[62]
            vertical_screen_size = pcx_header[63]
            reserved2= pcx_header[64]

            # Calculate image dimensions
            width = xmax - xmin + 1
            height = ymax - ymin + 1

            if width <= 0 or height <= 0:
                raise ValueError("Invalid PCX file: dimensions are non-positive.")

            # Display header information
            if manufacturer == 10:
                header_info = "Manufacturer: ZSoft .pcx (10)\n"
            else:
                header_info = "PCX File Information:\n"

            header_info += (
                # f"Manufacturer: {manufacturer}\n"
                f"Version: {version}\n"
                f"Encoding: {encoding}\n"
                f"Bits Per Pixel: {bits_per_pixel}\n"
                f"Image Dimensions: {xmin} {ymin} {xmax} {ymax}\n" 
                f"Horizontal Resolution (HDPI): {hres}\n"
                f"Vertical Resolution (VDPI): {vres}\n"
                f"Number of Color Planes: {nplanes}\n"
                f"Bytes per Line: {bytes_per_line}\n"
                f"Palette Type: {palette_type}\n"
                f"Horizontal Screen Size: {horizontal_screen_size}\n"
                f"Vertical Screen Size: {vertical_screen_size}"
            )

            # Hide the main frame and show the header information
            main_frame.place_forget()
            header_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

            # Update the header information label
            info_label.config(text=header_info)

            # Load the PCX image using PIL
            pcx_image = Image.open(file_path)
            pcx_photo = ImageTk.PhotoImage(pcx_image)
            img_label.config(image=pcx_photo)
            img_label.image = pcx_photo  # Keep a reference to avoid garbage collection
            img_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)

            # Show the back button
            back_button.place(relx=0.05, rely=0.05)

    except (FileNotFoundError, struct.error, ValueError) as e:
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

# Create header frame for displaying PCX header information
header_frame = tk.Frame(root, bg="#7db1ce")

# Create a frame to hold the image and info side by side
side_by_side_frame = tk.Frame(header_frame, bg="#7db1ce")
side_by_side_frame.pack(side=tk.TOP, expand=True)

# Image label on the left
img_label = tk.Label(side_by_side_frame, bg="#7db1ce")
img_label.pack(side=tk.LEFT, padx=(2, 2), pady=2)

# Info label on the right
info_label = tk.Label(side_by_side_frame, bg="#7db1ce", fg="#222437",  font=custom_font, justify="left")
info_label.pack(side=tk.RIGHT, padx=(2, 2), pady=2)

# Add the Viewer icon and text
viewer_button = tk.Button(
    main_frame,
    image=viewer_icon,
    bg="#7db1ce",
    bd=0,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
    command=open_image
)
viewer_button.place(relx=0.45, rely=0.15)
viewer_label = tk.Label(
    main_frame,
    text="Viewer",
    bg="#7db1ce",
    fg="#222437",
    font=custom_font
)
viewer_label.place(relx=0.47, rely=0.32)

# Add the SnapTune icon and text
snaptune_button = tk.Button(
    main_frame,
    image=snaptune_icon,
    bg="#7db1ce",
    bd=0,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
    relief="flat"
)
snaptune_button.place(relx=0.45, rely=0.40)
snaptune_label = tk.Label(
    main_frame,
    text="SnapTune",
    bg="#7db1ce",
    fg="#222437",
    font=custom_font
)
snaptune_label.place(relx=0.46, rely=0.57)

# Add the PCX Inspect icon and text
pcx_inspect_button = tk.Button(
    main_frame,
    image=pcx_inspect_icon,
    bg="#7db1ce",
    bd=0,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
    command=open_pcx_file  # Assign the function to open PCX files
)
pcx_inspect_button.place(relx=0.59, rely=0.38)
pcx_inspect_label = tk.Label(
    main_frame,
    text="PCX Inspect",
    bg="#7db1ce",
    fg="#222437",
    font=custom_font
)
pcx_inspect_label.place(relx=0.59, rely=0.57)

# Label to display the selected image
image_label = tk.Label(root, bg="#7db1ce")
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Adding a back button (initially hidden)
back_button = tk.Button(
    root,
    text=" < Back ",
    bg="#222437",
    fg="white",
    font=custom_font,
    command=go_back
)
back_button.place_forget()

# Run the main loop
root.mainloop()