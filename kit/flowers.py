"""Cut flowers and flower-workshop props, drawn botanically right in the storybook style.

Flowers (heads are drawn centred on (x, y); plants grow up from a ground point):
  zinnia_head   layered rows of rounded ray petals around a small dark cone ringed with tiny yellow florets
  cosmos_head   eight broad petals with notched tips around a yellow disc (foliage is fine and feathery)
  dahlia_head   many rings of pointed, cupped petals (decorative type)
  snapdragon    a tall spike of two-lipped florets, opening from the bottom up, green buds at the tip
  sweet_pea     a ruffled "standard" petal behind two wing petals, on a climbing vine with tendrils
  sunflower_head, branching_sunflower   gold rays around a brown disc; the branching kind carries several small heads
Stems and leaves: zinnia leaves are opposite, narrow and stalkless; cosmos leaves are thread-like.

Props: mason_jar (with an arrangement built in layers: greens, stars, fillers, dancers), vase, flower_bucket,
snips, name_card, care_card, wrapped_jar, workshop_table (guest stations), flower_row (a field row),
sweet_pea_trellis, open_barn (a barn workshop with the doors open and a table inside)."""
import math
import cairo
from gfx import *

# ------------------------------------------------------------------ palette
MAGENTA, ORANGE, CORAL = hx("d6336c"), hx("f07b21"), hx("ff7a5c")
SCARLET, LEMON, PINK = hx("e2452f"), hx("f6c431"), hx("f48fb1")
WINE, PEACH, LILAC = hx("8e1b3a"), hx("f6a87a"), hx("b39ddb")
BLUSH, WHITE_P = hx("f8c8d8"), hx("fbf6ee")
STEM, STEM_D = hx("4e8f3a"), hx("2f6b2a")
SAGE, MINT = hx("8fb38a"), hx("5fa25a")
DISC_BROWN, DISC_RED = hx("6b3f1f"), hx("7a2a2a")
TIN = hx("aeb8c8")
GLASS = hx("cfe8f2")
KRAFT = hx("d9b07a")

ZINNIA_COLS = [MAGENTA, ORANGE, CORAL, SCARLET, LEMON, PINK]
COSMOS_COLS = [PINK, MAGENTA, WHITE_P, BLUSH]
DAHLIA_COLS = [WINE, PEACH, LILAC, CORAL]
SNAP_COLS = [PINK, LEMON, WHITE_P, SCARLET]
PEA_COLS = [LILAC, BLUSH, hx("9575cd"), WHITE_P, hx("e57399")]


def _petal(c, length, width, tip="round"):
    """A petal path pointing up (-y) from the origin."""
    if tip == "round":
        c.move_to(0, 0)
        c.curve_to(width * 0.9, -length * 0.25, width * 0.8, -length, 0, -length)
        c.curve_to(-width * 0.8, -length, -width * 0.9, -length * 0.25, 0, 0)
    elif tip == "notch":  # cosmos: broad wedge with a toothed tip
        c.move_to(0, 0)
        c.curve_to(width * 0.5, -length * 0.3, width, -length * 0.7, width * 0.9, -length * 0.95)
        c.line_to(width * 0.45, -length * 0.88)
        c.line_to(0, -length)
        c.line_to(-width * 0.45, -length * 0.88)
        c.line_to(-width * 0.9, -length * 0.95)
        c.curve_to(-width, -length * 0.7, -width * 0.5, -length * 0.3, 0, 0)
    else:  # point (dahlia)
        c.move_to(0, 0)
        c.curve_to(width, -length * 0.35, width * 0.5, -length * 0.85, 0, -length)
        c.curve_to(-width * 0.5, -length * 0.85, -width, -length * 0.35, 0, 0)
    c.close_path()


def _ring(c, n, r0, length, width, col, rot=0.0, tip="round", lw=3, squash=1.0, shading=0.12):
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        c.save()
        c.scale(1, squash)
        c.rotate(a)
        c.translate(0, -r0)
        fill_ink(c, lambda: _petal(c, length, width, tip), col, lw, shading=shading)
        c.restore()


def zinnia_head(c, x, y, r=40, col=MAGENTA, t=0.0, seed=0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt + math.sin(t * 1.3 + seed) * 0.04)
    sq = 0.92
    _ring(c, 14, r * 0.25, r * 0.78, r * 0.2, shade(col, 0.08), 0.0, lw=max(2, r * 0.06), squash=sq)
    _ring(c, 12, r * 0.2, r * 0.58, r * 0.19, col, 0.26, lw=max(2, r * 0.055), squash=sq)
    _ring(c, 9, r * 0.15, r * 0.4, r * 0.17, tint(col, 0.12), 0.1, lw=max(1.5, r * 0.05), squash=sq)
    circle(c, 0, 0, r * 0.2, DISC_RED, max(2, r * 0.05), shading=0.2)
    for i in range(7):  # the tiny yellow star florets ringing the cone
        a = i * 2 * math.pi / 7 + seed
        circle(c, math.cos(a) * r * 0.15, math.sin(a) * r * 0.15, r * 0.045, LEMON, 0, shading=0)
    c.restore()


def cosmos_head(c, x, y, r=40, col=PINK, t=0.0, seed=0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt + math.sin(t * 1.6 + seed) * 0.06)
    _ring(c, 8, r * 0.12, r * 0.88, r * 0.3, col, seed * 0.3, tip="notch", lw=max(2, r * 0.055), squash=0.95)
    for i in range(8):  # faint darker veins at the petal base, as on real cosmos
        a = seed * 0.3 + i * 2 * math.pi / 8
        stroke(c, lambda: (c.move_to(math.sin(a) * r * 0.2, -math.cos(a) * r * 0.2),
                           c.line_to(math.sin(a) * r * 0.45, -math.cos(a) * r * 0.45)), shade(col, 0.2), max(1, r * 0.03))
    circle(c, 0, 0, r * 0.2, LEMON, max(2, r * 0.05), shading=0.25)
    c.restore()


def dahlia_head(c, x, y, r=50, col=WINE, t=0.0, seed=0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt + math.sin(t * 1.1 + seed) * 0.03)
    rings = [(16, 0.2, 0.82, 0.17, shade(col, 0.1)), (14, 0.15, 0.66, 0.17, col), (12, 0.12, 0.5, 0.16, tint(col, 0.1)),
             (10, 0.08, 0.36, 0.14, tint(col, 0.2)), (8, 0.04, 0.22, 0.12, tint(col, 0.3))]
    for k, (n, r0, L, wd, cl) in enumerate(rings):
        _ring(c, n, r * r0, r * L, r * wd, cl, k * 0.21, tip="point", lw=max(1.5, r * 0.045), squash=0.94)
    circle(c, 0, 0, r * 0.07, shade(col, 0.25), 0, shading=0)
    c.restore()


def sunflower_head(c, x, y, r=40, t=0.0, seed=0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt + math.sin(t + seed) * 0.05)
    _ring(c, 16, r * 0.42, r * 0.6, r * 0.17, GOLD, 0.0, lw=max(2, r * 0.05))
    circle(c, 0, 0, r * 0.48, DISC_BROWN, max(2, r * 0.06), shading=0.25)
    rr = rng_for("sun", seed)
    for i in range(10):
        a, d = rr.uniform(0, 6.28), rr.uniform(0, r * 0.38)
        circle(c, math.cos(a) * d, math.sin(a) * d, r * 0.04, shade(DISC_BROWN, 0.3), 0, shading=0)
    c.restore()


def snapdragon(c, x, y, h=220, col=PINK, t=0.0, seed=0, lean=0.0, s=1.0):
    """A whole spike from its cut end / ground point (x, y), height h."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.4 + seed) * 4 + lean
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -h * 0.4, sw * 0.5, -h * 0.8, sw, -h)), INK, 9)
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -h * 0.4, sw * 0.5, -h * 0.8, sw, -h)), STEM, 5)
    n = 9
    for i in range(n):
        f = i / (n - 1)
        yy = -h * (0.42 + 0.58 * f)
        xx = sw * (yy / -h)
        side = -1 if i % 2 else 1
        size = lerp(17, 7, f)
        if f > 0.75:  # green-tipped buds at the top
            oval(c, xx + side * 5, yy, size * 0.55, size * 0.8, mix(col, STEM, 0.55), 3, shading=0.1)
            continue
        # two-lipped floret: upper lip (two lobes) and a rounder lower lip, facing outward
        cx_ = xx + side * size * 0.75
        oval(c, cx_, yy - size * 0.35, size * 0.8, size * 0.55, tint(col, 0.1), 3, shading=0.1)
        oval(c, cx_ + side * size * 0.2, yy + size * 0.35, size * 0.75, size * 0.55, col, 3, shading=0.12)
        circle(c, cx_ + side * size * 0.45, yy + size * 0.05, size * 0.18, LEMON, 0, shading=0)
    c.restore()


def sweet_pea(c, x, y, r=26, col=LILAC, rot=0.0):
    """One sweet pea flower: a big ruffled standard petal behind two wings and a small keel."""
    c.save(); c.translate(x, y); c.rotate(rot)
    pts = []
    for i in range(13):  # ruffled fan edge
        a = math.pi + i * math.pi / 12
        rr = r * (1.0 + 0.08 * math.sin(i * 2.7))
        pts.append((math.cos(a) * rr, math.sin(a) * rr * 0.92))
    fill_ink(c, lambda: (smooth(c, [(0, r * 0.25)] + pts, True)), col, max(2, r * 0.1), shading=0.12)
    oval(c, -r * 0.35, r * 0.15, r * 0.4, r * 0.32, tint(col, 0.15), max(2, r * 0.09), shading=0.1)
    oval(c, r * 0.35, r * 0.15, r * 0.4, r * 0.32, tint(col, 0.15), max(2, r * 0.09), shading=0.1)
    oval(c, 0, r * 0.38, r * 0.16, r * 0.22, tint(col, 0.35), max(1.5, r * 0.07), shading=0)
    c.restore()


def tendril(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(14, -10, 22, -24, 14, -32), c.curve_to(8, -36, 4, -30, 9, -27)), STEM_D, 3)
    c.restore()


def _leaf(c, x, y, L, w, ang, col=STEM, lw=3):
    c.save(); c.translate(x, y); c.rotate(ang)
    fill_ink(c, lambda: (c.move_to(0, 0), c.curve_to(w, -L * 0.3, w * 0.6, -L * 0.85, 0, -L),
                         c.curve_to(-w * 0.6, -L * 0.85, -w, -L * 0.3, 0, 0), c.close_path()), col, lw, shading=0.12)
    stroke(c, lambda: (c.move_to(0, -2), c.line_to(0, -L * 0.85)), shade(col, 0.25), 1.5)
    c.restore()


def stem_line(c, x0, y0, x1, y1, w=6, bend=0.0):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    stroke(c, lambda: (c.move_to(x0, y0), c.curve_to(mx, my, mx, my, x1, y1)), INK, w + 4)
    stroke(c, lambda: (c.move_to(x0, y0), c.curve_to(mx, my, mx, my, x1, y1)), STEM, w)


def zinnia_plant(c, x, y, h=200, col=MAGENTA, t=0.0, seed=0, s=1.0, r=34):
    """Zinnia stem from the ground with opposite, narrow, stalkless leaves."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.2 + seed) * 5
    stem_line(c, 0, 0, sw, -h, 6, sw * 0.3)
    for k in range(3):
        yy = -h * (0.18 + k * 0.22)
        xx = sw * (yy / -h)
        _leaf(c, xx, yy, 46 - k * 6, 12, 1.05, STEM)
        _leaf(c, xx, yy, 46 - k * 6, 12, -1.05, STEM)
    zinnia_head(c, sw, -h, r, col, t, seed)
    c.restore()


def cosmos_plant(c, x, y, h=230, col=PINK, t=0.0, seed=0, s=1.0, r=34):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.5 + seed) * 7
    stem_line(c, 0, 0, sw, -h, 5, sw * 0.4)
    for k in range(4):  # feathery, thread-like foliage
        yy = -h * (0.12 + 0.17 * k)
        xx = sw * (yy / -h)
        for side in (-1, 1):
            for j in range(4):
                a = side * (0.6 + j * 0.25)
                stroke(c, lambda: (c.move_to(xx, yy), c.line_to(xx + math.sin(a) * 34, yy - math.cos(a) * 34 + 10)), STEM_D, 2.5)
    cosmos_head(c, sw, -h, r, col, t, seed)
    c.restore()


def dahlia_plant(c, x, y, h=210, col=WINE, t=0.0, seed=0, s=1.0, r=44):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.0 + seed) * 4
    stem_line(c, 0, 0, sw, -h, 8, sw * 0.3)
    for k, side in ((0, 1), (1, -1), (2, 1)):  # broad, toothed-looking compound leaves near the base
        yy = -h * (0.15 + 0.2 * k)
        _leaf(c, sw * (yy / -h), yy, 60, 24, side * 1.0, STEM_D)
    dahlia_head(c, sw, -h, r, col, t, seed)
    c.restore()


def branching_sunflower(c, x, y, h=260, t=0.0, seed=0, s=1.0):
    """Branching type: one main stem carrying several smaller heads on side shoots."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.0 + seed) * 4
    stem_line(c, 0, 0, sw, -h, 9, sw * 0.3)
    for k, (side, fy, L) in enumerate(((1, 0.55, 80), (-1, 0.7, 70), (1, 0.82, 55))):
        bx, by = sw * fy, -h * fy
        ex, ey = bx + side * L, by - L * 0.7
        stem_line(c, bx, by, ex, ey, 5, 0)
        sunflower_head(c, ex, ey, 26, t, seed + k)
    for k, side in ((0, -1), (1, 1)):
        yy = -h * (0.22 + 0.18 * k)
        _leaf(c, sw * 0.2, yy, 64, 30, side * 1.1, STEM)
    sunflower_head(c, sw, -h, 36, t, seed + 9)
    c.restore()


def sweet_pea_trellis(c, x, y, w=420, h=420, t=0.0, grow=1.0, seed=0):
    """A simple twine trellis between two posts with sweet pea vines climbing it. grow 0..1."""
    box(c, x - 10, y - h - 20, 20, h + 20, 4, WOOD, 4)
    box(c, x + w - 10, y - h - 20, 20, h + 20, 4, WOOD, 4)
    for i in range(7):
        gx = x + 10 + i * (w - 20) / 6
        stroke(c, lambda: (c.move_to(gx, y), c.line_to(gx, y - h)), hx("d9c49a"), 2)
    for j in range(5):
        gy = y - 20 - j * (h - 40) / 4
        stroke(c, lambda: (c.move_to(x, gy), c.line_to(x + w, gy)), hx("d9c49a"), 2)
    r = rng_for("pea", seed)
    vines = 6
    for v in range(vines):
        vx = x + 30 + v * (w - 60) / (vines - 1)
        top = y - h * 0.95 * grow
        if grow <= 0.02:
            continue
        pts = [(vx + math.sin(k * 0.9 + v) * 14, y - k * (y - top) / 8) for k in range(9)]
        stroke(c, lambda: smooth(c, pts, False), STEM_D, 5)
        for k in range(1, 9):
            px, py = pts[k]
            if k % 2 == 0:
                _leaf(c, px, py, 26, 11, 1.2 if k % 4 else -1.2, MINT, 2)
            else:
                tendril(c, px, py, 0.8, 0.4 if v % 2 else -0.4)
        nflow = int(4 * grow)
        for k in range(nflow):
            px, py = pts[min(8, 3 + k * 2) if 3 + k * 2 <= 8 else 8]
            sweet_pea(c, px + r.uniform(-14, 14), py + r.uniform(-10, 10), r.uniform(15, 21),
                      PEA_COLS[(v + k) % len(PEA_COLS)], r.uniform(-0.4, 0.4))


def greens_sprig(c, x, y, L=120, ang=0.0, col=MINT, kind="leafy"):
    c.save(); c.translate(x, y); c.rotate(ang)
    stroke(c, lambda: (c.move_to(0, 0), c.line_to(0, -L)), STEM_D, 4)
    if kind == "grass":
        oval(c, 0, -L - 14, 7, 22, hx("d8c27a"), 3, shading=0.1)
    else:
        for k in range(4):
            yy = -L * (0.35 + 0.18 * k)
            _leaf(c, 0, yy, 26 - k * 3, 12, 0.9, col, 2)
            _leaf(c, 0, yy, 26 - k * 3, 12, -0.9, col, 2)
    c.restore()


# ------------------------------------------------------------------ arrangements
def arrangement(c, x, y, s=1.0, t=0.0, layers=(1, 1, 1, 1), seed=0, palette=None):
    """A jar arrangement built in four layers, each 0..1: greens (frame), stars (three big blooms),
    fillers (around the stars), dancers (light, airy stems on top). (x, y) = the jar's mouth centre."""
    g, st, fi, da = layers
    c.save(); c.translate(x, y); c.scale(s, s)
    pal = palette or [WINE, ORANGE, MAGENTA]
    if da > 0:
        for k, (ang, L) in enumerate(((-0.45, 230), (0.4, 240), (-0.1, 270), (0.18, 255))):
            c.save(); c.translate(0, (1 - ease_out(da)) * 60)
            if k % 2 == 0:
                greens_sprig(c, 0, 0, L * ease_out(da), ang, kind="grass")
            else:
                cosmos_plant_stem = L * ease_out(da)
                stroke(c, lambda: (c.move_to(0, 0), c.line_to(math.sin(ang) * cosmos_plant_stem,
                                                               -math.cos(ang) * cosmos_plant_stem)), STEM_D, 3)
                cosmos_head(c, math.sin(ang) * cosmos_plant_stem, -math.cos(ang) * cosmos_plant_stem, 22, WHITE_P, t, k)
            c.restore()
    if g > 0:
        for k, ang in enumerate((-1.0, -0.65, -0.3, 0.05, 0.35, 0.7, 1.0)):
            greens_sprig(c, 0, 0, 150 * ease_out(g), ang, MINT if k % 2 else SAGE)
    if fi > 0:
        for k, (dx, dy) in enumerate(((-120, -80), (120, -90), (-60, -160), (70, -170), (0, -110))):
            p = ease_out(prog(fi, k * 0.12, 0.5))
            if p > 0:
                stroke(c, lambda: (c.move_to(0, 0), c.line_to(dx * p, dy * p)), STEM_D, 3)
                (zinnia_head if k % 2 else cosmos_head)(c, dx * p, dy * p, 26 * p + 1,
                                                       (ZINNIA_COLS if k % 2 else COSMOS_COLS)[(k + seed) % 4], t, k)
    if st > 0:
        for k, (dx, dy, fn) in enumerate(((-70, -130, dahlia_head), (75, -140, zinnia_head), (0, -200, dahlia_head))):
            p = ease_back(prog(st, k * 0.2, 0.5))
            if p > 0:
                stroke(c, lambda: (c.move_to(0, 0), c.line_to(dx, dy)), STEM, 4)
                fn(c, dx, dy, (46 if fn is dahlia_head else 42) * p + 1, pal[k % len(pal)], t, k)
    c.restore()


def mason_jar(c, x, y, s=1.0, t=0.0, layers=(0, 0, 0, 0), water=0.7, seed=0, palette=None):
    """Mason jar standing at (x, y) (its base). Height ~ 210*s."""
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 2, 90, 14, 0.18)
    w, h = 140, 200
    if any(layers):
        arrangement(c, 0, -h + 4, 1.0, t, layers, seed, palette)
    # stems seen through the glass
    if any(layers):
        for k in range(6):
            stroke(c, lambda: (c.move_to(-30 + k * 12, -h + 10), c.line_to(-20 + k * 8, -16)), STEM, 3, 0.6)
    body = lambda: rrect(c, -w / 2, -h, w, h, 26)
    body(); setc(c, GLASS, 0.35); c.fill()
    c.save(); body(); c.clip()
    setc(c, hx("a6d4e8"), 0.35); c.rectangle(-w / 2, -h * water, w, h * water); c.fill()
    c.restore()
    stroke(c, body, INK, 5, 0.9)
    stroke(c, lambda: (c.move_to(-w / 2 + 18, -h + 40), c.line_to(-w / 2 + 18, -30)), WHITE, 6, 0.6)
    for k in range(3):  # the threaded neck
        stroke(c, lambda: (c.move_to(-w / 2 + 12, -h + 8 + k * 9), c.line_to(w / 2 - 12, -h + 4 + k * 9)), INK, 2.5, 0.5)
    c.restore()


def vase(c, x, y, s=1.0, col=hx("4f7bd0"), t=0.0, layers=(0, 0, 0, 0), seed=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 2, 80, 12, 0.18)
    if any(layers):
        arrangement(c, 0, -230, 0.9, t, layers, seed)
    fill_ink(c, lambda: (c.move_to(-36, -230), c.curve_to(-30, -180, -100, -150, -80, -60), c.curve_to(-70, -10, -40, 0, 0, 0),
                         c.curve_to(40, 0, 70, -10, 80, -60), c.curve_to(100, -150, 30, -180, 36, -230), c.close_path()), col)
    oval(c, 0, -230, 38, 9, shade(col, 0.3), 4)
    c.restore()


def flower_bucket(c, x, y, s=1.0, t=0.0, kind="zinnia", n=9, seed=0, tag=None, col=TIN):
    """A tin flower bucket full of cut stems; (x, y) = base. Height ~ 110*s plus the flowers."""
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 2, 70, 12, 0.2)
    r = rng_for("bucket", seed)
    heads = []
    for i in range(n):
        ang = lerp(-0.55, 0.55, i / max(n - 1, 1)) + r.uniform(-0.08, 0.08)
        L = r.uniform(130, 175)
        hx_, hy_ = math.sin(ang) * L, -95 - math.cos(ang) * L
        stroke(c, lambda: (c.move_to(math.sin(ang) * 30, -90), c.line_to(hx_, hy_)), STEM_D, 4)
        if i % 3 == 0:
            _leaf(c, math.sin(ang) * 70, -150, 30, 9, ang + 1.0, STEM, 2)
        heads.append((hx_, hy_, i))
    for hx_, hy_, i in sorted(heads, key=lambda q: q[1]):
        if kind == "zinnia":
            zinnia_head(c, hx_, hy_, r.uniform(26, 32), ZINNIA_COLS[(i + seed) % len(ZINNIA_COLS)], t, i)
        elif kind == "mixed":
            fn = (zinnia_head, cosmos_head, dahlia_head)[i % 3]
            cl = (ZINNIA_COLS, COSMOS_COLS, DAHLIA_COLS)[i % 3][(i + seed) % 4]
            fn(c, hx_, hy_, r.uniform(24, 32), cl, t, i)
        elif kind == "sweetpea":
            sweet_pea(c, hx_, hy_, r.uniform(16, 20), PEA_COLS[i % len(PEA_COLS)], r.uniform(-0.3, 0.3))
    # the bucket itself (tapers towards the base, rolled rim, two side handles)
    fill_ink(c, lambda: poly(c, [(-62, -105), (62, -105), (48, 0), (-48, 0)]), col)
    stroke(c, lambda: (c.move_to(-58, -70), c.line_to(58, -70)), shade(col, 0.2), 3)
    stroke(c, lambda: (c.move_to(-54, -35), c.line_to(54, -35)), shade(col, 0.2), 3)
    oval(c, 0, -105, 64, 11, tint(col, 0.2), 5)
    for sx in (-1, 1):
        stroke(c, lambda: c.arc(sx * 66, -80, 12, -1.2, 1.2) if sx > 0 else c.arc_negative(sx * 66, -80, 12, math.pi + 1.2, math.pi - 1.2), INK, 4)
    if tag:
        stroke(c, lambda: (c.move_to(30, -110), c.line_to(70, -60)), INK, 2)
        box(c, 50, -62, 76, 44, 8, PAPER, 4, shading=0)
        text(c, tag, 88, -30, 30, DISPLAY, INK, "center")
    c.restore()


def snips(c, x, y, s=1.0, rot=0.0, open_=0.3, col=hx("e2452f")):
    """Flower snips (floral scissors): short blades, looped handles."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for side in (-1, 1):
        c.save(); c.rotate(side * open_ * 0.5)
        fill_ink(c, lambda: (c.move_to(0, 0), c.line_to(side * 6, -52), c.line_to(0, -60), c.line_to(-side * 3, -4)),
                 hx("cfd6e0"), 3, shading=0.1)
        fill_ink(c, lambda: (c.move_to(-side * 2, 4), c.curve_to(side * 22, 30, side * 26, 60, side * 10, 66),
                             c.curve_to(-side * 2, 60, -side * 4, 30, -side * 2, 4)), col, 3)
        c.restore()
    circle(c, 0, 0, 5, INK, 0, shading=0)
    c.restore()


def name_card(c, x, y, name, s=1.0, col=PAPER):
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: poly(c, [(-60, 0), (60, 0), (50, -44), (-50, -44)]), col, 3, shading=0.06)
    size = fit_size(c, name, BODY, 28, 96, 14)
    text(c, name, 0, -14, size, BODY, INK, "center")
    c.restore()


def care_card(c, x, y, s=1.0, lines=("Fresh water", "every day", "Trim the stems")):
    c.save(); c.translate(x, y); c.scale(s, s)
    box(c, -150, -86, 300, 172, 14, PAPER, 4, shading=0.05)
    circle(c, -124, -60, 8, KRAFT, 2, shading=0)
    for i, ln in enumerate(lines):
        text(c, ln, 0, -22 + i * 42, 32, BODY, INK, "center")
    c.restore()


def wrapped_jar(c, x, y, s=1.0, t=0.0, wrap_p=1.0, seed=0):
    """A finished jar arrangement with kraft paper folded up around it and twine at the neck."""
    mason_jar(c, x, y, s, t, (1, 1, 1, 1), seed=seed)
    if wrap_p <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    top = lerp(0, -260, ease_out(wrap_p))
    fill_ink(c, lambda: poly(c, [(-100, 0), (100, 0), (130, top), (40, top + 40), (0, top + 10), (-40, top + 40), (-130, top)]),
             KRAFT, 5, shading=0.12)
    if wrap_p > 0.8:
        stroke(c, lambda: (c.move_to(-78, -170), c.curve_to(-20, -160, 20, -160, 78, -170)), hx("8a6a3a"), 5)
    c.restore()


def workshop_table(c, x, y, w=1300, s=1.0, t=0.0, stations=5, guests=None, items=1.0, jars_layers=None,
                   names=None, extras=True):
    """A long workshop table seen from the front. Each station: a jar, a small water bucket, snips and a name card.
    guests: optional list of seeds; a guest stands behind each station wearing an apron.
    items: 0..1 how many station items are laid out. jars_layers: arrangement layers for every jar."""
    from chars import person
    c.save(); c.translate(x, y); c.scale(s, s)
    sp = w / stations
    if guests:
        for i, sd in enumerate(guests[:stations]):
            gx = -w / 2 + sp * (i + 0.5)
            person(c, gx + sp * 0.18, -70, 1.3, t, seed=sd, apron=hx("e9d7b0"),
                   pose=((1.0, 0.6), (1.0, 0.6)))
    box(c, -w / 2, -110, w, 30, 8, WOOD)
    fill_ink(c, lambda: (c.move_to(-w / 2, -84), c.line_to(w / 2, -84), c.line_to(w / 2 - 6, -40),
                         c.curve_to(w / 4, -30, -w / 4, -30, -w / 2 + 6, -40), c.close_path()), CREAM, 5)
    for lx in (-w / 2 + 30, w / 2 - 30):
        box(c, lx - 8, -40, 16, 40, 3, shade(WOOD, 0.2), 4)
    if extras:
        flower_bucket(c, 0, -104, 0.75, t, "mixed", 9, seed=3)
    for i in range(stations):
        sx = -w / 2 + sp * (i + 0.5)
        if extras and abs(sx) < sp * 0.6:
            continue
        p = ease_out(prog(items, i / stations * 0.6, 0.4))
        if p <= 0:
            continue
        c.save(); c.translate(0, (1 - p) * 20)
        mason_jar(c, sx - 40, -106, 0.42, t, jars_layers or (0, 0, 0, 0), seed=i)
        flower_bucket(c, sx + 60, -106, 0.42, t, "zinnia" if jars_layers is None else "mixed", 0, seed=i, col=TIN)
        snips(c, sx + 20, -96, 0.6, 1.4, 0.2)
        if names:
            name_card(c, sx - 40, -84 + 46, names[i % len(names)], 0.8)
        c.restore()
    c.restore()


def flower_row(c, y, s=1.0, t=0.0, kinds=("zinnia",), seed=0, x0=-60, x1=W + 60, gap=110, grow=1.0):
    """A row of flowers across the frame at ground line y."""
    r = rng_for("row", seed, y)
    x = x0
    i = 0
    stroke(c, lambda: (c.move_to(x0, y + 6), c.line_to(x1, y + 6)), hx("7a5636"), 10 * s, 0.35)
    while x < x1:
        k = kinds[i % len(kinds)]
        h = r.uniform(150, 200) * grow
        if h > 10:
            if k == "zinnia":
                zinnia_plant(c, x, y, h, ZINNIA_COLS[r.randrange(6)], t, i, s)
            elif k == "cosmos":
                cosmos_plant(c, x, y, h + 30, COSMOS_COLS[r.randrange(4)], t, i, s)
            elif k == "dahlia":
                dahlia_plant(c, x, y, h, DAHLIA_COLS[r.randrange(4)], t, i, s)
            elif k == "snap":
                snapdragon(c, x, y, h + 20, SNAP_COLS[r.randrange(4)], t, i, s=s)
            elif k == "sunflower":
                branching_sunflower(c, x, y, h + 60, t, i, s)
        x += gap * s * r.uniform(0.85, 1.15)
        i += 1


def open_barn(c, x, y, s=1.0, t=0.0, col=TOMATO, lights=1.0, inside=None):
    """A barn workshop: big front opening with the doors swung wide, a warm interior, string lights.
    inside(c) draws what's in the opening (coordinates relative to the barn's ground centre)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    w, h = 900, 430
    fill_ink(c, lambda: poly(c, [(-w / 2, 0), (-w / 2, -h), (0, -h - 230), (w / 2, -h), (w / 2, 0)]), col)
    for i in range(1, 14):
        stroke(c, lambda: (c.move_to(-w / 2 + i * w / 14, -6), c.line_to(-w / 2 + i * w / 14, -h + 4)), shade(col, 0.15), 3)
    fill_ink(c, lambda: poly(c, [(-w / 2 - 40, -h + 10), (0, -h - 250), (w / 2 + 40, -h + 10), (w / 2 + 40, -h - 8),
                                 (0, -h - 268), (-w / 2 - 40, -h - 8)]), CREAM, 5)
    ow, oh = 620, 340
    g = cairo.LinearGradient(0, -oh, 0, 0)
    g.add_color_stop_rgba(0, *hx("6b4a3a")); g.add_color_stop_rgba(1, *hx("caa274"))
    rrect(c, -ow / 2, -oh, ow, oh, 6); c.set_source(g); c.fill_preserve()
    setc(c, INK); c.set_line_width(6); c.stroke()
    if lights:
        for k in range(12):
            lx = -ow / 2 + 20 + k * (ow - 40) / 11
            ly = -oh + 30 + math.sin(k / 11 * math.pi) * 40
            glow(c, lx, ly, 28, GOLD, 0.5 * lights)
            circle(c, lx, ly, 7, hx("fff1b0"), 2, shading=0)
        stroke(c, lambda: smooth(c, [(-ow / 2 + 20 + k * (ow - 40) / 11, -oh + 24 + math.sin(k / 11 * math.pi) * 40)
                                     for k in range(12)], False), INK, 2, 0.7)
    if inside:
        c.save(); rrect(c, -ow / 2, -oh, ow, oh, 6); c.clip(); inside(c); c.restore()
    for sgn in (-1, 1):  # doors swung fully open against the walls
        dx = sgn * (ow / 2 + 70)
        box(c, dx - 70, -oh, 140, oh, 3, CREAM)
        stroke(c, lambda: (c.move_to(dx - 62, -oh + 8), c.line_to(dx + 62, -8)), col, 9)
        stroke(c, lambda: (c.move_to(dx + 62, -oh + 8), c.line_to(dx - 62, -8)), col, 9)
    c.restore()
