# EUobserver magazine viewer

Static, dependency-free flipbook viewer, hosted via GitHub Pages.

## Add an issue
1. `python3 -m venv .venv && .venv/bin/pip install pymupdf pillow`
2. `mkdir issues/2026-11 && .venv/bin/python tools/render.py issue.pdf issues/2026-11`
   (crops to the PDF TrimBox, removing bleed and crop marks)
3. Add an entry at the top of `issues.json` (newest first; the first entry is the default).
