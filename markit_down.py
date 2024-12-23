import os
from datetime import datetime
from markitdown import MarkItDown

def convert_excel_to_markdown(excel_path):
    # MarkItDown Instanz erstellen
    md = MarkItDown()
    
    # Excel konvertieren
    result = md.convert(excel_path)
    
    # Zeitstempel für den Dateinamen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Zielverzeichnis ist das gleiche wie die Excel-Datei
    excel_dir = os.path.dirname(excel_path)
    excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    
    # Markdown-Datei erstellen
    md_filename = f"{excel_name}_{timestamp}.md"
    md_path = os.path.join(excel_dir, md_filename)
    
    # Markdown-Header erstellen
    header = f"""# Excel-zu-Markdown Konvertierung

- **Ursprungsdatei**: {excel_path}
- **Konvertiert am**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
    
    # Inhalt in Markdown-Datei speichern
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(header + result.text_content)
    
    return md_path

def main():
    try:
        excel_path = input("Bitte geben Sie den Pfad zur Excel-Datei ein: ")
        if not os.path.exists(excel_path):
            print("Fehler: Die angegebene Datei existiert nicht.")
            return
            
        md_file = convert_excel_to_markdown(excel_path)
        print(f"\nKonvertierung erfolgreich!")
        print(f"Markdown-Datei wurde gespeichert unter: {md_file}")
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")

if __name__ == "__main__":
    main()
