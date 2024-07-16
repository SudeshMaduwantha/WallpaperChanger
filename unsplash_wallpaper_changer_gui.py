#UNSPLASH_ACCESS_KEY = 'x6vl-HZF9-Lt1LUk3IM5Y9387mehPi0utSuu2Kn6QNk'

import ctypes
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO
from PIL import Image

SPI_SETDESKWALLPAPER = 20

UNSPLASH_ACCESS_KEY = 'x6vl-HZF9-Lt1LUk3IM5Y9387mehPi0utSuu2Kn6QNk'  # Replace with your Unsplash API Access Key
UNSPLASH_URL = 'https://api.unsplash.com/photos/random'

# Specify absolute path for image saving
IMAGE_SAVE_PATH = r"C:\Users\sudes\Desktop\Wallpaper Changer\current_wallpaper.jpg"

def set_wallpaper(image_path):
    """Set desktop wallpaper using ctypes."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def fetch_random_image(category=None):
    """Fetch a random image from Unsplash."""
    params = {'client_id': UNSPLASH_ACCESS_KEY, 'count': 1}
    if category:
        params['query'] = category
    
    response = requests.get(UNSPLASH_URL, params=params)
    if response.status_code == 403:
        print("Error fetching image: 403 Forbidden")
        return None
    data = response.json()
    image_url = data[0]['urls']['full']

    # Download the image
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))

    # Save the image to a file
    image.save(IMAGE_SAVE_PATH)
    return IMAGE_SAVE_PATH

def change_wallpapers(interval, categories):
    """Thread function to change wallpapers at a specified interval."""
    while True:
        for category in categories:
            image_path = fetch_random_image(category)
            if image_path:
                set_wallpaper(image_path)
            time.sleep(interval)

def start_changing_wallpapers(interval, categories):
    """Start wallpaper changer in a separate thread."""
    t = threading.Thread(target=change_wallpapers, args=(interval, categories))
    t.daemon = True
    t.start()

def start():
    """Start button callback."""
    try:
        interval = int(interval_var.get())
        selected_categories = [category.get() for category in category_vars if category.get()]
        if not selected_categories:
            messagebox.showerror("Error", "Please select at least one category.")
            return
        start_changing_wallpapers(interval, selected_categories)
        messagebox.showinfo("Started", "Wallpaper changer started.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid interval.")

# Create the main window
root = tk.Tk()
root.title("Unsplash Wallpaper Changer")
root.configure(bg="white")  # Set background color
root.className = "UnsplashWallpaperChangerMainWindowClass"  # Set class name

# Center the window on the screen
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Interval input
tk.Label(root, text="Interval (seconds):").grid(row=0, column=0, padx=10, pady=10)
interval_var = tk.StringVar()
interval_var.set("60")  # Default interval value
tk.Entry(root, textvariable=interval_var, width=10).grid(row=0, column=1, padx=10, pady=10)

# Suggested categories
categories = ['Nature', 'Architecture', 'Technology', 'Travel']
category_vars = []
for i, category in enumerate(categories):
    var = tk.StringVar(value="")
    category_vars.append(var)
    tk.Checkbutton(root, text=category, variable=var, onvalue=category, offvalue="").grid(row=i+1, column=0, columnspan=2, padx=10, pady=5)

# Start button
start_button = tk.Button(root, text="Start", command=start)
start_button.grid(row=len(categories)+1, column=0, columnspan=2, pady=10)

# Label for software information
software_label = tk.Label(root, text="Software by Sudesh Maduwantha Kumarasiri", bg="white", fg="blue")
software_label.grid(row=len(categories)+2, column=0, columnspan=2, pady=5)

# Run the application
root.mainloop()
