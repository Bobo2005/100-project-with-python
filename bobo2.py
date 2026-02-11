import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Base URL
base_url = "https://thisischica.com/#image-03dc018dfbb53ced778d9827f2340e6a"

# Create a folder to save images
os.makedirs("downloaded_images", exist_ok=True)

def get_images_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    img_urls = []
    for img in soup.find_all("img"):
        img_url = img.get("src")
        if img_url:
            img_urls.append(urljoin(url, img_url))
    return img_urls

def download_image(url, folder="downloaded_images"):
    filename = os.path.join(folder, os.path.basename(url))
    try:
        img_data = requests.get(url).content
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Step 1: Get images from the main page
images = get_images_from_page(base_url)

# Step 2: Also crawl links on the page for more images
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")
links = [urljoin(base_url, a.get("href")) for a in soup.find_all("a", href=True)]

for link in links:
    images.extend(get_images_from_page(link))

# Step 3: Download all found images
for img_url in set(images):  # remove duplicates
    download_image(img_url)
