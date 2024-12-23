import requests
import json

# Firecrawl API-Einstellungen
API_URL = "http://localhost:3002/v1/scrape"  # Lokale URL des Firecrawl-Dienstes
API_KEY = "fc-YOUR_API_KEY"  # Deinen API-Key einfügen

# Die URL, die gecrawlt werden soll
payload = {
    "url": "https://www.statistik-berlin-brandenburg.de/",
    "formats": ["markdown", "html"]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Anfrage an die API senden
response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code == 200:
    # Antwort parsen
    data = response.json()
    
    # Extrahiere Markdown und Metadaten
    markdown_content = data.get("data", {}).get("markdown", "Keine Markdown-Daten gefunden.")
    metadata = data.get("data", {}).get("metadata", {})
    
    # Formatierte Ausgabe
    print("### Titel:")
    print(metadata.get("title", "Kein Titel gefunden."))
    
    print("\n### Beschreibung:")
    print(metadata.get("description", "Keine Beschreibung gefunden."))
    
    print("\n### Inhalt:")
    print(markdown_content)
    
    # Optional: Speichere Markdown in einer Datei
    with open("output.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)
    print("Markdown-Inhalt wurde in 'output.md' gespeichert.")
    
    # Optional: Speichere HTML in einer Datei
    html_content = data.get("data", {}).get("html", "Keine HTML-Daten gefunden.")
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML-Inhalt wurde in 'output.html' gespeichert.")
else:
    print(f"Fehler: {response.status_code} - {response.text}")
