import requests
from bs4 import BeautifulSoup
import os
import zipfile

# Step 1: Fetch the webpage
url = "https://thisischica.com/anime/"  # replace with your actual page
response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Failed to fetch page: {response.status_code}")

html_content = response.text  # <-- define it here

# Step 2: Parse the file links
soup = BeautifulSoup(html_content, "html.parser")
links = []

for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.endswith((".zip", ".rar", ".pdf", ".csv")):  # adjust file types
        links.append(href)

print("Found files:", links)

# Step 3: Download each file
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

for link in links:
    file_url = link if link.startswith("http") else url + "/" + link
    file_name = os.path.join(download_folder, os.path.basename(file_url))

    print(f"Downloading {file_url}...")
    file_response = requests.get(file_url)

    with open(file_name, "wb") as f:
        f.write(file_response.content)

    print(f"Saved to {file_name}")

# Step 4: Extract archives automatically
for file in os.listdir(download_folder):
    if file.endswith(".zip"):
        file_path = os.path.join(download_folder, file)
        extract_folder = os.path.join(download_folder, file.replace(".zip", ""))

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        print(f"Extracted {file} to {extract_folder}")
