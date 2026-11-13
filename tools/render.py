import sys, pymupdf, io
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
d = pymupdf.open(src)
tot = 0
for i, p in enumerate(d, 1):
    clip = p.trimbox          # crop to trim: drops bleed + crop marks
    for name, w, q in (("p", 1400, 80), ("t", 360, 72)):
        pix = p.get_pixmap(matrix=pymupdf.Matrix(w/clip.width, w/clip.width), clip=clip, alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        f = f"{out}/{name}{i:02d}.webp"; im.save(f, "WEBP", quality=q, method=6)
        import os; tot += os.path.getsize(f)
print(len(d), "pages", pix.width, pix.height, round(tot/1e6,1), "MB")
