"""
pdfkit Configuration für Windows ohne System-Installation
"""

import os
import sys
import pdfkit
from pathlib import Path

def configure_pdfkit_windows():
    """Konfiguriert pdfkit für Windows ohne System-Installation"""
    
    # Mögliche Pfade für wkhtmltopdf.exe
    possible_paths = [
        # Portable Installation im Projekt-Verzeichnis
        Path(__file__).parent / "wkhtmltopdf" / "bin" / "wkhtmltopdf.exe",
        Path(__file__).parent / "bin" / "wkhtmltopdf.exe",
        
        # Standard Windows-Installationspfade
        Path("C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"),
        Path("C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe"),
        
        # Chocolatey Installation
        Path("C:/ProgramData/chocolatey/lib/wkhtmltopdf/tools/wkhtmltopdf.exe"),
        
        # User-Installation
        Path.home() / "AppData" / "Local" / "Programs" / "wkhtmltopdf" / "bin" / "wkhtmltopdf.exe"
    ]
    
    # Suche nach verfügbarer Binary
    for path in possible_paths:
        if path.exists():
            print(f"✅ wkhtmltopdf gefunden: {path}")
            return str(path)
    
    print("❌ wkhtmltopdf nicht gefunden!")
    print("📥 Lade wkhtmltopdf herunter...")
    
    # Download-Link für Windows 64-bit
    download_url = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msi"
    
    print(f"🔗 Download Link: {download_url}")
    print("💡 Führe nach Download folgende Schritte aus:")
    print("   1. Installiere die MSI-Datei")
    print("   2. Oder extrahiere die Binary in den Projektordner")
    
    return None

def get_pdfkit_config():
    """Gibt pdfkit-Konfiguration für Windows zurück"""
    wkhtmltopdf_path = configure_pdfkit_windows()
    
    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        return config
    else:
        return None

def create_pdf_with_config(html_content, output_path=None, options=None):
    """Erstellt PDF mit korrekter Konfiguration"""
    
    config = get_pdfkit_config()
    if not config:
        raise Exception("wkhtmltopdf konnte nicht konfiguriert werden!")
    
    if options is None:
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
    
    if output_path:
        # PDF in Datei speichern
        pdfkit.from_string(html_content, output_path, 
                          options=options, configuration=config)
        return output_path
    else:
        # PDF als Bytes zurückgeben
        pdf_data = pdfkit.from_string(html_content, False, 
                                     options=options, configuration=config)
        return pdf_data

if __name__ == "__main__":
    print("🔧 Konfiguriere pdfkit für Windows...")
    config = get_pdfkit_config()
    
    if config:
        print("✅ pdfkit erfolgreich konfiguriert!")
    else:
        print("❌ pdfkit-Konfiguration fehlgeschlagen")
