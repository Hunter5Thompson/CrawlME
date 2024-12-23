import re

# Datei mit Crawling-Output einlesen
with open("curl.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Liste, um gültige Links zu speichern
valid_links = []

# Muster für erfolgreiche Crawling-Links
link_pattern = re.compile(r"Crawling:\s+(https?://\S+)")
error_pattern = re.compile(r"Fehler beim Crawling von .*?:\s+(400|500)")

# Iteriere über die Zeilen und prüfe auf fehlerfreie Links
for i, line in enumerate(lines):
    if "Crawling:" in line:
        match = link_pattern.search(line)
        if match:
            url = match.group(1)
            # Prüfe auf nachfolgende Fehlermeldung
            if i + 1 < len(lines) and error_pattern.search(lines[i + 1]):
                continue  # Überspringe Links mit Fehlern
            valid_links.append(url)

# Speichere die gültigen Links in einer neuen Datei
with open("valid_links.txt", "w", encoding="utf-8") as output_file:
    for link in valid_links:
        output_file.write(link + "\n")

print(f"{len(valid_links)} gültige Links wurden extrahiert und in 'valid_links.txt' gespeichert.")
