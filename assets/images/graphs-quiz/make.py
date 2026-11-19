"""Картинки для квиза по графам (posts/draft/graphs-quiz.md): SVG + PNG через headless Chrome.
Запуск: python3 assets/images/graphs-quiz/make.py
"""
import math, pathlib, subprocess

W, H, R = 1200, 675, 42
BG, INK, FILL = "#FAF7F2", "#2B2D42", "#FFFFFF"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = pathlib.Path(__file__).parent

GRAPHS = {
    # q1: список, нарисованный зигзагом
    "q1": dict(directed=True,
               nodes={3: (150, 190), 7: (380, 480), 1: (610, 190), 9: (840, 480), 4: (1060, 190)},
               edges=[(3, 7), (7, 1), (1, 9), (9, 4)]),
    # q2: дерево, нарисованное не сверху вниз
    "q2": dict(directed=False,
               nodes={1: (560, 330), 2: (330, 160), 3: (330, 500), 4: (800, 330),
                      5: (1010, 160), 6: (1010, 500), 7: (120, 420)},
               edges=[(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (3, 7)]),
    # q3: список с циклом, хвост смотрит назад на 3
    "q3": dict(directed=True,
               nodes={1: (140, 340), 2: (340, 340), 3: (560, 340), 4: (770, 160),
                      5: (980, 340), 6: (770, 520)},
               edges=[(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)]),
    # q4: лес, дерево плюс одинокая вершина 6
    "q4": dict(directed=False,
               nodes={1: (230, 180), 2: (450, 330), 3: (280, 510), 4: (690, 220),
                      5: (920, 420), 6: (640, 520)},
               edges=[(1, 2), (2, 3), (2, 4), (4, 5)]),
    # q5: классическое дерево сверху вниз (хитрый вопрос)
    "q5": dict(directed=False,
               nodes={8: (600, 100), 3: (380, 250), 10: (820, 250), 1: (250, 410),
                      6: (510, 410), 14: (950, 410), 4: (420, 570), 7: (600, 570)},
               edges=[(8, 3), (8, 10), (3, 1), (3, 6), (10, 14), (6, 4), (6, 7)]),
}


def svg(g):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="100%" height="100%" fill="{BG}"/>',
         '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
         f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>']
    for u, v in g["edges"]:
        (x1, y1), (x2, y2) = g["nodes"][u], g["nodes"][v]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        end = R + (6 if g["directed"] else 0)
        sx, sy, ex, ey = x1 + ux * R, y1 + uy * R, x2 - ux * end, y2 - uy * end
        m = ' marker-end="url(#a)"' if g["directed"] else ""
        p.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                 f'stroke="{INK}" stroke-width="5" stroke-linecap="round"{m}/>')
    for n, (x, y) in g["nodes"].items():
        p.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{FILL}" stroke="{INK}" stroke-width="5"/>')
        p.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
                 f'font-family="Helvetica, Arial, sans-serif" font-size="36" font-weight="700" fill="{INK}">{n}</text>')
    p.append("</svg>")
    return "\n".join(p)


for name, g in GRAPHS.items():
    s = OUT / f"{name}.svg"
    s.write_text(svg(g))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={W},{H}", f"--screenshot={OUT / (name + '.png')}", s.as_uri()],
                   check=True, capture_output=True)
    print("ok", name)
