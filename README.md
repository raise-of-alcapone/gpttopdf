# GPT zu PDF Converter

Eine Flask-Webanwendung zur Erstellung strukturierter PDF-Dokumente aus Web-Inhalten.

## Features

- 📝 **Rich-Text-Editor** mit Formatierungsoptionen
- 🧱 **Modulare Bausteine** (Text, Überschriften, Code)
- 🔄 **Drag & Drop** zum Sortieren der Blöcke
- 👁️ **Live-Vorschau** des Dokuments
- 📄 **PDF-Export** mit professionellem Layout
- 💻 **Responsive Web-Interface**

## Installation

1. **Repository klonen oder Dateien herunterladen**

2. **Python-Umgebung einrichten** (empfohlen: Virtual Environment)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Anwendung starten**
   ```bash
   python app.py
   ```

5. **Browser öffnen** und zu `http://127.0.0.1:5000` navigieren

## Verwendung

### Dokument erstellen

1. **Titel eingeben** (optional) im oberen Bereich
2. **Blöcke hinzufügen** über die Toolbar-Buttons:
   - **Text Block**: Für normalen Text mit Formatierung
   - **Überschrift**: Für Kapitelüberschriften  
   - **Code Block**: Für Programmcode
3. **Inhalte eingeben** in den Rich-Text-Editoren
4. **Blöcke sortieren** per Drag & Drop mit dem ⋮⋮ Symbol
5. **Live-Vorschau** in der rechten Seitenleiste betrachten

### PDF generieren

- Button **"PDF Generieren"** klicken
- PDF wird automatisch heruntergeladen
- Dateiname enthält Zeitstempel

### Block-Funktionen

- **Duplizieren**: Block kopieren mit dem 📋 Symbol
- **Löschen**: Block entfernen mit dem 🗑️ Symbol
- **Block-Titel**: Optionaler Titel für jeden Block
- **Formatierung**: Fett, kursiv, Listen, Links (außer Code-Blöcke)

## Technische Details

### Backend (Flask)
- **PDF-Generierung** mit ReportLab
- **HTML-zu-PDF Konvertierung** mit Text-Bereinigung
- **REST-API** für PDF-Export
- **Styles** für verschiedene Content-Typen

### Frontend
- **Bootstrap 5** für responsives Design
- **Quill.js** für Rich-Text-Editoren
- **SortableJS** für Drag & Drop
- **Font Awesome** für Icons

### PDF-Features
- **A4-Format** mit professionellen Rändern
- **Verschiedene Styles** für Text, Überschriften, Code
- **Automatische Formatierung** und Spacing
- **Zeitstempel** in Dateinamen

## Erweiterungsmöglichkeiten

- **Zusätzliche Block-Typen** (Bilder, Tabellen, etc.)
- **Themes/Templates** für verschiedene Dokumenttypen
- **Export-Formate** (Word, HTML, etc.)
- **Speichern/Laden** von Dokumenten
- **Collaboration-Features**
- **Mehr PDF-Optionen** (Seitenzahlen, Headers, etc.)

## Fehlerbehebung

### Häufige Probleme

**PDF wird nicht generiert:**
- Prüfen Sie die Browser-Konsole auf Fehler
- Stellen Sie sicher, dass ReportLab installiert ist
- Prüfen Sie, ob mindestens ein Block oder Titel vorhanden ist

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
