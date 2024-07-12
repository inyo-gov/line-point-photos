import os
from PIL import Image, ImageDraw, ImageFont

# Directories
base_input_dir = "downloaded_photos"
base_output_dir = "labeled_photos"
os.makedirs(base_output_dir, exist_ok=True)

# Font settings for the labels and values
font_path = "arial.ttf"  # Update with the path to your desired font file
font_size = 40  # Uniform font size for labels and values
font = ImageFont.truetype(font_path, font_size)

# Test mode variable
test = False  # Set to False to process all images

def draw_text_with_border(draw, position, text, font, border_color, text_color):
    x, y = position
    # Draw border
    draw.text((x-1, y-1), text, font=font, fill=border_color)
    draw.text((x+1, y-1), text, font=font, fill=border_color)
    draw.text((x-1, y+1), text, font=font, fill=border_color)
    draw.text((x+1, y+1), text, font=font, fill=border_color)
    draw.text((x-1, y), text, font=font, fill=border_color)
    draw.text((x+1, y), text, font=font, fill=border_color)
    draw.text((x, y-1), text, font=font, fill=border_color)
    draw.text((x, y+1), text, font=font, fill=border_color)
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)

def add_label_to_image(input_path, output_path, labels, values):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    x, y = 20, 20  # Position for the label text with larger margin

    max_label_width = max(draw.textsize(label, font=font)[0] for label in labels)
    max_value_width = max(draw.textsize(value, font=font)[0] for value in values)
    max_width = max(max_label_width, max_value_width)

    # Draw labels and values with the same font and aligned
    for label, value in zip(labels, values):
        label_position = (x, y)
        value_position = (x + max_width + 10, y)
        draw_text_with_border(draw, label_position, label, font, "black", "white")
        draw_text_with_border(draw, value_position, value, font, "white", "black")
        y += font_size + 10  # Move position for the next line
    
    image.save(output_path)

# Process images in the input directory
for year_dir in os.listdir(base_input_dir):
    year_input_dir = os.path.join(base_input_dir, year_dir)
    if os.path.isdir(year_input_dir):
        year_output_dir = os.path.join(base_output_dir, year_dir)
        os.makedirs(year_output_dir, exist_ok=True)
        
        for filename in os.listdir(year_input_dir):
            if filename.endswith(".jpg"):
                input_path = os.path.join(year_input_dir, filename)
                output_path = os.path.join(year_output_dir, filename)

                # Assuming the filename format is 'Parcel_TRANSECT_BEARING_YYYYMMDD.jpg'
                base_name = os.path.splitext(filename)[0]
                parts = base_name.split('_')
                if len(parts) == 4:
                    parcel, transect, bearing, visit_date = parts
                    labels = ["Parcel:", "TRANSECT:", "BEARING:", "Visit Date:"]
                    values = [parcel, transect, bearing, visit_date]
                    add_label_to_image(input_path, output_path, labels, values)
                    print(f"Labeled: {filename}")

                    if test:
                        break  # Process only the first image if in test mode

print("Labeling test completed.")
