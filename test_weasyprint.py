#!/usr/bin/env python3
import weasyprint
from io import BytesIO

# Einfacher Test
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; }
        h1 { color: blue; }
    </style>
</head>
<body>
    <h1>Test Titel</h1>
    <p>Das ist ein Test-Absatz.</p>
</body>
</html>
"""

try:
    pdf_buffer = BytesIO()
    html_doc = weasyprint.HTML(string=html_content)
    html_doc.write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    # PDF in Datei schreiben
    with open('test_output.pdf', 'wb') as f:
        f.write(pdf_buffer.read())
    
    print("✅ WeasyPrint funktioniert! PDF erstellt: test_output.pdf")
    
except Exception as e:
    print(f"❌ WeasyPrint Fehler: {e}")
    import traceback
    traceback.print_exc()
