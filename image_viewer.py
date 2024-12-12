import os
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, Slider, ColumnDataSource
from bokeh.plotting import figure
from PIL import Image, ImageEnhance
from io import BytesIO
import base64
import threading

# Path to the folder containing images
IMAGE_FOLDER = "image_folder"  # Replace with your actual folder path

# List of image file paths
image_files = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Index to track current image
current_index = 0

# Initial contrast level
contrast_level = 1.0

# Initial image
if image_files:
    encoded_img = base64.b64encode(open(image_files[current_index], "rb").read()).decode()
else:
    encoded_img = ""

source = ColumnDataSource(data=dict(url=[f"data:image/png;base64,{encoded_img}"]))

# Create a plot
plot = figure(x_range=(0, 1), y_range=(0, 1), title="Image Viewer", tools="", toolbar_location=None)
plot.image_url(url="url", source=source, x=0, y=1, w=1, h=1)

def update_image():
    global current_index, contrast_level
    if image_files:
        encoded_img = load_image(current_index, contrast_level)
        source.data = dict(url=[f"data:image/png;base64,{encoded_img}"])

def next_image():
    global current_index
    if image_files:
        current_index = (current_index + 1) % len(image_files)
        update_image()

def previous_image():
    global current_index
    if image_files:
        current_index = (current_index - 1) % len(image_files)
        update_image()

def load_image(index, contrast):
    img = Image.open(image_files[index])
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Debounce the slider update
debounce_timer = None

def update_contrast(attr, old, new):
    global contrast_level, debounce_timer
    contrast_level = new

    # Cancel the previous timer
    if debounce_timer:
        debounce_timer.cancel()

    # Start a new timer
    def debounce_update():
        curdoc().add_next_tick_callback(update_image)
    
    debounce_timer = threading.Timer(0.5, debounce_update)
    debounce_timer.start()

# Ensure the image updates when the slider value stops changing
def update_contrast_on_release(attr, old, new):
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    curdoc().add_next_tick_callback(update_image)

# Create buttons and slider
button_next = Button(label="Next", button_type="success")
button_previous = Button(label="Previous", button_type="success")
slider_contrast = Slider(start=0.1, end=3.0, value=1.0, step=0.1, title="Contrast")

# Add event listeners
button_next.on_click(next_image)
button_previous.on_click(previous_image)
slider_contrast.on_change('value', update_contrast)
slider_contrast.on_change('value_throttled', update_contrast_on_release)

# Layout
layout = column(plot, row(button_previous, button_next), slider_contrast)
curdoc().add_root(layout)
curdoc().title = "Interactive Image Viewer"

