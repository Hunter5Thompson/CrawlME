import requests
import os
from markdownify import markdownify as md
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup


# Firecrawl API-Einstellungen
API_URL = "http://localhost:3002/v1/scrape"  # Lokale URL des Firecrawl-Dienstes
API_KEY = "fc-YOUR_API_KEY"  # Deinen API-Key einfügen

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def sanitize_filename(filename):
    """Ersetzt ungültige Zeichen in Dateinamen durch Unterstriche."""
    return "".join(c if c.isalnum() or c in ('-', '_') else "_" for c in filename)

def scrape_page(url):
    """Scrape eine Seite mit Firecrawl und gibt den HTML-Inhalt zurück."""
    payload = {"url": url, "formats": ["html"]}
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("data", {}).get("html", "")
    else:
        print(f"Fehler beim Scrapen von {url}: {response.status_code}")
        return ""

def extract_links(html, base_url):
    """Extrahiert alle internen Links aus einer HTML-Seite."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/"):
            links.add(base_url.rstrip("/") + href)
        elif base_url in href:
            links.add(href)
    return links

def convert_to_markdown(html, output_dir, page_name):
    """Konvertiert HTML in Markdown und speichert es als Datei."""
    markdown_content = md(html)
    os.makedirs(output_dir, exist_ok=True)
    sanitized_name = sanitize_filename(page_name)
    file_path = os.path.join(output_dir, f"{sanitized_name}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Markdown gespeichert: {file_path}")

def crawl_and_convert(base_url, output_dir):
    """Crawlt die gesamte Seite und konvertiert Unterseiten in Markdown."""
    visited = set()
    to_visit = {base_url}
    
    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        print(f"Scraping: {url}")
        html_content = scrape_page(url)
        if not html_content:
            continue
        
        # Bereinige URL für Dateinamen
        parsed_url = urlparse(url)
        page_name = parsed_url.path.strip("/").replace("/", "_")
        if not page_name:
            page_name = "index"
        query_part = quote(parsed_url.query) if parsed_url.query else ""
        if query_part:
            page_name += f"_{query_part}"

        # Speichere als Markdown
        convert_to_markdown(html_content, output_dir, page_name)
        
        # Finde weitere Links
        new_links = extract_links(html_content, base_url)
        to_visit.update(new_links - visited)
        visited.add(url)
    
    print("Crawling abgeschlossen.")

# Hauptprogramm
if __name__ == "__main__":
    BASE_URL = "https://www.statistik-berlin-brandenburg.de"  # Start-URL
    OUTPUT_DIR = "output_markdown"  # Ordner für Markdown-Dateien
    
    crawl_and_convert(BASE_URL, OUTPUT_DIR)
