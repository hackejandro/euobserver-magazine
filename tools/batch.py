"""Render PDFs in source-pdfs/ to issues/<slug>/ and write tools/rendered.json.
Crops to TrimBox (drops bleed/crop marks) and splits double-page spreads into single pages.
Usage: batch.py [slug-substring ...]   (no args = everything)"""
import sys, os, re, json, glob, shutil, pymupdf
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
only = sys.argv[1:]
def clip_of(p):
    t, c = p.trimbox, p.cropbox
    t = pymupdf.Rect(t.x0 - c.x0, t.y0 - c.y0, t.x1 - c.x0, t.y1 - c.y0)   # trim box in page coordinates
    return t & p.rect
meta = []
for src in sorted(glob.glob(f"{root}/source-pdfs/*.pdf")):
    title = os.path.splitext(os.path.basename(src))[0]
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if only and not any(o in slug for o in only): continue
    out = f"{root}/issues/{slug}"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    d = pymupdf.open(src); n = 0; aspect = None
    for p in d:
        c = clip_of(p)
        if aspect is None: aspect = c.width / c.height
        halves = [c] if c.width / c.height < 1.2 else [
            pymupdf.Rect(c.x0, c.y0, c.x0 + c.width/2, c.y1), pymupdf.Rect(c.x0 + c.width/2, c.y0, c.x1, c.y1)]
        for h in halves:
            n += 1
            for name, w, q in (("p", 1400, 78), ("t", 360, 70)):
                s = w / h.width
                pix = p.get_pixmap(matrix=pymupdf.Matrix(s, s), clip=h, alpha=False)
                Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(f"{out}/{name}{n:02d}.webp", "WEBP", quality=q, method=6)
    meta.append({"id": slug, "title": title, "pages": n, "aspect": round(aspect, 4)})
    print(slug, n, round(aspect, 4), flush=True)
json.dump(meta, open(f"{root}/tools/rendered.json", "w"), indent=1)
