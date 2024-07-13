import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Directories
base_input_dir = "downloaded_photos"
base_output_dir = "labeled_photos"
os.makedirs(base_output_dir, exist_ok=True)

# Font settings for the labels and values
# c:\windows\Fonts\ARLRDBD.TTF
font_path = "C:\\windows\\Fonts\\ARLRDBD.TTF"  # Path to the ARIAL BOLD MT font file on Windows
font_size = 50  # Uniform font size for labels and values
font = ImageFont.truetype(font_path, font_size)

# Test mode variable
test =   False #Set to False to process all images

def draw_text_with_border(draw, position, text, font, border_color, text_color):
    x, y = position
    # Draw border with increased thickness for bold effect
    offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2),
               (-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
    for ox, oy in offsets:
        draw.text((x + ox, y + oy), text, font=font, fill=border_color)
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)

def add_label_to_image(input_path, output_path, label_text):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    x, y = 80, 60  # Position for the label text with larger margin
    
    # Draw label with the same font
    draw_text_with_border(draw, (x, y), label_text, font, "white", "black")
    
    image.save(output_path)

def format_filename(parcel, transect, bearing, date):
    # Ensure the correct format for the filename
    parcel = parcel.ljust(6, '0')
    transect = f"{int(transect):02d}"
    bearing = f"{int(bearing):03d}"
    year = datetime.strptime(date, '%Y%m%d').strftime('%Y')
    return f"{parcel}_{transect}_{bearing}_{year}.jpg"

# Process images in the input directory
for year_dir in os.listdir(base_input_dir):
    year_input_dir = os.path.join(base_input_dir, year_dir)
    if os.path.isdir(year_input_dir):
        year_output_dir = os.path.join(base_output_dir, year_dir)
        os.makedirs(year_output_dir, exist_ok=True)
        
        for filename in os.listdir(year_input_dir):
            if filename.endswith(".jpg"):
                input_path = os.path.join(year_input_dir, filename)
                
                # Assuming the filename format is 'Parcel_TRANSECT_BEARING_YYYYMMDD.jpg'
                base_name = os.path.splitext(filename)[0]
                parts = base_name.split('_')
                if len(parts) == 4:
                    parcel, transect, bearing, date = parts
                    # Format the transect and bearing
                    formatted_transect_bearing = f"{int(transect):02d}_{int(bearing):03d}"
                    # Format the label text
                    label_text = f"{parcel}\n{formatted_transect_bearing}\n{date}"
                    # Format the filename
                    formatted_filename = format_filename(parcel, transect, bearing, date)
                    output_path = os.path.join(year_output_dir, formatted_filename)
                    # Add label to image
                    add_label_to_image(input_path, output_path, label_text)
                    print(f"Labeled: {formatted_filename}")

                    if test:
                        break  # Process only the first image if in test mode

print("Labeling test completed.")
