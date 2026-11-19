"""Картинка «анатомия графа» для posts/draft/graph-anatomy.md: SVG + PNG через headless Chrome.
Три компоненты связности ({1,2,3}, {4,5}, {6}), направленные взвешенные ребра, петля у 3.
Запуск: python3 assets/images/graph-anatomy/make.py
"""
import math, pathlib, subprocess

W, H, R = 1200, 675, 42
BG, INK, FILL, ACC = "#FAF7F2", "#2B2D42", "#FFFFFF", "#C8553D"
FONT = "Helvetica, Arial, sans-serif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = pathlib.Path(__file__).parent

NODES = {1: (170, 430), 2: (390, 170), 3: (610, 430), 4: (840, 170), 5: (1060, 380), 6: (930, 570)}
# (откуда, куда, вес, изгиб): изгиб > 0 рисует дугу, нужен для пары встречных ребер 4 ⇄ 5
EDGES = [(1, 2, 4, 0), (2, 3, 3, 0), (1, 3, 9, 0), (4, 5, 5, 40), (5, 4, 8, 40)]
LOOP = (3, 2)  # петля у вершины 3 с весом 2


def weight(x, y, w):
    return (f'<rect x="{x - 24}" y="{y - 22}" width="48" height="44" rx="10" fill="{BG}" stroke="{ACC}" stroke-width="3"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" font-family="{FONT}" '
            f'font-size="30" font-weight="700" fill="{ACC}">{w}</text>')


def edge(u, v, w, bend):
    (x1, y1), (x2, y2) = NODES[u], NODES[v]
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    nx, ny = uy, -ux  # нормаль: дуга выгибается вправо по ходу ребра
    mx, my = (x1 + x2) / 2 + nx * bend * 2, (y1 + y2) / 2 + ny * bend * 2
    # точки на окружностях вершин в направлении контрольной точки
    def on_circle(cx, cy, tx, ty, extra=0):
        dd = math.hypot(tx - cx, ty - cy)
        return cx + (tx - cx) / dd * (R + extra), cy + (ty - cy) / dd * (R + extra)
    sx, sy = on_circle(x1, y1, mx, my)
    ex, ey = on_circle(x2, y2, mx, my, 6)
    path = f'<path d="M{sx:.1f},{sy:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{INK}" ' \
           f'stroke-width="5" stroke-linecap="round" marker-end="url(#a)"/>'
    # середина кривой Безье при t = 0.5
    lx, ly = 0.25 * sx + 0.5 * mx + 0.25 * ex, 0.25 * sy + 0.5 * my + 0.25 * ey
    if bend == 0:
        lx, ly = lx + nx * 32, ly + ny * 32
    return path, weight(lx, ly, w)


p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="100%" height="100%" fill="{BG}"/>',
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
     f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>']
labels = []
for e in EDGES:
    path, lab = edge(*e)
    p.append(path)
    labels.append(lab)

n, w = LOOP
x, y = NODES[n]
p.append(f'<path d="M{x - 20},{y + 37} C{x - 110},{y + 175} {x + 110},{y + 175} {x + 24},{y + 41}" fill="none" '
         f'stroke="{INK}" stroke-width="5" stroke-linecap="round" marker-end="url(#a)"/>')
labels.append(weight(x - 95, y + 115, w))

for k, (x, y) in NODES.items():
    p.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{FILL}" stroke="{INK}" stroke-width="5"/>')
    p.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" font-family="{FONT}" '
             f'font-size="36" font-weight="700" fill="{INK}">{k}</text>')
p += labels + ["</svg>"]

svg = OUT / "graph-anatomy.svg"
svg.write_text("\n".join(p))
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                f"--screenshot={OUT / 'graph-anatomy.png'}", svg.as_uri()], check=True, capture_output=True)
print("ok")
