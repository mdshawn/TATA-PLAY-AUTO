import requests

# URL of the website
url = 'https://tgaadi-web.tech/Tata-Play/'

# Fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the source code as text
    source_code = response.text
    
    # Save the source code to a .txt file
    with open('website_source_code.txt', 'w', encoding='utf-8') as file:
        file.write(source_code)
    
    print("Website source code saved to 'website_source_code.txt'.")
else:
    print(f"Failed to fetch the website. Status code: {response.status_code}")
