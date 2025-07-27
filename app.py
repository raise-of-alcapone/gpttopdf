from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import re
import html
import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
from datetime import datetime
import os

app = Flask(__name__)

def clean_heading_text(text):
    """Remove Markdown formatting from headings for clean bookmarks"""
    if not text:
        return text
    
    cleaned = text
    
    # Remove bold formatting: **text** and __text__
    cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
    cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
    
    # Remove italic formatting: *text* and _text_
    cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
    cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
    
    # Remove code formatting: `text`
    cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
    
    # Remove strikethrough: ~~text~~
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
    """Add hierarchical bookmarks to PDF - simple and reliable"""
    try:
        # Read PDF
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Hierarchical bookmarks
        parent_bookmarks = {}  # level -> bookmark_reference
        
        # Main title as Level 1
        if document_data.get('title'):
            main_bookmark = writer.add_outline_item(document_data['title'], 0)
            parent_bookmarks[1] = main_bookmark
        
        # Process all blocks
        for block in document_data.get('blocks', []):
            # Block title as Level 2
            if block.get('title'):
                title = block['title']
                parent = parent_bookmarks.get(1)  # Under main title
                block_bookmark = writer.add_outline_item(title, 0, parent=parent)
                parent_bookmarks[2] = block_bookmark
                
                # Reset deeper levels
                for level in list(parent_bookmarks.keys()):
                    if level > 2:
                        del parent_bookmarks[level]
            
            # Extract Markdown headings
            if block.get('type') == 'markdown' and block.get('content'):
                content = block['content']
                lines = content.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        # Determine level
                        level = 0
                        for char in line:
                            if char == '#':
                                level += 1
                            else:
                                break
                        
                        # Extract and clean text
                        text = line[level:].strip()
                        if text:
                            clean_text = text.replace('**', '').replace('*', '').replace('`', '')
                            
                            # Adjust level (# becomes Level 3, ## becomes Level 4, etc.)
                            bookmark_level = level + 2
                            
                            # Find parent
                            parent = None
                            for parent_level in range(bookmark_level - 1, 0, -1):
                                if parent_level in parent_bookmarks:
                                    parent = parent_bookmarks[parent_level]
                                    break
                            
                            # Add bookmark
                            bookmark = writer.add_outline_item(clean_text, 0, parent=parent)
                            parent_bookmarks[bookmark_level] = bookmark
                            
                            # Reset deeper levels
                            for level_key in list(parent_bookmarks.keys()):
                                if level_key > bookmark_level:
                                    del parent_bookmarks[level_key]
        
        # Create PDF
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer
        
    except Exception as e:
        # Return original on error
        pdf_buffer.seek(0)
        return pdf_buffer

def create_pdf_from_html(document_data):
    """Create PDF directly from HTML/CSS - for Advanced Markdown Editor"""
    import logging
    import os
    import tempfile
    
    # Setup production logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Starting PDF generation for: {document_data.get('title', 'Untitled')}")
    
    try:
        # Build HTML content for Markdown
        content_html = ""
        
        # Add title
        if document_data.get('title'):
            title = html.escape(document_data['title'])
            # Unique ID for bookmark navigation
            content_html += f'<h1 id="title-bookmark" style="color: #1e3a8a; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #ddd; padding-bottom: 10px;">{title}</h1>\n'
        
        # Process blocks - for Markdown blocks
        block_counter = 0
        for block in document_data.get('blocks', []):
            block_type = block.get('type', 'markdown')
            block_content = block.get('content', '')
            block_title = block.get('title', '')
            
            if not block_content.strip() and not block_title.strip():
                continue
            
            block_counter += 1
            
            # Add block title if present
            if block_title.strip():
                escaped_title = html.escape(block_title)
                # H2 for better structure - real HTML tag for Playwright
                content_html += f'<h2 id="block-{block_counter}" style="color: #1e3a8a; margin-top: 25px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 5px;">{escaped_title}</h2>\n'
            
            # Process block content by type
            if block_type == 'markdown':
                # Convert Markdown to HTML server-side for correct headings
                if block_content.strip():
                    # Convert Markdown to HTML
                    md = markdown.Markdown(extensions=[
                        'tables', 
                        'fenced_code'
                    ])
                    html_content = md.convert(block_content)
                    
                    # Manually add IDs to headings for bookmarks
                    import re
                    def add_heading_ids(match):
                        level = len(match.group(1))
                        text = match.group(2)
                        # Generate simple ID from text
                        heading_id = re.sub(r'[^a-zA-Z0-9]', '-', text.lower()).strip('-')
                        return f'<h{level} id="heading-{block_counter}-{heading_id}">{text}</h{level}>'
                    
                    # Regex for <h1>text</h1> to <h6>text</h6>
                    html_content = re.sub(r'<h([1-6])>([^<]+)</h[1-6]>', add_heading_ids, html_content)
                    
                    content_html += f'{html_content}\n'
            elif block_type == 'code':
                escaped_content = html.escape(block_content)
                content_html += f'<pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; border-radius: 4px; font-family: \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto; margin: 15px 0;"><code>{escaped_content}</code></pre>\n'
        
        # Create HTML template (for Markdown with marked.js)
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
                
                /* Headings in blue */
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
                
                /* Tables */
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
                
                /* Lists */
                ul, ol {{
                    margin: 1rem 0;
                    padding-left: 2rem;
                }}
                
                li {{
                    margin: 0.5rem 0;
                }}
                
                /* Paragraphs */
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
        
        # Generate PDF with Playwright (like a real browser)
        logger.info("🌐 Launching browser for PDF generation...")
        
        with sync_playwright() as p:
            # Enhanced browser launch for Docker/Linux
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--run-all-compositor-stages-before-draw',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-ipc-flooding-protection'
                ]
            )
            
            page = browser.new_page()
            
            # Load HTML and generate PDF
            page.set_content(full_html)
            page.wait_for_load_state('networkidle', timeout=30000)
            
            pdf_bytes = page.pdf(
                format='A4',
                margin={
                    'top': '0.5cm',
                    'right': '2cm', 
                    'bottom': '2cm',
                    'left': '2cm'
                },
                print_background=True,
                prefer_css_page_size=True,
                outline=False,
                display_header_footer=False
            )
            
            logger.info(f"✅ PDF generated successfully ({len(pdf_bytes)} bytes)")
            
            if len(pdf_bytes) == 0:
                raise Exception("PDF generation resulted in empty file")
            
            pdf_buffer = BytesIO()
            pdf_buffer.write(pdf_bytes)
            pdf_buffer.seek(0)
            
            browser.close()
        
        # Add simple bookmarks
        logger.info("🔖 Adding bookmarks...")
        pdf_buffer = add_simple_bookmarks(pdf_buffer, document_data)
        logger.info("✅ PDF generation completed successfully")
        
        return pdf_buffer
        
    except Exception as e:
        logger.error(f"❌ PDF generation failed: {str(e)}")
        
        # Create a simple fallback PDF with error message
        try:
            logger.info("🔄 Creating fallback PDF...")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                page = browser.new_page()
                
                error_html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>PDF Generation Error</title></head>
                <body>
                    <h1>PDF Generation Error</h1>
                    <p>Error: {str(e)}</p>
                    <p>Time: {datetime.now()}</p>
                </body>
                </html>
                """
                
                page.set_content(error_html)
                pdf_bytes = page.pdf(format='A4')
                browser.close()
                
                buffer = BytesIO()
                buffer.write(pdf_bytes)
                buffer.seek(0)
                return buffer
                
        except Exception as fallback_error:
            logger.error(f"❌ Fallback PDF creation failed: {str(fallback_error)}")
            # Return minimal PDF
            buffer = BytesIO()
            buffer.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
            buffer.seek(0)
            return buffer

@app.route('/')
def index():
    """Main page of the application"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Favicon route"""
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/debug/test-pdf')
def debug_test_pdf():
    """Debug route to test PDF generation - useful for monitoring"""
    try:
        # Test document
        test_data = {
            'title': 'System Health Check',
            'blocks': [
                {
                    'type': 'markdown',
                    'title': 'Health Check',
                    'content': '# PDF Generation Test\n\nThis PDF was generated automatically to test system health.\n\n## Status\n\n✅ PDF generation is working correctly.\n\n**Generated:** ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
        
        pdf_buffer = create_pdf_from_html(test_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="health_check.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({
            'error': str(e), 
            'status': 'PDF generation failed',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    """Modern PDF generation for Advanced Markdown Editor"""
    try:
        document_data = request.json
        
        pdf_buffer = create_pdf_from_html(document_data)
        
        # Derive filename from title
        title = document_data.get('title', '').strip()
        if not title:
            title = 'DocumentWithoutName'
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"{safe_title or 'document'}.pdf"
        
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
    # Production vs Development
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    if debug_mode:
        # Development mode with Flask dev server
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Production mode - should be run with Gunicorn
        print("Production mode detected. Please use Gunicorn:")
        print("gunicorn --config gunicorn.conf.py app:app")
