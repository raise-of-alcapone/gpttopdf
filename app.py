from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import re
import html
import markdown
import pdfkit
from pypdf import PdfWriter, PdfReader
import os
from pathlib import Path

app = Flask(__name__)

# pdfkit-Konfiguration für Windows und Linux/Render.com
def get_pdfkit_config():
    """Konfiguriert pdfkit basierend auf dem Betriebssystem und Umgebung"""
    
    # Render.com / Linux Environment
    if os.name == 'posix':  # Linux/Unix
        # Standard Linux-Pfade prüfen
        possible_linux_paths = [
            '/usr/bin/wkhtmltopdf',
            '/usr/local/bin/wkhtmltopdf',
            '/opt/bin/wkhtmltopdf'
        ]
        
        for path in possible_linux_paths:
            if os.path.exists(path):
                print(f"✅ wkhtmltopdf gefunden: {path}")
                return pdfkit.configuration(wkhtmltopdf=path)
        
        # Fallback: PATH verwenden
        try:
            import subprocess
            result = subprocess.run(['which', 'wkhtmltopdf'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                path = result.stdout.strip()
                print(f"✅ wkhtmltopdf im PATH gefunden: {path}")
                return pdfkit.configuration(wkhtmltopdf=path)
        except:
            pass
    
    # Windows Environment    
    elif os.name == 'nt':  # Windows
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(wkhtmltopdf_path):
            return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    # Default fallback
    print("⚠️ Verwende Standard-pdfkit-Konfiguration")
    return pdfkit.configuration()

def clean_heading_text(text):
    """Entfernt Markdown-Formatierungszeichen aus Überschriften für saubere Bookmarks"""
    if not text:
        return text
    
    # Entferne Markdown-Formatierungen
    cleaned = text
    
    # Fett-Formatierung entfernen: **text** und __text__
    cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
    cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
    
    # Kursiv-Formatierung entfernen: *text* und _text_
    cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
    cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
    
    # Code-Formatierung entfernen: `text`
    cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
    
    # Strikethrough entfernen: ~~text~~
    cleaned = re.sub(r'~~([^~]+)~~', r'\1', cleaned)
    
    # Links entfernen: [text](url) -> text
    cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)
    
    # Bilder entfernen: ![alt](url) -> alt
    cleaned = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', cleaned)
    
    # Blockquote-Zeichen entfernen
    cleaned = re.sub(r'^>\s*', '', cleaned)
    
    # Listen-Zeichen entfernen
    cleaned = re.sub(r'^\s*[-*+]\s+', '', cleaned)
    cleaned = re.sub(r'^\s*\d+\.\s+', '', cleaned)
    
    # HTML-Tags entfernen (falls vorhanden)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    
    # Mehrfache Leerzeichen normalisieren
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Führende und nachfolgende Leerzeichen entfernen
    cleaned = cleaned.strip()
    
    return cleaned

def add_simple_bookmarks(pdf_buffer, document_data):
    """Fügt hierarchische Bookmarks hinzu - einfach und sauber"""
    try:
        # PDF lesen
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        writer = PdfWriter()
        
        # Alle Seiten kopieren
        for page in reader.pages:
            writer.add_page(page)
        
        # Hierarchische Bookmarks
        parent_bookmarks = {}  # level -> bookmark_reference
        
        # Haupttitel als Level 1
        if document_data.get('title'):
            clean_title = document_data['title']
            main_bookmark = writer.add_outline_item(clean_title, 0)
            parent_bookmarks[1] = main_bookmark
        
        # Durch alle Blöcke gehen
        for block in document_data.get('blocks', []):
            # Block-Titel als Level 2
            if block.get('title'):
                title = block['title']
                clean_title = title
                parent = parent_bookmarks.get(1)  # Unter Haupttitel
                block_bookmark = writer.add_outline_item(clean_title, 0, parent=parent)
                parent_bookmarks[2] = block_bookmark
                
                # Alle tieferen Level zurücksetzen
                for level in list(parent_bookmarks.keys()):
                    if level > 2:
                        del parent_bookmarks[level]
            
            # Markdown-Überschriften extrahieren
            if block.get('type') == 'markdown' and block.get('content'):
                content = block['content']
                lines = content.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        # Level bestimmen
                        level = 0
                        for char in line:
                            if char == '#':
                                level += 1
                            else:
                                break
                        
                        # Text extrahieren und bereinigen
                        text = line[level:].strip()
                        if text:
                            clean_text = text.replace('**', '').replace('*', '').replace('`', '')
                            
                            # Level anpassen (# wird zu Level 3, ## zu Level 4, etc.)
                            bookmark_level = level + 2
                            
                            # Parent finden
                            parent = None
                            for parent_level in range(bookmark_level - 1, 0, -1):
                                if parent_level in parent_bookmarks:
                                    parent = parent_bookmarks[parent_level]
                                    break
                            
                            # Bookmark hinzufügen
                            bookmark = writer.add_outline_item(clean_text, 0, parent=parent)
                            parent_bookmarks[bookmark_level] = bookmark
                            
                            # Tiefere Level zurücksetzen
                            for level_key in list(parent_bookmarks.keys()):
                                if level_key > bookmark_level:
                                    del parent_bookmarks[level_key]
        
        # PDF erstellen
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer
        
    except Exception as e:
        # Bei Fehlern Original zurückgeben
        pdf_buffer.seek(0)
        return pdf_buffer

def create_pdf_from_html(document_data):
    """Erstellt ein PDF mit pdfkit/wkhtmltopdf - vollständige Emoji-Unterstützung"""
    try:
        # HTML-Inhalt für Markdown zusammenbauen
        content_html = ""
        
        # Titel hinzufügen
        if document_data.get('title'):
            # Titel direkt verwenden - pdfkit unterstützt Emojis nativ
            title = html.escape(document_data['title'])
            # Eindeutige ID für Bookmark-Navigation
            content_html += f'<h1 id="title-bookmark" style="color: #1e3a8a; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #ddd; padding-bottom: 10px;">{title}</h1>\n'
        
        # Blöcke verarbeiten - für Markdown-Blöcke
        block_counter = 0
        for block in document_data.get('blocks', []):
            block_type = block.get('type', 'markdown')
            block_content = block.get('content', '')
            block_title = block.get('title', '')
            
            if not block_content.strip() and not block_title.strip():
                continue
            
            block_counter += 1
            
            # Block-Titel hinzufügen falls vorhanden
            if block_title.strip():
                # Titel direkt verwenden - pdfkit unterstützt Emojis nativ
                escaped_title = html.escape(block_title)
                # H2 für bessere Gliederung
                content_html += f'<h2 id="block-{block_counter}" style="color: #1e3a8a; margin-top: 25px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 5px;">{escaped_title}</h2>\n'
            
            # Block-Inhalt je nach Typ verarbeiten
            if block_type == 'markdown':
                # Markdown serverseitig zu HTML konvertieren für korrekte Überschriften
                if block_content.strip():
                    # Markdown direkt konvertieren - pdfkit unterstützt Emojis nativ
                    
                    # Markdown zu HTML konvertieren
                    md = markdown.Markdown(extensions=[
                        'tables', 
                        'fenced_code'
                    ])
                    html_content = md.convert(block_content)
                    
                    # Manuell IDs zu Überschriften hinzufügen für Bookmarks
                    import re
                    def add_heading_ids(match):
                        level = len(match.group(1))
                        text = match.group(2)
                        # Einfache ID aus dem Text generieren
                        heading_id = re.sub(r'[^a-zA-Z0-9]', '-', text.lower()).strip('-')
                        return f'<h{level} id="heading-{block_counter}-{heading_id}">{text}</h{level}>'
                    
                    # Regex für <h1>text</h1> bis <h6>text</h6>
                    html_content = re.sub(r'<h([1-6])>([^<]+)</h[1-6]>', add_heading_ids, html_content)
                    
                    content_html += f'{html_content}\n'
            elif block_type == 'code':
                # Code direkt verwenden - pdfkit unterstützt Emojis nativ
                escaped_content = html.escape(block_content)
                content_html += f'<pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; border-radius: 4px; font-family: \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto; margin: 15px 0;"><code>{escaped_content}</code></pre>\n'
        
        # HTML-Template mit optimaler Emoji-Unterstützung erstellen
        full_html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @page {{
                    size: A4;
                    margin: 0.5cm 2cm 2cm 2cm;
                }}
                
                body {{
                    font-family: 'Noto Color Emoji', 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Emoji', 'Segoe UI', Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    background: white;
                }}
                
                /* Überschriften in blau */
                h1, h2, h3, h4, h5, h6 {{
                    color: #1e3a8a !important;
                    margin-top: 1.5rem;
                    margin-bottom: 1rem;
                    font-family: 'Noto Color Emoji', 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Emoji', 'Segoe UI', Arial, sans-serif;
                }}
                
                h1 {{
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 0.5rem;
                }}
                
                h2, h3 {{
                    border-bottom: 1px solid #eee;
                    padding-bottom: 0.3rem;
                }}
                
                /* Blockquotes */
                blockquote {{
                    border-left: 4px solid #007bff;
                    margin: 1rem 0;
                    padding: 0.5rem 1rem;
                    background-color: #f8f9fa;
                    font-style: italic;
                    color: #6c757d;
                }}
                
                /* Tabellen */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                    font-size: 0.9rem;
                }}
                
                table th, table td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                
                table th {{
                    background-color: #f8f9fa;
                    font-weight: bold;
                    color: #495057;
                }}
                
                table tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                /* Code */
                pre {{
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    padding: 1rem;
                    overflow-x: auto;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                }}
                
                code {{
                    background: #f8f9fa;
                    padding: 0.2rem 0.4rem;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    color: #e83e8c;
                }}
                
                pre code {{
                    background: none;
                    padding: 0;
                    color: inherit;
                }}
                
                /* Listen */
                ul, ol {{
                    margin: 1rem 0;
                    padding-left: 2rem;
                }}
                
                li {{
                    margin: 0.5rem 0;
                }}
                
                /* Absätze */
                p {{
                    margin-bottom: 1rem;
                    text-align: justify;
                }}
                
                /* Markdown Content Container */
                .markdown-content {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            {content_html}
        </body>
        </html>
        """
        
        # PDF mit pdfkit/wkhtmltopdf erstellen (vollständige Emoji-Unterstützung)
        try:
            # Konfiguration für das aktuelle System
            config = get_pdfkit_config()
            
            # Optionen für wkhtmltopdf mit verbesserter Emoji-Unterstützung
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'disable-smart-shrinking': None,  # Verhindert Emoji-Skalierung
                'print-media-type': None,         # Bessere CSS-Unterstützung
                'load-error-handling': 'ignore',  # Ignoriert Schrift-Fehler
                'load-media-error-handling': 'ignore'
            }
            
            # PDF generieren mit Konfiguration
            pdf_data = pdfkit.from_string(full_html, False, 
                                        options=options, 
                                        configuration=config)
            pdf_buffer = BytesIO()
            pdf_buffer.write(pdf_data)
            pdf_buffer.seek(0)
            
            print("✅ PDF erfolgreich mit pdfkit erstellt")
            
        except Exception as e:
            print(f"❌ pdfkit Error: {str(e)}")
            print("🔄 Versuche Fallback-Lösung...")
            
            # Fallback: Erstelle ein einfaches HTML-basiertes PDF
            try:
                # Vereinfachte HTML-Version für Fallback
                simple_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>PDF Fallback</title>
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif; 
                            padding: 20px; 
                            line-height: 1.6; 
                        }}
                        h1 {{ color: #1e3a8a; }}
                    </style>
                </head>
                <body>
                    <h1>⚠️ PDF Fallback Mode</h1>
                    <p>Das ursprüngliche PDF konnte nicht erstellt werden.</p>
                    <p>Grund: wkhtmltopdf nicht verfügbar auf diesem System.</p>
                    <hr>
                    {content_html}
                </body>
                </html>
                """
                
                # Minimales PDF erstellen
                pdf_buffer = BytesIO()
                pdf_buffer.write(simple_html.encode('utf-8'))
                pdf_buffer.seek(0)
                print("⚠️ Fallback-HTML erstellt")
                
            except Exception as fallback_error:
                print(f"❌ Auch Fallback fehlgeschlagen: {fallback_error}")
                # Letzter Fallback - minimales PDF
                pdf_buffer = BytesIO()
                pdf_buffer.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
                pdf_buffer.seek(0)
                return pdf_buffer
        
        # Einfache Bookmarks hinzufügen - garantiert funktionierend
        pdf_buffer = add_simple_bookmarks(pdf_buffer, document_data)
        
        return pdf_buffer
        
    except Exception as e:
        # Debug-Output für pdfkit-Fehler
        print(f"PDFKIT ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Einfacher Fallback - leeres PDF
        buffer = BytesIO()
        buffer.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
        buffer.seek(0)
        return buffer

@app.route('/')
def index():
    """Hauptseite der Anwendung"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Favicon Route"""
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    """Moderne PDF-Generierung für Advanced Markdown Editor"""
    try:
        document_data = request.json
        
        pdf_buffer = create_pdf_from_html(document_data)
        
        # Dateiname aus Titel ableiten
        title = document_data.get('title', '').strip()
        if not title:
            title = 'DokumentOhneNamen'
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"{safe_title or 'dokument'}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
