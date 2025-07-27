#!/usr/bin/env python3

"""
Ultimativer Test für farbige Emojis mit allen wkhtmltopdf-Tricks
"""

import pdfkit
import os
import sys

def get_pdfkit_config():
    """Konfiguriert pdfkit basierend auf dem Betriebssystem"""
    if os.name == 'nt':  # Windows
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(wkhtmltopdf_path):
            return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    return pdfkit.configuration()

def test_ultimate_emoji_support():
    """Ultimativer Test mit allen Tricks für Farbemojis"""
    
    # HTML mit mehreren Emoji-Font-Fallbacks
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Ultimate Emoji Test</title>
        <style>
            @font-face {
                font-family: 'EmojiFont';
                src: local('Segoe UI Emoji'), local('Apple Color Emoji'), local('Noto Color Emoji');
            }
            
            body {
                font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'EmojiFont', 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                line-height: 1.8;
                padding: 20px;
                background: white;
                color: #333;
            }
            
            .emoji-test {
                font-size: 28px;
                margin: 15px 0;
                padding: 15px;
                background: linear-gradient(90deg, #f0f8ff, #fff5ee);
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            
            .emoji-inline {
                font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji';
                font-size: 24px;
            }
        </style>
    </head>
    <body>
        <h1 style="color: #1e3a8a;">🌈 Ultimate Emoji Color Test</h1>
        
        <p><strong>Wenn diese Emojis FARBIG sind, funktioniert alles perfekt:</strong></p>
        
        <div class="emoji-test">
            <span class="emoji-inline">🎯</span> Ziel (rot/weiß)
            <span class="emoji-inline">🔥</span> Feuer (gelb/rot)
            <span class="emoji-inline">💡</span> Glühbirne (gelb)
            <span class="emoji-inline">🚀</span> Rakete (weiß/rot)
            <span class="emoji-inline">✅</span> Häkchen (grün)
        </div>
        
        <div class="emoji-test">
            <span class="emoji-inline">❌</span> Kreuz (rot)
            <span class="emoji-inline">⚠️</span> Warnung (gelb)
            <span class="emoji-inline">🌈</span> Regenbogen (bunt)
            <span class="emoji-inline">💪</span> Muskel (hautfarben)
            <span class="emoji-inline">🎉</span> Party (bunt)
        </div>
        
        <h2 style="color: #1e3a8a;">😀 Gesichter (müssen hautfarben sein)</h2>
        <div class="emoji-test">
            😀 😊 😍 🤔 😎 🙄 😅 🤗 🥳 🤩
        </div>
        
        <h2 style="color: #1e3a8a;">🍎 Essen (muss farbig sein)</h2>
        <div class="emoji-test">
            🍎 🍌 🍇 🍓 🥕 🍅 🥑 🍑 🍊 🍋
        </div>
        
        <p style="font-size: 16px; color: #666; margin-top: 30px;">
            <strong>Erwartung:</strong> Alle Emojis sollten ihre natürlichen Farben haben!<br>
            <strong>Problem falls vorhanden:</strong> Emojis sind blau/schwarz/grau statt farbig
        </p>
    </body>
    </html>
    """
    
    try:
        print("🔍 Ultimativer Farbemoji-Test...")
        
        config = get_pdfkit_config()
        
        # Erweiterte Optionen für maximale Kompatibilität
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in', 
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'disable-smart-shrinking': None,
            'print-media-type': None,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore',
            'enable-forms': None,
            'images': None,
            'enable-plugins': None
        }
        
        # PDF erstellen
        pdf_data = pdfkit.from_string(test_html, False, 
                                    options=options, 
                                    configuration=config)
        
        filename = 'ultimate_emoji_test.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_data)
            
        print(f"✅ Ultimate Test PDF erstellt: {filename}")
        print(f"📊 Größe: {len(pdf_data)} bytes")
        print()
        print("🔍 WICHTIGE PRÜFUNG:")
        print("   🎯 Ist das Ziel-Emoji rot/weiß?")
        print("   🔥 Ist das Feuer-Emoji gelb/rot?")
        print("   🌈 Ist der Regenbogen bunt?")
        print("   😀 Sind Gesichter hautfarben?")
        print("   🍎 Sind Früchte natürlich gefärbt?")
        print()
        print("❗ Falls sie immer noch blau/grau sind:")
        print("   → Das ist eine Limitation von wkhtmltopdf")
        print("   → Auf Windows werden oft nur monochrome Emojis unterstützt")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    print("🌈 ULTIMATIVER FARBEMOJI-TEST")
    print("=" * 50)
    test_ultimate_emoji_support()
