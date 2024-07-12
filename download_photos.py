from arcgis.features import FeatureLayer
import os
import requests
from datetime import datetime
import time

# Access the feature layer
feature_layer_url = "https://services.arcgis.com/0jRlQ17Qmni5zEMr/arcgis/rest/services/lpt_points_view/FeatureServer/0"
layer = FeatureLayer(feature_layer_url)

# Query the feature layer to get all features
features = layer.query(where="1=1", out_fields="*").features

# Base directory to save the photos
base_dir = "downloaded_photos"

# Function to format the visit date
def format_visit_date(visit_date):
    # Convert timestamp to datetime object
    date_obj = datetime.fromtimestamp(visit_date / 1000)  # assuming visit_date is in milliseconds
    return date_obj.strftime('%Y%m%d'), date_obj.strftime('%Y')

# Function to download and save attachment
def download_attachment(feature, attachment_id, attachment_name, save_dir):
    attachment_url = f"{feature_layer_url}/{feature.attributes['OBJECTID']}/attachments/{attachment_id}"
    response = requests.get(attachment_url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(save_dir, attachment_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded: {attachment_name}")
    else:
        print(f"Failed to download: {attachment_name}")

# Loop through each feature to download the photo
for feature in features:
    attributes = feature.attributes
    attachment_info = None

    # Retry logic for fetching attachment info
    retries = 3
    for attempt in range(retries):
        try:
            attachment_info = layer.attachments.get_list(feature.attributes['OBJECTID'])
            break
        except Exception as e:
            print(f"Error fetching attachments: {e}")
            if "503" in str(e):
                print("Service unavailable. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                raise
    else:
        print(f"Failed to fetch attachments after {retries} attempts. Skipping feature {feature.attributes['OBJECTID']}.")
        continue

    for attachment in attachment_info:
        attachment_id = attachment['id']
        # Assuming the feature has fields named 'Parcel', 'TRANSECT', 'BEARING', and 'visit_date'
        if 'visit_date' in attributes:
            visit_date = attributes['visit_date']
            formatted_visit_date, year = format_visit_date(visit_date)
            attachment_name = f"{attributes['Parcel']}_{attributes['TRANSECT']}_{attributes['BEARING']}_{formatted_visit_date}.jpg"
            
            # Create year-based directory
            save_dir = os.path.join(base_dir, year)
            os.makedirs(save_dir, exist_ok=True)
            
            # Check if the file already exists
            file_path = os.path.join(save_dir, attachment_name)
            if not os.path.exists(file_path):
                download_attachment(feature, attachment_id, attachment_name, save_dir)
            else:
                print(f"Skipped (already exists): {attachment_name}")
        else:
            print(f"visit_date field is missing in feature {feature.attributes['OBJECTID']}")

print("Download completed.")
