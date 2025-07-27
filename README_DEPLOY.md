# GPT zu PDF Converter - Live Demo

🚀 **Live-Version**: [Hier klicken für die Demo](https://gpttopdf.onrender.com)

Eine Flask-Webanwendung zur Erstellung strukturierter PDF-Dokumente aus Markdown-Inhalten.

## 🆕 Version 1.0 Features

- 📝 **Markdown Editor** mit EasyMDE (GitHub Flavored Markdown)
- 🎯 **Icon Picker** mit 95+ Emojis & Symbole
- 📊 **Smart Table Cleanup** für ChatGPT-Tabellen
- 🔄 **Drag & Drop** zum Sortieren der Blöcke
- 👁️ **Live-Vorschau** mit 1:1 PDF-Formatierung
- 📄 **PDF-Export** mit Bookmarks und professionellem Layout
- 💻 **Responsive Design** für alle Geräte
- 🎨 **Custom Button Styling** mit Gradient-Animationen

## 🛠️ Lokale Installation

1. **Repository klonen**
   ```bash
   git clone [repository-url]
   cd gpttopdf
   ```

2. **Python-Umgebung einrichten**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
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

## 📖 Verwendung

### Dokument erstellen

1. **Dokumenttitel eingeben** (optional, sonst "DokumentOhneNamen")
2. **Markdown-Blöcke hinzufügen** mit dem "Neuer Block" Button
3. **Inhalte eingeben** mit vollständiger Markdown-Syntax:
   - `**fett**` und `*kursiv*`
   - `# Überschriften` (H1-H6)
   - `> Blockquotes` mit blauem Strich
   - `| Tabellen |` mit automatischer Bereinigung
   - `` `Code` `` und ```Code-Blöcke```
   - `- Listen` und `1. Nummerierte Listen`
   - `[Links](https://...)`
   - `---` für Trennlinien
4. **Icon Picker** nutzen für 95+ Emojis & Symbole
5. **Drag & Drop** zum Sortieren der Blöcke
6. **Vorschau** zur Kontrolle vor PDF-Export

### PDF generieren

- **"Vorschau"** Button für Live-Preview
- **"PDF Erstellen"** für Download
- PDF enthält automatische Bookmarks aus Überschriften
- Dateiname basiert auf Dokumenttitel

### Pro-Features

- **Smart Paste** (Strg+V): Automatische Tabellen-Bereinigung
- **Block-Funktionen**: Duplizieren, Kollabieren, Löschen
- **Hilfe-Panel** mit Markdown-Syntax und Tipps
- **Fullscreen-Editor** mit Hilfe-Zugang
- **Custom Styling** für professionelle Optik

## 🏗️ Technische Details

### Backend
- **Flask** Web-Framework
- **Playwright** für HTML-zu-PDF Konvertierung
- **PyPDF** für Bookmark-Integration
- **Markdown** Parser für Content-Processing

### Frontend
- **Bootstrap 5** für responsives Design
- **EasyMDE** für Markdown-Editing mit Live-Preview
- **Marked.js** für Client-Side Markdown-Parsing
- **SortableJS** für Drag & Drop
- **Font Awesome** Icons

### Deployment
- **Render.com** Hosting (Production)
- **Gunicorn** WSGI Server
- **Environment Variables** für Configuration

## 📋 Kommende Features (Version 1.1)

- 👤 **User Management** (Login/Register)
- 💾 **Dokument Speichern/Laden**
- 📁 **Ordnerstruktur** für Organisation
- 👥 **Multi-User Support**
- 🔐 **Admin Panel**
- ☁️ **Cloud-Synchronisation**

## 🚀 Performance

- **Optimierte PDF-Generierung** mit Playwright
- **Client-Side Preview** für schnelle Vorschau
- **Lazy Loading** für große Dokumente
- **Responsive UI** für alle Bildschirmgrößen

## 🛡️ Sicherheit

- **Input Sanitization** für PDF-Generation
- **Error Handling** für robuste Performance
- **Production-Ready** Configuration

## 📄 Lizenz

MIT License - Frei verwendbar für persönliche und kommerzielle Projekte.

---

**🎯 Erstelle professionelle PDFs aus Markdown - Einfach, schnell, schön!**
