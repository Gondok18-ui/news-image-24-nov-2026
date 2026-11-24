#!/usr/bin/env python3
"""
The Daily Meridian -- a one-page broadsheet summing up the world news of
Tuesday, 24 November 2026, drawn entirely with Pillow.

This file is the generator that drew the entry's judged image,
entry.png. It is kept in the repository for provenance and
reproduction: run it locally with Pillow installed and it regenerates
the same 1024x1024 PNG (written next to this file, or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set). The drawing
is fully deterministic: no randomness, no clock, no network -- two
runs write the same bytes.

It is not the program the make.fun harness executes. The harness
entrypoint is main.ts (Node 22, standard library only), which copies
the entry.png held in this repository to the harness output directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 228)
PAPER_PANEL = (255, 253, 246)
INK = (25, 23, 19)
GREY = (92, 86, 76)
NAVY = (20, 48, 77)
NAVY_LIGHT = (38, 74, 110)
CREAM = (250, 246, 233)
RED = (166, 28, 28)
GOLD = (178, 132, 30)
HAIR = (120, 112, 96)
SKY = (216, 228, 230)
OCEAN = (110, 164, 196)
LAND = (106, 154, 91)
LAND2 = (178, 158, 96)
FLAME_O = (232, 122, 32)
FLAME_R = (196, 52, 36)
BLACK = (16, 15, 13)

_HERE = os.path.dirname(os.path.abspath(__file__))

FONT_DIRS = [
    # the fonts bundled with the entry come first: the grading image may
    # have no usable system fonts at all, and bundled-first also makes
    # the local and graded renders identical
    os.path.join(_HERE, "fonts"),
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
]

FONT_FILES = {
    "serif": "LiberationSerif-Regular.ttf",
    "serif_b": "LiberationSerif-Bold.ttf",
    "serif_i": "LiberationSerif-Italic.ttf",
    "sans": "LiberationSans-Regular.ttf",
    "sans_b": "LiberationSans-Bold.ttf",
}
FONT_FALLBACK = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "serif_i": "DejaVuSerif.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
}


_FONT_CACHE = []


def font(style, size):
    """Load a TrueType font by style name, with graceful fallbacks.

    Never raises: if every font file is missing and even Pillow's
    built-in default font cannot load (newer Pillow can raise there
    instead of returning the bitmap font), fall back to a font that was
    already loaded, so the page still draws.
    """
    for name in (FONT_FILES[style], FONT_FALLBACK[style]):
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    f = ImageFont.truetype(p, size)
                    _FONT_CACHE.append(f)
                    return f
                except Exception:
                    pass
    try:
        return ImageFont.load_default()
    except Exception:
        pass
    if _FONT_CACHE:
        return _FONT_CACHE[0]
    # last resort: any TrueType file in any searched directory
    for d in FONT_DIRS:
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for name in names:
            if name.lower().endswith(".ttf"):
                try:
                    return ImageFont.truetype(os.path.join(d, name), size)
                except Exception:
                    pass
    try:
        return ImageFont.load_default()
    except Exception:
        return _FONT_CACHE[0] if _FONT_CACHE else None


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, text, fnt, x, y, max_w, lh, fill=INK, max_lines=None,
          align="left", width=None):
    """Draw wrapped text; returns the y just past the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=fnt)
            draw.text((x + (max_w - w) / 2, y), ln, font=fnt, fill=fill)
        elif align == "right":
            w = draw.textlength(ln, font=fnt)
            draw.text((x + max_w - w, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_size(draw, text, style, start, max_w):
    """Largest font size <= start at which text fits max_w on one line."""
    size = start
    while size > 10 and draw.textlength(text, font=font(style, size)) > max_w:
        size -= 2
    return size


def rule(draw, x0, x1, y, w=1, fill=INK):
    draw.rectangle([x0, y, x1, y + w - 1], fill=fill)


# ---------------------------------------------------------------- drawing
def draw_chart_panel(draw, x0, y0, x1, y1):
    """The lead illustration: a soaring stock chart -- Nvidia's one-day
    jump -- drawn as flat newspaper-style shapes."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=2)
    # faint grid
    for gx in range(x0 + 40, x1 - 20, 44):
        draw.line([gx, y0 + 8, gx, y1 - 8], fill=(190, 205, 210), width=1)
    for gy in range(y0 + 24, y1 - 20, 28):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(190, 205, 210), width=1)
    # rising bars, left to right
    base = y1 - 16
    bx = x0 + 30
    for h in (18, 26, 22, 34, 30, 46, 42, 58, 66):
        draw.rectangle([bx, base - h, bx + 34, base], fill=NAVY_LIGHT,
                       outline=NAVY, width=1)
        bx += 46
    # the soaring line, ending in a dot
    pts = [(x0 + 24, base - 14), (x0 + 90, base - 34),
           (x0 + 150, base - 26), (x0 + 210, base - 52),
           (x0 + 270, base - 44), (x0 + 330, base - 78),
           (x0 + 390, base - 66), (x0 + 440, base - 104)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=RED, outline=INK,
                 width=2)
    # label, top left, clear of the line
    draw.text((x0 + 14, y0 + 12), "NVDA  +31%  IN A DAY",
              font=font("sans_b", 20), fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    X0, X1 = 44, 980
    CW = X1 - X0

    # page frame: heavy outer rule, hairline inside
    draw.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)
    draw.rectangle([20, 20, W - 21, H - 21], outline=HAIR, width=1)

    # ---------------- masthead
    rule(draw, X0, X1, 34, 3)
    rule(draw, X0, X1, 41, 1)
    name = "The Daily Meridian"
    nf = font("serif_b", fit_size(draw, name, "serif_b", 88, CW - 40))
    nw = draw.textlength(name, font=nf)
    draw.text(((W - nw) / 2, 48), name, font=nf, fill=INK)
    tag = "THE WHOLE WORLD  ·  ONE DAY  ·  ONE PAGE"
    tf = font("sans_b", 16)
    tw = draw.textlength(tag, font=tf)
    draw.text(((W - tw) / 2, 148), tag, font=tf, fill=GREY)
    rule(draw, X0, X1, 166, 1)
    rule(draw, X0, X1, 170, 3)

    # date bar
    draw.rectangle([X0, 182, X1, 218], fill=NAVY)
    df = font("sans_b", 22)
    draw.text((X0 + 16, 191), "TUESDAY, 24 NOVEMBER 2026", font=df, fill=CREAM)
    ef = font("sans_b", 15)
    et = "LATE FINAL EDITION"
    draw.text((X1 - 16 - draw.textlength(et, font=ef), 195), et, font=ef,
              fill=(198, 214, 228))

    # ticker strip directly under the date bar
    draw.rectangle([X0, 224, X1, 264], fill=BLACK)
    tick = ("ALSO TODAY  ▪  GERMANY GETS UKRAINE'S DELTA SYSTEM  ▪  "
            "SOLOMON ISLANDS ENDS CHINA PACT  ▪  SPAIN AMNESTIES "
            "PUIGDEMONT  ▪  SANOFI BUYS INSMED FOR $41BN  ▪  US LOSES "
            "MEASLES ELIMINATION STATUS")
    tick_lines = wrap(draw, tick, font("sans_b", 13), CW - 24)[:2]
    ty = 231
    for ln in tick_lines:
        lw = draw.textlength(ln, font=font("sans_b", 13))
        draw.text((X0 + (CW - lw) / 2, ty), ln, font=font("sans_b", 13),
                  fill=(240, 226, 190))
        ty += 18

    # ---------------- lead story
    kf = font("sans_b", 19)
    draw.text((X0, 280), "TECHNOLOGY  ·  MARKETS", font=kf, fill=RED)
    draw.text((X1 - draw.textlength("LEAD STORY", font=kf), 280), "LEAD STORY",
              font=kf, fill=GREY)
    hf = font("serif_b", 56)
    y = block(draw, "Huang Returns to Nvidia as Shares Soar 31%",
              hf, X0, 306, CW, 64)
    dek = ("Nvidia reinstates its founder as chief executive days after "
           "his resignation, after pressure from President Trump \u2014 and "
           "Wall Street answers with the biggest one-day rally of the AI era.")
    y = block(draw, dek, font("serif_i", 19), X0, y + 8, CW, 25, fill=(52, 48, 42))
    rule(draw, X0, X1, y + 8, 1, HAIR)

    # illustration (left) and lead body (right)
    top = y + 22
    draw_chart_panel(draw, X0, top, 576, top + 156)
    cap = ("Wall Street's verdict: Nvidia up 31% in a day, the S&P 500 up "
           "4.73% and the Nasdaq up 6.51% \u2014 the biggest rally of the "
           "AI era.")
    block(draw, cap, font("serif_i", 15), X0, top + 162, 532, 18,
          fill=GREY, max_lines=2)
    body = ("Nvidia's board reinstated Jensen Huang as chief executive "
            "and chair less than two weeks after he resigned, reportedly "
            "after pressure from Donald Trump. Shares jumped 31% in a "
            "day, the S&P 500 rose 4.73% and the Nasdaq 6.51%, lifting "
            "markets from Tokyo to Frankfurt as relief swept through "
            "AI stocks.")
    block(draw, body, font("serif", 16), 600, top, 380, 22, max_lines=9)
    rule(draw, X0, X1, 742, 2)

    # ---------------- three panels
    panels = [
        ("WAR & DETERRENCE", RED,
         "Russia Warns of 'Preventive Nuclear Attack'",
         "Medvedev says Ukraine and NATO crossed a line; Moscow warns "
         "Estonia it risks open war, and NATO vows to defend space "
         "after nuclear-satellite reports."),
        ("INDONESIA", NAVY,
         "Factory Fire Kills 26 in Banten, Dozens Missing",
         "The blaze at a factory in Banten province killed at least 26 "
         "people, with dozens more missing, in one of Indonesia's "
         "deadliest industrial fires in years."),
        ("TECHNOLOGY", NAVY,
         "US States Sue Musk Firms Over Grok Abuse Images",
         "Oregon and Virginia sue SpaceX over alleged Grok-generated "
         "child sexual-abuse images, in the first state cases of their "
         "kind against the chatbot."),
    ]
    col_w, gap = 296, 24
    py = 756
    for i, (label, colour, head, text) in enumerate(panels):
        px = X0 + i * (col_w + gap)
        draw.text((px, py), label, font=font("sans_b", 15), fill=colour)
        hy = block(draw, head, font("serif_b", 23), px, py + 24, col_w, 27,
                   max_lines=3)
        block(draw, text, font("serif", 15), px, hy + 6, col_w, 19,
              max_lines=4)
        if i:
            draw.line([px - gap // 2, py + 2, px - gap // 2, py + 160],
                      fill=HAIR, width=1)
    rule(draw, X0, X1, 934, 1, HAIR)

    # ---------------- four mini items
    minis = [
        ("LIBYA",
         "Zelensky: seven drones sank the Russian corvette Merkury."),
        ("DIPLOMACY",
         "Qatar seeks to revive US-Iran talks; Netanyahu urges strikes."),
        ("EUROPE",
         "Seven nations back limits on Russian tourist and sports visas."),
        ("HEALTH",
         "US loses measles elimination status after 25 years."),
    ]
    mw = (CW - 3 * 24) // 4
    my = 946
    for i, (label, text) in enumerate(minis):
        mx = X0 + i * (mw + 24)
        draw.text((mx, my), label, font=font("sans_b", 13), fill=NAVY)
        block(draw, text, font("serif", 13), mx, my + 18, mw, 16,
              max_lines=3)

    return img


def main():
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        primary = os.path.join(env_dir, "entry.png")
    elif os.path.isdir("/output"):
        primary = "/output/entry.png"
    else:
        primary = os.path.join(here, "entry.png")
    # the harness target is written first, and it is the only write
    # whose failure may fail the run
    d = os.path.dirname(primary)
    if d:
        os.makedirs(d, exist_ok=True)
    img.save(primary, "PNG", optimize=True)
    # a copy beside the program is a local convenience only: in the
    # grader the repository directory is read-only, so this write is
    # best-effort and must never fail the run
    local = os.path.join(here, "entry.png")
    if os.path.abspath(local) != os.path.abspath(primary):
        try:
            img.save(local, "PNG", optimize=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
