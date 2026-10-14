import csv
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

START_URL = "https://example.com"
OUTPUT_FILE = "results.csv"
TIMEOUT = 10


def crawl_page(url):
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "SimplePythonCrawler/1.0"}
        )
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Could not access {url}: {error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    page_title = soup.title.get_text(strip=True) if soup.title else "No title"

    links = []

    for tag in soup.find_all("a", href=True):
        link = urljoin(url, tag["href"])
        parsed_link = urlparse(link)

        # Keep only HTTP and HTTPS links.
        if parsed_link.scheme in ("http", "https"):
            links.append(link)

    # Remove duplicate links while preserving their order.
    links = list(dict.fromkeys(links))

    return [(url, page_title, link) for link in links]


def main():
    results = crawl_page(START_URL)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["page_url", "page_title", "extracted_link"])
        writer.writerows(results)

    print(f"Finished! Found {len(results)} links.")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
