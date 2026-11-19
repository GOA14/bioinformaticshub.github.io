#!/usr/bin/env python3
"""Regenerate the Bioinformatics Hub logo set.

    python scripts/make_logo.py            # writes assets/brand/svg/*.svg
    python scripts/make_logo.py --png      # also rasterises (needs cairosvg, pillow)

The mark is the outline of Nigeria carrying the community network: a node for each
major university / research city, linked through Abuja (the amber hub node). The
outline is real geometry, simplified from the open `datasets/geo-countries` boundary
file to 158 vertices. Wordmark type is converted to outlines with matplotlib so the
files render identically without the font installed.

Edit CITIES / EDGES / the palette below and re-run to change the mark.
"""
from __future__ import annotations

import argparse
import math
import pathlib

from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "brand"

# --- palette ---------------------------------------------------------------
NG_GREEN = "#008751"   # Nigerian flag green, primary
NG_DARK  = "#00603a"
NG_LIGHT = "#6fc79b"
AMBER    = "#c98a00"   # hub node / accent
INK      = "#0f1f18"
WHITE    = "#ffffff"
WORDMARK_FONT = "DejaVu Sans"   # swap for Inter/Source Sans once installed

# --- geometry --------------------------------------------------------------
NGA_PATH = "M 83.5 166.1 L 85.9 163.9 L 83.7 158.9 L 85.0 137.9 L 94.8 129.9 L 100.2 121.4 L 101.5 105.1 L 114.4 97.4 L 126.3 94.7 L 138.9 95.8 L 148.9 91.1 L 170.1 99.3 L 177.8 99.8 L 197.1 121.5 L 201.6 121.4 L 206.0 117.3 L 212.5 117.4 L 227.2 109.4 L 236.8 111.0 L 256.3 123.9 L 287.3 128.1 L 305.3 112.7 L 324.2 108.4 L 350.2 108.8 L 371.2 117.3 L 385.3 119.1 L 388.3 113.0 L 396.6 108.5 L 397.9 104.5 L 411.0 102.5 L 414.5 96.9 L 423.9 97.1 L 439.5 118.6 L 443.7 142.9 L 453.8 144.1 L 460.0 149.5 L 455.7 165.6 L 458.4 168.4 L 457.9 172.3 L 442.9 181.8 L 436.7 180.5 L 428.9 189.4 L 421.6 203.0 L 418.1 219.1 L 411.1 222.8 L 409.9 240.1 L 398.3 245.7 L 399.8 249.7 L 395.5 267.0 L 388.2 272.3 L 381.8 272.1 L 383.0 276.0 L 377.0 279.8 L 375.8 294.4 L 369.9 302.7 L 370.0 307.6 L 360.3 318.4 L 364.9 324.7 L 354.4 331.7 L 354.4 337.3 L 348.5 345.5 L 339.1 346.9 L 336.5 336.3 L 320.9 322.9 L 318.1 331.7 L 308.4 331.6 L 306.1 327.2 L 297.0 334.7 L 294.0 334.5 L 290.8 343.5 L 278.8 351.0 L 266.6 365.4 L 262.3 367.0 L 261.1 372.0 L 264.0 375.7 L 260.4 390.7 L 251.2 406.1 L 239.2 396.4 L 245.2 408.2 L 243.0 411.6 L 218.2 412.4 L 217.7 406.1 L 216.3 410.8 L 208.8 409.8 L 210.6 412.3 L 208.8 413.1 L 205.1 407.5 L 201.7 404.4 L 205.5 412.7 L 200.7 415.5 L 199.3 405.8 L 198.9 409.6 L 195.8 407.0 L 200.0 416.8 L 195.1 417.2 L 191.9 402.4 L 189.5 401.8 L 194.8 418.1 L 189.5 418.3 L 190.2 409.6 L 188.8 416.0 L 187.5 412.9 L 188.6 418.9 L 186.0 418.9 L 185.0 413.0 L 184.6 419.0 L 174.4 420.4 L 176.5 415.5 L 174.2 416.9 L 173.5 413.4 L 172.6 420.5 L 168.5 420.9 L 167.1 416.1 L 167.3 420.4 L 164.8 416.2 L 163.4 419.0 L 150.5 407.3 L 144.3 391.8 L 148.1 391.3 L 143.6 390.5 L 143.0 383.9 L 150.9 383.0 L 149.4 379.8 L 153.0 377.6 L 144.0 382.4 L 137.7 377.1 L 148.3 374.9 L 142.3 375.3 L 142.5 371.2 L 137.3 376.1 L 134.2 371.8 L 141.1 364.9 L 132.7 369.8 L 122.6 357.0 L 111.0 349.5 L 77.5 347.6 L 91.9 340.8 L 80.7 343.7 L 79.6 341.1 L 76.3 348.1 L 53.1 349.1 L 56.1 311.0 L 52.0 296.6 L 55.3 256.8 L 65.8 255.5 L 67.7 243.0 L 74.5 236.3 L 74.3 231.2 L 80.6 229.6 L 83.2 226.1 L 85.9 219.3 L 82.7 214.6 L 85.4 209.4 L 89.5 210.4 L 91.7 203.8 L 88.0 196.6 L 87.7 186.2 L 79.1 175.6 Z"

# Projection constants matching NGA_PATH (equirectangular, cos-lat corrected).
PROJ = dict(lat0=0.14217295515246964, minx=2.6441319518965773, miny=4.278144, scale=34.35455476899937,
            offx=52.0, offy=91.06125749425851)

CITIES = {'Sokoto': (5.24, 13.06), 'Kano': (8.52, 12.0), 'Maiduguri': (13.15, 11.83), 'Abuja': (7.49, 9.06), 'Jos': (8.89, 9.9), 'Ilorin': (4.55, 8.5), 'Ibadan': (3.9, 7.38), 'Lagos': (3.38, 6.52), 'Enugu': (7.5, 6.44), 'Port Harcourt': (7.01, 4.82), 'Calabar': (8.32, 4.95), 'Yola': (12.49, 9.21)}
EDGES = [('Abuja', 'Kano'), ('Abuja', 'Jos'), ('Abuja', 'Ilorin'), ('Abuja', 'Enugu'), ('Abuja', 'Lagos'), ('Kano', 'Sokoto'), ('Kano', 'Maiduguri'), ('Jos', 'Yola'), ('Ilorin', 'Ibadan'), ('Ibadan', 'Lagos'), ('Enugu', 'Port Harcourt'), ('Port Harcourt', 'Calabar'), ('Maiduguri', 'Yola')]


def proj(lon: float, lat: float) -> tuple[float, float]:
    x = (lon * math.cos(PROJ["lat0"]) - PROJ["minx"]) * PROJ["scale"] + PROJ["offx"]
    y = 512 - ((lat - PROJ["miny"]) * PROJ["scale"] + PROJ["offy"])
    return x, y


def text_path_d(text: str, size: float = 100, weight: str = "bold"):
    tp = TextPath((0, 0), text, size=size, prop=FontProperties(family=WORDMARK_FONT, weight=weight))
    out = []
    for v, code in tp.iter_segments():
        v = list(v)
        if code == 1:    out.append(f"M {v[0]:.2f} {-v[1]:.2f}")
        elif code == 2:  out.append(f"L {v[0]:.2f} {-v[1]:.2f}")
        elif code == 3:  out.append(f"Q {v[0]:.2f} {-v[1]:.2f} {v[2]:.2f} {-v[3]:.2f}")
        elif code == 4:  out.append(f"C {v[0]:.2f} {-v[1]:.2f} {v[2]:.2f} {-v[3]:.2f} {v[4]:.2f} {-v[5]:.2f}")
        elif code == 79: out.append("Z")
    ext = tp.get_extents()
    return " ".join(out), ext.width, ext.x0


def svg(body: str, w: int = 512, h: int = 512, bg: str | None = None) -> str:
    back = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-label="Bioinformatics Hub">\n'
            f'  <title>Bioinformatics Hub</title>\n  {back}\n  {body}\n</svg>\n')


def mark(colour_body: str = NG_GREEN, node: str = WHITE, link: str = WHITE,
         hub: str = AMBER, outline: bool = False) -> str:
    p = ([f'<path d="{NGA_PATH}" fill="none" stroke="{colour_body}" stroke-width="14" '
          f'stroke-linejoin="round"/>'] if outline else
         [f'<path d="{NGA_PATH}" fill="{colour_body}"/>'])
    for a, b in EDGES:
        x1, y1 = proj(*CITIES[a]); x2, y2 = proj(*CITIES[b])
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{link}" stroke-width="7" opacity="0.8" stroke-linecap="round"/>')
    for name, (lon, lat) in CITIES.items():
        x, y = proj(lon, lat)
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{20 if name == "Abuja" else 13}" '
                 f'fill="{hub if name == "Abuja" else node}"/>')
    return "\n  ".join(p)


def mark_mono(colour: str, uid: str = "net") -> str:
    """Single-colour mark: the network is knocked out of the silhouette."""
    cut = ['<rect width="512" height="512" fill="#fff"/>']
    for a, b in EDGES:
        x1, y1 = proj(*CITIES[a]); x2, y2 = proj(*CITIES[b])
        cut.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="#000" stroke-width="9" stroke-linecap="round"/>')
    for name, (lon, lat) in CITIES.items():
        x, y = proj(lon, lat)
        cut.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{21 if name == "Abuja" else 14}" fill="#000"/>')
        if name == "Abuja":
            cut.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#fff"/>')
    return (f'<defs><mask id="{uid}">{"".join(cut)}</mask></defs>'
            f'<g mask="url(#{uid})"><path d="{NGA_PATH}" fill="{colour}"/></g>')


def tile(radius: int = 112, bg: str = NG_GREEN, plain: bool = False) -> str:
    p = [f'<rect width="512" height="512" rx="{radius}" fill="{bg}"/>']
    inner = [f'<path d="{NGA_PATH}" fill="{WHITE}"/>']
    if not plain:
        inner += [f'<line x1="{proj(*CITIES[a])[0]:.1f}" y1="{proj(*CITIES[a])[1]:.1f}" '
                  f'x2="{proj(*CITIES[b])[0]:.1f}" y2="{proj(*CITIES[b])[1]:.1f}" stroke="{bg}" '
                  f'stroke-width="8" stroke-linecap="round" opacity="0.85"/>' for a, b in EDGES]
        inner += [f'<circle cx="{proj(lo, la)[0]:.1f}" cy="{proj(lo, la)[1]:.1f}" '
                  f'r="{19 if n == "Abuja" else 12}" fill="{AMBER if n == "Abuja" else bg}"/>'
                  for n, (lo, la) in CITIES.items()]
    p.append(f'<g transform="translate(256 256) scale(0.80) translate(-256 -256)">{"".join(inner)}</g>')
    return "\n  ".join(p)


SUBTITLE = "N I G E R I A   \u00b7   S I N C E   2 0 1 6"


def lockup_h(style: str = "light", h: int = 420) -> str:
    cfg = {"light": (INK, NG_GREEN, WHITE, mark()),
           "dark": (WHITE, NG_LIGHT, INK, mark()),
           "mono-black": (INK, INK, WHITE, mark_mono(INK)),
           "mono-white": (WHITE, WHITE, INK, mark_mono(WHITE))}[style]
    ink, sub_col, bg, body_mark = cfg
    box, mx, my = 320, 60, (h - 320) / 2
    d1, w1, x0 = text_path_d("Bioinformatics Hub", size=104)
    tx, ty = mx + box + 60, h / 2 - 8
    w = max(1600, int(tx + w1 + 60))
    d2, _, x02 = text_path_d(SUBTITLE, size=29)
    body = [f'<rect width="{w}" height="{h}" fill="{bg}"/>',
            f'<g transform="translate({mx} {my}) scale({box/512:.4f})">{body_mark}</g>',
            f'<g transform="translate({tx - x0:.1f} {ty:.1f})"><path d="{d1}" fill="{ink}"/></g>',
            f'<g transform="translate({tx - x02:.1f} {ty + 66:.1f})"><path d="{d2}" fill="{sub_col}"/></g>']
    return svg("\n  ".join(body), w=w, h=h)


def lockup_stacked(style: str = "light", h: int = 1020) -> str:
    on_dark = style == "dark"
    ink, sub_col, bg = (WHITE, NG_LIGHT, INK) if on_dark else (INK, NG_GREEN, WHITE)
    d1, w1, x0 = text_path_d("Bioinformatics Hub", size=92)
    w = int(w1 + 160)
    box = 520
    d2, w2, x02 = text_path_d(SUBTITLE, size=27)
    body = [f'<rect width="{w}" height="{h}" fill="{bg}"/>',
            f'<g transform="translate({(w - box)/2} 70) scale({box/512:.4f})">{mark()}</g>',
            f'<g transform="translate({(w - w1)/2 - x0:.1f} 790)"><path d="{d1}" fill="{ink}"/></g>',
            f'<g transform="translate({(w - w2)/2 - x02:.1f} 852)"><path d="{d2}" fill="{sub_col}"/></g>']
    return svg("\n  ".join(body), w=w, h=h)


def social_card(w: int = 1280, h: int = 640) -> str:
    body = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{NG_DARK}"/><stop offset="0.6" stop-color="{NG_GREEN}"/>'
            f'<stop offset="1" stop-color="#13996b"/></linearGradient></defs>',
            f'<rect width="{w}" height="{h}" fill="url(#g)"/>',
            f'<g transform="translate({w-430} {h/2-215}) scale({430/512:.4f})" opacity="0.18">'
            f'{mark(WHITE, NG_GREEN, NG_GREEN, NG_GREEN)}</g>',
            f'<g transform="translate(72 {h/2-180}) scale({200/512:.4f})">'
            f'{mark(WHITE, NG_GREEN, NG_GREEN, AMBER)}</g>']
    for text, size, y, fill in [("Bioinformatics Hub", 86, 420, WHITE),
                                ("The bioinformatics community for scientists", 36, 486, "#d9f0e4"),
                                ("and researchers in Nigeria", 36, 536, "#d9f0e4"),
                                ("bioinformaticshub.github.io", 30, 596, NG_LIGHT)]:
        d, _, x0 = text_path_d(text, size=size)
        body.append(f'<g transform="translate({72 - x0:.1f} {y})"><path d="{d}" fill="{fill}"/></g>')
    return svg("\n  ".join(body), w=w, h=h)


FILES = {
    "mark-primary.svg": lambda: svg(mark()),
    "mark-outline.svg": lambda: svg(mark(NG_GREEN, NG_GREEN, NG_LIGHT, AMBER, outline=True)),
    "mark-mono-black.svg": lambda: svg(mark_mono(INK)),
    "mark-mono-white.svg": lambda: svg(mark_mono(WHITE), bg=INK),
    "mark-mono-green.svg": lambda: svg(mark_mono(NG_GREEN)),
    "icon-tile.svg": lambda: svg(tile()),
    "icon-tile-square.svg": lambda: svg(tile(radius=0)),
    "icon-favicon.svg": lambda: svg(tile(radius=96, plain=True)),
    "lockup-horizontal.svg": lambda: lockup_h("light"),
    "lockup-horizontal-dark.svg": lambda: lockup_h("dark"),
    "lockup-horizontal-mono-black.svg": lambda: lockup_h("mono-black"),
    "lockup-horizontal-mono-white.svg": lambda: lockup_h("mono-white"),
    "lockup-stacked.svg": lambda: lockup_stacked("light"),
    "lockup-stacked-dark.svg": lambda: lockup_stacked("dark"),
    "social-card.svg": lambda: social_card(),
}

RASTER = [("icon-tile.svg", "icon-{}.png", [1024, 512, 256, 128, 64]),
          ("icon-favicon.svg", "favicon-{}.png", [180, 48, 32, 16]),
          ("mark-primary.svg", "mark-{}.png", [1024, 512])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true", help="also write PNG/ICO exports")
    args = ap.parse_args()

    (OUT / "svg").mkdir(parents=True, exist_ok=True)
    for name, fn in FILES.items():
        (OUT / "svg" / name).write_text(fn(), encoding="utf-8")
    print(f"wrote {len(FILES)} SVG files to {OUT / 'svg'}")

    if args.png:
        import cairosvg
        from PIL import Image
        (OUT / "png").mkdir(exist_ok=True)
        for src, pattern, sizes in RASTER:
            for px in sizes:
                cairosvg.svg2png(url=str(OUT / "svg" / src), output_width=px, output_height=px,
                                 write_to=str(OUT / "png" / pattern.format(px)))
        for src, name, px in [("lockup-horizontal.svg", "lockup-horizontal-2400.png", 2400),
                              ("lockup-stacked.svg", "lockup-stacked-1600.png", 1600),
                              ("social-card.svg", "social-card-1280x640.png", 1280)]:
            cairosvg.svg2png(url=str(OUT / "svg" / src), output_width=px,
                             write_to=str(OUT / "png" / name))
        Image.open(OUT / "png" / "favicon-180.png").convert("RGBA").save(
            OUT / "png" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        print(f"wrote PNG/ICO exports to {OUT / 'png'}")


if __name__ == "__main__":
    main()
