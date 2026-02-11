import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# target URL
url = "https://thisischica.com/wallpapers/"

# send HTTP GET
response = requests.get(url)
response.raise_for_status()

# parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# find all <img> tags
img_tags = soup.find_all("img")

image_urls = []

for img in img_tags:
    src = img.get("src")
    if not src:
        continue
    
    # convert relative URL to absolute
    full_url = urljoin(url, src)
    
    # filter by common image extensions
    if any(full_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"]):
        image_urls.append(full_url)

# remove duplicates
image_urls = list(set(image_urls))

# print results
for i, img_url in enumerate(image_urls, 1):
    print(f"{i}. {img_url}")

