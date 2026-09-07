"""Subset Jua + Pretendard to the glyphs used in an SVG and embed them as
@font-face data URIs, so the SVG renders identically without network access.

Usage:
    python embed_fonts.py <in.svg> <out.svg>

Then open <out.svg> with agent-browser, screenshot to PNG, and put only the PNG
in the post. Requires: fonttools, brotli  (pip install fonttools brotli)
"""
import sys
import re
import io
import base64
import os

from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

FONTS_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = {
    ("Jua", 400, "normal"): "Jua-Regular.ttf",
    ("Pretendard", 400, "normal"): "Pretendard-Regular.ttf",
    ("Pretendard", 600, "normal"): "Pretendard-SemiBold.ttf",
}


def text_chars(svg):
    chars = set()
    for m in re.finditer(r"<text[^>]*>(.*?)</text>", svg, re.S):
        chars |= set(re.sub(r"<[^>]+>", "", m.group(1)))
    for m in re.finditer(r"<tspan[^>]*>(.*?)</tspan>", svg, re.S):
        chars |= set(m.group(1))
    chars |= set(" 0123456789.,%()/-~·")
    return "".join(sorted(c for c in chars if c == " " or c.strip()))


def subset_woff2(path, text):
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.notdef_outline = True
    opts.layout_features = ["*"]
    font = TTFont(path)
    s = Subsetter(opts)
    s.populate(text=text)
    s.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def families_used(svg):
    used = set(re.findall(r"font-family\s*[:=]\s*['\"]?\s*([A-Za-z][\w-]*)", svg))
    return used


def main():
    inp, outp = sys.argv[1], sys.argv[2]
    svg = open(inp, encoding="utf-8").read()
    text = text_chars(svg)
    used = families_used(svg)
    faces = []
    for (fam, weight, style), fn in FONT_FILES.items():
        if used and fam not in used:
            continue
        data = subset_woff2(os.path.join(FONTS_DIR, fn), text)
        b64 = base64.b64encode(data).decode()
        faces.append(
            f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
        print(f"  {fam} {weight}: {len(data)} bytes")
    style_block = "<style>\n" + "\n".join(faces) + "\n</style>"
    svg = re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + "\n" + style_block, svg, count=1)
    open(outp, "w", encoding="utf-8").write(svg)
    print(f"wrote {outp}")


if __name__ == "__main__":
    main()
