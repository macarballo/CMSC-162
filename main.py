# Program Overview:
# This application, developed by Meekah Yzabelle Carballo and Khublei Mo Satori Belayo,
# both 4th-year Bachelor of Science in Computer Science students, implements several
# image processing techniques.

# It includes functionalities for unraveling PCX image files (Guide 2), basic image 
# enhancement such as channel separation and histogram analysis (Guide 3), and various 
# point-processing methods (Guide 4) including Grayscale Transformation, Negative, 
# B/W Thresholding with user-selected thresholds, and Power-law (Gamma) Transformation. 
# Additionally, we have integrated spatial domain filters (Guide 5), such as Averaging 
# and Median Filters, Highpass Filtering with a Laplacian operator, Unsharp Masking, 
# Highboost Filtering with amplification options, and edge detection through Sobel gradient 
# operators. 

# This project aims to provide comprehensive image manipulation capabilities for PCX 
# files, demonstrating a wide range of filtering and transformation techniques for both 
# educational and practical applications.

# Import the necessary libraries
import tkinter as tk  # Standard GUI toolkit for Python
from tkinter import (  # Importing specific components from the tkinter module
    font,               # For custom font handling
    filedialog,        # For opening file dialog windows
    messagebox,        # For displaying message boxes to the user
    Toplevel,          # For creating new windows
    Frame,             # For creating frame widgets to organize the layout
    Button,            # For creating clickable buttons
    Label             # For creating label widgets to display text
)
from PIL import Image, ImageTk  # Importing PIL (Pillow) for image handling and manipulation
import struct  # For working with C-style data structures and binary data
import numpy as np  # For numerical operations and array manipulation
import matplotlib.pyplot as plt  # For creating static, animated, and interactive visualizations
import cv2  # OpenCV library for computer vision tasks

# The imported libraries serve the following purposes:
# - tkinter: Create a graphical user interface (GUI) for the application.
# - PIL (Pillow): Handle image loading, processing, and conversion to a format suitable for tkinter.
# - struct: Manage binary data structures, useful for reading and writing binary files.
# - numpy: Perform numerical computations, particularly with arrays, and facilitate image processing.
# - matplotlib: Generate plots and visualizations, particularly useful for displaying image data.
# - cv2: Provide functions for advanced image processing and computer vision tasks.

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
    """
    Opens an image file, resizes it to maintain the aspect ratio, and displays it in the main application window.
    The function supports various image formats, including JPG, PNG, TIFF, JPEG, BMP, and PCX.

    Parameters:
    - None

    Internal Parameters and Behavior:
    - `file_path`: str, stores the file path of the selected image.
    - `image_ratio`: float, calculated ratio of the image's width to its height.
    - `frame_ratio`: float, the aspect ratio of the display area in the application (1070/600).
    - `new_width`: int, the resized width of the image based on the aspect ratio.
    - `new_height`: int, the resized height of the image based on the aspect ratio.

    The image is resized based on whether its aspect ratio exceeds that of the application window, 
    ensuring it fits within the predefined frame (1070x600 pixels) while maintaining its proportions.
    
    Returns:
    - None

    This function interacts with:
    - `image_label`: A Tkinter Label widget where the image is displayed.
    - `back_button`: A Tkinter Button widget for navigation, positioned once the image is displayed.
    """
    
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.png;*.tiff;*.jpeg;*.bmp;*.pcx")]
    )
    
    if file_path:
        # Open the image file and get its dimensions
        image = Image.open(file_path)
        image_ratio = image.width / image.height  # Calculate image aspect ratio
        frame_ratio = 1070 / 600  # Aspect ratio of the display frame
        
        # Resize the image based on the aspect ratio
        if image_ratio > frame_ratio:
            new_width = 1070
            new_height = int(1070 / image_ratio)
        else:
            new_height = 600
            new_width = int(600 * image_ratio)
        
        # Resize the image using a high-quality resampling filter
        image = image.resize((new_width, new_height), Image.LANCZOS)
        image_photo = ImageTk.PhotoImage(image)  # Convert to a Tkinter-compatible photo object
        
        # Configure the image_label to display the image
        image_label.config(image=image_photo)
        image_label.image = image_photo  # Prevent the image from being garbage collected
        
        # Ensure the image occupies the entire label space
        image_label.place(relwidth=1, relheight=1)
        
        # Position the back button for navigation
        back_button.place(relx=0.05, rely=0.05)

# Function to return to the main screen
def go_back():
    """
    Restores the application to its main screen by hiding the current image and its associated UI elements.
    
    This function is used to transition from the image display mode back to the main screen layout.
    
    Parameters:
    - None

    Internal Behavior:
    - `image_label`: The Tkinter Label widget displaying the image, which is hidden using `place_forget()`.
    - `header_frame`: A Tkinter Frame widget that acts as the header of the image view, also hidden using `place_forget()`.
    - `main_frame`: The main frame of the application, shown again with specified relative dimensions (relwidth, relheight) and positioning (relx, rely) when returning to the main screen.
    - `back_button`: A Tkinter Button widget for returning to the main screen, which is hidden when the main screen is displayed.

    Returns:
    - None

    Function Workflow:
    - Hides the image and header using `place_forget()`, making them invisible.
    - Repositions and resizes the main application frame to cover the display area.
    - Hides the back button to restore the original interface.
    """
    
    # Hide the image label to remove the image from view
    image_label.place_forget()
    
    # Hide the header frame
    header_frame.place_forget()
    
    # Restore the main application interface
    main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    
    # Hide the back button to complete the transition to the main screen
    back_button.place_forget()

# GUIDE 2: Unraveling a PCX Image File
# Function to open and display a PCX file
def open_pcx_file():
    """
    Opens a PCX file, extracts its metadata (header information), and displays both the metadata 
    and image data on the user interface. If the file is valid, the image is shown alongside its 
    header information; otherwise, an error is raised.

    Parameters:
    - None

    Internal Parameters:
    - `file_path`: str, the file path of the selected PCX file.
    - `header`: bytes, the first 128 bytes of the PCX file that contain its metadata.
    - `pcx_header`: tuple, unpacked data from the header, which includes details like manufacturer, 
      version, encoding type, image dimensions, and other critical metadata.
    - `manufacturer`: int, identifies the PCX manufacturer (should always be 10).
    - `version`: int, identifies the PCX version.
    - `encoding`: int, indicates the encoding type used (should always be 1).
    - `bits_per_pixel`: int, the number of bits per pixel (color depth).
    - `xmin`, `ymin`, `xmax`, `ymax`: int, specify the boundaries of the image in the PCX file.
    - `hres`, `vres`: int, the horizontal and vertical DPI (resolution) of the image.
    - `palette`: bytes, contains the color palette data from the header.
    - `nplanes`: int, the number of color planes in the image (e.g., RGB).
    - `bytes_per_line`: int, the number of bytes per scanline (line of pixels).
    - `palette_type`: int, indicates whether the image uses a color palette (usually 1 for color, 0 for grayscale).
    - `width`, `height`: int, the calculated width and height of the image based on the header information.

    Returns:
    - None

    Function Workflow:
    1. Prompts the user to select a PCX file using a file dialog.
    2. If a file is selected, reads the first 128 bytes as the header and unpacks them to extract the PCX metadata.
    3. Calculates image dimensions (`width` and `height`) based on the header.
    4. If the dimensions are valid, the function displays the image and header information in the application window.
    5. Handles errors such as missing files, invalid header structure, or invalid image dimensions.
    6. Calls `display_color_palette()` to show the color palette of the PCX file (if applicable).

    Raises:
    - FileNotFoundError: If the file cannot be found.
    - struct.error: If the header structure is incorrect or corrupted.
    - ValueError: If the file dimensions are invalid (non-positive values).

    Interactions with UI Elements:
    - `main_frame`: The main application interface that is hidden once the PCX image is displayed.
    - `header_frame`: A frame that displays the header metadata and image once the PCX file is opened.
    - `info_label`: A label widget that shows the extracted PCX header information.
    - `img_label`: A label widget that displays the image extracted from the PCX file.
    - `back_button`: A button widget that allows the user to return to the main screen.
    - `display_color_palette()`: A helper function that displays the color palette of the PCX file.
    """

    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    if not file_path:
        return  # If no file is selected, return

    try:
        # Open the file and read the first 128 bytes as the header
        with open(file_path, 'rb') as f:
            header = f.read(128)

            # Unpack the PCX header to extract metadata
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

            # Calculate image dimensions
            width = xmax - xmin + 1
            height = ymax - ymin + 1

            # Ensure dimensions are valid
            if width <= 0 or height <= 0:
                raise ValueError("Invalid PCX file: dimensions are non-positive.")

            # Prepare header information for display
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

            # Update the UI to display the header and image
            main_frame.place_forget()
            header_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

            info_label.config(text=header_info)

            # Load and display the PCX image
            pcx_image = Image.open(file_path)
            pcx_photo = ImageTk.PhotoImage(pcx_image)
            img_label.config(image=pcx_photo)
            img_label.image = pcx_photo  # Prevent garbage collection
            img_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)

            # Display the back button
            back_button.place(relx=0.05, rely=0.05)

            # Display the color palette from the PCX file (if available)
            display_color_palette(file_path)

    except (FileNotFoundError, struct.error, ValueError) as e:
        # Handle potential errors when opening or reading the PCX file
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

# Function to display the color palette from a PCX file
def display_color_palette(file_path):
    """
    Extracts and displays the color palette from a PCX file, if the palette is present. 
    The color palette is shown as a 16x16 grid of colors in the user interface.

    Parameters:
    - file_path: str, the file path of the selected PCX file.

    Internal Parameters:
    - `f`: file object, represents the open PCX file.
    - `palette_header`: bytes, a 1-byte value that identifies the start of the color palette. 
      In PCX files, this should be `\x0C`.
    - `palette_data`: bytes, contains the actual RGB values for the palette, with each color 
      represented by 3 bytes (R, G, B).
    - `colors`: list of tuples, where each tuple represents a color in (R, G, B) format. 
      The palette contains 256 colors, so `colors` will be a list of 256 tuples.
    - `palette_image`: PIL Image object, a 16x16 pixel image created to represent the palette, 
      where each pixel corresponds to one of the 256 colors in the PCX palette.
    - `palette_tk`: PhotoImage, a Tkinter-compatible image object that allows the palette to be 
      displayed on the interface.

    Returns:
    - None

    Function Workflow:
    1. Opens the PCX file in binary mode and seeks to the last 769 bytes of the file. The palette 
       starts 769 bytes from the end, and the preceding byte should be `\x0C` (a specific marker).
    2. Verifies if the palette header is valid by checking if it equals `\x0C`.
    3. Reads the following 768 bytes, which represent the RGB values of the 256-color palette.
    4. Converts the palette data into a list of 256 RGB tuples, where each tuple is 3 bytes 
       representing Red, Green, and Blue.
    5. Creates a 16x16 pixel image where each pixel corresponds to one of the 256 colors in the palette.
    6. Enlarges the image to 128x128 pixels to make it visible and converts it to a format compatible 
       with Tkinter for display.
    7. Updates the `palette_label` widget to display the image in the interface.

    Raises:
    - None

    Interactions with UI Elements:
    - `palette_label`: A label widget in the user interface that displays the color palette as an image.
    """

    # Open the PCX file in binary mode
    with open(file_path, 'rb') as f:
        # Move to the location of the palette data (last 769 bytes)
        f.seek(-769, 2)  # Seek to the position 769 bytes before the end of the file
        
        # Read the palette header, which should be 1 byte (\x0C) to indicate the presence of a palette
        palette_header = f.read(1)
        
        if palette_header == b'\x0C':  # Validate the palette header
            # Read the next 768 bytes containing the RGB values of the palette (256 colors, 3 bytes each)
            palette_data = f.read(768)

            # Convert the palette data into a list of 256 RGB tuples
            colors = [tuple(palette_data[i:i + 3]) for i in range(0, 768, 3)]

            # Create a 16x16 image with the extracted color palette
            palette_image = Image.new('RGB', (16, 16))  # Create a blank 16x16 RGB image
            palette_image.putdata(colors)  # Populate the image with the palette colors

            # Resize the palette image to 128x128 for better visibility
            palette_image = palette_image.resize((128, 128), Image.NEAREST)

            # Convert the palette image to a Tkinter-compatible format
            palette_tk = ImageTk.PhotoImage(palette_image)

            # Update the palette_label in the UI with the new image
            palette_label.config(image=palette_tk)
            palette_label.image = palette_tk  # Prevent garbage collection by keeping a reference

# GUIDE 3: Image Enhancement Basics (Channels and Histograms)
# Function to allow the user to choose which channels to display using buttons and show the corresponding histograms
def display_histogram():
    """
    Opens a PCX file, allows the user to select an RGB channel or grayscale version, and 
    displays both the selected image and its corresponding histogram.

    Parameters:
    - None: This function does not take any external parameters.
    
    Internal Parameters:
    - `file_path`: str, the file path of the selected PCX image.
    - `pcx_image`: PIL Image object, represents the loaded PCX image file.
    - `r`, `g`, `b`: PIL Image objects, the red, green, and blue channels extracted from the PCX image.
    - `gray_image`: PIL Image object, a grayscale version of the PCX image.
    - `selection_window`: Toplevel, a new window that allows the user to choose which channel to display.
    - `custom_font`: tkFont object, defines the custom font used for labels and buttons in the window.
    - `channel`: PIL Image object, passed as a parameter to the `show_channel` function to represent the selected channel (R, G, B, or grayscale).
    - `channel_name`: str, name of the channel being displayed (e.g., "Red", "Green", "Blue", or "Grayscale").
    - `color`: str, the color corresponding to the selected channel, used in titles and display.
    - `img`: PIL Image object, the image corresponding to the selected channel, used for display in `imshow`.
    - `ax_color_map`: str, the color map for displaying the channel using Matplotlib (e.g., "Reds", "Greens", "Blues", or "gray").
    - `hist_color`: str, the color used to display the histogram for the selected channel.
    
    Function Workflow:
    1. Opens a file dialog for the user to select a PCX file.
    2. Loads the selected PCX image and ensures it's in RGB format. If not, it converts the image to RGB.
    3. Splits the image into its red, green, and blue channels. Additionally, converts the image into grayscale.
    4. Opens a new window allowing the user to choose which channel (Red, Green, Blue, or Grayscale) to display.
    5. Defines a nested function `show_channel` that takes the selected channel, displays it using Matplotlib, 
       and plots a histogram of the pixel intensities for the selected channel.
    6. Provides buttons in the selection window for each channel. When a button is clicked, 
       it calls `show_channel` with the appropriate parameters to display the channel and its histogram.

    Returns:
    - None
    
    Raises:
    - Exception: If the file cannot be opened, it displays an error message in a messagebox.

    Interactions with UI Elements:
    - `selection_window`: A new window is created for channel selection.
    - `custom_font`: Used to style the text for buttons and labels in the selection window.
    - `show_channel`: Called by each button to display the selected channel and its histogram.
    """

    # Set a custom font for labels and buttons
    custom_font = font.Font(family="HYWenHei-85W", size=12)

    # Open a file dialog to select the PCX file
    file_path = filedialog.askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    if not file_path:
        return  # If no file is selected, return

    try:
        # Load the PCX image using PIL
        pcx_image = Image.open(file_path)

        # Ensure the image is in RGB mode, converting if necessary
        if pcx_image.mode != 'RGB':
            pcx_image = pcx_image.convert('RGB')

        # Split the image into its red, green, and blue channels
        r, g, b = pcx_image.split()

        # Convert the image to grayscale
        gray_image = pcx_image.convert('L')

        # Create a new window to let the user select which channel to view
        selection_window = Toplevel(root)
        selection_window.title("Select Channels")

        # Update label with custom font
        Label(selection_window, text="Select a channel:", font=custom_font).pack(padx=10, pady=10)

        # Nested function to display the selected channel and its histogram
        def show_channel(channel, channel_name, color, img, ax_color_map, hist_color):
            """
            Displays the selected image channel and its histogram in a Matplotlib figure.

            Parameters:
            - channel: PIL Image object, the selected image channel (R, G, B, or grayscale).
            - channel_name: str, the name of the channel (e.g., "Red", "Green", "Blue", or "Grayscale").
            - color: str, the color associated with the channel, used for display purposes.
            - img: PIL Image object, the image corresponding to the selected channel.
            - ax_color_map: str, the color map used for displaying the image.
            - hist_color: str, the color used for the histogram plot.

            Workflow:
            1. Creates a Matplotlib figure with two subplots (one for the image and one for the histogram).
            2. Displays the selected channel using the appropriate color map.
            3. Plots a histogram showing the pixel intensity distribution for the selected channel.
            4. Adjusts the layout and displays the figure.
            """
            fig, axs = plt.subplots(2, 1, figsize=(6, 6))
            fig.suptitle(f'{channel_name} Channel and Histogram')

            # Display the selected image channel
            axs[0].imshow(img, cmap=ax_color_map)
            axs[0].set_title(f"{channel_name} Channel")
            axs[0].axis("off")

            # Display the histogram for the selected channel
            axs[1].hist(np.array(channel).ravel(), bins=256, color=hist_color, alpha=0.6)
            axs[1].set_title(f"{channel_name} Histogram")

            # Adjust layout and display
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
        # Display an error message if file opening fails
        messagebox.showerror("Error", f"Failed to open PCX file: {e}")

# Function for grayscale transformation using the formula s = (R + G + B) / 3
def grayscale_transformation(image):
    """
    Converts an RGB image to grayscale using the formula: 
    s = (R + G + B) / 3, where s is the grayscale value.

    Parameters:
    - image (PIL.Image.Image): The input image in RGB mode that will be converted to grayscale.

    Returns:
    - grayscale_image (PIL.Image.Image): A new image in grayscale mode ("L") where each pixel 
      is the result of applying the formula to the corresponding RGB values from the original image.

    Internal Parameters:
    - width (int): The width of the input image in pixels.
    - height (int): The height of the input image in pixels.
    - r, g, b (int): The red, green, and blue values for each pixel in the image, respectively.
    - gray_value (int): The calculated grayscale value for each pixel, obtained by averaging the RGB values.

    Function Workflow:
    1. Checks if the input image is in RGB mode. If not, it converts the image to RGB.
    2. Creates a new blank image in grayscale mode ("L") with the same width and height as the original.
    3. Iterates over each pixel of the input image:
        - Retrieves the RGB values for the current pixel.
        - Computes the grayscale value by averaging the red, green, and blue values.
        - Updates the pixel in the new grayscale image with this computed value.
    4. Returns the newly generated grayscale image.

    Returns:
    - A new grayscale image (mode "L") with the same dimensions as the input image.

    Example:
    - If the original image is 200x300 in RGB, the resulting grayscale image will also be 200x300,
      but each pixel will contain a single grayscale value (instead of RGB values).

    Notes:
    - The conversion is a simple average method. Other grayscale conversion methods may use different
      weightings for R, G, and B components (e.g., luminosity method), but this function uses a basic average.
    """

    # Convert the image to RGB mode (if not already)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get the width and height of the input image
    width, height = image.size

    # Create a new image for grayscale (mode "L" for 8-bit pixels, black and white)
    grayscale_image = Image.new("L", (width, height))

    # Iterate over each pixel and apply the grayscale formula
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # Get the RGB values at pixel (x, y)
            # Calculate the grayscale value by averaging the RGB values
            gray_value = int((r + g + b) / 3)
            # Set the grayscale pixel at the corresponding (x, y) location in the new image
            grayscale_image.putpixel((x, y), gray_value)

    return grayscale_image

# Function for negative of an image
def negative_transformation(image):
    """
    Converts an RGB image to its negative using the formula: 
    s = 255 - r, g, b for each pixel in the image.

    Parameters:
        image (PIL.Image.Image): An image object in RGB mode or another mode 
        that can be converted to RGB. The image should be provided as a PIL Image object.

    Returns:
        PIL.Image.Image: A new image object representing the negative transformation of the input image.
    """

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
    """
    Converts an image to black and white using a manual threshold.

    The function converts the input image to grayscale and applies a binary threshold.
    Pixels with a value above the threshold are set to white (255), and those below
    are set to black (0).

    Parameters:
        image (PIL.Image.Image): An image object that will be converted to black and white.
        threshold_value (int): A value between 0 and 255 that determines the threshold
                               for converting pixels to black or white.

    Returns:
        PIL.Image.Image: A new image object in black and white (binary image) 
                         resulting from the thresholding operation.
    """

    # Convert the image to an array for processing
    image_array = np.array(image.convert('RGB'))
    
    # Convert to grayscale
    grayscale_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Apply threshold
    _, bw_image = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Convert back to PIL Image for consistency
    return Image.fromarray(bw_image)
  
# Function for power-law (gamma) transformation
def gamma_transformation(image, gamma_value):
    """
    Applies gamma transformation to an image, adjusting the brightness 
    of the image based on the specified gamma value.

    The gamma transformation formula is given by:
        s = 255 * (r / 255) ** gamma_value
    where r, g, and b are the original pixel values.

    Parameters:
        image (PIL.Image.Image): An image object that will be transformed.
        gamma_value (float): A positive value that determines the level of 
                             transformation. Values less than 1 darken the image,
                             while values greater than 1 brighten it.

    Returns:
        PIL.Image.Image: A new image object resulting from the gamma transformation.
    """
    
    # Convert the image to RGB mode (if not already)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a new image for the gamma transformation
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

# GUIDE 4: Point-Processing Methods
def apply_point_processing():
    """
    Displays a menu for the user to choose an image enhancement or point processing method.

    This function creates a graphical user interface (GUI) window that allows users to select
    different point processing techniques for image enhancement. The options include grayscale
    transformation, negative transformation, black and white thresholding, and gamma transformation.
    Based on the user's selection, the appropriate filters are applied to the chosen image, 
    and the results are displayed side-by-side.

    Global Variables:
        enhancement_window (tk.Toplevel): A reference to the current enhancement window, 
                                           allowing for window management.

    Functions Defined:
        - display_results(original_image, processed_image, title): Displays the original and processed images.
        - apply_filter(filter_func, *args): Applies the chosen filter to the selected image.
        - show_threshold_slider(): Displays the UI for black and white thresholding.
        - show_gamma_slider(): Displays the UI for gamma transformation.
        - confirm_point_processing(): Applies the selected point processing method based on user input.

    No parameters are required to call this function.
    No return value; it creates and manages a GUI window for user interaction.
    """
    
    global enhancement_window  # Use the global variable
    selected_filter = None  # Initialize the selected filter variable

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
    enhancement_window.title("Point Processing")

    # Keep the enhancement window on top of others
    enhancement_window.attributes('-topmost', True)

    # Create frames for layout
    left_frame = Frame(enhancement_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = Frame(enhancement_window)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    custom_font = font.Font(family="HYWenHei-85W", size=12)

    # Add labels or instructions in the left column
    Label(left_frame, text="Select a point-processing method:", font=custom_font).pack(pady=5)

    # Create a label and entry for threshold and gamma value (initially hidden)
    threshold_label = Label(left_frame, text="Threshold Value (0-255):", font=custom_font)
    threshold_slider = tk.Scale(left_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200)

    gamma_label = Label(left_frame, text="Gamma Value (0.0-5.0):", font=custom_font)
    gamma_slider = tk.Scale(left_frame, from_=0.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)

    # Button for confirming filter with dynamic input (initially hidden)
    confirm_button = Button(left_frame, text="Confirm", command=lambda: confirm_point_processing(), font=custom_font)

    def show_threshold_slider():
        """Show the threshold input for black/white thresholding."""
        nonlocal selected_filter  # Access and modify the outer variable
        selected_filter = 'Black and White Thresholding'  # Set the selected filter

        gamma_slider.pack_forget()
        gamma_label.pack_forget()
        threshold_label.pack(pady=5)
        threshold_slider.pack(pady=5)
        confirm_button.pack(pady=5)  # Show confirm button

    def show_gamma_slider():
        """Show the gamma input for gamma transformation."""
        nonlocal selected_filter  # Access and modify the outer variable
        selected_filter = 'Gamma Transformation'  # Set the selected filter

        threshold_slider.pack_forget()
        threshold_label.pack_forget()
        gamma_label.pack(pady=5)
        gamma_slider.pack(pady=5)
        confirm_button.pack(pady=5)  # Show confirm button

    def confirm_point_processing():
        """Applies the selected point processing method."""
        # Apply the appropriate method based on user selection
        threshold_value = threshold_slider.get()
        gamma_value = gamma_slider.get()

        if selected_filter == 'Black and White Thresholding':
            apply_filter(black_white_thresholding, threshold_value)
        elif selected_filter == 'Gamma Transformation':
            apply_filter(gamma_transformation, gamma_value)

        # Hide the confirm button after processing
        confirm_button.pack_forget()
        # Hide sliders after confirmation
        if selected_filter == 'Black and White Thresholding':
            threshold_label.pack_forget()
            threshold_slider.pack_forget()
        elif selected_filter == 'Gamma Transformation':
            gamma_label.pack_forget()
            gamma_slider.pack_forget()

    # Add buttons for the point processing filters in the right column
    Button(right_frame, text="Grayscale Transformation", command=lambda: apply_filter(grayscale_transformation), font=custom_font).pack(pady=5)
    Button(right_frame, text="Negative Transformation", command=lambda: apply_filter(negative_transformation), font=custom_font).pack(pady=5)
    Button(right_frame, text="Black and White Thresholding", command=show_threshold_slider, font=custom_font).pack(pady=5)
    Button(right_frame, text="Gamma Transformation", command=show_gamma_slider, font=custom_font).pack(pady=5)

# Functions for image enhancements: UNSHARP MASK
def apply_unsharp_mask(image, sigma=10.0, strength=1.5):
    """
    Applies unsharp masking to the input PCX image by processing each RGB channel separately.

    Unsharp masking enhances the sharpness of an image by subtracting a blurred version 
    of the image from the original, effectively increasing the contrast of the edges.

    Parameters:
        image (PIL.Image): The input image in RGB format that will be sharpened.
        sigma (float, optional): The standard deviation of the Gaussian kernel used for blurring. 
                                 Default value is 10.0. A larger sigma results in a more blurred 
                                 image, which can enhance the sharpening effect.
        strength (float, optional): The strength of the sharpening effect. Default value is 1.5. 
                                     A higher value results in a stronger sharpening effect.

    Returns:
        PIL.Image: The sharpened image in RGB format, with pixel values clipped to the range [0, 255].
    
    Raises:
        ValueError: If the input image is not a color image with 3 channels (RGB).
    """
    
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

# Functions for image enhancements: HIGHBOOST FILTER
def apply_highboost_filter(image, amplification=2.0):
    """
    Applies highboost filtering to the input image, enhancing its sharpness 
    by amplifying the high-frequency components while retaining the original image.

    Highboost filtering is a technique used to enhance the sharpness of an image 
    by subtracting a blurred version of the image from the original and then 
    amplifying the result.

    Parameters:
        image (PIL.Image): The input RGB image to be processed.
        amplification (float, optional): The factor by which to amplify the high-frequency details. 
                                          Default value is 2.0. Higher values result in a stronger 
                                          sharpening effect.

    Returns:
        PIL.Image: The highboost-filtered image in RGB format, with pixel values clipped 
                    to the range [0, 255].
    
    Raises:
        ValueError: If the input image is not a color image with 3 channels (RGB).
    """

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

# Functions for image enhancements: SOBEL MAGNITUDE OPERATOR
def apply_sobel_operator(image):
    """
    Applies the Sobel magnitude operator for edge detection in the input image.

    The Sobel operator computes the gradient of the image intensity function, 
    providing information about the edges present in the image. This function 
    calculates the gradient in both the x and y directions and combines them 
    to determine the overall edge strength.

    Parameters:
        image (PIL.Image): The input RGB or grayscale image to be processed.

    Returns:
        PIL.Image: An image highlighting the edges detected using the Sobel operator, 
                    normalized to an 8-bit unsigned integer format.
    """

    # Convert the input image to a grayscale image (L mode) and then to a numpy array
    image_array = np.array(image.convert('L'))

    # Apply the Sobel operator in the x direction to detect horizontal edges
    sobel_x = cv2.Sobel(image_array, cv2.CV_64F, 1, 0, ksize=3)

    # Apply the Sobel operator in the y direction to detect vertical edges
    sobel_y = cv2.Sobel(image_array, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the magnitude of the Sobel gradients using the Pythagorean theorem
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalize the Sobel magnitude to the range [0, 255]
    sobel_magnitude = (sobel_magnitude / np.max(sobel_magnitude)) * 255

    # Convert the Sobel magnitude array to an 8-bit unsigned integer format
    sobel_magnitude = np.uint8(sobel_magnitude)

    # Convert the resulting numpy array back to a PIL Image
    sobel_image = Image.fromarray(sobel_magnitude)

    return sobel_image

# Functions for image enhancements: AVERAGING FILTER
def apply_averaging(image):
    """
    Applies an averaging filter to the input image to create a blurring effect.

    The averaging filter smoothens the image by replacing each pixel's value 
    with the average of its neighboring pixels. This can help reduce noise 
    and detail in the image.

    Parameters:
        image (PIL.Image): The input RGB image to be blurred.

    Returns:
        PIL.Image: The blurred image resulting from the application of the 
                    averaging filter, normalized to an 8-bit unsigned integer format.
    """

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

# Functions for image enhancements: MEDIAN FILTER
def apply_median(image):
    """
    Applies a median filter to the input image to reduce noise and smooth the image.

    The median filter replaces each pixel's value with the median value of the 
    intensities in its neighborhood. This is particularly effective for reducing 
    salt-and-pepper noise while preserving edges.

    Parameters:
        image (PIL.Image): The input RGB image to be processed.

    Returns:
        PIL.Image: The image after applying the median filter, normalized to an 
                    8-bit unsigned integer format.
    """

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
    
    # Clip pixel values to ensure they are within the valid range [0, 255] 
    # and return as a PIL Image
    return Image.fromarray(np.clip(median_filtered_image, 0, 255).astype(np.uint8))

# Functions for image enhancements: HIGHPASS FILTER
def apply_highpass(image):
    """
    Applies a high-pass filter to the input image using the Laplacian operator to 
    enhance the edges.

    The high-pass filter works by subtracting the low-frequency components from 
    the original image, allowing the high-frequency details (edges) to be accentuated. 
    This is useful in image processing tasks where edge detection or enhancement is needed.

    Parameters:
        image (PIL.Image): The input image to be processed. This should be in RGB or grayscale format.

    Returns:
        PIL.Image: The image after applying the high-pass filter, represented in 
                    8-bit unsigned integer format suitable for display.
    """

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

# GUIDE 5: Image Enhancement - Spatial Domain
# Function to handle the menu for image enhancement 
def image_enhancement():
    """
    Displays a menu for the user to choose an image enhancement method.

    This function creates a GUI window that allows the user to select from various 
    image enhancement techniques such as averaging, median filtering, highpass filtering, 
    and others. It allows users to load an image file, apply the chosen enhancement, 
    and view the results.

    Global Variables:
        enhancement_window (Tkinter.Toplevel): A window that displays the enhancement options.
    """

    global enhancement_window  # Use the global variable

    custom_font = font.Font(family="HYWenHei-85W", size=12)

    # Check if the enhancement window already exists
    if enhancement_window is not None and enhancement_window.winfo_exists():
        enhancement_window.lift()  # Bring the existing window to the front
        return  # Exit the function to avoid creating a new window

    def display_results(original_image, processed_image, title):
        """
        Displays the original and processed images in a new figure.

        Parameters:
            original_image (PIL.Image): The original image before processing.
            processed_image (numpy.ndarray): The processed image after applying the filter.
            title (str): Title for the figure.
        """
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns layout
        fig.suptitle(title)

        # Display the original image
        axs[0].imshow(original_image.convert("RGB"))  # Convert original to RGB for correct display
        axs[0].set_title('Original Image')
        axs[0].axis('off')

        # Display the processed image as grayscale
        axs[1].imshow(processed_image, cmap='gray')  # Ensure processed image is displayed in grayscale
        axs[1].set_title('Processed Image')
        axs[1].axis('off')

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)  # Adjust title positioning
        plt.show()

    def apply_filter(filter_func, *args):
        """
        Applies the chosen filter to the selected image.

        Parameters:
            filter_func (function): The filter function to apply to the image.
            *args: Additional arguments to pass to the filter function.
        """
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

    # Add a label above the enhancement buttons in the right column
    method_label = Label(left_frame, text="Select an enhancement method:", font=custom_font)
    method_label.pack(pady=5)

    # Create a label and slider for amplification value (initially hidden)
    amplification_label = Label(left_frame, text="Amplification Value (default: 2.0):", font=custom_font)
    amplification_slider = tk.Scale(left_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
    amplification_slider.set(2.0)  # Default value

    # Button for confirming highboost filter (initially hidden)
    confirm_button = Button(left_frame, text="Confirm Highboost Filtering", command=lambda: confirm_highboost_filter(), font=custom_font)

    def show_amplification_input():
        """Show the amplification input when the highboost filtering button is clicked."""
        amplification_label.pack(pady=5)
        amplification_slider.pack(pady=5)
        confirm_button.pack(pady=5)  # Show confirm button

    def confirm_highboost_filter():
        """Applies the highboost filter with the specified amplification value."""
        amplification_value = amplification_slider.get()
        apply_filter(apply_highboost_filter, amplification_value)
        # Hide the amplification input after applying
        amplification_label.pack_forget()
        amplification_slider.pack_forget()
        confirm_button.pack_forget()

    # Add buttons for the image enhancement filters in the right column
    Button(right_frame, text="Averaging Filter", command=lambda: apply_filter(apply_averaging), font=custom_font).pack(pady=5)
    Button(right_frame, text="Median Filter", command=lambda: apply_filter(apply_median), font=custom_font).pack(pady=5)
    Button(right_frame, text="Highpass Filter (Laplacian)", command=lambda: apply_filter(apply_highpass), font=custom_font).pack(pady=5)
    Button(right_frame, text="Unsharp Masking", command=lambda: apply_filter(apply_unsharp_mask), font=custom_font).pack(pady=5)
    Button(right_frame, text="Highboost Filtering", command=show_amplification_input, font=custom_font).pack(pady=5)
    Button(right_frame, text="Sobel Magnitude Operator", command=lambda: apply_filter(apply_sobel_operator), font=custom_font).pack(pady=5)

# Create the header frame to display the image and header information
header_frame = tk.Frame(root, bg="#7db1ce", bd=0)
header_frame.place_forget()  # Initially hidden to prevent display until needed

# Label for displaying information (e.g., image metadata)
info_label = tk.Label(header_frame, text="", justify=tk.LEFT, bg="#7db1ce", font=custom_font)
info_label.pack(side=tk.LEFT, padx=(150, 60), pady=10)

# Label for displaying the main image in the header
img_label = tk.Label(header_frame, bg="#7db1ce")
img_label.pack(side=tk.LEFT, padx=(5, 5), pady=10)

# Label for displaying a palette or color reference, aligned to the right
palette_label = tk.Label(header_frame, bg="#7db1ce")
palette_label.pack(side=tk.RIGHT, padx=(60, 150), pady=10)

# Create an image label for the displayed image on the main canvas
image_label = tk.Label(root, bg="#7db1ce")

# Load images for the icons (including the new image enhancement icon)
image_enhancement_image = Image.open("image_enhancement.png")
image_enhancement_image = image_enhancement_image.resize(viewer_image.size, Image.LANCZOS)  # Resize to match viewer dimensions
image_enhancement_icon = ImageTk.PhotoImage(image_enhancement_image)  # Convert to PhotoImage for use in buttons

# Create the back button (initially hidden) with custom styling
back_button = tk.Button(
    root, 
    text="< Back", 
    command=go_back,  # Function to navigate back in the application
    font=custom_font,  # Apply custom font for consistency
    bg="#222437",      # Background color to match the application's theme
    fg="white",        # Text color for contrast against the background
    bd=0,              # Borderless button for a modern look
    padx=10,           # Horizontal padding to increase the clickable area
    pady=5             # Vertical padding to enhance button size
)
back_button.place_forget()  # Hide initially until required

# Add buttons for different functionalities in the main application frame
button_viewer = tk.Button(
    main_frame, 
    image=viewer_icon,  # Icon for the image viewer button
    text="Image Viewer", 
    compound=tk.TOP,    # Position text above the image
    command=open_image,  # Function to open the image viewer
    font=custom_font     # Apply the custom font
)
button_viewer.grid(row=1, column=0, padx=50, pady=50)  # Position in the grid layout

button_pcx = tk.Button(
    main_frame, 
    image=pcx_inspect_icon,  # Icon for the PCX inspector button
    text="PCX Inspector", 
    compound=tk.TOP,         # Position text above the image
    command=open_pcx_file,   # Function to open the PCX file inspector
    font=custom_font         # Apply the custom font
)
button_pcx.grid(row=1, column=1, padx=50, pady=50)  # Position in the grid layout

button_histogram = tk.Button(
    main_frame, 
    image=histogram_icon,  # Icon for the histogram button
    text="Histogram", 
    compound=tk.TOP,       # Position text above the image
    command=display_histogram,  # Function to display the histogram
    font=custom_font       # Apply the custom font
)
button_histogram.grid(row=1, column=2, padx=50, pady=50)  # Position in the grid layout

button_point_processing = tk.Button(
    main_frame, 
    image=point_processing_icon,  # Icon for the point processing button
    text="Point Processing", 
    compound=tk.TOP,              # Position text above the image
    command=apply_point_processing,  # Function to apply point processing operations
    font=custom_font              # Apply the custom font
)
button_point_processing.grid(row=1, column=3, padx=50, pady=50)  # Position in the grid layout

# Add Image Enhancement button to the main frame
image_enhancement_button = tk.Button(
    main_frame, 
    image=image_enhancement_icon,  # Icon for the image enhancement button
    text="Image Enhancement", 
    compound="top",                # Position text above the image
    command=image_enhancement,     # Function to open the image enhancement menu
    font=custom_font               # Apply the custom font
)
image_enhancement_button.grid(row=1, column=4, padx=20, pady=20)  # Position in the grid layout

# Run the main loop
root.mainloop()