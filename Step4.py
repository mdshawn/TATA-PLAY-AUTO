import json
import re
import os

# Step 1: Read all HTML files in the channel_html_sources directory
directory = 'channel_html_sources'
channels_data = []

# Load the existing channels.json data
with open('channels.json', 'r', encoding='utf-8') as file:
    channels_data = json.load(file)

# Process each HTML file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract the file URL using regex
        file_match = re.search(r'file:\s*"(.*?)"', html_content)
        if file_match:
            file_url = file_match.group(1)
        else:
            print(f"File URL not found in {filename}")
            continue  # Skip to the next file

        # Extract the drm object using regex
        drm_match = re.search(r'drm:\s*({.*?clearkey:.*?{.*?key:.*?\'(.*?)\'.*?keyId:.*?\'(.*?)\'.*?}.*?})', html_content, re.DOTALL)
        if drm_match:
            drm_object = drm_match.group(1)
            # Ensure the JSON string is properly formatted
            drm_object = re.sub(r"(\w+):", r'"\1":', drm_object)  # Add double quotes around property names
            drm_object = drm_object.replace("'", '"')  # Replace single quotes with double quotes for JSON compatibility
            drm_data = json.loads(drm_object)  # Parse the string as a JSON object
        else:
            print(f"DRM object not found in {filename}")
            continue  # Skip to the next file

        # Extract the URL from the comment
        url_match = re.search(r'<!--\s*Source URL:\s*(http[s]?://[^\s]+)\s*-->', html_content)
        if url_match:
            url = url_match.group(1)
        else:
            print(f"URL not found in {filename}")
            continue  # Skip to the next file

        # Step 2: Find the entry with the matching URL and add the file and drm object
        for channel in channels_data:
            if channel.get('url') == url:
                channel['file'] = file_url
                channel['drm'] = drm_data
                break
        else:
            print(f"Matching URL not found in channels.json for {filename}")
            continue  # Skip to the next file

# Step 3: Save the updated channels.json file
with open('channels.json', 'w', encoding='utf-8') as file:
    json.dump(channels_data, file, indent=4)

print("channels.json has been updated successfully.")
