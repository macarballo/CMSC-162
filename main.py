import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import struct
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Function to draw a rounded rectangle on a canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    """Draws a rounded rectangle on a specified canvas.

    Args:
        canvas: The tkinter canvas to draw on.
        x1, y1: Top-left corner coordinates of the rectangle.
        x2, y2: Bottom-right corner coordinates of the rectangle.
        r: The radius of the corners.
        **kwargs: Additional options for the rectangle and ovals.
    """
    canvas.create_oval(x1, y1, x1 + r * 2, y1 + r * 2, **kwargs)
    canvas.create_oval(x2 - r * 2, y1, x2, y1 + r * 2, **kwargs)
    canvas.create_oval(x1, y2 - r * 2, x1 + r * 2, y2, **kwargs)
    canvas.create_oval(x2 - r * 2, y2 - r * 2, x2, y2, **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)

# Create the main application window
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
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_columnconfigure(3, weight=1)  # New column for Histogram button
main_frame.grid_columnconfigure(4, weight=1)  # New column for Point Processing button
main_frame.grid_rowconfigure(0, weight=0)  # Add weight to row above icons to center them vertically
main_frame.grid_rowconfigure(1, weight=1)  # Row containing icons
main_frame.grid_rowconfigure(2, weight=0)  # Add weight to row below icons to center them vertically

# Load images for the icons
viewer_image = Image.open("viewer_icon.png")
snaptune_image = Image.open("snaptune_icon.png")
snaptune_image = snaptune_image.resize(viewer_image.size, Image.LANCZOS)
pcx_inspect_image = Image.open("pcx_inspect.png")
pcx_inspect_image = pcx_inspect_image.resize(viewer_image.size, Image.LANCZOS)
histogram_image = Image.open("histogram_icon.png")  # New histogram icon
histogram_image = histogram_image.resize(viewer_image.size, Image.LANCZOS)
point_processing_image = Image.open("pprocessing_icon.png")  # Point processing icon
point_processing_image = point_processing_image.resize(viewer_image.size, Image.LANCZOS)

# Convert images to PhotoImage
viewer_icon = ImageTk.PhotoImage(viewer_image)
snaptune_icon = ImageTk.PhotoImage(snaptune_image)
pcx_inspect_icon = ImageTk.PhotoImage(pcx_inspect_image)
histogram_icon = ImageTk.PhotoImage(histogram_image)  # New histogram PhotoImage
point_processing_icon = ImageTk.PhotoImage(point_processing_image)  # Point processing PhotoImage

# Define the custom font for buttons and labels
try:
    custom_font = font.Font(family="HYWenHei-85W", size=12, weight="bold")
except Exception as e:
    print(f"Error loading font: {e}")
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Function to open and display an image file
def open_image():
    """Opens an image file and displays it in the main application window.

    The image is resized to maintain aspect ratio and fit within the window.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.png;*.tiff;*.jpeg;*.bmp;*.pcx")]
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
    """Hides the current image and returns to the main screen."""
    image_label.place_forget()  # Hide the image label
    header_frame.place_forget()  # Hide the header frame
    main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)  # Show the main frame
    back_button.place_forget()  # Hide the back button

# Function to open and display a PCX file
def open_pcx_file():
    """Opens a PCX file and extracts its metadata and image data for display.

    If successful, it shows the header information and the image on the interface.
    """
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

# Function to split image into RGB channels, and a grayscale image, and display histograms.
def display_histogram():
    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    if not file_path:
        return  # If no file is selected, return

    try:
        pcx_image = Image.open(file_path)

        # Ensure the image is in RGB mode
        if pcx_image.mode != 'RGB':
            pcx_image = pcx_image.convert('RGB')

        # Split image into RGB channels
        r, g, b = pcx_image.split()

        # Convert image to grayscale
        gray_image = pcx_image.convert('L')

        fig, axs = plt.subplots(2, 4, figsize=(12, 6))  # Increase size to fit 4 columns
        fig.suptitle('RGB Channels, Black & White, and Histograms')

        # Display the RGB channels
        axs[0, 0].imshow(r, cmap="Reds")
        axs[0, 0].set_title("Red Channel")
        axs[0, 1].imshow(g, cmap="Greens")
        axs[0, 1].set_title("Green Channel")
        axs[0, 2].imshow(b, cmap="Blues")
        axs[0, 2].set_title("Blue Channel")

        # Display the grayscale image
        axs[0, 3].imshow(gray_image, cmap="gray")
        axs[0, 3].set_title("Grayscale")

        # Hide axis for clarity
        for ax in axs[0]:
            ax.axis("off")

        # Display histograms
        axs[1, 0].hist(np.array(r).ravel(), bins=256, color='red', alpha=0.6)
        axs[1, 0].set_title("Red Histogram")
        axs[1, 0].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        axs[1, 1].hist(np.array(g).ravel(), bins=256, color='green', alpha=0.6)
        axs[1, 1].set_title("Green Histogram")
        axs[1, 1].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        axs[1, 2].hist(np.array(b).ravel(), bins=256, color='blue', alpha=0.6)
        axs[1, 2].set_title("Blue Histogram")
        axs[1, 2].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        # Display histogram for black and white (grayscale) image
        axs[1, 3].hist(np.array(gray_image).ravel(), bins=256, color='black', alpha=0.6)
        axs[1, 3].set_title("Grayscale Histogram")
        axs[1, 3].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)  # Adjust title positioning
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

# Function for grayscale transformation using the formula s = (R + G + B) / 3
def grayscale_transformation(image):
    """Converts an RGB image to grayscale using the formula: s = (R + G + B) / 3."""
    # Convert the image to RGB mode (if not already)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Create a new image for grayscale
    width, height = image.size
    grayscale_image = Image.new("L", (width, height))  # Create a new grayscale image

    # Iterate over each pixel and apply the formula
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # Get the RGB values
            # Calculate the grayscale value
            gray_value = int((r + g + b) / 3)
            grayscale_image.putpixel((x, y), gray_value)  # Set the grayscale pixel

    return grayscale_image

# Function for negative of an image
def negative_transformation(image):
    """Converts an RGB image to its negative using the formula: s = 255 - r, g, b."""
    # Convert the image to RGB mode (if not already)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a new image for the negative transformation
    width, height = image.size
    negative_image = Image.new("RGB", (width, height))  # Create a new RGB image

    # Iterate over each pixel and apply the transformation
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # Get the RGB values
            neg_r = 255 - r  # Invert red
            neg_g = 255 - g  # Invert green
            neg_b = 255 - b  # Invert blue
            negative_image.putpixel((x, y), (neg_r, neg_g, neg_b))  # Set the new pixel value

    return negative_image

# Function for black/white thresholding
def black_white_thresholding(image, threshold_value):
    """Converts an image to black and white using a manual threshold."""
    # Convert the image to an array for processing
    image_array = np.array(image.convert('RGB'))
    grayscale_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Apply threshold
    _, bw_image = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Convert back to PIL Image for consistency
    return Image.fromarray(bw_image)

# Skeleton function for power-law (gamma) transformation
def gamma_transformation(image, gamma_value):
    """Applies gamma transformation to an image."""
    """Converts an RGB image to its negative using the formula: s = 255 - r, g, b."""
    # Convert the image to RGB mode (if not already)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a new image for the negative transformation
    width, height = image.size
    gamma_image = Image.new("RGB", (width, height))  # Create a new RGB image

    # Iterate over each pixel and apply the transformation
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # Get the RGB values
            gam_r = int(255 * (r / 255) ** gamma_value)
            gam_g = int(255 * (g / 255) ** gamma_value)
            gam_b = int(255 * (b / 255) ** gamma_value)
            gamma_image.putpixel((x, y), (gam_r, gam_g, gam_b))  # Set the new pixel value

    return gamma_image

# Label and Slider for threshold value input
threshold_label = tk.Label(main_frame, text="Threshold (0-255):", font=custom_font, bg="#7db1ce")
threshold_label.grid(row=3, column=1, padx=10, pady=5, sticky='e')
threshold_slider = tk.Scale(main_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
threshold_slider.set(128)  # Set default value to 128
threshold_slider.grid(row=3, column=2, padx=10, pady=5, sticky='w')

# Label and Slider for gamma value input
gamma_label = tk.Label(main_frame, text="Gamma (0.0-5.0):", font=custom_font, bg="#7db1ce")
gamma_label.grid(row=4, column=1, padx=10, pady=5, sticky='e')
gamma_slider = tk.Scale(main_frame, from_=0.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
gamma_slider.set(1.0)  # Set default value to 1.0
gamma_slider.grid(row=4, column=2, padx=10, pady=5, sticky='w')

def apply_point_processing():
    """Open a PCX image and apply point processing methods."""
    # Get user inputs from sliders
    threshold_value = threshold_slider.get()
    gamma_value = gamma_slider.get()

    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])  # Only allow PCX files
    if not file_path:
        return

    # Open the PCX image
    try:
        image = Image.open(file_path)

        # Apply the point processing methods
        grayscale_image = grayscale_transformation(image)  # Use the custom transformation
        gamma_image = gamma_transformation(image, gamma_value)
        negative_image = negative_transformation(image)
        bw_image = black_white_thresholding(image, threshold_value)
        

        # Create a new figure to display the results and histograms
        fig, axs = plt.subplots(2, 5, figsize=(12, 6))  # 2 rows, 5 columns layout
        fig.suptitle('Original and Point Processing Methods with Histograms')

        # Display the original image
        axs[0, 0].imshow(image)
        axs[0, 0].set_title('Original Image')
        axs[0, 0].axis('off')
        axs[1, 0].hist(np.array(image).ravel(), bins=256, color='blue', alpha=0.6)
        axs[1, 0].set_title('Original Histogram')
        axs[1, 0].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        # Display the grayscale image
        axs[0, 1].imshow(grayscale_image, cmap='gray')
        axs[0, 1].set_title('Grayscale Transformation')
        axs[0, 1].axis('off')
        axs[1, 1].hist(np.array(grayscale_image).ravel(), bins=256, color='gray', alpha=0.6)
        axs[1, 1].set_title('Grayscale Histogram')
        axs[1, 1].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        # Display the negative image
        axs[0, 2].imshow(negative_image)
        axs[0, 2].set_title('Negative Transformation')
        axs[0, 2].axis('off')
        axs[1, 2].hist(np.array(negative_image).ravel(), bins=256, color='red', alpha=0.6)
        axs[1, 2].set_title('Negative Histogram')
        axs[1, 2].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        # Display the thresholded BW image
        axs[0, 3].imshow(bw_image, cmap='gray')
        axs[0, 3].set_title('Black and White Thresholding')
        axs[0, 3].axis('off')
        axs[1, 3].hist(np.array(bw_image).ravel(), bins=256, color='violet', alpha=0.6)
        axs[1, 3].set_title('BW Thresholding Histogram')
        axs[1, 3].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        # Display the gamma transformed image
        axs[0, 4].imshow(gamma_image)  # Ensure type is correct for displaying
        axs[0, 4].set_title('Gamma Transformation')
        axs[0, 4].axis('off')
        axs[1, 4].hist(np.array(gamma_image).ravel(), bins=256, color='orange', alpha=0.6)
        axs[1, 4].set_title('Gamma Histogram')
        axs[1, 4].legend(['Pixels'], loc='upper right', fontsize='medium', frameon=True)

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)  # Adjust title positioning
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

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
    bd=0,              # Borderless button for a modern look
    padx=10,           # Padding to make the button larger and more clickable
    pady=5             # Vertical padding
)
back_button.place_forget()  # Hide initially

# Add buttons for image viewer, snaptune, PCX inspection, histogram, and point processing
button_viewer = tk.Button(
    main_frame, 
    image=viewer_icon, 
    text="Image Viewer", 
    compound=tk.TOP, 
    command=open_image,
    font=custom_font  # Apply the custom font
)
button_viewer.grid(row=1, column=0, padx=50, pady=50)

button_snaptune = tk.Button(
    main_frame, 
    image=snaptune_icon, 
    text="SnapTune", 
    compound=tk.TOP,
    font=custom_font  # Apply the custom font
)
button_snaptune.grid(row=1, column=1, padx=50, pady=50)

button_pcx = tk.Button(
    main_frame, 
    image=pcx_inspect_icon, 
    text="PCX Inspector", 
    compound=tk.TOP, 
    command=open_pcx_file,
    font=custom_font  # Apply the custom font
)
button_pcx.grid(row=1, column=2, padx=50, pady=50)

button_histogram = tk.Button(
    main_frame, 
    image=histogram_icon, 
    text="Histogram", 
    compound=tk.TOP, 
    command=display_histogram,
    font=custom_font  # Apply the custom font
)
button_histogram.grid(row=1, column=3, padx=50, pady=50)

button_point_processing = tk.Button(
    main_frame, 
    image=point_processing_icon, 
    text="Point Processing", 
    compound=tk.TOP, 
    command=apply_point_processing,
    font=custom_font
)
button_point_processing.grid(row=1, column=4, padx=50, pady=50)

# Run the main loop
root.mainloop()