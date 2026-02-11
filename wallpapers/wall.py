import requests
from bs4 import BeautifulSoup
import os

# Base URL of the site
base_url = "https://thisischica.com/anime/"  # replace with the actual domain
start_page = base_url + "/anime"   # starting page that lists subpages

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

# Create a folder to save images
download_folder = "wallpapers"
os.makedirs(download_folder, exist_ok=True)

# Step 1: Get all subpage links
resp = requests.get(start_page, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

subpages = []
for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.startswith("/anime/"):  # only anime subpages
        subpages.append(base_url + href)

print(f"Found {len(subpages)} subpages.")

# Step 2: Visit each subpage and collect image links
for page_url in subpages:
    print(f"Visiting {page_url}...")
    resp = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    for img_tag in soup.find_all("img", src=True):
        img_url = img_tag["src"]

        # Make sure it's a full URL
        if not img_url.startswith("http"):
            img_url = base_url + img_url

        # Only download jpg/png
        if img_url.endswith((".jpg", ".jpeg", ".png")):
            file_name = os.path.join(download_folder, os.path.basename(img_url))

            print(f"Downloading {img_url}...")
            img_resp = requests.get(img_url, headers=headers)

            with open(file_name, "wb") as f:
                f.write(img_resp.content)

print("✅ All wallpapers downloaded!")
