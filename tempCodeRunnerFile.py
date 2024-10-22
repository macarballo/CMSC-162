import tkinter as tk
from tkinter import font, filedialog, messagebox, Toplevel, Frame, Button, Label,messagebox, Entry, ttk
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

# Set the window size to be full screen
window_width = int(screen_width * 1.0)
window_height = int(screen_height * 1.0)

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
main_frame.grid_columnconfigure(1, weight=1)  # PCX Inspector column (was column 2)
main_frame.grid_columnconfigure(2, weight=1)  # Histogram column (was column 3)
main_frame.grid_columnconfigure(3, weight=1)  # Point Processing column (was column 4)
main_frame.grid_columnconfigure(4, weight=1)  # Image Enhancement column (was column 5)
main_frame.grid_rowconfigure(0, weight=0)  # Add weight to row above icons to center them vertically
main_frame.grid_rowconfigure(1, weight=1)  # Row containing icons
main_frame.grid_rowconfigure(2, weight=0)  # Add weight to row below icons to center them vertically

# Load images for the icons
viewer_image = Image.open("viewer_icon.png")
pcx_inspect_image = Image.open("pcx_inspect.png")
pcx_inspect_image = pcx_inspect_image.resize(viewer_image.size, Image.LANCZOS)
histogram_image = Image.open("histogram_icon.png")  # New histogram icon
histogram_image = histogram_image.resize(viewer_image.size, Image.LANCZOS)
point_processing_image = Image.open("pprocessing_icon.png")  # Point processing icon
point_processing_image = point_processing_image.resize(viewer_image.size, Image.LANCZOS)

# Convert images to PhotoImage
viewer_icon = ImageTk.PhotoImage(viewer_image)
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

# Function to allow user to choose which channels to display using buttons and show the corresponding histograms
def display_histogram():
    # Open a file dialog to select the PCX file
    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    if not file_path:
        return  # If no file is selected, return

    try:
        # Load the PCX image
        pcx_image = Image.open(file_path)

        # Ensure the image is in RGB mode
        if pcx_image.mode != 'RGB':
            pcx_image = pcx_image.convert('RGB')

        # Split the image into RGB channels and convert to grayscale
        r, g, b = pcx_image.split()
        gray_image = pcx_image.convert('L')

        # Create a window for the user to choose which channel to display
        selection_window = Toplevel(root)
        selection_window.title("Select Channels")

        # Update label to use custom font
        Label(selection_window, text="Click a button to display the corresponding channel and histogram", 
              font=custom_font).pack(padx=10, pady=10)

        # Function to display a single channel and its histogram
        def show_channel(channel, channel_name, color, img, ax_color_map, hist_color):
            fig, axs = plt.subplots(2, 1, figsize=(6, 6))
            fig.suptitle(f'{channel_name} Channel and Histogram')

            # Display the selected channel
            axs[0].imshow(img, cmap=ax_color_map)
            axs[0].set_title(f"{channel_name} Channel")
            axs[0].axis("off")

            # Display the histogram for the selected channel
            axs[1].hist(np.array(channel).ravel(), bins=256, color=hist_color, alpha=0.6)
            axs[1].set_title(f"{channel_name} Histogram")

            plt.tight_layout()
            plt.subplots_adjust(top=0.88)
            plt.show()

        # Buttons for each channel with the customized font
        Button(selection_window, text="Red Channel", font=custom_font, 
               command=lambda: show_channel(r, "Red", 'red', r, "Reds", 'red')).pack(pady=10)

        Button(selection_window, text="Green Channel", font=custom_font, 
               command=lambda: show_channel(g, "Green", 'green', g, "Greens", 'green')).pack(pady=10)

        Button(selection_window, text="Blue Channel", font=custom_font, 
               command=lambda: show_channel(b, "Blue", 'blue', b, "Blues", 'blue')).pack(pady=10)

        Button(selection_window, text="Grayscale", font=custom_font, 
               command=lambda: show_channel(gray_image, "Grayscale", 'black', gray_image, "gray", 'black')).pack(pady=10)

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
    
# Functions for image enhancements
def apply_unsharp_mask(image, sigma=10.0, strength=1.5):
    """Applies unsharp masking to the input PCX image by processing each RGB channel separately."""
    # Convert image to numpy array
    image_array = np.array(image)

    # Check the number of dimensions
    if image_array.ndim != 3:
        raise ValueError("Input image must be a color image with 3 channels (RGB).")

    # Check if the image has 3 channels (RGB)
    if image_array.shape[2] != 3:
        raise ValueError("Image does not have 3 channels (RGB). Check image format.")

    # Split into R, G, B channels
    r, g, b = cv2.split(image_array)

    # Apply Gaussian blur and unsharp masking to each RGB channel
    r_blurred = cv2.GaussianBlur(r, (11, 11), sigma)
    r_unsharp = cv2.addWeighted(r, 1.0 + strength, r_blurred, -strength, 0)

    g_blurred = cv2.GaussianBlur(g, (11, 11), sigma)
    g_unsharp = cv2.addWeighted(g, 1.0 + strength, g_blurred, -strength, 0)

    b_blurred = cv2.GaussianBlur(b, (11, 11), sigma)
    b_unsharp = cv2.addWeighted(b, 1.0 + strength, b_blurred, -strength, 0)

    # Merge the processed R, G, B channels back together
    unsharp_image = cv2.merge((r_unsharp, g_unsharp, b_unsharp))

    # Ensure pixel values are in valid range and return the processed image
    return Image.fromarray(np.clip(unsharp_image, 0, 255).astype(np.uint8))

def apply_highboost_filter(image, amplification=2.0):
    """Applies highboost filtering to the input image by processing each RGB channel separately."""
    # Convert image to numpy array
    image_array = np.array(image)

    # Check the number of dimensions
    if image_array.ndim != 3:
        raise ValueError("Input image must be a color image with 3 channels (RGB).")

    # Split into R, G, B channels
    r, g, b = cv2.split(image_array)

    # Apply Gaussian blur to each channel
    r_blurred = cv2.GaussianBlur(r, (9, 9), 10.0)
    g_blurred = cv2.GaussianBlur(g, (9, 9), 10.0)
    b_blurred = cv2.GaussianBlur(b, (9, 9), 10.0)

    # Apply highboost filtering to each channel
    r_highboost = cv2.addWeighted(r, amplification, r_blurred, -(amplification - 1), 0)
    g_highboost = cv2.addWeighted(g, amplification, g_blurred, -(amplification - 1), 0)
    b_highboost = cv2.addWeighted(b, amplification, b_blurred, -(amplification - 1), 0)

    # Merge the processed R, G, B channels back together
    highboost_image = cv2.merge((r_highboost, g_highboost, b_highboost))

    # Ensure pixel values are in valid range and return the processed image
    return Image.fromarray(np.clip(highboost_image, 0, 255).astype(np.uint8))

def apply_sobel_operator(image):
    """Applies the Sobel magnitude operator for edge detection."""
    # Convert the input image to a grayscale image (L mode) and then to a numpy array
    image_array = np.array(image.convert('L'))

    # Apply the Sobel operator in the x direction to detect horizontal edges
    # cv2.CV_64F allows for more precise calculations with double precision
    sobel_x = cv2.Sobel(image_array, cv2.CV_64F, 1, 0, ksize=3)

    # Apply the Sobel operator in the y direction to detect vertical edges
    # Again using cv2.CV_64F for precision
    sobel_y = cv2.Sobel(image_array, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the magnitude of the Sobel gradients using the Pythagorean theorem
    # This combines the horizontal and vertical edge detections
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Convert the Sobel magnitude array to an 8-bit unsigned integer format
    # Use np.absolute to ensure all values are non-negative
    sobel_magnitude = np.uint8(np.absolute(sobel_magnitude))

    # Convert the resulting numpy array back to a PIL Image and return it
    return Image.fromarray(sobel_magnitude)

def apply_averaging(image):
    """Applies an averaging filter to the input image to blur it."""
    # Convert the input image to a NumPy array in RGB format
    image_array = np.array(image.convert('RGB'))

    # Split the image into its Blue, Green, and Red channels
    b_channel, g_channel, r_channel = cv2.split(image_array)
    
    # Define the kernel size for the averaging filter
    kernel_size = (5, 5)
    
    # Create the averaging filter kernel, normalizing by the area of the kernel
    averaging_filter = np.ones(kernel_size, np.float32) / (kernel_size[0] * kernel_size[1])
    
    # Apply the averaging filter to each color channel separately
    b_blurred = cv2.filter2D(b_channel, -1, averaging_filter)
    g_blurred = cv2.filter2D(g_channel, -1, averaging_filter)
    r_blurred = cv2.filter2D(r_channel, -1, averaging_filter)
    
    # Merge the blurred channels back into a single image
    averaged_image = cv2.merge((b_blurred, g_blurred, r_blurred))
    
    # Clip the pixel values to ensure they fall within the valid range [0, 255]
    # and convert the result back to a PIL Image before returning
    return Image.fromarray(np.clip(averaged_image, 0, 255).astype(np.uint8))

def apply_median(image):
    """Applies a median filter to the input image to reduce noise."""
    # Convert the input image to a NumPy array in RGB format
    image_array = np.array(image.convert('RGB')) 
    
    # Split the image into its Blue, Green, and Red channels
    b_channel, g_channel, r_channel = cv2.split(image_array)
    
    # Apply the median blur filter to each color channel separately with a kernel size of 3
    b_median = cv2.medianBlur(b_channel, 3)
    g_median = cv2.medianBlur(g_channel, 3)
    r_median = cv2.medianBlur(r_channel, 3)
    
    # Merge the median filtered channels back into a single image
    median_filtered_image = cv2.merge((b_median, g_median, r_median))
    
    # Clip pixel values to ensure they are within the valid range [0, 255] and return as a PIL Image
    return Image.fromarray(np.clip(median_filtered_image, 0, 255).astype(np.uint8))

def apply_highpass(image):
    """Applies a high-pass filter to the input image using the Laplacian operator."""
    # Convert the input image to a NumPy array in grayscale format
    image_array = np.array(image.convert('L')) 
    
    # Apply the Laplacian operator to detect edges in the image
    laplacian_filtered_image = cv2.Laplacian(image_array, cv2.CV_64F)
    
    # Convert the filtered image to an 8-bit unsigned integer format, suitable for display
    laplacian_filtered_image = cv2.convertScaleAbs(laplacian_filtered_image)
    
    # Return the resulting high-pass filtered image as a PIL Image
    return Image.fromarray(laplacian_filtered_image)


# Global variable to keep track of the enhancement window
enhancement_window = None

# Function to handle the menu for image enhancement
def image_enhancement():
    """Displays a menu for the user to choose an image enhancement method."""
    global enhancement_window  # Use the global variable

    # Check if the enhancement window already exists
    if enhancement_window is not None and enhancement_window.winfo_exists():
        enhancement_window.lift()  # Bring the existing window to the front
        return  # Exit the function to avoid creating a new window

    def display_results(original_image, processed_image, title):
        """Displays the original image and processed image in a new figure."""
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns layout
        fig.suptitle(title)

        # Display the original image
        axs[0].imshow(original_image, cmap='gray')
        axs[0].set_title('Original Image')
        axs[0].axis('off')

        # Display the processed image
        axs[1].imshow(processed_image, cmap='gray')
        axs[1].set_title('Processed Image')
        axs[1].axis('off')

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)  # Adjust title positioning
        plt.show()

    def apply_filter(filter_func, *args):
        """Applies the chosen filter to the selected image."""
        file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
        if file_path:
            try:
                pcx_image = Image.open(file_path)

                # Convert image to RGB (ensures 3 channels)
                pcx_image = pcx_image.convert("RGB")

                # Apply the selected filter and display results
                processed_image = filter_func(pcx_image, *args)
                display_results(pcx_image, processed_image, filter_func.__name__)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {e}")

    # Create a new window for the image enhancement options
    enhancement_window = Toplevel(root)
    enhancement_window.title("Image Enhancement")

    # Keep the enhancement window on top of others
    enhancement_window.attributes('-topmost', True)

    # Create frames for layout
    left_frame = Frame(enhancement_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = Frame(enhancement_window)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Add labels or instructions in the left column
    Label(left_frame, text="Select an enhancement method from the right:").pack(pady=5)

    # Create a label and entry for amplification value (initially hidden)
    amplification_label = Label(left_frame, text="Enter Amplification Value (default: 2.0):")
    amplification_entry = Entry(left_frame)
    
    # Button for confirming highboost filter (initially hidden)
    confirm_button = Button(left_frame, text="Confirm Highboost Filtering", command=lambda: confirm_highboost_filter())
    
    def show_amplification_input():
        """Show the amplification input when highboost filtering button is clicked."""
        amplification_label.pack(pady=5)
        amplification_entry.pack(pady=5)
        amplification_entry.insert(0, "2.0")  # Default value
        confirm_button.pack(pady=5)  # Show confirm button

    def confirm_highboost_filter():
        """Applies the highboost filter with the specified amplification value."""
        amplification_value = amplification_entry.get()
        try:
            amplification_value = float(amplification_value)
            apply_filter(apply_highboost_filter, amplification_value)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numerical amplification value.")
            confirm_button.pack_forget()  # Hide confirm button if input is invalid
        else:
            confirm_button.pack_forget()  # Hide confirm button after successful input

    # Add buttons for the image enhancement filters in the right column
    Button(right_frame, text="Averaging Filter", command=lambda: apply_filter(apply_averaging)).pack(pady=5)
    Button(right_frame, text="Median Filter", command=lambda: apply_filter(apply_median)).pack(pady=5)
    Button(right_frame, text="Highpass Filter (Laplacian)", command=lambda: apply_filter(apply_highpass)).pack(pady=5)
    Button(right_frame, text="Unsharp Masking", command=lambda: apply_filter(apply_unsharp_mask)).pack(pady=5)
    Button(right_frame, text="Highboost Filtering", command=show_amplification_input).pack(pady=5)
    Button(right_frame, text="Sobel Magnitude Operator", command=lambda: apply_filter(apply_sobel_operator)).pack(pady=5)
    
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

# Load images for the icons (including the new image enhancement icon)
image_enhancement_image = Image.open("image_enhancement.png")
image_enhancement_image = image_enhancement_image.resize(viewer_image.size, Image.LANCZOS)
image_enhancement_icon = ImageTk.PhotoImage(image_enhancement_image)

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

button_pcx = tk.Button(
    main_frame, 
    image=pcx_inspect_icon, 
    text="PCX Inspector", 
    compound=tk.TOP, 
    command=open_pcx_file,
    font=custom_font  # Apply the custom font
)
button_pcx.grid(row=1, column=1, padx=50, pady=50)

button_histogram = tk.Button(
    main_frame, 
    image=histogram_icon, 
    text="Histogram", 
    compound=tk.TOP, 
    command=display_histogram,
    font=custom_font  # Apply the custom font
)
button_histogram.grid(row=1, column=2, padx=50, pady=50)

button_point_processing = tk.Button(
    main_frame, 
    image=point_processing_icon, 
    text="Point Processing", 
    compound=tk.TOP, 
    command=apply_point_processing,
    font=custom_font
)
button_point_processing.grid(row=1, column=3, padx=50, pady=50)

# Add Image Enhancement button to the main frame
image_enhancement_button = tk.Button(
    main_frame, 
    image=image_enhancement_icon, 
    text="Image Enhancement", 
    compound="top", 
    command=image_enhancement,
    font=custom_font)
image_enhancement_button.grid(row=1, column=4, padx=20, pady=20)

# Run the main loop
root.mainloop()