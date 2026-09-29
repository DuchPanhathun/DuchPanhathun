#!/usr/bin/env python3
"""Add custom key/value lines to a gh-ascii card (https://gh.crafter.run).

gh-ascii builds the card's text from GitHub profile fields and live stats only,
so this script post-processes the downloaded SVG: it inserts the lines listed
in card-lines.json right after the "Uptime" row, styled exactly like the
card's own rows, and re-centres the columns (growing the card if needed).

Usage: python3 scripts/customize_card.py card-lines.json dark_mode.svg light_mode.svg
"""
import json
import re
import sys
from html import escape

# Layout constants mirrored from gh-ascii lib/svg.ts
PAD = 28
LINE_HEIGHT = 20
ASCII_LINE_HEIGHT = 9.6
INFO_COLS = 58

PALETTES = {
    "dark": {"key": "#ffa657", "dots": "#484f58", "value": "#c9d1d9"},
    "light": {"key": "#953800", "dots": "#8c959f", "value": "#24292f"},
}

TEXT_RE = re.compile(r'<text x="([\d.]+)" y="([\d.]+)"([^>]*)>(.*?)</text>')


def fmt(n: float) -> str:
    return f"{round(n, 2):g}"


def kv_line(key: str, value: str, x: str, attrs: str, c: dict) -> str:
    max_val = INFO_COLS - len(key) - 8
    val = value if len(value) <= max_val else value[: max_val - 1] + "…"
    dots = max(2, INFO_COLS - len(key) - len(val) - 6)
    spans = (
        f'<tspan fill="{c["key"]}">{escape(f". {key}: ", quote=True)}</tspan>'
        f'<tspan fill="{c["dots"]}">{"." * dots}</tspan>'
        f'<tspan fill="{c["value"]}">{escape(" " + val, quote=True)}</tspan>'
    )
    return f'<text x="{x}" y="{{Y}}"{attrs}>{spans}</text>'


def customize(svg: str, lines: list[dict]) -> str:
    theme = "light" if 'fill="#ffffff"' in svg.split("<text", 1)[0] else "dark"
    c = PALETTES[theme]

    head_m = re.search(r'<svg [^>]*width="([\d.]+)" height="([\d.]+)"', svg)
    width, height = float(head_m.group(1)), float(head_m.group(2))

    ascii_els, info_els = [], []
    for m in TEXT_RE.finditer(svg):
        x, y, attrs, body = m.group(1), float(m.group(2)), m.group(3), m.group(4)
        target = ascii_els if 'font-size="8"' in attrs else info_els
        target.append({"x": x, "y": y, "attrs": attrs, "body": body})
    if not info_els:
        raise SystemExit("no info column found — has the gh-ascii format changed?")

    # Skip if this card was already customized (idempotent re-runs).
    first_key = lines[0]["key"] if lines else None
    if first_key and any(f". {first_key}: " in e["body"] for e in info_els):
        return svg

    # Rebuild the info column as rows, keeping blank rows as None.
    y0 = info_els[0]["y"]
    rows: list = []
    for e in info_els:
        idx = round((e["y"] - y0) / LINE_HEIGHT)
        while len(rows) < idx:
            rows.append(None)
        rows.append(e)
    info_x, info_attrs = info_els[0]["x"], info_els[0]["attrs"]

    insert_at = next(
        (i + 1 for i, r in enumerate(rows) if r and ". Uptime: " in r["body"]), 1
    )
    new_rows = [
        {"template": kv_line(l["key"], l["value"], info_x, info_attrs, c)}
        for l in lines
    ]
    rows[insert_at:insert_at] = new_rows

    # Original geometry → derive the ASCII column's height.
    content = height - 2 * PAD
    old_info_h = (round((info_els[-1]["y"] - y0) / LINE_HEIGHT) + 1) * LINE_HEIGHT
    if ascii_els:
        ys = [e["y"] for e in ascii_els]
        ascii_h = content if old_info_h < content - 0.01 else (max(ys) - min(ys) + ASCII_LINE_HEIGHT)
        old_ascii_top = PAD + (content - ascii_h) / 2
    else:
        ascii_h, old_ascii_top = 0, PAD

    info_h = len(rows) * LINE_HEIGHT
    new_content = max(ascii_h, info_h)
    new_height = PAD * 2 + new_content
    info_top = PAD + (new_content - info_h) / 2
    ascii_shift = (PAD + (new_content - ascii_h) / 2) - old_ascii_top

    out = []
    for e in ascii_els:
        out.append(f'<text x="{e["x"]}" y="{fmt(e["y"] + ascii_shift)}"{e["attrs"]}>{e["body"]}</text>')
    for i, r in enumerate(rows):
        if r is None:
            continue
        y = fmt(info_top + (i + 1) * LINE_HEIGHT - 5)
        if "template" in r:
            out.append(r["template"].replace("{Y}", y))
        else:
            out.append(f'<text x="{r["x"]}" y="{y}"{r["attrs"]}>{r["body"]}</text>')

    open_tag = svg[: svg.index(">", svg.index("<svg")) + 1]
    open_tag = re.sub(r'height="[\d.]+"', f'height="{fmt(new_height)}"', open_tag, count=1)
    open_tag = re.sub(
        r'viewBox="0 0 ([\d.]+) [\d.]+"', lambda m: f'viewBox="0 0 {m.group(1)} {fmt(new_height)}"', open_tag
    )
    rect = re.search(r"<rect [^>]*/>", svg).group(0)
    rect = re.sub(r'height="[\d.]+"', f'height="{fmt(new_height - 1)}"', rect, count=1)
    return open_tag + "\n  " + rect + "\n  " + "\n  ".join(out) + "\n</svg>\n"


def main() -> None:
    config_path, *svg_paths = sys.argv[1:]
    with open(config_path, encoding="utf-8") as f:
        lines = json.load(f)["lines"]
    for path in svg_paths:
        with open(path, encoding="utf-8") as f:
            svg = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(customize(svg, lines))
        print(f"customized {path}")


if __name__ == "__main__":
    main()
