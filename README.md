 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..f98d3e9be9328ba4e373bf7383e103989f30cc78
--- /dev/null
+++ b/README.md
@@ -0,0 +1,110 @@
+# NotSan Curriculum Navigator
+
+Interaktive Website, um Lernfelder und Lernsituationen aus dem Curriculum der Notfallsanitäter:innen zu durchsuchen. Die Daten werden aus vorhandenen HTML-Dateien generiert und in einer kompakten Navigation dargestellt.
+
+## Vorbereitung
+1. Lege deine bestehenden Lernsituations-HTML-Dateien in den Ordner `data/`.
+2. Installiere die Python-Abhängigkeit, falls noch nicht vorhanden:
+   ```bash
+   pip install -r requirements.txt
+   ```
+
+## Manifest generieren
+Die Website liest ihre Inhalte aus `site/manifest.json`. Dieses Manifest wird aus den HTML-Dateien erzeugt:
+
+```bash
+python scripts/generate_manifest.py
+```
+
+- Standardmäßig werden alle `data/*.html`-Dateien verarbeitet.
+- Alternativ kannst du weitere Muster angeben, z. B. `python scripts/generate_manifest.py data/**/*.html extra/*.html`.
+
+## Website starten
+Öffne `site/index.html` direkt im Browser oder starte z. B. mit Python einen lokalen Server:
+```bash
+python -m http.server --directory site 8000
+```
+Rufe anschließend `http://localhost:8000` auf.
+
+## Funktionsweise
+- Links siehst du alle erkannten Lernfelder; beim Ausklappen erscheinen die zugehörigen Lernsituationen.
+- Beim Klick auf eine Lernsituation werden Ziele, Inhalte, Stundenverteilung, Prüfungsform, Quellen und Bezüge angezeigt (wenn in der HTML-Datei vorhanden).
+- Die Suchleiste filtert Lernsituationen nach Titel.
+
+## Hinweise zur Struktur-Erkennung
+- Lernfeld-Nummern werden aus Dateinamen wie `LF01_LS02.html` oder aus Überschriften wie `Lernfeld 1 – ...` abgeleitet.
+- Lernsituationen werden ähnlich aus `LS`-Angaben im Dateinamen oder in der Überschrift erkannt.
+- Abschnittsüberschriften, die eines der Wörter „Ziele“, „Inhalte“, „Stundenverteilung“, „Prüfungsform“, „Quellen“ oder „Bezüge“ enthalten, werden übernommen; alle Inhalte bis zur nächsten Überschrift werden angezeigt.
+
+## Beispielinhalte
+Im Ordner `data/` liegen zwei Beispiel-HTML-Dateien aus Lernfeld 1. Nach dem Generieren des Manifests kannst du deren Darstellung im `site/`-Ordner testen.
+
+## Dateien auf GitHub finden
+- **`data/`**: Hier liegen alle gelieferten Lernsituations-HTMLs (z. B. `LF01_LS1-1.html`, `LF01_LS1-2.html`).
+- **`scripts/generate_manifest.py`**: Parser, der die HTMLs in `site/manifest.json` überführt.
+- **`site/`**: Statische Website, die das Manifest konsumiert (`site/index.html`, `site/app.js`, `site/styles.css`).
+- **`main/`**: Falls du den Navigator später mit einem Framework weiterentwickeln willst, kannst du hier starten.
+
+Wenn du das Repo auf GitHub aufrufst, findest du diese Ordner direkt im Root. Öffne zum schnellen Check einfach `site/index.html` („View raw“) im Browser oder klone das Repo lokal und starte den kleinen Server wie oben beschrieben.
+
+### Schritt-für-Schritt auf GitHub (für Einsteiger:innen)
+1. Öffne auf GitHub die Repository-Startseite (z. B. `https://github.com/<dein-account>/NotSanCurriculum`).
+2. Achte links oben auf den Branch: Wähle **`main`**, damit du die neueste Version siehst.
+3. Scrolle auf der Startseite nach unten – dort siehst du die Ordner `data/`, `scripts/`, `site/` und `main/`.
+4. Klicke auf `site/` → dort findest du `index.html` (Ansicht: “View raw” zeigt die Datei direkt im Browser) sowie `app.js` und `styles.css`.
+5. Klicke auf `data/` → hier liegen die Lernsituations-HTMLs (z. B. `LF01_LS1-1.html`, `LF01_LS1-2.html`).
+6. Wenn du gerade ein Update gepusht hast und nichts siehst: drücke **F5/Reload** oder prüfe, ob dein Push auf `main` gelandet ist. Falls du einen anderen Branch benutzt, wähle ihn oben im Branch-Dropdown aus.
+7. Für eine komplette Vorschau kannst du stattdessen das Repo klonen und lokal starten (siehe Abschnitt „Website starten“ oben).
+
+### Wenn du auf GitHub nichts Neues siehst
+Falls du die Dateien nur lokal geändert hast, aber noch kein Remote-Repo oder keinen Push gemacht hast, erscheint online weiterhin nur der alte Stand. So schiebst du deine Änderungen auf GitHub:
+
+1. **Remote hinzufügen (nur einmal nötig):**
+   - Lege zuerst auf GitHub ein leeres Repository an (z. B. `https://github.com/<dein-account>/NotSanCurriculum`).
+   - Verbinde dein lokales Repo damit:
+     ```bash
+     git remote add origin https://github.com/<dein-account>/NotSanCurriculum.git
+     ```
+
+2. **Aktuellen Branch hochladen:**
+   - Du arbeitest hier auf dem Branch `work`. Lade ihn samt Historie hoch:
+     ```bash
+     git push -u origin work
+     ```
+   - Wenn du stattdessen `main` nutzen willst:
+     ```bash
+     git branch -M main
+     git push -u origin main
+     ```
+
+3. **Online prüfen:**
+   - Öffne dein GitHub-Repo, wähle oben den Branch (z. B. `work` oder `main`) und lade die Seite neu. Danach siehst du die Ordner `data/`, `scripts/`, `site/` usw.
+
+Tipp: Wenn du später neue Commits machst, reicht `git push` (mit dem gesetzten Upstream) aus, damit GitHub den aktuellen Stand bekommt.
+
+### Schnellhilfe, falls dein GitHub-Repo leer aussieht
+Wenn du online nur deinen allerersten Mini-Commit siehst (z. B. 7 Zeilen mit `echo "# NotSanCurriculum" > README.md`), hast du wahrscheinlich noch keinen Push mit dem aktuellen Stand gemacht. So gehst du vor:
+
+1. **Prüfen, auf welchem Branch du arbeitest** (hier ist es `work`):
+   ```bash
+   git status -sb
+   ```
+
+2. **Remote setzen (nur falls noch nicht vorhanden)** – ersetze `<dein-account>` durch deinen GitHub-Namen:
+   ```bash
+   git remote add origin https://github.com/<dein-account>/NotSanCurriculum.git
+   ```
+
+3. **Aktuellen Stand hochladen** (Variante A: Branch `work` beibehalten):
+   ```bash
+   git push -u origin work
+   ```
+   Oder (Variante B: Branch in `main` umbenennen und pushen):
+   ```bash
+   git branch -M main
+   git push -u origin main
+   ```
+
+4. **Im Browser neu laden**: Öffne dein Repo auf GitHub und wähle oben im Branch-Menü denselben Branch, den du gerade gepusht hast (`work` oder `main`). Danach solltest du die Ordner `data/`, `scripts/`, `site/` usw. sehen.
+
+5. **Danach reicht ein einfaches `git push`** für alle weiteren Änderungen.
 
EOF
)
