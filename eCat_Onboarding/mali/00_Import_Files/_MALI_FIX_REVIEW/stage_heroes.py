#!/usr/bin/env python3
"""Stage catalogue-extracted + website-scraped clean hero JPGs into catA_images/.
Each output is sRGB, white background, exact ImageFileName casing, .jpg."""
import os
from PIL import Image

REV=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(REV,"catA_work","extract2")
SCR=os.path.join(REV,"scraped_images")
OUT=os.path.join(REV,"catA_images")
os.makedirs(OUT,exist_ok=True)

def to_srgb_white(src, dst, maxdim=1400):
    im=Image.open(src)
    if im.mode in ("RGBA","LA","P"):
        im=im.convert("RGBA")
        bg=Image.new("RGBA", im.size, (255,255,255,255))
        bg.alpha_composite(im); im=bg.convert("RGB")
    else:
        im=im.convert("RGB")
    if max(im.size)>maxdim:
        im.thumbnail((maxdim,maxdim), Image.LANCZOS)
    im.save(dst, "JPEG", quality=92, optimize=True)
    return im.size

# (target filename, source path)
jobs=[
    ("LTSPRO-9-WH.jpg",       os.path.join(SRC,"p27_x1264_788x296.jpeg")),
    ("LTSPRO-SW-09-WH.jpg",   os.path.join(SRC,"p28_x16555_797x256.jpeg")),
    ("DL-FR-5CCT-4-WH.jpg",   os.path.join(SRC,"p66_x699_369x233.jpeg")),
    ("RGL-FR-5CCT-4-WH.jpg",  os.path.join(SRC,"p67_x715_475x257.jpeg")),
    ("LV-SPIR-1CH-LV.jpg",    os.path.join(SRC,"p85_x803_260x142.jpeg")),
    ("LV-DL-EX-10-L.jpg",     os.path.join(SCR,"LV-DL-EX-10-L.jpg")),
    ("LV-DL-EX-30-L.jpg",     os.path.join(SCR,"LV-DL-EX-30-L.jpg")),
]
for tgt,src in jobs:
    if not os.path.exists(src):
        print("MISSING SRC:",src); continue
    sz=to_srgb_white(src, os.path.join(OUT,tgt))
    print(f"staged {tgt:24} <- {os.path.basename(src):28} {sz}")

# optional catalogue fallbacks for the repoint targets (NOT overwriting live good files)
os.makedirs(os.path.join(REV,"catA_work","fallback"),exist_ok=True)
fb=[("LEDLB-5CCT-BAR_catalogue.jpg", os.path.join(SRC,"p29_x347_410x117.jpeg")),
    ("GDL_gimbal_catalogue.jpg",     os.path.join(SRC,"p60_x659_304x223.jpeg"))]
for tgt,src in fb:
    if os.path.exists(src):
        to_srgb_white(src, os.path.join(REV,"catA_work","fallback",tgt))
        print("fallback",tgt)
