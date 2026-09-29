#!/usr/bin/env python3
"""Customize a gh-ascii card (https://gh.crafter.run) after downloading it.

gh-ascii builds the card's text from GitHub profile fields and live stats only,
and its ASCII portrait varies between runs (its background removal succeeds on
some runs and falls back on others). This script post-processes the SVG:

  * inserts the lines from card-lines.json — right after "Uptime" by default,
    or at the end of a named section (e.g. "Contact") — styled like the
    card's own rows;
  * optionally swaps in a saved ASCII portrait (portraits/<theme>.txt) so the
    picture stays the same while the stats refresh;
  * re-lays out both columns, growing the card if needed.

Usage:
  python3 scripts/customize_card.py card-lines.json [--portraits DIR] dark_mode.svg light_mode.svg
"""
import json
import os
import re
import sys
from html import escape

# Layout constants mirrored from gh-ascii lib/svg.ts
PAD = 28
GAP = 32
LINE_HEIGHT = 20
CHAR_WIDTH = 16 * 0.6
ASCII_CHAR_WIDTH = 4.8
ASCII_LINE_HEIGHT = 9.6
INFO_COLS = 58

PALETTES = {
    "dark": {"key": "#ffa657", "dots": "#484f58", "value": "#c9d1d9"},
    "light": {"key": "#953800", "dots": "#8c959f", "value": "#24292f"},
}

TEXT_RE = re.compile(r'<text x="([\d.]+)" y="([\d.]+)"([^>]*)>(.*?)</text>')


def fmt(n: float) -> str:
    return f"{round(n, 2):g}"


def kv_body(key: str, value: str, c: dict) -> str:
    max_val = INFO_COLS - len(key) - 8
    val = value if len(value) <= max_val else value[: max_val - 1] + "…"
    dots = max(2, INFO_COLS - len(key) - len(val) - 6)
    return (
        f'<tspan fill="{c["key"]}">{escape(f". {key}: ", quote=True)}</tspan>'
        f'<tspan fill="{c["dots"]}">{"." * dots}</tspan>'
        f'<tspan fill="{c["value"]}">{escape(" " + val, quote=True)}</tspan>'
    )


def customize(svg: str, lines: list, portrait: list | None) -> str:
    theme = "light" if 'fill="#ffffff"' in svg.split("<text", 1)[0] else "dark"
    c = PALETTES[theme]

    head_m = re.search(r'<svg [^>]*width="([\d.]+)" height="([\d.]+)"', svg)
    width, height = float(head_m.group(1)), float(head_m.group(2))

    ascii_els, info_els = [], []
    for m in TEXT_RE.finditer(svg):
        x, y, attrs, body = m.group(1), float(m.group(2)), m.group(3), m.group(4)
        target = ascii_els if 'font-size="8"' in attrs else info_els
        target.append({"x": x, "y": y, "attrs": attrs, "body": body})
    if not info_els or not ascii_els:
        raise SystemExit("unexpected card layout — has the gh-ascii format changed?")

    # Skip if this card was already customized (idempotent re-runs).
    if lines and any(f'. {lines[0]["key"]}: ' in e["body"] for e in info_els):
        return svg

    # --- Info column: rebuild as rows (None = blank row), insert custom lines.
    y0 = info_els[0]["y"]
    rows: list = []
    for e in info_els:
        idx = round((e["y"] - y0) / LINE_HEIGHT)
        while len(rows) < idx:
            rows.append(None)
        rows.append(e["body"])

    def section_end(name: str):
        for i, r in enumerate(rows):
            if r and f"> {name} <" in r:
                j = i + 1
                while j < len(rows) and rows[j] is not None:
                    j += 1
                return j
        return None

    uptime_at = next((i + 1 for i, r in enumerate(rows) if r and ". Uptime: " in r), 1)
    rows[uptime_at:uptime_at] = [kv_body(l["key"], l["value"], c) for l in lines if not l.get("section")]
    for l in lines:
        if l.get("section"):
            at = section_end(l["section"])
            if at is not None:
                rows.insert(at, kv_body(l["key"], l["value"], c))

    # --- ASCII column: saved portrait, or the one gh-ascii produced.
    ascii_attrs = ascii_els[0]["attrs"]
    if portrait:
        ascii_rows = [escape(l, quote=True) if l.strip() else None for l in portrait]
    else:
        ay0 = ascii_els[0]["y"]
        ascii_rows = []
        for e in ascii_els:
            idx = round((e["y"] - ay0) / ASCII_LINE_HEIGHT)
            while len(ascii_rows) < idx:
                ascii_rows.append(None)
            ascii_rows.append(e["body"])
    ascii_cols = (
        max(len(l) for l in portrait)
        if portrait
        else round((float(info_els[0]["x"]) - PAD - GAP) / ASCII_CHAR_WIDTH)
    )

    # --- Layout (same formulas as gh-ascii's renderSvg).
    info_x = PAD + ascii_cols * ASCII_CHAR_WIDTH + GAP
    new_width = round(info_x + INFO_COLS * CHAR_WIDTH + PAD)
    ascii_h = len(ascii_rows) * ASCII_LINE_HEIGHT
    info_h = len(rows) * LINE_HEIGHT
    content = max(ascii_h, info_h)
    new_height = PAD * 2 + content
    ascii_top = PAD + (content - ascii_h) / 2
    info_top = PAD + (content - info_h) / 2
    info_attrs = info_els[0]["attrs"]

    out = []
    for i, body in enumerate(ascii_rows):
        if body:
            y = fmt(ascii_top + (i + 1) * ASCII_LINE_HEIGHT - 3)
            out.append(f'<text x="{PAD}" y="{y}"{ascii_attrs}>{body}</text>')
    for i, body in enumerate(rows):
        if body:
            y = fmt(info_top + (i + 1) * LINE_HEIGHT - 5)
            out.append(f'<text x="{fmt(info_x)}" y="{y}"{info_attrs}>{body}</text>')

    open_tag = svg[: svg.index(">", svg.index("<svg")) + 1]
    open_tag = re.sub(r'width="[\d.]+"', f'width="{new_width}"', open_tag, count=1)
    open_tag = re.sub(r'height="[\d.]+"', f'height="{fmt(new_height)}"', open_tag, count=1)
    open_tag = re.sub(r'viewBox="[^"]*"', f'viewBox="0 0 {new_width} {fmt(new_height)}"', open_tag)
    rect = re.search(r"<rect [^>]*/>", svg).group(0)
    rect = re.sub(r'width="[\d.]+"', f'width="{new_width - 1}"', rect, count=1)
    rect = re.sub(r'height="[\d.]+"', f'height="{fmt(new_height - 1)}"', rect, count=1)
    return open_tag + "\n  " + rect + "\n  " + "\n  ".join(out) + "\n</svg>\n"


def main() -> None:
    args = sys.argv[1:]
    portraits_dir = None
    if "--portraits" in args:
        i = args.index("--portraits")
        portraits_dir = args[i + 1]
        del args[i : i + 2]
    config_path, *svg_paths = args
    with open(config_path, encoding="utf-8") as f:
        lines = json.load(f)["lines"]
    for path in svg_paths:
        with open(path, encoding="utf-8") as f:
            svg = f.read()
        theme = "light" if 'fill="#ffffff"' in svg.split("<text", 1)[0] else "dark"
        portrait = None
        if portraits_dir:
            p = os.path.join(portraits_dir, f"{theme}.txt")
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    portrait = f.read().rstrip("\n").split("\n")
        with open(path, "w", encoding="utf-8") as f:
            f.write(customize(svg, lines, portrait))
        print(f"customized {path}" + (f" (portrait: {theme}.txt)" if portrait else ""))


if __name__ == "__main__":
    main()
