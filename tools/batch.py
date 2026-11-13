"""Render every PDF in source-pdfs/ to issues/<slug>/ (cropped to TrimBox) and write tools/rendered.json."""
import sys, os, re, json, glob, pymupdf
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_meta = []
for src in sorted(glob.glob(f"{root}/source-pdfs/*.pdf")):
    title = os.path.splitext(os.path.basename(src))[0]
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    out = f"{root}/issues/{slug}"; os.makedirs(out, exist_ok=True)
    d = pymupdf.open(src); clip0 = d[0].trimbox
    for i, p in enumerate(d, 1):
        clip = p.trimbox
        for name, w, q in (("p", 1400, 78), ("t", 360, 70)):
            s = w / clip.width
            pix = p.get_pixmap(matrix=pymupdf.Matrix(s, s), clip=clip, alpha=False)
            Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(f"{out}/{name}{i:02d}.webp", "WEBP", quality=q, method=6)
    out_meta.append({"id": slug, "title": title, "pages": len(d), "aspect": round(clip0.width / clip0.height, 4)})
    print(slug, len(d), flush=True)
json.dump(out_meta, open(f"{root}/tools/rendered.json", "w"), indent=1)
