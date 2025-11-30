# GitHub Wiki Setup - Anleitung

Diese Anleitung erklärt, wie du das zweisprachige Wiki für dein Repository einrichtest.

---

## 📁 Wiki-Struktur

Das Wiki ist zweisprachig organisiert:

```
wiki/
├── Home.md                          # Startseite mit Sprachauswahl
├── _Sidebar.md                      # Navigation (erscheint auf jeder Seite)
│
├── 🇩🇪 Deutsche Seiten
├── Konfiguration.md
├── Einfache-Motorinteraktionen.md
├── Berechnungen.md
├── Gyro-Funktionen.md
├── Gyro-drive-distance.md
├── Gyro-turn-to-angle.md
├── Gyro-Sensorfunktionen.md
├── Gyro-Tipps.md
│
└── 🇬🇧 English Pages
    ├── Configuration-EN.md
    ├── Simple-Motor-Interactions-EN.md
    ├── Calculations-EN.md
    ├── Gyro-Functions-EN.md
    ├── Gyro-drive-distance-EN.md
    ├── Gyro-turn-to-angle-EN.md
    ├── Gyro-Sensor-Functions-EN.md
    └── Gyro-Tips-EN.md
```

---

## 🚀 Wiki auf GitHub aktivieren

### Schritt 1: Wiki klonen

Dein Repository-Wiki hat eine eigene Git-URL:

```bash
# Wiki klonen (ersetze USERNAME und REPO)
git clone https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague.wiki.git

# In Wiki-Verzeichnis wechseln
cd MPDVeRruEcKtEn-FirstLegoLeague.wiki
```

### Schritt 2: Wiki-Dateien kopieren

```bash
# Zurück zum Haupt-Repository
cd ..

# Wiki-Dateien ins Wiki-Repository kopieren
cp -r wiki/* MPDVeRruEcKtEn-FirstLegoLeague.wiki/

# Ins Wiki-Repository wechseln
cd MPDVeRruEcKtEn-FirstLegoLeague.wiki
```

### Schritt 3: Änderungen commiten und pushen

```bash
# Status prüfen
git status

# Alle Dateien hinzufügen
git add .

# Commit erstellen
git commit -m "Initiales zweisprachiges Wiki (DE/EN)"

# Zum GitHub Wiki pushen
git push origin master
```

---

## 🌐 Wiki online aktivieren

1. Gehe zu deinem Repository auf GitHub: `https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague`
2. Klicke oben auf **"Settings"** (Einstellungen)
3. Scrolle zu **"Features"**
4. Aktiviere **"Wikis"** (Häkchen setzen)
5. Klicke auf den **"Wiki"**-Tab oben

Das Wiki ist jetzt unter dieser URL erreichbar:
```
https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague/wiki
```

---

## ✏️ Wiki bearbeiten

### Option 1: Direkt auf GitHub

1. Gehe zum Wiki: `https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague/wiki`
2. Klicke auf eine Seite
3. Klicke auf **"Edit"** (Bearbeiten)
4. Mache deine Änderungen
5. Klicke auf **"Save Page"**

### Option 2: Lokal bearbeiten (empfohlen für größere Änderungen)

```bash
# Wiki klonen (falls noch nicht getan)
git clone https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague.wiki.git

cd MPDVeRruEcKtEn-FirstLegoLeague.wiki

# Datei bearbeiten (z.B. mit VS Code)
code Home.md

# Änderungen commiten
git add .
git commit -m "Wiki aktualisiert"
git push
```

---

## 📝 Neue Wiki-Seite hinzufügen

### Deutsche Seite

1. Erstelle neue Datei: `Neue-Seite.md`
2. Füge Inhalt hinzu
3. Verlinke in `_Sidebar.md` unter "🇩🇪 Deutsch"
4. Verlinke in relevanten Seiten mit `[Link-Text](Neue-Seite)`

### Englische Seite

1. Erstelle neue Datei: `New-Page-EN.md`
2. Füge englischen Inhalt hinzu
3. Verlinke in `_Sidebar.md` unter "🇬🇧 English"
4. Verlinke in relevanten Seiten mit `[Link Text](New-Page-EN)`

---

## 🎨 Wiki-Formatierung

### Interne Links

```markdown
[Link zur Konfiguration](Konfiguration)
[Link to Configuration](Configuration-EN)
```

### Navigation Links

```markdown
[← Zurück](Vorherige-Seite) | [🏠 Home](Home) | [Weiter →](Nächste-Seite)
```

### Code-Blöcke

```markdown
```python
robot.drive_distance(distance=50)
\```
```

### Warnungen/Hinweise

```markdown
⚠️ **Vorsicht:** Wichtiger Hinweis!
💡 **Tipp:** Nützlicher Tipp!
✅ **Empfohlen:** Beste Vorgehensweise
```

---

## 🔄 Workflow für Updates

Wenn du Code oder Dokumentation änderst:

1. **Hauptrepository aktualisieren:**
   ```bash
   cd MPDVeRruEcKtEn-FirstLegoLeague
   # Ändere Dokumentation.md oder Code
   git add .
   git commit -m "Dokumentation aktualisiert"
   git push
   ```

2. **Wiki aktualisieren:**
   ```bash
   cd ../MPDVeRruEcKtEn-FirstLegoLeague.wiki
   # Ändere entsprechende Wiki-Seiten
   git add .
   git commit -m "Wiki aktualisiert"
   git push
   ```

---

## 🔗 Nützliche Links

- **Wiki URL:** `https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague/wiki`
- **Repository:** `https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague`
- **GitHub Wiki Docs:** https://docs.github.com/en/communities/documenting-your-project-with-wikis

---

## ❓ Häufige Fragen

### Wie erstelle ich eine neue Seite?

Einfach eine neue `.md` Datei im Wiki-Verzeichnis erstellen und pushen.

### Wie ändere ich die Sidebar?

Bearbeite die Datei `_Sidebar.md`.

### Kann ich Bilder einfügen?

Ja! Lade Bilder ins Wiki hoch oder verlinke sie:
```markdown
![Beschreibung](https://url-zum-bild.png)
```

### Wie lösche ich eine Seite?

Lösche die `.md` Datei und pushe die Änderung. Entferne auch alle Links zur Seite.

---

## 🎯 Nächste Schritte

1. ✅ Wiki auf GitHub aktivieren
2. ✅ Wiki-Dateien hochladen
3. ✅ Links testen
4. ✅ Fehlende englische Seiten ergänzen
5. ✅ Bilder/Diagramme hinzufügen (optional)
6. ✅ Wiki-Link im README.md des Hauptrepositories verlinken

---

Viel Erfolg mit deinem Wiki! 🚀
