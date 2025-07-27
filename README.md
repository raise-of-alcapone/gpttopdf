# GPT zu PDF Converter

Eine moderne Flask-Webanwendung zur Erstellung professioneller PDF-Dokumente aus Markdown-Inhalten mit hierarchischen Bookmarks.

## Features

- 📝 **Advanced Markdown Editor** mit EasyMDE
- 🧱 **Modulare Bausteine** für strukturierte Dokumente
- 🔄 **Drag & Drop** zum Sortieren der Blöcke
- 👁️ **Live-Vorschau** mit Syntax-Highlighting
- 📄 **PDF-Export** mit Playwright (hochwertige Ausgabe)
- 🔖 **Hierarchische Bookmarks** für Navigation
- 💻 **Responsive Web-Interface**

## Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd gpttopdf
```

### 2. Python Virtual Environment erstellen
```bash
python -m venv .venv
```

### 3. Virtual Environment aktivieren
**Windows:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 5. Playwright Browser installieren
```bash
playwright install chromium
```

### 6. Anwendung starten
```bash
python app.py
```

### 7. Browser öffnen
Navigiere zu `http://127.0.0.1:5000`

## Abhängigkeiten

- **Flask 3.0.3** - Web Framework
- **Playwright 1.48.0** - Browser-Engine für PDF-Generierung
- **PyPDF 4.3.1** - PDF-Manipulation für Bookmarks
- **Markdown 3.7** - Markdown-zu-HTML-Konvertierung

## Verwendung

### Dokument erstellen

1. **Titel eingeben** im Haupttitel-Feld
2. **Blöcke hinzufügen**:
   - **Markdown Block**: Für formatierten Text mit Markdown-Syntax
   - **Code Block**: Für Programmcode
3. **Inhalte bearbeiten** mit dem integrierten Editor
4. **Blöcke sortieren** per Drag & Drop
5. **Live-Vorschau** betrachten

### PDF generieren

Klicke den **"PDF Generieren"** Button - das PDF wird automatisch heruntergeladen.

### Markdown-Unterstützung

Der Editor unterstützt vollständige Markdown-Syntax:
- **Überschriften**: `# H1`, `## H2`, `### H3`, etc.
- **Formatierung**: `**fett**`, `*kursiv*`, `~~durchgestrichen~~`
- **Listen**: Bullet-Points und nummerierte Listen
- **Code**: `inline code` und Code-Blöcke
- **Links**: `[Text](URL)`
- **Tabellen**: Pipe-separierte Tabellen
- **Blockquotes**: `> Zitat`

### Block-Funktionen

- **Hinzufügen**: Neue Blöcke über die Toolbar
- **Sortieren**: Drag & Drop mit dem ⋮⋮ Handle
- **Löschen**: ✕ Button am Block-Header
- **Collapse/Expand**: Blöcke ein-/ausklappen
- **Block-Titel**: Optionale Titel für bessere Organisation

## Technische Details

### PDF-Generierung
- **Playwright** rendert HTML/CSS wie ein echter Browser
- **PyPDF** fügt hierarchische Bookmarks hinzu
- **Markdown-zu-HTML** Konvertierung mit syntax highlighting
- **A4-Format** mit professionellem Layout

### Frontend-Technologien
- **Bootstrap 5** für responsive UI
- **EasyMDE** für Markdown-Editor
- **SortableJS** für Drag & Drop
- **Font Awesome** für Icons

### PDF-Features
- **Hierarchische Bookmarks** für Navigation
- **Professionelles Styling** mit CSS
- **Syntax Highlighting** für Code-Blöcke
- **Responsive Tabellen** und Listen
- **Automatische Seitennummerierung**

## Deployment (Linux VPS)

### Systemabhängigkeiten installieren
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Browser-Abhängigkeiten für Playwright
sudo apt install libnss3 libnspr4 libatk-bridge2.0-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2
```

### Anwendung einrichten
```bash
# Repository klonen
git clone <your-repo>
cd gpttopdf

# Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
playwright install chromium

# Produktionsmodus starten
python app.py
```

### Mit Gunicorn (empfohlen)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Fehlerbehebung

### Playwright-Probleme
```bash
# Browser neu installieren
playwright install chromium

# Systemabhängigkeiten prüfen
playwright install-deps chromium
```

### PDF-Generierung fehlschlägt
- Prüfe Browser-Konsole auf JavaScript-Fehler
- Stelle sicher, dass Chromium installiert ist
- Prüfe Server-Logs für Python-Fehler

### Performance optimieren
- Für Produktion: `app.run(debug=False)`
- Gunicorn mit mehreren Workern verwenden
- Reverse Proxy (nginx) für statische Dateien

**Layout-Probleme:**
- Browser-Cache leeren
- Auf aktuellen Browser upgraden
- JavaScript-Fehler in der Konsole prüfen

**Installation-Probleme:**
- Python 3.7+ verwenden
- Virtual Environment nutzen
- Abhängigkeiten einzeln installieren bei Problemen

## Entwicklung

```bash
# Development-Modus mit Auto-Reload
python app.py

# Tests (falls vorhanden)
python -m pytest

# Abhängigkeiten updaten
pip freeze > requirements.txt
```

## Lizenz

MIT License - Frei verwendbar für persönliche und kommerzielle Projekte.
