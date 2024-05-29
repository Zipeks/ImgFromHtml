import os
import requests
from bs4 import BeautifulSoup
import re

anime = 'onepiece.txt' 


# Function to extract image URLs from the HTML text
def extract_image_urls(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags]
    return img_urls

# Function to download images given their URLs
def download_images(img_urls, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, img_url in enumerate(img_urls):
        response = requests.get(img_url, verify=False)
        if response.status_code == 200:
            with open(os.path.join(output_folder, f"{filePrefix}_{chapter}_{i+1}.jpg"), 'wb') as img_file:
                img_file.write(response.content)
                print(f"Downloaded {filePrefix}_{chapter}_{i+1}.jpg")
        else:
            print(f"Failed to download {img_url}")

# Read the HTML text from the file
file_path = 'ToExtractUrl.txt'  # Replace 'your_input_file.txt' with the path to your input file
with open(file_path, 'r', encoding="utf8") as file:
    html_text = re.sub(r'<noscript>.*?</noscript>', '', file.read())

# Extract image URLs
image_urls = extract_image_urls(html_text)

# Download images to a folder
with open(anime, 'r') as f:
    output_folder = f.readline().rstrip() # Replace 'downloaded_images' with your desired output folder name
    filePrefix = f.readline().rstrip()
    chapter = f.readline().rstrip()

download_images(image_urls, output_folder)

lines = []

with open(anime, 'r') as f:
        lines = f.readlines()[:-1]
        lines.append(f"{int(chapter) + 1}")
with open(anime, 'w') as f:
        f.writelines(lines)
