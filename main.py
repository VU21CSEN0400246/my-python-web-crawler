import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = ['https://example.com']


def vizitate(site):
    try:
        response = requests.get(site, timeout=10)
        response.raise_for_status()

        with open("visited.txt", "w", encoding="utf-8") as file:
            file.write(site)

        parsed1 = BeautifulSoup(response.text, "html.parser")
        print(response.headers)

        for link in parsed1.find_all('a', href=True):
            full_url = urljoin(site, link['href'])

            if full_url.startswith(('http://', 'https://')) and not full_url.lower().endswith('.pdf'):
                if full_url not in url:
                    url.append(full_url)

    except requests.RequestException as error:
        print("Error visiting website:", error)


vizitate(url[0])
print(url)
