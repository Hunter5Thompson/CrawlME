import os
import requests

# Pfad zur Datei mit den Download-Links
input_file = "firecrawl_download_links.txt"
# Verzeichnis, in dem die Dateien gespeichert werden sollen
output_dir = "downloaded_files"

# Sicherstellen, dass das Ausgabe-Verzeichnis existiert
os.makedirs(output_dir, exist_ok=True)

def download_file(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Fehlerprüfung
        filename = url.split("/")[-1].split("?")[0]  # Nur der Dateiname
        output_path = os.path.join(output_dir, filename)
        
        # Datei schreiben
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Erfolgreich heruntergeladen: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen von {url}: {e}")

# Dateien aus der Liste herunterladen
with open(input_file, "r") as file:
    for line in file:
        url = line.strip()
        if url.endswith(".xlsx"):  # Nur .xlsx-Dateien
            download_file(url, output_dir)
