import requests
import json
from urllib.parse import urljoin

# Firecrawl API-Konfiguration
API_URL = "http://localhost:3002/v1/scrape"  # Endpoint für Firecrawl
API_KEY = "fc-YOUR_API_KEY"  # Deinen API-Key hier einfügen
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

BASE_URL = "https://www.statistik-berlin-brandenburg.de/"
visited_urls = set()
download_links = []

def crawl_with_firecrawl(url, max_depth=2, depth=0):
    """
    Rekursives Crawling einer Website mit Firecrawl bis zu einer bestimmten Tiefe.
    """
    if url in visited_urls or depth > max_depth:
        return

    print(f"Crawling: {url}")
    payload = {
        "url": url,
        "formats": ["html"]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Crawling von {url}: {e}")
        return

    visited_urls.add(url)

    # HTML-Inhalt auslesen
    html_content = data.get("data", {}).get("html", "")
    if not html_content:
        return

    # Suche nach Download-Links
    download_links.extend(find_download_links(html_content, url))

    # Suche nach weiteren Links auf der Seite
    links = find_links(html_content, url)
    for link in links:
        crawl_with_firecrawl(link, max_depth, depth + 1)

def find_links(html, base_url):
    """
    Extrahiert alle Links aus dem HTML.
    """
    from selectolax.parser import HTMLParser
    tree = HTMLParser(html)
    links = []
    for node in tree.css("a"):
        href = node.attributes.get("href")
        if href:
            links.append(urljoin(base_url, href))
    return links

def find_download_links(html, base_url):
    """
    Sucht nach Links mit Download-Möglichkeiten.
    """
    from selectolax.parser import HTMLParser
    tree = HTMLParser(html)
    downloads = []
    for node in tree.css("a"):
        href = node.attributes.get("href")
        if href and node.text() and "download" in node.text().lower():
            downloads.append(urljoin(base_url, href))
    return downloads

# Crawl starten
crawl_with_firecrawl(BASE_URL)

# Ergebnisse speichern
with open("firecrawl_download_links.txt", "w", encoding="utf-8") as file:
    for link in download_links:
        file.write(link + "\n")

print("Crawling abgeschlossen. Gefundene Download-Links wurden gespeichert.")
print(f"Besuchte Seiten: {len(visited_urls)}")
