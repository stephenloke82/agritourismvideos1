"""Drawing kit for video 088: cards, pills, the five-step roadmap, price board, truck tailgate, phones, covers.
Reusable flowers and workshop props live in the shared kit (kit/flowers.py)."""
import math
import cairo
from gfx import *
from chars import person, SKINS, HAIR, COATS
from props import barn, tree, fence, sign, stamp
from sets import season_bg
from sarah import sarah
from flowers import *
import timeline

GREY = hx("b9b4ad")
GREY_D = hx("8f8a84")
NAVY = hx("1b2a6b")
DEEP = hx("2f6f2c")


def M(S, t):
    return timeline.mouth(S, t)


def P(S, i, default=0.0):
    if not S.ph:
        return default
    return S.ph[min(i, len(S.ph) - 1)]


def SAR(c, S, t, x, y, s=1.0, **kw):
    sarah(c, x, y, s, t, mouth=M(S, t), **kw)


def countup(v, t, start, dur=1.6):
    return v * ease_out(prog(t, start, dur))


def cam(c, t, dur, z0=1.0, z1=1.05, fx=W / 2, fy=H / 2):
    z = lerp(z0, z1, ease(t / max(dur, 0.1)))
    c.translate(fx, fy); c.scale(z, z); c.translate(-fx, -fy)


# ---------------------------------------------------------------- text
def card(c, lines, x, y, t, starts, size=64, face=BODY, align="left", anchor="tl", col=INK, bg=PAPER, pad=40,
         gap=1.32, minw=0, lw=6, radius=28, maxw=None):
    items = []
    for ln in lines:
        if isinstance(ln, str):
            ln = (ln, size, face, col)
        items.append(ln)
    if maxw:
        items = [(s, min(sz, fit_size(c, s, f, sz, maxw - 2 * pad, 36)), f, cl) for (s, sz, f, cl) in items]
    ws = [text_w(c, s, f, sz) for (s, sz, f, _) in items]
    w = max(max(ws) + 2 * pad, minw)
    hs = [sz * gap for (_, sz, _, _) in items]
    h = sum(hs) - items[-1][1] * (gap - 1) + 2 * pad + items[0][1] * 0.12
    bx = x - (w / 2 if anchor in ("tc", "c") else w if anchor == "tr" else 0)
    by = y - (h / 2 if anchor == "c" else 0)
    a = ease_out(prog(t, starts[0] - 0.15, 0.6))
    if a <= 0:
        return (bx, by, w, h)
    c.push_group()
    shadow(c, bx + w / 2 + 10, by + h + 8, w * 0.5, 16, 0.18)
    box(c, bx, by, w, h, radius, bg, lw, shading=0.05)
    c.pop_group_to_source()
    c.paint_with_alpha(a)
    yy = by + pad
    for (s, sz, f, cl), st in zip(items, starts):
        yy += sz * 0.86
        tx = bx + pad if align == "left" else bx + w / 2 if align == "center" else bx + w - pad
        ease_text(c, s, tx, yy, sz, t, st, f, cl, align)
        yy += sz * (gap - 0.86)
    return (bx, by, w, h)


def pill(c, s, x, y, t, start, size=56, bg=PAPER, col=INK, mark=None, anchor="c", lw=6):
    a = ease_out(prog(t, start, 0.6))
    if a <= 0:
        return 0
    tw = text_w(c, s, BODY, size)
    extra = size * 0.9 if mark else 0
    w, h = tw + 70 + extra, size * 1.7
    bx = x - w / 2 if anchor == "c" else x
    dy = (1 - a) * 14
    c.push_group()
    shadow(c, bx + w / 2, y + h / 2 + 8, w * 0.45, 12, 0.16)
    box(c, bx, y - h / 2 + dy, w, h, h / 2, bg, lw, shading=0.05)
    tx = bx + 35
    if mark == "x":
        circle(c, tx + size * 0.32, y + dy, size * 0.36, TOMATO, 4, shading=0)
        stroke(c, lambda: (c.move_to(tx + size * 0.14, y - size * 0.18 + dy), c.line_to(tx + size * 0.5, y + size * 0.18 + dy),
                           c.move_to(tx + size * 0.5, y - size * 0.18 + dy), c.line_to(tx + size * 0.14, y + size * 0.18 + dy)),
               PAPER, 6)
        tx += extra
    elif mark == "v":
        circle(c, tx + size * 0.32, y + dy, size * 0.36, LEAF, 4, shading=0)
        stroke(c, lambda: (c.move_to(tx + size * 0.12, y + dy), c.line_to(tx + size * 0.28, y + size * 0.16 + dy),
                           c.line_to(tx + size * 0.54, y - size * 0.18 + dy)), PAPER, 6)
        tx += extra
    text(c, s, tx, y + size * 0.35 + dy, size, BODY, col)
    c.pop_group_to_source(); c.paint_with_alpha(a)
    return w


def title(c, s, x, y, t, start, size=110, col=PAPER, outline=INK, align="center", olw=16, maxw=1800):
    size = fit_size(c, s, DISPLAY, size, maxw, 50)
    ease_text(c, s, x, y, size, t, start, DISPLAY, col, align, outline=outline, olw=olw, dur=0.9)


def tracker5(c, n, t, a=1.0):
    if not n:
        return
    s = f"No. {n} of 5"
    w = text_w(c, s, DISPLAY, 50) + 60
    c.push_group()
    box(c, W - 40 - w, 36, w, 84, 42, GOLD, 6)
    text(c, s, W - 40 - w / 2, 92, 50, DISPLAY, INK, "center")
    c.pop_group_to_source(); c.paint_with_alpha(a)


ROAD = ["Plant", "Table", "Pick, arrange, take home", "Price", "Fill"]


def roadmap(c, lit, t, t0=0.0, y=860, gold=None, starts=None):
    """Five numbered tiles along the bottom; `lit` = current (1..5), 0 = all equal."""
    a = ease_out(prog(t, t0, 0.7))
    if a <= 0:
        return
    widths = [230, 230, 560, 230, 230]
    gap, th = 26, 140
    total = sum(widths) + gap * 4
    x0 = (W - total) / 2
    c.push_group()
    box(c, x0 - 26, y - 26, total + 52, th + 52, 36, DEEP, 6, shading=0.05)
    x = x0
    for i, tw in enumerate(widths):
        pa = 1.0 if starts is None else ease_out(prog(t, starts[i], 0.5))
        if pa > 0:
            on = lit == 0 or (i + 1) == lit
            col = GOLD if gold == i + 1 else (CREAM if on else hx("d9d2c2"))
            c.push_group()
            box(c, x, y, tw, th, 24, col, 6)
            circle(c, x + 58, y + th / 2, 38, LEAF if on else GREY, 5)
            text(c, str(i + 1), x + 58, y + th / 2 + 19, 54, DISPLAY, PAPER, "center")
            lsz = fit_size(c, ROAD[i], BODY, 44, tw - 120, 26)
            text(c, ROAD[i], x + 108, y + th / 2 + lsz * 0.36, lsz, BODY, INK)
            if (i + 1) == lit or gold == i + 1:
                stroke(c, lambda: rrect(c, x - 8, y - 8, tw + 16, th + 16, 30), GOLD, 8)
            c.pop_group_to_source(); c.paint_with_alpha(pa * (1.0 if on else 0.55))
        x += tw + gap
    c.pop_group_to_source(); c.paint_with_alpha(a)


# ---------------------------------------------------------------- backgrounds
def soft_bg(c, t, col=CREAM):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *tint(col, 0.3)); g.add_color_stop_rgba(1, *col)
    c.set_source(g); c.paint()
    r = rng_for("dots", 1)
    for k in range(60):
        circle(c, r.uniform(0, W), r.uniform(0, H), 5, shade(col, 0.08), 0, shading=0)


def flower_farm(c, t, seed=2, tod="day", rows=True, barn_x=1640, season="summer"):
    """The farm: sky and hills, a red barn, and flower rows in the foreground."""
    season_bg(c, season, t, tod=tod, seed=seed)
    if barn_x is not None:
        barn(c, barn_x, 760, 0.95)
    tree(c, 1320, 760, 0.7, "leafy", t, seed=4)
    if rows:
        flower_row(c, 790, 0.55, t, ("zinnia", "cosmos", "zinnia", "snap"), seed=seed, gap=120)
        flower_row(c, 900, 0.75, t, ("cosmos", "zinnia", "dahlia", "zinnia"), seed=seed + 1, gap=150)


def field_close(c, t, seed=3, tod="day"):
    """Standing among the rows: big flowers fore and back."""
    season_bg(c, "summer", t, tod=tod, seed=seed, layers=(0, 1, 2))
    flower_row(c, 700, 0.6, t, ("zinnia", "cosmos", "snap", "zinnia"), seed=seed, gap=110)
    flower_row(c, 840, 0.85, t, ("cosmos", "zinnia", "dahlia"), seed=seed + 1, gap=150)
    g = cairo.LinearGradient(0, 900, 0, H)
    g.add_color_stop_rgba(0, *hx("8a6a44")); g.add_color_stop_rgba(1, *hx("6b4f33"))
    c.rectangle(0, 900, W, H - 900); c.set_source(g); c.fill()


def kitchen_bg(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hx("fbe9c8")); g.add_color_stop_rgba(1, *hx("f3d9a8"))
    c.set_source(g); c.paint()
    # window with a sunny town street
    box(c, 1180, 120, 560, 420, 12, hx("bfe3f7"), 8)
    for k in range(3):
        box(c, 1220 + k * 170, 330, 140, 210, 6, [hx("e9b97a"), hx("d98a6a"), hx("a9c48a")][k], 4)
    stroke(c, lambda: (c.move_to(1460, 120), c.line_to(1460, 540), c.move_to(1180, 330), c.line_to(1740, 330)), WOOD, 12)
    glow(c, 1460, 300, 500, hx("fff4c4"), 0.35)
    # table top
    box(c, -20, 760, W + 40, 60, 10, hx("c8955a"))
    c.rectangle(0, 820, W, H - 820); setc(c, hx("e8c99a")); c.fill()


# ---------------------------------------------------------------- props for this story
def truck_tailgate(c, x, y, s=1.0, t=0.0, col=hx("4f7bd0")):
    """The back of a pickup with its tailgate down. (x, y) = ground under the centre of the bumper."""
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 0, 520, 30, 0.25)
    for wx in (-330, 330):
        circle(c, wx, -70, 82, hx("2d2f3a"), 6)
        circle(c, wx, -70, 36, GREY, 4)
    # the cab seen from behind: roof and rear window above the bed
    box(c, -330, -500, 660, 190, 40, col)
    box(c, -260, -470, 520, 120, 20, hx("bfe3f7"), 5)
    box(c, -470, -330, 940, 210, 26, col)          # bed walls
    box(c, -440, -300, 880, 40, 10, shade(col, 0.3), 4)
    box(c, -480, -150, 960, 60, 12, hx("c9ccd6"))  # bumper
    box(c, -450, -140, 120, 34, 8, TOMATO, 4); box(c, 330, -140, 120, 34, 8, TOMATO, 4)
    # tailgate dropped flat, seen from above-ish
    fill_ink(c, lambda: poly(c, [(-440, -330), (440, -330), (500, -250), (-500, -250)]), tint(col, 0.15))
    c.restore()


def coin(c, x, y, r=34):
    circle(c, x, y, r, GOLD, 5)
    text(c, "$", x, y + r * 0.36, r * 1.0, DISPLAY, shade(GOLD, 0.45), "center")


def hand(c, x, y, s=1.0, flip=False, skin=None, palm_up=True):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    sk = skin or SKINS[1]
    fill_ink(c, lambda: rrect(c, -260, -40, 200, 80, 30), hx("3558c8"))  # sleeve
    fill_ink(c, lambda: smooth(c, [(-80, -40), (40, -50), (90, -20), (95, 20), (40, 40), (-80, 40)]), sk)
    c.restore()


def thought(c, x, y, w, h, t, start, draw=None):
    a = ease_out(prog(t, start, 0.6))
    if a <= 0:
        return
    c.push_group()
    for k, (dx, dy, r) in enumerate(((-w * 0.45, h * 0.7, 14), (-w * 0.38, h * 0.55, 22))):
        circle(c, x + dx, y + dy, r, PAPER, 5)
    oval(c, x, y, w / 2, h / 2, PAPER, 6)
    if draw:
        draw(c, x, y)
    c.pop_group_to_source(); c.paint_with_alpha(a)


def phone_frame(c, x, y, w, h, screen, t, tilt=0.0):
    c.save()
    c.translate(x + w / 2, y + h / 2); c.rotate(tilt); c.translate(-w / 2, -h / 2)
    shadow(c, w / 2 + 16, h + 14, w * 0.45, 22, 0.2)
    box(c, 0, 0, w, h, 54, NAVY, 7, shading=0.05)
    sx, sy, sw, sh = 22, 70, w - 44, h - 140
    c.save(); rrect(c, sx, sy, sw, sh, 18); c.clip()
    setc(c, PAPER); c.paint()
    screen(c, sx, sy, sw, sh, t)
    c.restore()
    stroke(c, lambda: rrect(c, sx, sy, sw, sh, 18), INK, 4)
    box(c, w / 2 - 50, 30, 100, 16, 8, hx("0f1846"), 0, shading=0)
    c.restore()


def browser(c, x, y, w, h, url, t, body=None):
    shadow(c, x + w / 2, y + h + 10, w * 0.45, 18, 0.2)
    box(c, x, y, w, h, 24, PAPER, 6)
    box(c, x, y, w, 80, 24, hx("e6e2db"), 6, shading=0)
    for k, col in enumerate((TOMATO, GOLD, LEAF)):
        circle(c, x + 40 + k * 36, y + 40, 11, col, 3, shading=0)
    box(c, x + 160, y + 18, w - 200, 44, 22, PAPER, 3, shading=0)
    text(c, url, x + 190, y + 52, 34, BODYM, INK)
    if body:
        body(c, x, y + 80, w, h - 80, t)


def ebook_cover(c, x, y, s, t):
    """Stephen's free 150 Ways ebook (same cover as video 008)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 410, 220, 22, 0.25)
    fill_ink(c, lambda: rrect(c, -230, -400, 460, 800, 20), LEAF)
    text(c, "150 WAYS", 0, -230, 88, DISPLAY, PAPER, "center")
    text(c, "to Unlock", 0, -150, 50, BODY, CREAM, "center")
    text(c, "Hidden Wealth", 0, -90, 58, DISPLAY, GOLD, "center")
    text(c, "From Your Farm", 0, -30, 50, BODY, CREAM, "center")
    barn(c, 0, 240, 0.6)
    text(c, "FREE EBOOK", 0, 350, 40, DISPLAY, PAPER, "center")
    c.restore()


def flower_ebook_cover(c, x, y, s, t):
    """The How to Start a Flower Arranging Class ebook: title only, because the book isn't written yet."""
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 410, 220, 22, 0.25)
    fill_ink(c, lambda: rrect(c, -230, -400, 460, 800, 20), hx("8e1b3a"))
    text(c, "How to Start a", 0, -270, 48, BODY, CREAM, "center")
    text(c, "FLOWER", 0, -180, 92, DISPLAY, GOLD, "center")
    text(c, "ARRANGING", 0, -95, 78, DISPLAY, GOLD, "center")
    text(c, "CLASS", 0, -10, 78, DISPLAY, PAPER, "center")
    mason_jar(c, 0, 380, 0.6, t, (1, 1, 1, 1), palette=[PEACH, LEMON, PINK])
    c.restore()


def price_board(c, x, y, w, rows, t, starts, band=0.0):
    """A wooden board; rows = list of (farm, place, price, note). Each row slides in at its start."""
    rh = 150
    h = 60 + rh * len(rows)
    box(c, x, y, w, h, 24, WOOD, 7)
    for k in range(1, 6):
        stroke(c, lambda: (c.move_to(x + 20, y + k * h / 6), c.line_to(x + w - 20, y + k * h / 6)), shade(WOOD, 0.12), 2)
    for i, ((farm, place, price, note), st) in enumerate(zip(rows, starts)):
        a = ease_out(prog(t, st, 0.6))
        if a <= 0:
            continue
        ry = y + 30 + i * rh + (1 - a) * 30
        c.push_group()
        box(c, x + 24, ry, w - 48, rh - 18, 18, PAPER, 5, shading=0.04)
        fsz = fit_size(c, farm, DISPLAY, 50, w - 420, 30)
        text(c, farm, x + 56, ry + 58, fsz, DISPLAY, INK)
        nsz = fit_size(c, place + " · " + note, BODY, 38, w - 420, 24)
        text(c, place + " · " + note, x + 56, ry + 108, nsz, BODY, GREY_D)
        box(c, x + w - 300, ry + 18, 250, rh - 54, 20, GOLD, 5)
        text(c, price, x + w - 175, ry + 92, 62, DISPLAY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if band > 0:
        a = ease_back(band)
        c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(-0.06); c.scale(a, a)
        box(c, -w * 0.5 - 30, -70, w + 60, 140, 30, TOMATO, 7)
        text(c, "ONE PRICE. EVERYTHING IN.", 0, 30, 84, DISPLAY, PAPER, "center", outline=INK, olw=12)
        c.restore()


def chapter_card(c, t, S, title_s, col_key):
    cols = {"tomato": hx("c4553c"), "barn": hx("9c3b2a"), "sky": SKY, "leaf": hx("2f7f2c"), "gold": hx("d99a1f")}
    col = cols[col_key]
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *tint(col, 0.15)); g.add_color_stop_rgba(1, *shade(col, 0.15))
    c.set_source(g); c.paint()
    c.move_to(0, 900)
    for k in range(9):
        c.line_to(k * 240, 880 + math.sin(k * 1.3 + t * 0.3) * 30)
    c.line_to(W, H); c.line_to(0, H); c.close_path()
    setc(c, shade(col, 0.3), 0.5); c.fill()
    flower_bucket(c, 300, 960, 1.1, t, "mixed", 9, seed=5)
    mason_jar(c, 1640, 960, 1.0, t, (1, 1, 1, 1), seed=2)
    title(c, title_s, W / 2, 520, t, 0.1, 120, maxw=1200)
