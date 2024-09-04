import tkinter as tk
from tkinter import font, filedialog
from PIL import Image, ImageTk, ImageDraw

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

    for rect in rectangles:
        canvas.delete(rect)
    rectangles.clear()



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

# Label to display the selected image
image_label = tk.Label(root, bg="#7db1ce")
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

# Run the main loop
root.mainloop()