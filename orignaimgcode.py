"""Download all images from a web page."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://www.justice.gov/epstein/doj-disclosures/data-set-5-files?page=1"  # replace with your target page
OUTPUT_DIR = Path("downloaded_images 4")


def normalize_url(base_url: str, raw_url: str) -> str | None:
    if not raw_url:
        return None
    if raw_url.startswith("//"):
        raw_url = f"https:{raw_url}"
    return urljoin(base_url, raw_url)


def collect_image_urls(base_url: str, html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    image_urls: set[str] = set()
    for img in soup.find_all("img"):
        for attr in ("src", "data-src", "data-lazy-src", "data-original"):
            candidate = normalize_url(base_url, img.get(attr, ""))
            if candidate:
                image_urls.add(candidate)
        srcset = img.get("srcset", "")
        if srcset:
            for entry in srcset.split(","):
                url_part = entry.strip().split(" ")[0]
                candidate = normalize_url(base_url, url_part)
                if candidate:
                    image_urls.add(candidate)
    return image_urls


def filename_from_url(url: str) -> str:
    name = os.path.basename(url.split("?")[0])
    if name:
        return name
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"image_{digest}.bin"


def download_image(url: str, output_dir: Path) -> Path:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    filename = filename_from_url(url)
    destination = output_dir / filename
    with destination.open("wb") as file_handle:
        file_handle.write(response.content)
    return destination


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    image_urls = collect_image_urls(URL, response.text)
    print(f"Found {len(image_urls)} images.")

    for image_url in sorted(image_urls):
        try:
            saved_path = download_image(image_url, OUTPUT_DIR)
            print(f"Downloaded {image_url} -> {saved_path}")
        except requests.RequestException as exc:
            print(f"Failed to download {image_url}: {exc}")


if __name__ == "__main__":
    main()