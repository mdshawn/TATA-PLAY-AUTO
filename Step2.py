from bs4 import BeautifulSoup
import json

# Read the content of the website_source_code.txt file
with open('website_source_code.txt', 'r', encoding='utf-8') as file:
    source_code = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(source_code, 'html.parser')

# Initialize an empty list to store the extracted data
channels = []

# Find all the div elements with the class 'box1'
for box in soup.find_all('div', class_='box1'):
    # Extract the URL
    a_tag = box.find('a')
    channel_url = a_tag['href']
    
    # Extract the image source
    img_tag = box.find('img')
    logo_url = img_tag['src']
    
    # Extract the channel name
    h2_tag = box.find('h2')
    channel_name = h2_tag.text.strip()
    
    # Extract the category
    p_tag = box.find('p')
    category_name = p_tag.text.strip()
    
    # Append to the list as a dictionary
    channels.append({
        'url': 'https://tgaadi-web.tech/Tata-Play/'+channel_url,
        'logo': logo_url,
        'name': channel_name,
        'category': category_name
    })

# Check if any channels were found
if not channels:
    print("No channels found. Check the HTML structure.")
else:
    print(f"Found {len(channels)} channels.")

# Save the extracted data to a JSON file
with open('channels.json', 'w', encoding='utf-8') as json_file:
    json.dump(channels, json_file, ensure_ascii=False, indent=4)

print("Data saved to 'channels.json'.")