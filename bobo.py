import requests

url = "https://www.justice.gov/epstein/doj-disclosures/data-set-5-files?page=1"  # replace with your target page
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    print("Page downloaded successfully!")
else:
    print("Failed to fetch page:", response.status_code)


from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")
links = []

for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.endswith((".zip", ".rar", ".pdf", ".csv")):  # adjust file types
        links.append(href)

print("Found files:", links)

import os

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

import zipfile

for file in os.listdir(download_folder):
    if file.endswith(".zip"):
        file_path = os.path.join(download_folder, file)
        extract_folder = os.path.join(download_folder, file.replace(".zip", ""))

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        print(f"Extracted {file} to {extract_folder}")
