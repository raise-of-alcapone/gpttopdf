from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import re
import html
import markdown
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
# from playwright.sync_api import sync_playwright  # Temporarily disabled for deployment

app = Flask(__name__)

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
            main_bookmark = writer.add_outline_item(document_data['title'], 0)
            parent_bookmarks[1] = main_bookmark
        
        # Durch alle Blöcke gehen
        for block in document_data.get('blocks', []):
            # Block-Titel als Level 2
            if block.get('title'):
                title = block['title']
                parent = parent_bookmarks.get(1)  # Unter Haupttitel
                block_bookmark = writer.add_outline_item(title, 0, parent=parent)
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
    """Erstellt ein PDF direkt aus HTML/CSS - für Advanced Markdown Editor"""
    try:
        # HTML-Inhalt für Markdown zusammenbauen
        content_html = ""
        
        # Titel hinzufügen
        if document_data.get('title'):
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
                escaped_title = html.escape(block_title)
                # H2 für bessere Gliederung - echtes HTML-Tag für Playwright
                content_html += f'<h2 id="block-{block_counter}" style="color: #1e3a8a; margin-top: 25px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 5px;">{escaped_title}</h2>\n'
            
            # Block-Inhalt je nach Typ verarbeiten
            if block_type == 'markdown':
                # Markdown serverseitig zu HTML konvertieren für korrekte Überschriften
                if block_content.strip():
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
                escaped_content = html.escape(block_content)
                content_html += f'<pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; border-radius: 4px; font-family: \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto; margin: 15px 0;"><code>{escaped_content}</code></pre>\n'
        
        # HTML-Template erstellen (für Markdown mit marked.js)
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
                    font-family: 'Segoe UI', Arial, sans-serif;
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
        
        # PDF mit Playwright erstellen (wie ein echter Browser)
        # Temporarily disabled for deployment - using simple fallback
        # with sync_playwright() as p:
        #     browser = p.chromium.launch(headless=True)
        #     page = browser.new_page()
        #     
        #     # HTML laden
        #     page.set_content(full_html)
        #     
        #     # Warten bis alle Fonts geladen sind
        #     page.wait_for_load_state('networkidle')
        #     
        #     # PDF generieren mit hoher Qualität und Gliederungspunkten
        #     pdf_buffer = BytesIO()
        #     pdf_bytes = page.pdf(
        #         format='A4',
        #         margin={
        #             'top': '0.5cm',
        #             'right': '2cm', 
        #             'bottom': '2cm',
        #             'left': '2cm'
        #         },
        #         print_background=True,
        #         prefer_css_page_size=True,
        #         outline=False,  # Deaktiviert, verwende manuelle Bookmarks
        #         display_header_footer=False
        #     )
        #     pdf_buffer.write(pdf_bytes)
        #     pdf_buffer.seek(0)
        #     
        #     browser.close()
        
        # Simple fallback PDF generation (temporary)
        pdf_buffer = BytesIO()
        # Create minimal PDF with content
        
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4
        
        # Add title if available
        if document_data.get('title'):
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, document_data['title'])
        
        # Add simple content note
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, "PDF generation temporarily simplified for deployment.")
        c.drawString(50, height - 120, "Advanced PDF features will be restored after successful deployment.")
        
        c.save()
        pdf_buffer.seek(0)
        
        # Einfache Bookmarks hinzufügen - garantiert funktionierend
        pdf_buffer = add_simple_bookmarks(pdf_buffer, document_data)
        
        return pdf_buffer
        
    except Exception as e:
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
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
