#!/usr/bin/env python3

"""
Test Script für pdfkit mit farbigen Emojis
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

def test_color_emojis():
    """Testet pdfkit mit farbigen Emojis"""
    
    # HTML mit verschiedenen Emoji-Tests
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Farbige Emoji Test</title>
        <style>
            body {
                font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.8;
                padding: 20px;
                background: white;
            }
            h1 {
                color: #1e3a8a;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }
            .emoji-test {
                font-size: 24px;
                margin: 10px 0;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 8px;
            }
            .emoji-large {
                font-size: 32px;
            }
        </style>
    </head>
    <body>
        <h1>🎯 Farbige Emoji-Tests mit wkhtmltopdf</h1>
        
        <h2>🌈 Basis-Test</h2>
        <div class="emoji-test">
            Normal: 🎯 ✅ ❌ 🔥 💡 🚀 ⭐ 💪 🎉
        </div>
        
        <h2>😀 Gesichter (sollten farbig sein)</h2>
        <div class="emoji-test">
            😀 😊 😍 🤔 😎 🙄 😅 🤗 🥳 🤩
        </div>
        
        <h2>🌿 Natur (sollten farbig sein)</h2>
        <div class="emoji-test">
            🌱 🌳 🌊 ⚡ 🌈 ☀️ 🌙 🔥 ❄️ 🌟
        </div>
        
        <h2>🚗 Transport (sollten farbig sein)</h2>
        <div class="emoji-test">
            🚗 ✈️ 🚢 🚂 🛸 🚁 🚲 🛵 🏃 🚀
        </div>
        
        <h2>📱 Objekte (sollten farbig sein)</h2>
        <div class="emoji-test">
            📝 📊 📈 💻 🔧 ⚙️ 🛠️ 📦 🎁 💼
        </div>
        
        <h2>🔵 Große Emojis</h2>
        <div class="emoji-test emoji-large">
            🎯 🚀 💡 🔥 ✅ ❌ 🌈 😀 💪
        </div>
        
        <h2>📋 Test-Checklist</h2>
        <ul>
            <li>✅ Emojis werden angezeigt (nicht als Kästchen)</li>
            <li>🎨 Emojis haben Farben (nicht nur blau/schwarz)</li>
            <li>📏 Verschiedene Größen funktionieren</li>
            <li>🔤 Text und Emojis zusammen: Das ist ein 🎯 Test mit 💡 Ideen!</li>
        </ul>
        
        <h2>🧪 Kritischer Test</h2>
        <p style="font-size: 20px;">
            Wenn diese Emojis <strong>farbig</strong> sind, funktioniert alles: 
            🎯🚀💡🔥✅❌🌈😀💪🎉
        </p>
        
        <p style="font-size: 14px; color: #666; margin-top: 30px;">
            Generated with wkhtmltopdf - Expected: Full color emoji support
        </p>
    </body>
    </html>
    """
    
    try:
        print("🔍 Teste farbige Emojis mit wkhtmltopdf...")
        
        # Konfiguration
        config = get_pdfkit_config()
        
        # Optionen für beste Darstellung
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'disable-smart-shrinking': None,  # Verhindert Skalierung
            'print-media-type': None,         # Für bessere CSS-Unterstützung
        }
        
        # PDF erstellen
        pdf_data = pdfkit.from_string(test_html, False, 
                                    options=options, 
                                    configuration=config)
        
        # Datei speichern
        filename = 'color_emoji_test.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_data)
            
        print(f"✅ PDF erstellt: {filename}")
        print(f"📊 Größe: {len(pdf_data)} bytes")
        print()
        print("🔍 PRÜFE DAS PDF:")
        print("   ✅ Sind die Emojis farbig (nicht blau/schwarz)?")
        print("   ✅ Werden alle Emojis korrekt angezeigt?")
        print("   ✅ Keine blauen Kästchen oder Platzhalter?")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    print("🌈 Farbiger Emoji-Test mit wkhtmltopdf")
    print("=" * 50)
    
    success = test_color_emojis()
    
    print("=" * 50)
    if success:
        print("🎉 Test abgeschlossen! Prüfe die PDF-Datei.")
    else:
        print("❌ Test fehlgeschlagen.")
