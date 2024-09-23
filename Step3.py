import json
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the data from channels.json
with open('channels.json', 'r',encoding='utf-8') as file:
    channels = json.load(file)

# Create a directory to save HTML files if it doesn't exist
output_dir = 'channel_html_sources'
os.makedirs(output_dir, exist_ok=True)

# Function to fetch the HTML source and save it to a file with retry logic
def fetch_and_save_html(channel):
    url, index = channel['url'], channel['index']
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Fetch the page content (HTML source)
            response = requests.get(url, timeout=10)  # Set a timeout for the request
            response.raise_for_status()

            # Save the HTML to a file with a specific name inside the output directory
            html_filename = os.path.join(output_dir, f'channel_{index + 1}.html')
            with open(html_filename, 'w', encoding='utf-8') as html_file:
                html_file.write(f'<!-- Source URL: {url} -->\n')
                html_file.write(response.text)

            return html_filename

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(1)  # Wait a bit before retrying

    return None

# Prepare channels with index for easier reference
channels_with_index = [{'url': channel['url'], 'index': i} for i, channel in enumerate(channels)]

# Use ThreadPoolExecutor for batch processing
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_and_save_html, channel): channel for channel in channels_with_index}

    for future in as_completed(futures):
        html_file = future.result()
        if html_file:
            print(f"Saved HTML source to {html_file}")

print("Finished processing all channels.")
