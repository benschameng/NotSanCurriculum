diff --git a/scripts/generate_manifest.py b/scripts/generate_manifest.py
new file mode 100644
index 0000000000000000000000000000000000000000..0d5b6c7793d1d13eb84a0d4ff94d1d38a0e9ec03
--- /dev/null
+++ b/scripts/generate_manifest.py
@@ -0,0 +1,159 @@
+#!/usr/bin/env python3
+"""
+Generate a manifest.json file for the curriculum site by parsing HTML source files.
+The script expects HTML files in the `data/` directory but also works with any
+glob passed as argument. It groups files by Lernfeld (LF) and extracts sections
+like Ziele, Inhalte, Stundenverteilung, Prüfungsform, Quellen und Bezüge.
+"""
+import argparse
+import json
+import re
+from collections import defaultdict
+from datetime import datetime
+from html import unescape
+from pathlib import Path
+
+KNOWN_SECTION_KEYS = {
+    "ziele": "Ziele",
+    "inhalte": "Inhalte",
+    "stundenverteilung": "Stundenverteilung",
+    "pruefungsform": "Prüfungsform",
+    "prüfungsform": "Prüfungsform",
+    "quellen": "Quellen",
+    "bezüge": "Bezüge",
+    "bezuege": "Bezüge",
+}
+
+SECTION_HEADINGS = {k.lower(): v for k, v in KNOWN_SECTION_KEYS.items()}
+HEADING_PATTERN = re.compile(r"<(h[1-6])[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
+PARAGRAPH_PATTERN = re.compile(r"<p[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
+TAG_PATTERN = re.compile(r"<[^>]+>")
+
+
+def strip_html(text: str) -> str:
+    return unescape(TAG_PATTERN.sub("", text)).strip()
+
+
+def detect_lernfeld(path: Path, heading_text: str | None) -> tuple[str, str]:
+    """Return (id, title) based on filename or heading fallback."""
+    patterns = [
+        re.compile(r"lf\s*(\d+)", re.IGNORECASE),
+        re.compile(r"lernfeld\s*(\d+)", re.IGNORECASE),
+    ]
+    text = " ".join(filter(None, [path.stem, heading_text or ""]))
+    for pattern in patterns:
+        match = pattern.search(text)
+        if match:
+            number = int(match.group(1))
+            return (f"LF{number:02d}", f"Lernfeld {number}")
+    return ("Unsortiert", "Ohne Lernfeld")
+
+
+def detect_lernsituation(path: Path, heading_text: str | None) -> tuple[str, str]:
+    patterns = [
+        re.compile(r"ls\s*(\d+)", re.IGNORECASE),
+        re.compile(r"lernsituation\s*(\d+)", re.IGNORECASE),
+    ]
+    text = " ".join(filter(None, [path.stem, heading_text or ""]))
+    for pattern in patterns:
+        match = pattern.search(text)
+        if match:
+            number = int(match.group(1))
+            return (f"LS{number:02d}", f"Lernsituation {number}")
+    return (path.stem, heading_text or path.stem)
+
+
+def extract_sections(html: str):
+    sections = []
+    headings = list(HEADING_PATTERN.finditer(html))
+    for index, heading in enumerate(headings):
+        title_raw = heading.group(2)
+        key = strip_html(title_raw).lower()
+        normalized = None
+        for label, clean in SECTION_HEADINGS.items():
+            if label in key:
+                normalized = clean
+                break
+        if not normalized:
+            continue
+
+        start = heading.end()
+        end = headings[index + 1].start() if index + 1 < len(headings) else len(html)
+        content_html = html[start:end]
+        content_html = re.sub(r"</\s*(body|html)\s*>", "", content_html, flags=re.IGNORECASE)
+        content_html = content_html.strip()
+        sections.append({
+            "title": normalized,
+            "html": content_html or "<p>Keine Inhalte hinterlegt.</p>",
+        })
+    return sections
+
+
+def extract_heading_text(html: str) -> str | None:
+    match = HEADING_PATTERN.search(html)
+    return strip_html(match.group(2)) if match else None
+
+
+def extract_overview(html: str) -> str:
+    paragraphs = [strip_html(p) for p in PARAGRAPH_PATTERN.findall(html)]
+    return " ".join(p for p in paragraphs if p)
+
+
+def build_manifest(source_files: list[Path]):
+    manifest = {
+        "generatedAt": datetime.utcnow().isoformat() + "Z",
+        "lernfelder": [],
+    }
+
+    grouped: dict[str, dict] = defaultdict(lambda: {"title": "", "situationen": []})
+
+    for file_path in sorted(source_files):
+        html = file_path.read_text(encoding="utf-8")
+        heading_text = extract_heading_text(html)
+        lernfeld_id, lernfeld_title = detect_lernfeld(file_path, heading_text)
+        ls_id, _ = detect_lernsituation(file_path, heading_text)
+
+        title = heading_text or file_path.stem
+        sections = extract_sections(html)
+        overview = extract_overview(html)
+
+        grouped[lernfeld_id]["title"] = lernfeld_title
+        source_path = file_path.resolve().relative_to(Path.cwd())
+
+        grouped[lernfeld_id]["situationen"].append({
+            "id": ls_id,
+            "title": title,
+            "overview": overview,
+            "source": str(source_path),
+            "sections": sections,
+        })
+
+    for lf_id in sorted(grouped.keys()):
+        lf_entry = grouped[lf_id]
+        lf_entry["id"] = lf_id
+        lf_entry["situationen"].sort(key=lambda x: x["id"])
+        manifest["lernfelder"].append(lf_entry)
+    return manifest
+
+
+def main():
+    parser = argparse.ArgumentParser(description="Generate manifest.json for the curriculum site")
+    parser.add_argument("paths", nargs="*", default=["data/*.html"], help="Glob patterns for HTML files")
+    parser.add_argument("--output", "-o", default=Path("site/manifest.json"), type=Path, help="Output JSON path")
+    args = parser.parse_args()
+
+    files = []
+    for pattern in args.paths:
+        files.extend(Path().glob(pattern))
+    source_files = [p for p in files if p.is_file()]
+    if not source_files:
+        raise SystemExit("Keine HTML-Dateien gefunden. Lege Dateien in data/ ab oder gib ein Muster an.")
+
+    manifest = build_manifest(source_files)
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
+    print(f"Manifest erzeugt: {args.output} ({len(source_files)} Dateien verarbeitet)")
+
+
+if __name__ == "__main__":
+    main()
