#!/usr/bin/env python3

"""
Test Script für pdfkit mit Emoji-Unterstützung
"""

import pdfkit
import os
import sys

# pdfkit-Konfiguration für Windows
def get_pdfkit_config():
    """Konfiguriert pdfkit basierend auf dem Betriebssystem"""
    if os.name == 'nt':  # Windows
        # Standard Windows-Installationspfad
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(wkhtmltopdf_path):
            return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    # Linux/macOS - Standard-PATH verwenden
    return pdfkit.configuration()

def test_pdfkit_emojis():
    """Testet pdfkit mit verschiedenen Emojis"""
    
    # Teste HTML mit Emojis
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Emoji Test</title>
        <style>
            body {
                font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.6;
                padding: 20px;
            }
            h1 {
                color: #1e3a8a;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>🎯 Emoji Test mit pdfkit</h1>
        <p>Verschiedene Emojis:</p>
        <ul>
            <li>🎯 Ziel</li>
            <li>✅ Häkchen</li>
            <li>❌ Kreuz</li>
            <li>🚀 Rakete</li>
            <li>💡 Glühbirne</li>
            <li>⚡ Blitz</li>
            <li>🔥 Feuer</li>
            <li>👍 Daumen hoch</li>
            <li>🎉 Party</li>
            <li>📝 Notiz</li>
        </ul>
        <h2>🧪 Komplexere Tests</h2>
        <p>Emoji in verschiedenen Kontexten: 🎯 Das ist ein <strong>fetter Text mit 💪 Emoji</strong>!</p>
        <blockquote>
            ⚠️ Dies ist ein wichtiger Hinweis mit Emojis! 🔔
        </blockquote>
    </body>
    </html>
    """
    
    # Versuche pdfkit zu verwenden
    try:
        print("🔍 Teste pdfkit...")
        
        # Konfiguration für das aktuelle System
        config = get_pdfkit_config()
        
        # Optionen für beste Emoji-Darstellung
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
        
        # Versuche PDF zu erstellen mit Konfiguration
        pdf_data = pdfkit.from_string(test_html, False, 
                                    options=options, 
                                    configuration=config)
        
        # Speichere als Datei zum Testen
        with open('emoji_test.pdf', 'wb') as f:
            f.write(pdf_data)
            
        print("✅ PDF erfolgreich erstellt: emoji_test.pdf")
        print(f"📊 PDF Größe: {len(pdf_data)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim PDF-Test: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        
        # Spezifische Behandlung für häufige Probleme
        if "wkhtmltopdf" in str(e).lower():
            print("🚨 wkhtmltopdf binary nicht gefunden!")
            print("💡 Lösungen:")
            print("   1. wkhtmltopdf aus: https://wkhtmltopdf.org/downloads.html")
            print("   2. Oder über Chocolatey: choco install wkhtmltopdf")
            print("   3. Pfad in pdfkit konfigurieren")
        
        return False

def check_wkhtmltopdf():
    """Prüft ob wkhtmltopdf verfügbar ist"""
    try:
        # Windows-Pfad prüfen
        if os.name == 'nt':
            wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            if os.path.exists(wkhtmltopdf_path):
                print(f"✅ wkhtmltopdf gefunden: {wkhtmltopdf_path}")
                return True
        
        # PATH prüfen
        import subprocess
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print(f"✅ wkhtmltopdf gefunden: {result.stdout.strip()}")
        return True
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        print("❌ wkhtmltopdf nicht im PATH gefunden")
        return False

if __name__ == "__main__":
    print("🧪 pdfkit Emoji-Test startet...")
    print("=" * 50)
    
    # Prüfe wkhtmltopdf
    if not check_wkhtmltopdf():
        print("\n🔧 Versuche trotzdem pdfkit Test...")
    
    # Teste pdfkit
    success = test_pdfkit_emojis()
    
    print("=" * 50)
    if success:
        print("🎉 Test erfolgreich! Emojis sollten im PDF sichtbar sein.")
    else:
        print("❌ Test fehlgeschlagen. Siehe Fehlerdetails oben.")
