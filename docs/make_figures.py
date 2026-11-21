"""Regenerate the SVG figures used in the README.

Run: python3 docs/make_figures.py
Writes docs/images/*.svg. Numbers come from the test results in README.md.
"""
import math
import pathlib

OUT = pathlib.Path(__file__).parent / "images"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# Light/dark tokens. GitHub shows README SVGs as images, and an SVG's own
# prefers-color-scheme media query follows the viewer's theme.
STYLE = f"""
<style>
  svg {{ font-family: {FONT}; }}
  .bg {{ fill: #fcfcfb; }}
  .t1 {{ fill: #0b0b0b; }}
  .t2 {{ fill: #52514e; }}
  .t3 {{ fill: #7a7974; }}
  .grid {{ stroke: #e4e3df; }}
  .axis {{ stroke: #b9b8b2; }}
  .muted {{ fill: #c3c2bd; }}
  .hl {{ fill: #2a78d6; }}
  .gen {{ fill: #eaf2fc; stroke: #2a78d6; }}
  .cut {{ fill: #fdf0ea; stroke: #eb6834; }}
  .badge-gen {{ fill: #2a78d6; }}
  .badge-cut {{ fill: #eb6834; }}
  .badge-tx {{ fill: #ffffff; }}
  .arrow {{ stroke: #7a7974; fill: none; }}
  .arrowhead {{ fill: #7a7974; }}
  .loop {{ stroke: #2a78d6; fill: none; }}
  .loophead {{ fill: #2a78d6; }}
  .wall {{ fill: #a8a7a1; }}
  .zone {{ fill: #a8a7a1; fill-opacity: 0.12; stroke: #7a7974; }}
  .inside {{ fill: #e34948; }}
  .edge {{ fill: #eda100; }}
  .out {{ fill: #1baf7a; }}
  .ring {{ stroke: #fcfcfb; }}
  @media (prefers-color-scheme: dark) {{
    .bg {{ fill: #1a1a19; }}
    .t1 {{ fill: #f0efec; }}
    .t2 {{ fill: #c3c2b7; }}
    .t3 {{ fill: #9a998f; }}
    .grid {{ stroke: #33332f; }}
    .axis {{ stroke: #55544e; }}
    .muted {{ fill: #55544e; }}
    .hl {{ fill: #3987e5; }}
    .gen {{ fill: #1b2a3d; stroke: #3987e5; }}
    .cut {{ fill: #3a241b; stroke: #d95926; }}
    .badge-gen {{ fill: #3987e5; }}
    .badge-cut {{ fill: #d95926; }}
    .arrow {{ stroke: #9a998f; }}
    .arrowhead {{ fill: #9a998f; }}
    .loop {{ stroke: #3987e5; }}
    .loophead {{ fill: #3987e5; }}
    .wall {{ fill: #77766f; }}
    .zone {{ fill: #77766f; fill-opacity: 0.18; stroke: #9a998f; }}
    .inside {{ fill: #e66767; }}
    .edge {{ fill: #c98500; }}
    .out {{ fill: #199e70; }}
    .ring {{ stroke: #1a1a19; }}
  }}
</style>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>{STYLE}"
        f'<rect class="bg" x="0" y="0" width="{w}" height="{h}" rx="12"/>\n'
        + body
        + "</svg>\n"
    )


def text(x, y, s, cls="t1", size=13, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>\n'
    )


def arrow(x1, y1, x2, y2, cls="arrow", head="arrowhead"):
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    p1 = (x2, y2)
    p2 = (ex - 5 * math.sin(ang), ey + 5 * math.cos(ang))
    p3 = (ex + 5 * math.sin(ang), ey - 5 * math.cos(ang))
    return (
        f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{ex:.1f}" y2="{ey:.1f}" stroke-width="2"/>\n'
        f'<polygon class="{head}" points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}"/>\n'
    )


# ---------------------------------------------------------------- pipeline
def pipeline():
    W, H = 900, 400
    bw, bh, gap, mx = 190, 96, 30, 25
    y1, y2 = 70, 250
    steps = [
        ("Pin the brief", ["Who it's for, budget, time.", "Sets the payoff test."]),
        ("Write the cliché wall", ["The ideas any AI would", "give. All banned."]),
        ("Draw a map", ["Two axes for the brief.", "Spread ideas across cells."]),
        ("Generate", ["Forcing techniques. Cut", "likely ones, make bolder."]),
        ("Vector check", ["Embed every idea. Drop", "the ones in the crowd."]),
        ("Skeptical judge", ["Blind review: originality,", "reality, payoff, red team."]),
        ("Shortlist", ["Feasibility 4+, Payoff 3+.", "One last wall check."]),
        ("Show the work", ["Finalists, first steps,", "and what got dropped."]),
    ]
    # Snake layout: row 1 left to right, row 2 right to left.
    pos = []
    for i in range(4):
        pos.append((mx + i * (bw + gap), y1))
    for i in range(4):
        pos.append((mx + (3 - i) * (bw + gap), y2))

    b = ""
    b += text(mx, 44, "1. Push past the obvious", "t2", 14, 600)
    b += text(mx, y2 + bh + 38, "2. Check originality and feasibility", "t2", 14, 600)

    for i, ((x, y), (title, lines)) in enumerate(zip(pos, steps)):
        kind = "gen" if i < 4 else "cut"
        b += f'<rect class="{kind}" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" stroke-width="1.5"/>\n'
        b += f'<circle class="badge-{kind}" cx="{x + 22}" cy="{y + 24}" r="12"/>\n'
        b += text(x + 22, y + 29, str(i + 1), "badge-tx", 13, 700, "middle")
        b += text(x + 42, y + 29, title, "t1", 14, 600)
        for j, ln in enumerate(lines):
            b += text(x + 16, y + 58 + j * 18, ln, "t2", 12.5)

    # arrows along row 1
    for i in range(3):
        x = pos[i][0] + bw
        b += arrow(x + 3, y1 + bh / 2, x + gap - 3, y1 + bh / 2)
    # arrows along row 2 (right to left)
    for i in range(4, 7):
        x = pos[i][0]
        b += arrow(x - 3, y2 + bh / 2, x - gap + 3, y2 + bh / 2)
    # 4 -> 5 down, and the loop 5 -> 4 up
    cx = pos[3][0] + bw / 2
    b += arrow(cx - 40, y1 + bh + 4, cx - 40, y2 - 4)
    b += arrow(cx + 40, y2 - 4, cx + 40, y1 + bh + 4, "loop", "loophead")
    b += text(cx - 52, y1 + bh + 34, "Too close to the wall?", "loophead", 11.5, 600, "end")
    b += text(cx - 52, y1 + bh + 50, "Write more toward open space.", "loophead", 11.5, 600, "end")
    return svg(W, H, b, "How the idea-generation skill works: eight steps in two phases")


# ---------------------------------------------------------------- vector check
def vector_check():
    W, H = 900, 400
    cx, cy, r = 250, 215, 118
    b = ""
    b += text(30, 40, "The vector check, drawn in two dimensions", "t1", 16, 600)
    b += text(30, 62, "Illustration. The real check compares 384-number embeddings with cosine similarity.", "t3", 12.5)

    # crowded zone and wall ideas (hand placed so labels don't collide)
    b += f'<circle class="zone" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.5" stroke-dasharray="5 4"/>\n'
    named = [(170, 150, "bake sale"), (280, 140, "car wash"), (160, 210, "raffle"),
             (290, 230, "t-shirts"), (180, 270, "GoFundMe"), (270, 290, "trivia night")]
    plain = [(225, 175), (235, 228), (205, 240), (320, 175), (255, 262), (140, 180),
             (330, 262), (200, 300), (240, 148), (195, 120), (300, 310)]
    for x, y, name in named:
        b += f'<circle class="wall ring" cx="{x}" cy="{y}" r="5" stroke-width="2"/>\n'
        b += text(x + 9, y + 4, name, "t3", 11)
    for x, y in plain:
        b += f'<circle class="wall ring" cx="{x}" cy="{y}" r="5" stroke-width="2"/>\n'
    b += text(cx, cy + r + 27, "Obvious ideas (the cliché wall)", "t2", 12.5, 600, "middle")

    # candidates
    cands = [((245, 200), "inside", "INSIDE"), ((cx + r + 12, 245), "edge", "EDGE"),
             ((470, 150), "out", "OUT"), ((515, 290), "out", "OUT")]
    for (x, y), cls, lab in cands:
        b += f'<circle class="{cls} ring" cx="{x}" cy="{y}" r="8" stroke-width="2"/>\n'
        b += text(x + 13, y + 4, lab, "t1", 11.5, 700)
    # "write toward open space" arrow
    b += arrow(500, 245, 545, 195, "loop", "loophead")
    b += text(425, 340, "Farthest from the wall and each", "t2", 11.5)
    b += text(425, 355, "other: write a few more here.", "t2", 11.5)

    # legend / rules
    lx = 620
    rows = [
        ("inside", "INSIDE", ["As close to an obvious idea as", "obvious ideas sit to each other.", "Dropped or reworked."]),
        ("edge", "EDGE", ["Close to the zone but outside.", "Kept."]),
        ("out", "OUT", ["Clear of the crowd."]),
    ]
    y = 110
    for cls, lab, lines in rows:
        b += f'<circle class="{cls}" cx="{lx + 8}" cy="{y - 4}" r="7"/>\n'
        b += text(lx + 24, y, lab, "t1", 13, 700)
        for j, ln in enumerate(lines):
            b += text(lx + 24, y + 19 + j * 17, ln, "t2", 12.5)
        y += 34 + 17 * len(lines)
    b += text(lx, y + 4, "Zone radius = the median distance from", "t3", 12)
    b += text(lx, y + 21, "each obvious idea to its nearest neighbour,", "t3", 12)
    b += text(lx, y + 38, "so it adapts to every brief.", "t3", 12)
    return svg(W, H, b, "Diagram of the vector check: obvious ideas form a crowded zone; candidates are marked INSIDE, EDGE or OUT")


# ---------------------------------------------------------------- bar panels
def panels(title, subtitle, cats, metrics, hl_index, fname_title):
    """Small multiples: one panel per metric, one bar per version, own axis each."""
    n = len(metrics)
    W = 900
    pw = (W - 60 - (n - 1) * 30) / n
    top, ph = 120, 190
    H = top + ph + 60
    b = text(30, 40, title, "t1", 16, 600)
    b += text(30, 62, subtitle, "t3", 12.5)
    for k, (mtitle, note, vals, vmax, fmt) in enumerate(metrics):
        x0 = 30 + k * (pw + 30)
        b += text(x0, top - 30, mtitle, "t1", 13.5, 600)
        b += text(x0, top - 12, note, "t3", 11.5)
        base = top + ph
        b += f'<line class="axis" x1="{x0}" y1="{base}" x2="{x0 + pw}" y2="{base}" stroke-width="1"/>\n'
        nb = len(cats)
        slot = pw / nb
        bwid = min(44, slot * 0.6)
        for i, (c, v) in enumerate(zip(cats, vals)):
            bx = x0 + i * slot + (slot - bwid) / 2
            h = ph * v / vmax
            cls = "hl" if i == hl_index else "muted"
            rr = min(4, h / 2)
            # bar with rounded top only
            b += (
                f'<path class="{cls}" d="M{bx:.1f},{base} V{base - h + rr:.1f} '
                f"Q{bx:.1f},{base - h:.1f} {bx + rr:.1f},{base - h:.1f} "
                f"H{bx + bwid - rr:.1f} Q{bx + bwid:.1f},{base - h:.1f} {bx + bwid:.1f},{base - h + rr:.1f} "
                f'V{base} Z"/>\n'
            )
            weight = 700 if i == hl_index else 500
            b += text(bx + bwid / 2, base - h - 7, fmt(v), "t1", 12.5, weight, "middle")
            for j, part in enumerate(c.split("\n")):
                b += text(bx + bwid / 2, base + 18 + j * 15, part, "t2" if i != hl_index else "t1", 11.5,
                          600 if i == hl_index else 400, "middle")
    return svg(W, H, b, fname_title)


def results():
    cats = ["No\nskill", "v1", "v2", "This\nversion"]
    metrics = [
        ("Picks on the obvious list", "lower is better",
         [23 / 30 * 100, 9 / 30 * 100, 2 / 30 * 100, 3 / 28 * 100], 100, lambda v: f"{v:.0f}%"),
        ("Same idea in both runs", "lower is better", [9, 6, 2, 6], 10, lambda v: f"{v:.0f}"),
        ("Workability", "1 to 5, higher is better", [3.7, 3.1, 3.1, 3.3], 5, lambda v: f"{v:.1f}"),
    ]
    return panels(
        "Skill versions on three everyday briefs",
        "Two runs per brief per version, judged blind. Each panel has its own scale.",
        cats, metrics, 3, "Bar charts comparing no skill, v1, v2 and this version on obvious picks, repeats and workability",
    )


def vector_results():
    cats = ["Before", "First\ntry", "Shipped"]
    metrics = [
        ("Same idea in 2+ runs", "lower is better", [6, 3, 3], 8, lambda v: f"{v:.0f}"),
        ("Novelty", "1 to 5", [3.69, 3.97, 3.81], 5, lambda v: f"{v:.2f}"),
        ("Workability", "1 to 5", [3.23, 3.23, 3.32], 5, lambda v: f"{v:.2f}"),
        ("Rated 4+ on both", "count of final ideas", [4, 6, 7], 8, lambda v: f"{v:.0f}"),
    ]
    return panels(
        "Adding the vector check",
        "Three briefs, three runs each, 111 final ideas rated together by one blind judge.",
        cats, metrics, 2, "Bar charts comparing the skill before the vector check, a first try, and the shipped version",
    )


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pipeline.svg").write_text(pipeline())
    (OUT / "vector-check.svg").write_text(vector_check())
    (OUT / "test-results.svg").write_text(results())
    (OUT / "vector-test-results.svg").write_text(vector_results())
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
