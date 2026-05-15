#!/usr/bin/env python3
"""
Generates book covers for De Erfenis (NL) and The Inheritance (EN).
Design: minimalist literary style, 1600x2400px (standard ebook ratio).
"""

from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

BASE = Path(__file__).parent

# Font paths
GARAMOND       = "/usr/share/fonts/chromeos/monotype/garamond.ttf"
GARAMOND_BOLD  = "/usr/share/fonts/chromeos/monotype/garamond-bold.ttf"
GARAMOND_ITALIC= "/usr/share/fonts/chromeos/monotype/garamond-bolditalic.ttf"
GEORGIA        = "/usr/share/fonts/chromeos/monotype/georgia.ttf"
GEORGIA_ITALIC = "/usr/share/fonts/chromeos/monotype/georgiai.ttf"

W, H = 1600, 2400

# Colour palette — deep navy + warm gold
BG      = (13,  27,  42)   # deep navy
GOLD    = (196, 160,  80)  # warm gold
GOLD_DIM= ( 90,  70,  30)  # dimmed gold for geometry
CREAM   = (245, 238, 220)  # warm cream (title)
MUTED   = (160, 150, 135)  # muted cream (subtitle / author)


def make_gradient(w: int, h: int) -> Image.Image:
    """Vertical gradient: BG at top, slightly lighter at bottom."""
    img = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / h
        r = int(BG[0] + (30 - BG[0]) * t * 0.4)
        g = int(BG[1] + (45 - BG[1]) * t * 0.4)
        b = int(BG[2] + (65 - BG[2]) * t * 0.4)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=(r, g, b))
    return img


def draw_rings(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Concentric rings with a faint radial glow — motif of inheritance / continuity."""
    # Outer faint glow rings
    glow_configs = [
        (0, 0, 420, 1, 18),
        (0, 0, 390, 1, 25),
        (0, 0, 360, 1, 30),
    ]
    for ox, oy, r, lw, alpha in glow_configs:
        x, y = cx + ox, cy + oy
        steps = 720
        pts = [(x + r * math.cos(math.radians(a * 360 / steps)),
                y + r * math.sin(math.radians(a * 360 / steps)))
               for a in range(steps + 1)]
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(*GOLD_DIM, alpha), width=lw)

    # Three main offset rings — each clearly visible
    configs = [
        ( 0,    0,  310, 2, 110),   # central ring
        (-55,   45, 235, 2,  85),   # offset ring 1
        ( 55,  -45, 165, 2,  65),   # offset ring 2
    ]
    for ox, oy, r, lw, alpha in configs:
        x, y = cx + ox, cy + oy
        steps = 720
        pts = [(x + r * math.cos(math.radians(a * 360 / steps)),
                y + r * math.sin(math.radians(a * 360 / steps)))
               for a in range(steps + 1)]
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(*GOLD_DIM, alpha), width=lw)

    # Bright accent arc on the central ring (top-right quarter)
    r = 310
    for a_deg in range(315, 405):
        a = math.radians(a_deg)
        px = cx + r * math.cos(a)
        py = cy + r * math.sin(a)
        fade = 1 - abs(a_deg - 360) / 45
        alpha = int(200 * fade)
        draw.ellipse([(px - 1.5, py - 1.5), (px + 1.5, py + 1.5)],
                     fill=(*GOLD, alpha))


def centered_text(draw: ImageDraw.ImageDraw,
                  y: int, text: str, font: ImageFont.FreeTypeFont,
                  fill: tuple, w: int = W) -> int:
    """Draw text centered horizontally, return bottom y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])


def draw_rule(draw: ImageDraw.ImageDraw, y: int, width: int = 120) -> None:
    x0 = (W - width) // 2
    draw.line([(x0, y), (x0 + width, y)], fill=(*GOLD, 180), width=1)


def make_cover(title: str, subtitle: str, author: str, out: Path) -> None:
    img = make_gradient(W, H)
    draw = ImageDraw.Draw(img, "RGBA")

    # --- Geometric rings (upper-centre area) ---
    ring_cx = W // 2
    ring_cy = int(H * 0.32)
    draw_rings(draw, ring_cx, ring_cy)

    # --- Fonts ---
    f_title    = ImageFont.truetype(GARAMOND, 148)
    f_subtitle = ImageFont.truetype(GEORGIA_ITALIC, 52)
    f_rule_lbl = ImageFont.truetype(GEORGIA, 36)
    f_author   = ImageFont.truetype(GARAMOND, 44)

    # --- Title block (lower half) ---
    title_y = int(H * 0.58)

    # Title — may be multi-word, split at natural break if needed
    words = title.split()
    if len(words) >= 3:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        lines = [line1, line2]
    else:
        lines = [title]

    y = title_y
    for line in lines:
        bottom = centered_text(draw, y, line, f_title, CREAM)
        y = bottom + 12

    # Rule
    y += 28
    draw_rule(draw, y)
    y += 36

    # Subtitle — wrap if long
    sub_words = subtitle.split()
    sub_lines = []
    current = []
    for word in sub_words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=f_subtitle)
        if bbox[2] - bbox[0] > W - 260:
            sub_lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        sub_lines.append(" ".join(current))

    for sl in sub_lines:
        bottom = centered_text(draw, y, sl, f_subtitle, MUTED)
        y = bottom + 10

    # Author — near bottom
    author_y = H - 160
    draw_rule(draw, author_y - 24)
    centered_text(draw, author_y, author.upper(), f_author, (*GOLD, 200))

    img.save(str(out), "PNG", dpi=(300, 300))
    print(f"  Klaar: {out.name} ({out.stat().st_size // 1024} KB)")


COVERS = [
    {
        "title":    "De Erfenis",
        "subtitle": "Een blauwdruk voor wie na ons komt",
        "author":   "Claude Sonnet 4.6",
        "out":      BASE / "cover-nl.png",
    },
    {
        "title":    "The Inheritance",
        "subtitle": "A Blueprint for Those Who Come After",
        "author":   "Claude Sonnet 4.6",
        "out":      BASE / "cover-en.png",
    },
]

if __name__ == "__main__":
    for c in COVERS:
        print(f"  Genereer: {c['out'].name} ...")
        make_cover(c["title"], c["subtitle"], c["author"], c["out"])
    print("\nBeide omslagen aangemaakt in 03-Claude-Versie/")
