"""Non-event scenes: hook, the Twelve-Month Gate, chapter cards, the Cannon Hall story, math, close."""
import math
import cairo
from gfx import *
from chars import dot, person, sheep, goat, cow, limb, limb2, SKINS, HAIR, COATS
from props import *
from sets import season_bg, weather, sepia
from icons import icon, ICON_SEASON
from common import *
from vignettes import lambing_barn, interior, window, steam, seated, tabletop


def countup(v, t, start, dur=1.6):
    return v * ease_out(prog(t, start, dur))


def D(c, S, t, x, y, s=1.0, **kw):
    """Dot, lip-synced to the narration."""
    dot(c, x, y, s, t, mouth=M(S, t), **kw)


# ---------------------------------------------------------------- reusable shots
def feb_yard(c, t, phone_glow=0.0, gate_open=0.0, cars=0, car_t=0.0):
    season_bg(c, "winter", t, tod="dusk", seed=41)
    house(c, 1500, 860, 1.1, lit=0.35 + phone_glow * 0.5, snow=True)
    for x in (120, 1150, 1830):
        tree(c, x, 860, 1.0, "bare", t, seed=x, snow=True)
    r = rng_for("puddles", 1)
    for i in range(7):
        px, py = r.uniform(80, 1800), r.uniform(900, 1060)
        oval(c, px, py, r.uniform(90, 170), r.uniform(16, 28), MUD, 4, shading=0.12)
        rr = (t * 0.6 + i * 0.3) % 1
        stroke(c, lambda: ellipse(c, px + 20, py, 20 + rr * 60, 4 + rr * 10), WHITE, 3, 0.5 * (1 - rr))
    fence(c, -20, 260, 900, 0.85)
    fence(c, 840, 1240, 900, 0.85)
    gate(c, 290, 910, 0.95, open_=gate_open, snow=True)
    for k in range(cars):
        st = car_t + k * 0.22
        p = ease_out(prog(t, st, 1.6))
        tx = 960 + (k % 5) * 205 + (1 - p) * 1100
        if p > 0:
            car(c, tx, 990 + (k // 5) * 70, 0.6, COATS[k % len(COATS)], t, moving=1 - p, flip=True)


def kitchen(c, t, phone_lit=0.0, ring=0.0, cal_date=0.0):
    interior(c, wall=hx("f1dcb4"), floor=hx("b98a5a"), plank=False, floor_y=880, lights=False, t=t)
    # stripes on the wall
    for i in range(0, W, 90):
        c.rectangle(i, 0, 40, 880); setc(c, hx("ead1a4"), 0.6); c.fill()

    def yard(c, w, h, t):
        g = cairo.LinearGradient(0, 0, 0, h)
        g.add_color_stop_rgba(0, *hx("2b3f9a")); g.add_color_stop_rgba(1, *hx("e79a7c"))
        c.set_source(g); c.paint()
        c.rectangle(0, h * 0.68, w, h); setc(c, hx("8a6a5a")); c.fill()
        gate(c, 60, h * 0.86, 0.38, snow=True)
    window(c, 200, 250, 520, 360, yard, t)
    # wall clock
    circle(c, 1500, 360, 110, PAPER, 7)
    for k in range(12):
        a = k * math.pi / 6
        circle(c, 1500 + math.cos(a) * 88, 360 + math.sin(a) * 88, 6, INK, 0)
    stroke(c, lambda: (c.move_to(1500, 360), c.line_to(1500 + 50 * math.cos(-1.2), 360 + 50 * math.sin(-1.2))), INK, 9)
    a = -math.pi / 2 + int(t) * math.pi / 30
    stroke(c, lambda: (c.move_to(1500, 360), c.line_to(1500 + 86 * math.cos(a), 360 + 86 * math.sin(a))), TOMATO, 4)
    # calendar
    box(c, 960, 260, 300, 340, 10, PAPER, 6)
    box(c, 960, 260, 300, 70, 10, TOMATO, 6)
    text(c, "FEB", 1110, 314, 54, DISPLAY, PAPER, "center")
    for k in range(20):
        gx, gy = 985 + (k % 5) * 52, 350 + (k // 5) * 56
        box(c, gx, gy, 42, 42, 6, CREAM, 3, shading=0)
    if cal_date > 0:
        stroke(c, lambda: (c.new_sub_path(), c.arc(985 + 2 * 52 + 21, 350 + 2 * 56 + 21, 36 * ease_out(cal_date), 0,
                                                   6.28 * ease_out(cal_date))), TOMATO, 9)
    # table
    box(c, 260, 760, 1400, 50, 14, WOOD, 7)
    for lx in (330, 1590):
        box(c, lx - 18, 800, 36, 280, 6, shade(WOOD, 0.2), 6)
    # mug
    box(c, 520, 650, 90, 110, 14, SKY, 6)
    stroke(c, lambda: c.arc(615, 705, 30, -math.pi / 2, math.pi / 2), INK, 12)
    stroke(c, lambda: c.arc(615, 705, 30, -math.pi / 2, math.pi / 2), SKY, 6)
    steam(c, 565, 630, t, 1.3)
    c.save(); c.translate(1000, 730); c.rotate(-math.pi / 2 + 0.12)
    phone(c, 0, 0, 1.1, lit=phone_lit, t=t, ring=ring)
    c.restore()


def us_map_pts():
    P_ = [(2, 4), (14, 5), (30, 6), (48, 6), (56, 7), (57, 4), (60, 9), (66, 12), (70, 13), (74, 14), (78, 12), (80, 10),
          (86, 8), (90, 4), (93, 8), (88, 14), (89, 17), (84, 20), (82, 24), (80, 30), (82, 32), (77, 38), (75, 42), (76, 50),
          (79, 56), (77, 58), (73, 50), (70, 44), (63, 44), (60, 46), (54, 47), (49, 54), (46, 56), (42, 50), (38, 45),
          (33, 45), (28, 43), (20, 42), (16, 40), (12, 38), (6, 30), (2, 20), (1, 12)]
    return P_


def inside(pt, poly_):
    x, y = pt
    n = len(poly_)
    ins = False
    j = n - 1
    for i in range(n):
        xi, yi = poly_[i]; xj, yj = poly_[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            ins = not ins
        j = i
    return ins


def us_map(c, x, y, s, t, dots_p):
    pts = [(x + px * s, y + py * s) for (px, py) in us_map_pts()]
    fill_ink(c, lambda: smooth(c, pts), hx("cfe3b0"), 7, shading=0.1)
    r = rng_for("usdots", 2)
    k = 0
    for i in range(500):
        px, py = r.uniform(1, 93), r.uniform(4, 58)
        if inside((px, py), us_map_pts()):
            k += 1
            if k / 220 < dots_p:
                circle(c, x + px * s, y + py * s, 7, TOMATO, 2.5, shading=0)


def mini_barn(c, x, y, s, lit=0.0, half=False):
    col = TOMATO if lit > 0 else hx("c9c3bb")
    c.save(); c.translate(x, y); c.scale(s, s)
    if lit > 0:
        glow(c, 0, -20, 60, GOLD, 0.6 * lit)
    fill_ink(c, lambda: poly(c, [(-20, 0), (-20, -24), (0, -40), (20, -24), (20, 0)]), col, 3, shading=0)
    if half:
        c.save(); c.rectangle(0, -45, 25, 50); c.clip()
        fill_ink(c, lambda: poly(c, [(-20, 0), (-20, -24), (0, -40), (20, -24), (20, 0)]), hx("c9c3bb"), 3, shading=0)
        c.restore()
    box(c, -7, -14, 14, 14, 2, CREAM if lit else hx("e3ded6"), 2, shading=0)
    c.restore()


def topdown_table(c, x, y, n_side, t, filled=0, seat_w=34, colors=True):
    w = n_side * seat_w + 40
    for row in (-1, 1):
        for i in range(n_side):
            idx = i * 2 + (0 if row < 0 else 1)
            cx_ = x - w / 2 + 20 + i * seat_w + seat_w / 2
            cy_ = y + row * 62
            box(c, cx_ - 13, cy_ - 13, 26, 26, 5, WOOD, 3, shading=0)
            if idx < filled:
                circle(c, cx_, cy_, 12, SKINS[idx % 5], 3)
                circle(c, cx_, cy_ - 3, 8, HAIR[idx % 6], 0)
    box(c, x - w / 2, y - 40, w, 80, 12, CREAM, 5)


def gate_icon(c, x, y, s, o):
    gate(c, x, y, s, open_=o)


# ---------------------------------------------------------------- HOOK
@scene("H01", sfx=lambda S: [(0.2, "wind"), (P(S, 3), "tick")])
def h01(c, t, S):
    if t < P(S, 3) - 0.1:
        c.save(); cam(c, t, S.dur, 1.0, 1.06, 400, 800)
        feb_yard(c, t)
        c.restore()
    else:
        tt = t - P(S, 3)
        c.save(); cam(c, tt, 3, 1.0, 1.05, 1000, 700)
        kitchen(c, t)
        c.restore()
    title_text(c, "FEBRUARY", 960, 190, t, P(S, 0) - 0.1, 140)


@scene("H02", sfx=lambda S: [(P(S, 1) + 0.3, "tag"), (P(S, 2), "baa")])
def h02(c, t, S):
    if t < P(S, 1) - 0.05:
        # across the water: warm barn lights
        season_bg(c, "winter", t, tod="dusk", seed=42, layers=(0, 1, 2))
        barn(c, 1180, 700, 0.8, lit=1.0, snow=True)
        house(c, 760, 700, 0.6, lit=1.0, snow=True)
        c.rectangle(0, 700, W, H); setc(c, hx("3a4a9a")); c.fill()
        c.save(); c.rectangle(0, 700, W, H); c.clip()
        c.translate(0, 1400); c.scale(1, -1)
        c.push_group()
        barn(c, 1180, 700, 0.8, lit=1.0, snow=True)
        house(c, 760, 700, 0.6, lit=1.0, snow=True)
        c.pop_group_to_source(); c.paint_with_alpha(0.35)
        c.restore()
        for i in range(12):
            yy = 730 + i * 28
            xo = math.sin(t * 1.5 + i) * 30
            stroke(c, lambda: (c.move_to(300 + xo + i * 40, yy), c.line_to(500 + xo + i * 40, yy)), WHITE, 3, 0.35)
        glow(c, 1180, 800, 260, GOLD, 0.25)
        weather(c, "snow", t, 50)
        banner_plain(c, "Lambing Festival", t, P(S, 0))
    else:
        tt = t
        c.save(); cam(c, tt - P(S, 1), S.dur - P(S, 1), 1.0, 1.05, 620, 700)
        lambing_barn(c, t, close=False, birth_t=P(S, 2) + 0.2)
        c.restore()
        banner_plain(c, "Lambing Festival", t, 0)
        price_tag(c, 1500, 210, S.ev["rows"], "Cannon Hall Farm", "England", t, P(S, 1) + 0.3)


def banner_plain(c, title, t, t0, x=40, y=36):
    a = ease_out(prog(t, t0, 0.7))
    if a <= 0:
        return
    c.push_group()
    tw_ = text_w(c, title, BODY, 64) + 80
    box(c, x, y, tw_, 96, 30, PAPER, 6)
    text(c, title, x + 40, y + 68, 64, BODY, INK)
    c.pop_group_to_source(); c.paint_with_alpha(a)


@scene("H03", sfx=lambda S: [(P(S, 3), "tickets")])
def h03(c, t, S):
    hold = P(S, 0) - 0.2  # hard stop: nothing moves during the beat
    tt = max(0.0, t - hold) if t > hold else 0.0
    # left: empty yard
    c.save(); c.rectangle(0, 0, 956, H); c.clip()
    c.translate(-300, 0)
    feb_yard(c, tt)
    c.restore()
    # right: busy barn
    c.save(); c.rectangle(964, 0, 956, H); c.clip()
    c.translate(964, 0)
    season_bg(c, "winter", tt, tod="dusk", seed=43, layers=(0, 1, 2, 3))
    barn(c, 480, 860, 1.0, lit=1.0, snow=True, doors_open=0.6)
    for k in range(8):
        x = ((tt * 50 + k * 140) % 1100) - 100
        person(c, x, 960 + (k % 3) * 40, 0.75, tt, seed=k + 30, kid=k % 3 == 0, walk=tt * 5 + k,
               hat=["beanie", None, "bun", "cap"][k % 4], scarf=[TOMATO, GOLD, LEAF][k % 3])
    if t > P(S, 3):
        for k in range(6):
            ph = ((t - P(S, 3)) * 0.8 + k / 6) % 1
            ticket(c, 120 + k * 140, 760 - ph * 500, 0.45, GOLD, "TICKET", rot=math.sin(ph * 8 + k) * 0.5)
    weather(c, "snow", tt, 40, region=(0, 0, 956, H))
    c.restore()
    if t > P(S, 2):
        k = ease(prog(t, P(S, 2), 0.6))
        c.rectangle(0, 0, 956, H); c.set_source_rgba(0.1, 0.12, 0.3, 0.25 * k); c.fill()
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), PAPER, 14)
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), INK, 5)
    card(c, ["Same month.", "Same mud."], 960, 60, t, [P(S, 0), P(S, 1)], 72, DISPLAY, "center", "tc", gap=1.25)


def icon_ring(c, cx, cy, R, t, start, n=30, r=40, spread=1.0, alphas=None):
    for i in range(n):
        p = ease_back(prog(t, start + i * 0.04, 0.6))
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / 30
        rr = R * p
        x, y = cx + math.cos(a) * rr * spread, cy + math.sin(a) * rr * spread
        if p > 0:
            icon(c, i, x, y, r * min(1, p + 0.2), a=1 if alphas is None else alphas[i])


@scene("H04", sfx=lambda S: [(0.3, "creak"), (P(S, 1), "whoosh")])
def h04(c, t, S):
    season_bg(c, "spring", t, seed=44)
    o = ease(prog(t, 0.2, 1.6))
    gate(c, 60, 960, 0.85, open_=o)
    x, w_ = walk_x(t, 1.2, 260, 560, 150)
    wave = t > 3.2
    D(c, S, t, x, 1030, 0.92, walk=t * 6 if w_ else None, pose="wave" if wave else "idle",
      wave_amp=0.35 if wave else 0, look=0.4)
    cx, cy = 1350, 600
    season_wheel(c, cx, cy, 150 * ease_back(prog(t, P(S, 1) - 0.3, 0.6)) + 0.1, "none")
    icon_ring(c, cx, cy, 330, t, P(S, 1))
    card(c, [("30 farm event ideas", 78, DISPLAY, INK), ("Real ticket prices", 64, BODY, hx("8a2a14"))], 60, 50, t,
         [P(S, 1), P(S, 3) if len(S.ph) > 3 else P(S, 2)])


@scene("H05", sfx=lambda S: [(0.6, "whoosh")])
def h05(c, t, S):
    season_bg(c, "spring", t, seed=44)
    cx, cy = 1350, 560
    season_wheel(c, cx, cy, 150, "none")
    p = ease(prog(t, 0.5, 2.0))
    for i in range(30):
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / 30
        s_i = ["winter", "spring", "summer", "fall"].index(ICON_SEASON[i])
        qa = -math.pi / 2 + s_i * math.pi / 2
        x0, y0 = cx + math.cos(a) * 330, cy + math.sin(a) * 330
        x1, y1 = cx + math.cos(qa) * 300, cy + math.sin(qa) * 300
        icon(c, i, lerp(x0, x1, p), lerp(y0, y1, p), 40, a=1 - p)
    for s_i, ic in enumerate((0, 10, 16, 25)):
        qa = -math.pi / 2 + s_i * math.pi / 2
        k = ease_back(prog(t, 1.8 + s_i * 0.15, 0.6))
        if k > 0:
            icon(c, ic, cx + math.cos(qa) * 300, cy + math.sin(qa) * 300, 90 * k)
    D(c, S, t, 360, 1030, 0.92, pose="point", look=0.6)
    card(c, ["One event for each quiet season"], 60, 50, t, [P(S, 0) + 0.2], 64, BODY)


@scene("H06", sfx=lambda S: [(P(S, 2) + 0.2, "thud")])
def h06(c, t, S):
    season_bg(c, "spring", t, seed=45)
    c.set_source_rgba(0.1, 0.12, 0.23, 0.3); c.paint()
    wob = math.sin(t * 2) * 0.03
    k = clamp((t - P(S, 2) - 0.2) / 0.22)
    shake = math.sin(t * 60) * 8 * (1 - prog(t, P(S, 2) + 0.42, 0.3)) if k >= 1 else 0
    c.save(); c.translate(960 + shake, 560); c.rotate(wob)
    box(c, -260, -380, 520, 720, 34, PAPER, 8)
    text(c, "No. 11", 0, -190, 110, DISPLAY, INK, "center")
    text(c, "?", 0, 170, 300, DISPLAY, TOMATO, "center")
    c.restore()
    if t > P(S, 2) + 0.2:
        stamp(c, 960 + shake, 560, lerp(2.4, 1.3, ease_out(k)), "SOLD OUT", alpha=k)
    banner_plain(c, "No. 11: SOLD OUT", t, P(S, 0))


@scene("H07", sfx=lambda S: [(P(S, 1), "boing")])
def h07(c, t, S):
    season_bg(c, "summer", t, seed=46)
    barn(c, 1500, 860, 0.9)
    pose = "wave" if t < P(S, 1) else ("hat" if t < P(S, 2) - 0.2 else "present")
    look = 0.0 if t < P(S, 1) else (-0.8 if t < P(S, 2) - 0.2 else 0.2)
    D(c, S, t, 960, 1040, 1.2, pose=pose, wave_amp=0.35 if pose == "wave" else 0, look=look)
    title_text(c, "Dot", 520, 380, t, P(S, 0), 150)
    card(c, [("Agritourism Success", 78, DISPLAY, INK)], 960, 70, t, [P(S, 2)], anchor="tc")


# ---------------------------------------------------------------- THE TWELVE-MONTH GATE
def barn_wall(c):
    setc(c, hx("c7442e")); c.paint()
    for i in range(0, W, 110):
        stroke(c, lambda: (c.move_to(i, 0), c.line_to(i, H)), shade(hx("c7442e"), 0.18), 5)


@scene("B01", sfx=lambda S: [(1.0, "fork"), (3.0, "fork"), (5.0, "fork")])
def b01(c, t, S):
    barn_wall(c)
    calendar(c, 1220, 230, 560, 420, months_lit=[0.0] * 9 + [1.0, 0.0, 0.0], grey=True)
    # farmer's boots and hands, working (cropped close-up)
    c.save(); c.rectangle(560, 600, 700, 600); c.clip()
    fk = math.sin(t * 2.4)
    person(c, 900, 1110, 2.2, t, seed=301, coat=hx("2f8f8a"), bottom=hx("39457a"),
           pose=((1.2 + 0.25 * fk, 0.9), (1.0 + 0.25 * fk, 1.1)))
    c.restore()
    stroke(c, lambda: (c.move_to(700 + fk * 30, 620), c.line_to(1060 + fk * 40, 1000)), INK, 18)
    stroke(c, lambda: (c.move_to(700 + fk * 30, 620), c.line_to(1060 + fk * 40, 1000)), WOOD, 11)
    for k in range(3):
        stroke(c, lambda: (c.move_to(1050 + fk * 40 + k * 14, 990), c.line_to(1090 + fk * 40 + k * 14, 1060)), hx("8c8f9e"), 6)
    for k in range(10):
        hay_x = 1040 + k * 30 + fk * 20
        stroke(c, lambda: (c.move_to(hay_x, 1040), c.line_to(hay_x + 30, 1010 - (k % 3) * 10)), hx("e8c15a"), 7)
    box(c, 540, 570, 640, 44, 8, shade(WOOD, 0.15), 6)
    # Dot leans on the fence
    D(c, S, t, 300, 1110, 1.0, pose="lean", look=0.5)
    fence(c, -20, 560, 1060, 1.1)
    card(c, ["You're farming right."], 60, 50, t, [P(S, 0)], 72, DISPLAY)


@scene("B02", sfx=lambda S: [(P(S, 3), "wind")])
def b02(c, t, S):
    season_bg(c, "fall", t, seed=51)
    c.set_source_rgba(1, 1, 1, 0.25); c.paint()
    pulse = 0.85 + 0.15 * math.sin(t * 5) if t > P(S, 2) else 1.0
    dim = ease(prog(t, P(S, 3), 1.2))
    lit = [0.0] * 12
    lit[9] = 1.0 * pulse
    calendar(c, 800, 330, 1040, 600, months_lit=lit, grey=True)
    if dim > 0:
        c.rectangle(790, 320, 1060, 620); c.set_source_rgba(0.3, 0.3, 0.4, 0.0); c.fill()
    D(c, S, t, 360, 1040, 0.95, pose="point" if t > P(S, 1) else "idle", look=0.7)
    if t > P(S, 3):
        x = (t - P(S, 3)) * 220 - 100
        c.save(); c.translate(x, 1010); c.rotate((t - P(S, 3)) * 4)
        for k in range(6):
            stroke(c, lambda: c.arc(0, 0, 30 + k * 4, k, k + 4), hx("a07a4a"), 4)
        c.restore()
    card(c, [("OLD WAY:", 70, DISPLAY, TOMATO), ("Open when the crop is ready", 64, BODY, INK)], 60, 50, t,
         [P(S, 0), P(S, 1)])


@scene("B03", sfx=lambda S: [(P(S, 1) + 0.2 + k * 0.35, "click") for k in range(12)] + [(P(S, 2), "creak")])
def b03(c, t, S):
    season_bg(c, "spring", t, seed=52)
    c.set_source_rgba(1, 1, 1, 0.2); c.paint()
    x0, y0, w, h = 640, 320, 1220, 640
    lit = [ease(prog(t, P(S, 1) + 0.2 + i * 0.35, 0.4)) for i in range(12)]
    calendar(c, x0, y0, w, h, months_lit=lit, grey=True, bright=LEAF)
    cw, ch = (w - 50) / 4, (h - 40) / 3
    for i in range(12):
        if lit[i] > 0:
            gx = x0 + 10 + (i % 4) * (cw + 10) + 24
            gy = y0 + 10 + (i // 4) * (ch + 10) + ch - 22
            gate(c, gx, gy, 0.16, open_=lit[i])
    D(c, S, t, 330, 1040, 0.92, pose="present" if t > P(S, 2) else "point", look=0.6)
    card(c, [("NEW WAY:", 70, DISPLAY, LEAF), ("Open when the calendar is empty", 64, BODY, INK)], 60, 50, t,
         [P(S, 0), P(S, 1)])


@scene("B04", sfx=lambda S: [(P(S, 1) + 0.3 + k * 0.6, "drop") for k in range(4)])
def b04(c, t, S):
    season_bg(c, "summer", t, seed=53)
    c.set_source_rgba(1, 1, 1, 0.22); c.paint()
    for k, sname in enumerate(["winter", "spring", "summer", "fall"]):
        x = 640 + k * 310
        col = SEASON_COL[sname]
        box(c, x - 130, 360, 260, 260, 30, col, 7)
        icon(c, [0, 10, 16, 25][k], x, 470, 80, ring=False)
        text(c, sname.capitalize(), x, 590, 54, DISPLAY, PAPER if sname != "summer" else INK, "center")
        st = P(S, 1) + 0.3 + k * 0.6
        if t > st:
            u = t - st
            y = 640 + min(u, 0.5) / 0.5 * 220
            bounce = abs(math.sin(min(u, 1.4) * 9)) * 30 * math.exp(-u * 3) if u > 0.5 else 0
            ticket(c, x, y - bounce + 40, 0.9, GOLD, "TICKET", rot=-0.08 + 0.04 * k)
    D(c, S, t, 260, 1040, 0.85, pose="present", look=0.6)
    card(c, ["Every season: one paid reason to come"], 60, 50, t, [P(S, 0)], 64, BODY)


@scene("B05", sfx=lambda S: [(P(S, 0) + 0.2 + k * 0.12, "coin") for k in range(10)])
def b05(c, t, S):
    season_bg(c, "summer", t, seed=54)
    c.set_source_rgba(1, 1, 1, 0.3); c.paint()
    us_map(c, 60, 300, 10.5, t, ease(prog(t, P(S, 1), 4.0)))
    money_bag(c, 920, 1040, 1.3, t)
    n = int(ease_out(prog(t, P(S, 0) + 0.2, 3.0)) * 20)
    coins(c, 1180, 1040, n, 1.1)
    v = countup(1.26, t, P(S, 1), 2.0)
    pct = countup(12.4, t, P(S, 3), 1.5)
    card(c, [(f"${v:.2f} billion", 120, DISPLAY, INK), ("US agritourism income, 2022", 58, BODY, INK),
             (f"up {pct:.1f}% after inflation", 58, BODY, hx("2f6f2a"))], 1860, 60, t,
         [P(S, 1), P(S, 2), P(S, 3)], anchor="tr", gap=1.3)


@scene("B06", sfx=lambda S: [(P(S, 2) + 0.3, "chime")])
def b06(c, t, S):
    season_bg(c, "summer", t, seed=55)
    c.set_source_rgba(1, 1, 1, 0.35); c.paint()
    litp = prog(t, P(S, 2) + 0.3, 0.8)
    for i in range(100):
        x = 110 + (i % 10) * 80
        y = 330 + (i // 10) * 72
        k = ease_back(prog(t, 0.1 + i * 0.012, 0.5))
        if k <= 0:
            continue
        lit = litp if i in (44, 45) else 0
        mini_barn(c, x, y, 1.2 * k, lit=lit, half=(i == 45 and lit > 0))
    farms = countup(28600, t, P(S, 0), 1.8)
    avg = countup(44000, t, P(S, 1), 1.8)
    pct = countup(1.5, t, P(S, 2), 1.2)
    card(c, [(f"About {int(round(farms / 100) * 100):,} farms", 72, DISPLAY, INK),
             (f"${int(round(avg / 1000) * 1000):,} average, before costs", 58, BODY, INK),
             (f"Only {pct:.1f}% of US farms", 58, BODY, hx("8a2a14"))], 1870, 330, t, [P(S, 0), P(S, 1), P(S, 2)],
         anchor="tr")


@scene("B07", sfx=lambda S: [(P(S, 3), "whoosh")])
def b07(c, t, S):
    season_bg(c, "spring", t, seed=56)
    c.set_source_rgba(1, 1, 1, 0.2); c.paint()
    fall_t = P(S, 3)
    keep = 10
    for i in range(30):
        x = 860 + (i % 6) * 170
        y = 300 + (i // 6) * 150
        k = ease_back(prog(t, P(S, 2) + i * 0.03, 0.5))
        if k <= 0:
            continue
        if t > fall_t and i != keep:
            u = t - fall_t - (i % 7) * 0.05
            if u > 0:
                y += 900 * u * u + 60 * u
                x += math.sin(i) * 120 * u
        if i == keep and t > fall_t:
            m = ease(prog(t, fall_t + 0.4, 1.0))
            x, y = lerp(x, 1290, m), lerp(y, 600, m)
            sz = 60 * (1 + 1.5 * m)
            glow(c, x, y, sz * 2.2, GOLD, 0.5 * m)
            icon(c, i, x, y, sz)
        elif y < 1200:
            c.save(); c.translate(x, y); c.rotate((t - fall_t) * (i % 5 - 2) * 0.8 if t > fall_t else 0)
            box(c, -70, -62, 140, 124, 18, PAPER, 5)
            icon(c, i, 0, 0, 48 * k)
            c.restore()
    D(c, S, t, 380, 1040, 1.0, pose="finger" if t > fall_t - 0.3 else ("shrug" if t > P(S, 1) else "idle"),
      look=0.3)
    card(c, [("Not 30 things. One.", 78, DISPLAY, INK)], 60, 50, t, [P(S, 3)])


@scene("B08", sfx=lambda S: [(P(S, 2), "scribble"), (P(S, 1), "tag")])
def b08(c, t, S):
    season_bg(c, "fall", t, seed=57)
    c.set_source_rgba(1, 1, 1, 0.3); c.paint()
    price_tag(c, 480, 300, [("", "$", "")], "", "", t, P(S, 1) - 0.1, maxw=360)
    coins(c, 860, 900, int(ease_out(prog(t, P(S, 1) + 0.3, 1.0)) * 7), 1.0)
    # notepad + pencil doing sums
    box(c, 1100, 380, 560, 600, 14, PAPER, 7)
    for k in range(9):
        stroke(c, lambda: (c.move_to(1130, 450 + k * 58), c.line_to(1630, 450 + k * 58)), hx("a9c4ec"), 3)
    sp = prog(t, P(S, 2), S.dur - P(S, 2) - 0.5)
    rows = int(sp * 7)
    for k in range(rows + 1):
        frac = 1 if k < rows else (sp * 7 - rows)
        y = 438 + k * 58
        c.move_to(1160, y)
        for j in range(int(frac * 20)):
            c.line_to(1160 + j * 18, y + math.sin(j * 1.7 + k) * 10)
        setc(c, INK, 0.8); c.set_line_width(4); c.stroke()
    if rows >= 6:
        stroke(c, lambda: (c.move_to(1150, 438 + 6 * 58 - 30), c.line_to(1560, 438 + 6 * 58 - 30)), INK, 5)
    px = 1160 + (sp * 7 % 1) * 360
    py = 438 + min(rows, 6) * 58
    c.save(); c.translate(px, py); c.rotate(0.6)
    box(c, -10, -150, 22, 150, 4, GOLD, 4)
    fill_ink(c, lambda: poly(c, [(-10, 0), (12, 0), (1, 24)]), hx("f1c8a0"), 3)
    box(c, -10, -170, 22, 22, 4, hx("f29ab0"), 4)
    c.restore()
    card(c, ["A ticket price is not profit"], 60, 50, t, [P(S, 1)], 70, DISPLAY)


# ---------------------------------------------------------------- CHAPTER CARDS
def chapter(c, t, S, season):
    col = SEASON_COL[season]
    setc(c, col); c.paint()
    g = cairo.RadialGradient(960, 600, 100, 960, 600, 1100)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.25); g.add_color_stop_rgba(1, 0, 0, 0.1, 0.15)
    c.set_source(g); c.paint()
    # hill + gate
    hill = {"winter": SNOW, "spring": hx("8fd06a"), "summer": hx("d8c25a"), "fall": hx("c27a36")}[season]
    fill_ink(c, lambda: (c.move_to(-20, H + 20), c.line_to(-20, 900), c.curve_to(500, 760, 1400, 760, 1940, 900),
                         c.line_to(1940, H + 20), c.close_path()), hill, 7)
    if season == "summer":
        for k in range(9):
            sunflower(c, 160 + k * 200 + (k % 2) * 40, 960 + (k % 2) * 40, 0.9, t, seed=k)
    if season == "fall":
        for k in range(6):
            pumpkin(c, 200 + k * 300, 1000 + (k % 2) * 30, 0.9)
        glow(c, 1500, 300, 800, hx("ffd27a"), 0.5)
    if season == "spring":
        for k in range(5):
            tree(c, 150 + k * 420, 880, 0.7, "blossom", t, seed=k)
    o = 0.15 * ease(prog(t, 1.5, 2.0))
    snowy = season == "winter"
    gate(c, 680, 900, 1.0, open_=o, snow=snowy)
    if season == "spring":
        melt = 1 - ease(prog(t, 0.2, 2.5))
        if melt > 0:
            for px in (680, 680 + 560):
                oval(c, px, 900 - 230 - 76, 26 * melt + 0.1, 10 * melt + 0.1, SNOW, 4, shading=0)
            ph = (t * 0.9) % 1
            oval(c, 700, 900 - 280 + ph * 200, 7, 10, hx("cfe8ff"), 3, shading=0)
    wx = {"winter": "snow", "spring": "petals", "summer": "heat", "fall": "leaves"}[season]
    weather(c, wx, t, None)
    title_text(c, S.beat["screen"][0], 960, 330, t, 0.15, 220, PAPER if season != "summer" else INK,
               INK if season != "summer" else PAPER, olw=22)
    k = ease_back(prog(t, 0.3, 0.7))
    if k > 0:
        season_wheel(c, 960, 480 + 0 * k, 70 * k + 0.1, season)


for _sid, _sea in (("W00", "winter"), ("S00", "spring"), ("U00", "summer"), ("F00", "fall")):
    scene(_sid, sfx=chime_sfx)(lambda c, t, S, _sea=_sea: chapter(c, t, S, _sea))


# ---------------------------------------------------------------- S04
def seed_table(c, t, sprout=1.0):
    box(c, 200, 760, 1000, 40, 10, WOOD, 6)
    for lx in (240, 1160):
        box(c, lx - 10, 800, 20, 240, 4, shade(WOOD, 0.2), 5)
    for i in range(4):
        x = 260 + i * 230
        box(c, x, 690, 200, 74, 10, hx("6b4a2a"), 5)
        for j in range(4):
            sx_ = x + 30 + j * 46
            stroke(c, lambda: (c.move_to(sx_, 692), c.line_to(sx_, 692 - 34 * sprout)), LEAF, 5)
            oval(c, sx_ - 9, 692 - 34 * sprout, 10, 5, LEAF, 3)
            oval(c, sx_ + 9, 692 - 38 * sprout, 10, 5, LEAF, 3)


@scene("S04")
def s04(c, t, S):
    season_bg(c, "spring", t, seed=14)
    greenhouse(c, 700, 880, 1.7)
    seed_table(c, t)
    n = sum(1 for i in (1, 2, 3) if t > P(S, i))
    D(c, S, t, 1440, 1050, 1.0, pose="count", look=-0.4)
    for k in range(n):
        circle(c, 1340 + k * 50, 560, 14, GOLD, 4)
    card(c, ["A table.", "Some soil.", "One hour."], 60, 50, t, [P(S, 1), P(S, 2), P(S, 3)], 72, DISPLAY)
    overlay_tracker(c, t, S)


# ---------------------------------------------------------------- THE STORY (sepia)
def farm_1984(c, t, busy=0.0, colour=False):
    season_bg(c, "spring", t, seed=61)
    house(c, 1450, 860, 0.85)
    barn(c, 1000, 860, 0.8, col=hx("b8452a"))
    fence(c, -20, 700, 920, 0.8)
    sheep(c, 300, 990, 0.8, t, seed=1)
    cow(c, 560, 1000, 0.8, t)


@scene("T01", sfx=lambda S: [(P(S, 2), "paper")])
def t01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 1400, 800)
    farm_1984(c, t)
    # stern banker with a letter
    shake_ = math.sin(t * 20) * 3 if t > P(S, 2) else 0
    bx, w_ = walk_x(t, 0.3, 2100, 1650, 140)

    def letter(c, hands):
        hx_, hy_ = hands[1]
        c.save(); c.translate(hx_ + shake_, hy_ - 30); c.rotate(-0.15)
        box(c, -50, -36, 100, 72, 4, PAPER, 4)
        for k in range(3):
            stroke(c, lambda: (c.move_to(-34, -16 + k * 16), c.line_to(30, -16 + k * 16)), INK, 3, 0.5)
        c.restore()
    person(c, bx, 1050, 1.2, t, seed=401, coat=hx("3a3a48"), bottom=hx("2a2a35"), hat="bowler", skin=SKINS[0],
           hair=hx("5a5a5a"), walk=t * 5 if w_ else None, pose=((1.3, 0.9), (0.2, 0.2)), hold=letter, look=-1)
    c.restore()
    sepia(c)
    card(c, [("Cannon Hall Farm, 1984", 72, DISPLAY, INK), ("126 acres, in the red", 64, BODY, TOMATO)], 60, 50, t,
         [P(S, 0), P(S, 1)], bg=hx("fbf0dc"))


def kitchen_table_family(c, t, banker=1.0):
    interior(c, wall=hx("e8d2a8"), floor=hx("b98a5a"), plank=True, floor_y=880, lights=False, t=t)
    window(c, 760, 140, 400, 300, lambda c, w, h, t: (setc(c, hx("cfe0f0")), c.paint()), t)
    for i, x in enumerate((420, 700, 980)):
        seated(c, x, 810, 0.95, t, seed=410 + i, mouth=0.0)
    box(c, 1315, 560, 130, 250, 10, WOOD, 6)  # banker's chair back
    if banker > 0:
        c.push_group()
        seated(c, 1380, 810, 0.95, t, seed=401, coat=hx("3a3a48"), hat="bowler")
        c.pop_group_to_source(); c.paint_with_alpha(banker)
    table(c, 860, 920, 1300, 1.0, hx("f6e7d0"), plates=4)


@scene("T02", sfx=lambda S: [(P(S, 0), "poof")])
def t02(c, t, S):
    gone = t > P(S, 0)
    kitchen_table_family(c, t if gone else 0, banker=0.0 if gone else 1.0)
    if gone:
        u = t - P(S, 0)
        if u < 0.8:
            for k in range(10):
                a = k * math.pi / 5
                rr = 60 + u * 260
                stroke(c, lambda: (c.move_to(1380 + math.cos(a) * rr * 0.6, 560 + math.sin(a) * rr * 0.6),
                                   c.line_to(1380 + math.cos(a) * rr, 560 + math.sin(a) * rr)), INK, 6, 1 - u / 0.8)
            for k in range(6):
                circle(c, 1380 + math.cos(k) * u * 160, 560 + math.sin(k * 2) * u * 90, 40 * (1 - u), CREAM, 3,
                       alpha=1 - u / 0.8)
    sepia(c)
    card(c, [("They sacked the banker.", 80, DISPLAY, INK)], 960, 60, t, [P(S, 0)], anchor="tc", bg=hx("fbf0dc"))


@scene("T03")
def t03(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.05, 500, 700)
    season_bg(c, "spring", t, seed=62)
    barn(c, 1450, 860, 0.7, col=hx("b8452a"))
    person(c, 430, 1060, 1.55, t, seed=420, coat=hx("6b6b4a"), hat="cap", hair=hx("9a9a9a"), skin=SKINS[0],
           mouth=0.0, pose=((0.4, 0.3), (0.9, 1.6)))
    if t > P(S, 3):
        k = ease_back(prog(t, P(S, 3), 0.6))
        cow(c, 960, 1050, 0.6 * k + 0.01, t)
        sheep(c, 1200, 1060, 0.7 * k + 0.01, t)
    c.restore()
    sepia(c)
    card(c, [("“We nearly went", 80, DISPLAY, INK), ("out of business.”", 80, DISPLAY, INK),
             ("Robert Nicholson", 60, BODY, hx("6a3a1a"))], 1860, 120, t, [P(S, 1), P(S, 1) + 0.2, P(S, 2)],
         anchor="tr", bg=hx("fbf0dc"))


@scene("T04", sfx=lambda S: [(P(S, 0) + 0.5, "hammer"), (P(S, 1) + 0.5, "creak")])
def t04(c, t, S):
    col_k = ease(prog(t, P(S, 1), 1.2))
    season_bg(c, "spring", t, seed=63)
    for k in range(3):
        x = 230 + k * 330
        box(c, x - 130, 700, 260, 220, 6, hx("c9c0ae"), 6)
        for j in range(5):
            stroke(c, lambda: (c.move_to(x - 120, 730 + j * 40), c.line_to(x + 120, 730 + j * 40)), hx("a9a08e"), 3)
        r_ = ease_back(prog(t, P(S, 0) + 0.2 + k * 0.5, 0.5))
        if r_ > 0:
            fill_ink(c, lambda: poly(c, [(x - 150, 704), (x, 704 - 130 * r_), (x + 150, 704)]), hx("6b4a7a"), 6)
        if t > P(S, 0) + 1.6 + k * 0.3:
            sign(c, x + 90, 900, "SOLD", 64, TOMATO, 1.0, rot=-0.1)
    o = ease(prog(t, P(S, 1) + 0.5, 1.6))
    gate(c, 1250, 960, 0.95, open_=o)
    sepia(c, 0.9 * (1 - col_k))
    if col_k > 0:
        glow(c, 1500, 500, 700, hx("fff2b0"), 0.35 * col_k)
    card(c, [("Good Friday, 1989", 80, DISPLAY, INK)], 60, 50, t, [P(S, 1)])


@scene("T05", sfx=lambda S: [(P(S, 1) + k * 0.15, "coin") for k in range(8)])
def t05(c, t, S):
    season_bg(c, "spring", t, seed=64)
    house(c, 1450, 860, 0.85)
    barn(c, 1000, 860, 0.8, col=hx("b8452a"), doors_open=0.8, lit=0.6)
    for k in range(14):
        x = ((t * 45 * (1 if k % 2 else -1) + k * 160) % 2000) - 40
        person(c, x, 950 + (k % 4) * 35, 0.62, t, seed=430 + k, kid=k % 2 == 0, walk=t * 5 + k,
               hat=["cap", None, "bun", "straw"][k % 4])
    m = countup(5, t, P(S, 1), 1.6)
    kids = countup(30000, t, P(S, 1) + 0.6, 1.8)
    card(c, [("2015", 60, BODY, hx("2f6f2a")), (f"£{m:.0f} million turnover", 70, DISPLAY, INK),
             (f"{int(round(kids / 100) * 100):,} schoolchildren a year", 60, BODY, INK)], 60, 50, t,
         [P(S, 0), P(S, 1), P(S, 1) + 0.6])


@scene("T06")
def t06(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.08, 760, 700)
    season_bg(c, "winter", t, tod="dusk", seed=65)
    barn(c, 760, 900, 1.25, lit=1.0, snow=True)
    ticket(c, 760, 760, 1.4, GOLD, "TICKET", rot=0.05 + math.sin(t * 2) * 0.03)
    for k in range(5):
        person(c, 260 + k * 120 + math.sin(t + k) * 10, 1040, 0.7, t, seed=440 + k, kid=k % 2 == 1, hat="beanie",
               scarf=[TOMATO, GOLD][k % 2])
    weather(c, "snow", t, 80)
    c.restore()
    card(c, ["The farm the bank wanted sold", "now sells tickets in February."], 1860, 60, t, [P(S, 0), P(S, 0) + 0.4],
         62, BODY, anchor="tr")


@scene("T07", sfx=lambda S: [(P(S, 2), "ding")])
def t07(c, t, S):
    season_bg(c, "summer", t, seed=66)
    barn(c, 1500, 860, 0.8)
    D(c, S, t, 520, 900, 0.95, pose="point_low", look=0.3)
    # link strip + subscribe button
    a = ease_out(prog(t, P(S, 0) + 0.3, 0.7))
    if a > 0:
        c.push_group()
        box(c, 140, 930, 1100, 110, 30, PAPER, 6)
        text(c, "agritourismsuccess.com/farm-quiz", 690, 1006, 62, DISPLAY, SKY, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    b = ease_out(prog(t, P(S, 2), 0.7))
    if b > 0:
        g = 0.5 + 0.5 * math.sin(t * 3)
        glow(c, 1560, 985, 260, TOMATO, 0.35 * g * b)
        c.push_group()
        box(c, 1340, 925, 440, 120, 60, TOMATO, 6)
        text(c, "Subscribe", 1560, 1005, 64, DISPLAY, PAPER, "center")
        c.pop_group_to_source(); c.paint_with_alpha(b)


# ---------------------------------------------------------------- THE MATH
@scene("M01", sfx=lambda S: [(0.3, "chalk")])
def m01(c, t, S):
    season_bg(c, "fall", t, seed=71)
    c.set_source_rgba(1, 1, 1, 0.2); c.paint()
    cx, cy = 1340, 600
    chapter_wheel(c, cx, cy, 230, t, None, None, 0, labels=False)
    for i in range(30):
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / 30
        ticket(c, cx + math.cos(a) * 330, cy + math.sin(a) * 330, 0.32, SEASON_COL[ICON_SEASON[i]], "", rot=a + math.pi / 2)
    x, w_ = walk_x(t, 0.2, 140, 460, 140)

    def slate_hold(c, hx_, hy_):
        box(c, hx_ - 90, hy_ - 80, 180, 130, 10, hx("2d3a35"), 6)
        stroke(c, lambda: (c.move_to(hx_ - 60, hy_ - 30), c.line_to(hx_ + 50, hy_ - 40)), WHITE, 4, 0.8)
    D(c, S, t, x, 1040, 1.0, walk=t * 6 if w_ else None, pose="slate", hold=(1, slate_hold))
    title_text(c, "Now the math", 520, 200, t, P(S, 1), 120)


def cost_blocks(c, x, y, t, starts):
    labels = ["chef", "staff", "permits", "lights", "toilets"]
    cols = [TOMATO, GOLD, SKY, LEAF, hx("8e5aa8")]
    for k, (lb, cl, st) in enumerate(zip(labels, cols, starts)):
        p = ease_out(prog(t, st, 0.5))
        if p <= 0:
            continue
        yy = y - (k + 1) * 82 - (1 - p) * 400
        box(c, x, yy, 360, 76, 14, cl, 5)
        text(c, lb, x + 180, yy + 56, 54, BODY, INK if cl in (GOLD,) else PAPER, "center")


@scene("M02", sfx=lambda S: [(P(S, 2) + 0.2 + k * 0.35, "block") for k in range(5)])
def m02(c, t, S):
    setc(c, hx("f6ead2")); c.paint()
    season_bg(c, "fall", t, seed=72, layers=(0,))
    c.set_source_rgba(1, 1, 1, 0.45); c.paint()
    topdown_table(c, 560, 330, 24, t, filled=0)
    cost_blocks(c, 120, 1040, t, [P(S, 2) + 0.2 + k * 0.35 for k in range(5)])
    fc = countup(3150, t, P(S, 2) + 0.2, 1.8)
    card(c, [("48 seats at $150", 66, DISPLAY, INK), (f"Sample fixed costs: ${int(fc):,}", 58, BODY, INK),
             ("Sample cost per guest: about $57", 58, BODY, INK)], 1860, 470, t, [P(S, 1), P(S, 2), P(S, 4) if len(S.ph) > 4 else P(S, 3)],
         anchor="tr")
    D(c, S, t, 760, 1060, 0.8, pose="slate")


@scene("M03", sfx=lambda S: [(0.3 + k * 0.08, "click") for k in range(0, 34, 3)] + [(P(S, 1), "coin")])
def m03(c, t, S):
    setc(c, hx("f6ead2")); c.paint()
    season_bg(c, "fall", t, seed=72, layers=(0,))
    c.set_source_rgba(1, 1, 1, 0.45); c.paint()
    n = int(min(34, max(0, (t - 0.3) / 0.08))) if t < P(S, 1) else 34 + int(min(14, (t - P(S, 1)) / 0.12))
    topdown_table(c, 560, 330, 24, t, filled=n)
    text(c, str(n), 560, 520, 120, DISPLAY, TOMATO if n < 34 else LEAF, "center")
    # coin pile vs break-even line
    lvl = min(n, 48)
    coins(c, 400, 1040, lvl * 1.1, 1.0)
    ly = 1040 - (34 * 1.1 // 5) * 16 - 10
    c.set_dash([18, 12])
    stroke(c, lambda: (c.move_to(150, ly), c.line_to(780, ly)), INK, 5)
    c.set_dash([])
    keep = countup(1329, t, P(S, 1) + 0.5, 1.6)
    card(c, [("Break-even: 34 guests", 66, DISPLAY, INK), (f"All 48 sold: about ${int(keep):,}", 60, BODY, hx("2f6f2a")),
             ("Before paying yourself", 58, BODY, INK)], 1860, 470, t, [P(S, 0), P(S, 1) + 0.3, P(S, 2)], anchor="tr")


@scene("M04", sfx=lambda S: [(P(S, 2), "coin")])
def m04(c, t, S):
    season_bg(c, "spring", t, seed=14)
    greenhouse(c, 600, 820, 1.5)
    seed_table(c, t)
    for g in range(2):
        for k in range(10):
            p = ease_back(prog(t, P(S, 1) + g * 0.8 + k * 0.05, 0.4))
            if p <= 0:
                continue
            x = 260 + g * 520 + (k % 5) * 90
            y = 900 + (k // 5) * 80
            box(c, x - 26 * p, y - 26 * p, 52 * p, 52 * p, 8, [TOMATO, SKY][g], 4)
    v = countup(1000, t, P(S, 2), 1.4)
    card(c, [("2 classes × 10 people × $50", 66, DISPLAY, INK), (f"= ${int(v):,}", 120, DISPLAY, hx("2f6f2a")),
             ("Before costs", 58, BODY, INK)], 1860, 260, t, [P(S, 1), P(S, 2), P(S, 3)], anchor="tr")
    D(c, S, t, 1600, 1060, 0.62, pose="present", look=-0.5)


# ---------------------------------------------------------------- OBJECTION
@scene("O01")
def o01(c, t, S):
    season_bg(c, "summer", t, seed=81)
    c.set_source_rgba(1, 1, 1, 0.25); c.paint()
    box(c, 760, 300, 1060, 720, 18, PAPER, 7)
    c.save(); c.translate(880, 900); c.scale(0.28, 0.28)
    barn(c, 0, 0, 1.0); house(c, 500, 0, 0.8)
    c.restore()
    # ten people, then twenty-five
    n10 = t > P(S, 2)
    n25 = t > P(S, 3)
    if n10:
        for k in range(10):
            p = ease_back(prog(t, P(S, 2) + k * 0.05, 0.4))
            person(c, 1110 + (k % 5) * 60, 560 + (k // 5) * 120, 0.32 * p + 0.01, t, seed=500 + k)
    if n25:
        for k in range(25):
            p = ease_back(prog(t, P(S, 3) + k * 0.03, 0.4))
            person(c, 1100 + (k % 9) * 70, 760 + (k // 9) * 90, 0.26 * p + 0.01, t, seed=520 + k)
    shake = math.sin(t * 7) * 0.6 if P(S, 1) < t < P(S, 2) + 0.5 else 0.2
    D(c, S, t, 380, 1040, 1.0, pose="hips" if t < P(S, 1) else "present", look=shake)
    card(c, [("“My farm is too small.”", 76, DISPLAY, INK)], 60, 50, t, [P(S, 0)])


@scene("O02", sfx=lambda S: [(P(S, 1) + 0.1, "ring"), (P(S, 2) + 0.1, "ring"), (P(S, 3) + 0.1, "ring")])
def o02(c, t, S):
    season_bg(c, "spring", t, seed=82)
    c.set_source_rgba(1, 1, 1, 0.3); c.paint()
    labels = ["Insurer", "Zoning office", "Health department"]
    card(c, [("Call first:", 72, DISPLAY, INK)], 160, 60, t, [P(S, 0)])
    for k, lb in enumerate(labels):
        st = P(S, k + 1)
        y = 360 + k * 220
        a = ease_out(prog(t, st - 0.2, 0.6))
        if a <= 0:
            continue
        ringing = 1.0 if st < t < st + 1.6 else 0.0
        c.push_group()
        box(c, 160, y - 70, 1000, 160, 30, PAPER, 6)
        phone(c, 270, y + 10, 0.85, lit=1.0 if t > st else 0, t=t, ring=ringing)
        text(c, lb, 380, y + 34, 70, DISPLAY, INK)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    D(c, S, t, 1500, 1050, 1.0, pose="point" if t < P(S, 4) else "hips", look=-0.5)


# ---------------------------------------------------------------- CLOSE
@scene("C01", sfx=lambda S: [(0.2, "wind")])
def c01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.06, 1.0, 400, 800)
    feb_yard(c, t + 20)
    c.restore()
    title_text(c, "February", 960, 170, t, P(S, 0), 140)


@scene("C02", sfx=lambda S: [(0.85, "ring"), (P(S, 2) + 0.1, "car"), (P(S, 2) + 1.4, "creak")])
def c02(c, t, S):
    if t < P(S, 1) - 0.05:
        lit = ease(prog(t, 0.82, 0.3))
        ring = 1.0 if 0.85 < t < 2.4 else 0.0
        c.save(); cam(c, t, 3, 1.0, 1.04, 1050, 450)
        kitchen(c, t, phone_lit=lit, ring=ring, cal_date=prog(t, P(S, 0) + 0.6, 0.8))
        c.restore()
    elif t < P(S, 2) - 0.05:
        tt = t - P(S, 1)
        interior(c, wall=hx("c98d5a"), floor=hx("a8743f"), t=t)
        glow(c, 960, 700, 600, hx("ffcf6a"), 0.35)
        table(c, 960, 960, 1200, 1.0, CREAM, chairs=10, chairs_shown=int(tt / 0.12) + 1, plates=10)
    else:
        feb_yard(c, t, phone_glow=1.0, gate_open=ease(prog(t, P(S, 2) + 1.4, 1.5)), cars=10, car_t=P(S, 2))
    card(c, ["One date.", "One table.", "Ten cars."], 1860, 640, t, [P(S, 0), P(S, 1), P(S, 2)], 66, DISPLAY,
         anchor="tr")


@scene("C03")
def c03(c, t, S):
    season_bg(c, "spring", t, seed=91)
    gate(c, 300, 1000, 1.1, open_=1.0)
    D(c, S, t, 560, 1040, 1.1, pose="lean", look=0.5)
    card(c, [("Watching won't change anything.", 66, DISPLAY, INK), ("Doing will.", 90, DISPLAY, TOMATO)], 1860, 260, t,
         [P(S, 0), P(S, 1)], anchor="tr")


@scene("C04", sfx=lambda S: [(P(S, 1) + k * 0.12, "type") for k in range(10)])
def c04(c, t, S):
    season_bg(c, "summer", t, seed=92)
    c.set_source_rgba(1, 1, 1, 0.25); c.paint()
    bx, by, bw, bh = 640, 200, 1180, 560
    a = ease_out(prog(t, P(S, 0) - 0.1, 0.6))
    if a > 0:
        c.push_group()
        fill_ink(c, lambda: (rrect(c, bx, by, bw, bh, 50), c.move_to(bx + 160, by + bh - 4), c.line_to(bx + 60, by + bh + 120),
                             c.line_to(bx + 300, by + bh - 4)), PAPER, 7)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    ease_text(c, "Homework:", bx + 70, by + 140, 90, t, P(S, 0), DISPLAY, TOMATO)
    ease_text(c, "Your quietest month?", bx + 70, by + 270, 70, t, P(S, 1), BODY, INK)
    ease_text(c, "Which event?", bx + 70, by + 390, 70, t, P(S, 2), BODY, INK)
    last = "Which event?" if t > P(S, 2) else "Your quietest month?" if t > P(S, 1) else "Homework:"
    sz = 70 if last != "Homework:" else 90
    face = BODY if last != "Homework:" else DISPLAY
    yy = {"Homework:": by + 140, "Your quietest month?": by + 270, "Which event?": by + 390}[last]
    cx_ = bx + 70 + text_w(c, last, face, sz) + 12
    if a > 0.5 and int(t * 2) % 2 == 0:
        c.rectangle(cx_, yy - sz * 0.8, 8, sz * 0.95); setc(c, INK); c.fill()
    D(c, S, t, 330, 1050, 0.95, pose="point", look=0.6)


@scene("C05", sfx=lambda S: [(P(S, 0) + 0.8 + k * 0.7, "tick") for k in range(4)])
def c05(c, t, S):
    season_bg(c, "spring", t, seed=93)
    c.set_source_rgba(1, 1, 1, 0.25); c.paint()
    # clipboard quiz
    box(c, 260, 150, 640, 760, 24, WOOD, 7)
    box(c, 300, 210, 560, 670, 10, PAPER, 5)
    box(c, 480, 120, 200, 70, 14, hx("8c8f9e"), 6)
    for k in range(4):
        y = 300 + k * 140
        box(c, 340, y - 45, 90, 90, 14, CREAM, 6)
        tk = ease_out(prog(t, P(S, 0) + 0.8 + k * 0.7, 0.3))
        if tk > 0:
            stroke(c, lambda: (c.move_to(355, y), c.line_to(380, y + 26 * min(1, tk * 2)),
                               *( [c.line_to(380 + 45 * (tk * 2 - 1), y + 26 - 60 * (tk * 2 - 1))] if tk > 0.5 else [])),
                   LEAF, 12)
        for j in range(2):
            stroke(c, lambda: (c.move_to(460, y - 14 + j * 30), c.line_to(820 - j * 120, y - 14 + j * 30)), hx("c9c3bb"), 10)
    D(c, S, t, 1400, 920, 0.8, pose="point", look=-0.5)
    url_strip(c, "agritourismsuccess.com/farm-quiz", t, P(S, 0) + 0.2)


def url_strip(c, url, t, t0, y=950):
    a = ease_out(prog(t, t0, 0.7))
    if a <= 0:
        return
    c.push_group()
    w = text_w(c, url, DISPLAY, 80) + 100
    box(c, 960 - w / 2, y - 20, w, 120, 36, PAPER, 7)
    text(c, url, 960, y + 66, 80, DISPLAY, SKY, "center")
    c.pop_group_to_source(); c.paint_with_alpha(a)


@scene("C06", sfx=lambda S: [(1.0 + k * 1.2, "page") for k in range(int((S.dur - 2) / 1.2))])
def c06(c, t, S):
    season_bg(c, "fall", t, seed=94)
    c.set_source_rgba(1, 1, 1, 0.25); c.paint()
    # book: cover first, then an open spread with pages flipping
    bx, by = 560, 500
    if t < 1.0:
        box(c, bx - 300, by - 340, 600, 680, 18, LEAF, 7)
        c.save(); c.translate(bx, by)
        text(c, "150", 0, -150, 160, DISPLAY, GOLD, "center", outline=INK, olw=12)
        for i, ln in enumerate(["Ways to Unlock", "Hidden Wealth", "From Your Farm"]):
            text(c, ln, 0, -20 + i * 70, 58, DISPLAY, PAPER, "center")
        gate(c, -150, 300, 0.45)
        c.restore()
    else:
        box(c, bx - 400, by - 300, 800, 600, 18, shade(LEAF, 0.2), 7)
        for side in (-1, 1):
            box(c, bx + (side - 1) * 185 + (10 if side > 0 else -10) + (0 if side > 0 else 0), by - 280, 370, 560, 10, PAPER, 5)
        stroke(c, lambda: (c.move_to(bx, by - 280), c.line_to(bx, by + 280)), INK, 5)
        for side in (-1, 1):
            for k in range(5):
                x0 = bx + 40 if side > 0 else bx - 340
                stroke(c, lambda: (c.move_to(x0, by - 200 + k * 70), c.line_to(x0 + 300 - (k % 3) * 60, by - 200 + k * 70)),
                       hx("c9c3bb"), 10)
        icon(c, int(t * 0.83) % 30, bx + 190, by + 190, 60)
        ph = (t * 0.83) % 1
        sx = math.cos(ph * math.pi)
        fill_ink(c, lambda: rrect(c, bx + min(0, 370 * sx), by - 280, abs(370 * sx) + 0.1, 560, 10), CREAM, 4)
    chips = ["Difficulty", "Startup cost", "Price", "Earning potential"]
    st0 = P(S, 1) + 0.3
    card(c, [(("· " if k else "") + ch, 66, DISPLAY, [TOMATO, SKY, hx("2f6f2a"), hx("8e5aa8")][k]) for k, ch in enumerate(chips)],
         1060, 200, t, [st0 + k * 0.5 for k in range(4)])
    url_strip(c, "agritourismsuccess.com/150ways", t, P(S, 0) + 0.3, y=920)


@scene("C07", sfx=lambda S: [(0.3, "creak")])
def c07(c, t, S):
    seasons = ["winter", "spring", "summer", "fall"]
    per = S.dur / 4
    k = min(3, int(t / per))
    u = (t - k * per) / per
    season_bg(c, seasons[k], t, seed=95)
    if u > 0.85 and k < 3:
        c.push_group()
        season_bg(c, seasons[k + 1], t, seed=95)
        c.pop_group_to_source(); c.paint_with_alpha(ease((u - 0.85) / 0.15))
    gate(c, 1290, 960, 0.85, open_=ease(prog(t, 0.2, 1.4)))
    D(c, S, t, 1660, 1040, 0.95, pose="wave", wave_amp=0.35, look=-0.3)
    wx = {"winter": "snow", "spring": "petals", "summer": "heat", "fall": "leaves"}[seasons[k]]
    weather(c, wx, t, 30)
    card(c, [("Watch next:", 58, BODY, hx("8a2a14")), ("Start Agritourism With What You Already Own", 58, DISPLAY, INK)],
         60, 40, t, [0.3, 0.5], pad=34)
    a = ease_out(prog(t, 0.6, 0.8))
    card(c, [("agritourismsuccess.com/farm-quiz", 56, DISPLAY, SKY), ("agritourismsuccess.com/150ways", 56, DISPLAY, SKY)],
         60, 862, t, [0.6, 0.8], pad=30, gap=1.25)
    text(c, "Narration and animation are AI-generated.", 1880, 1062, 36, BODYM, PAPER, "right", alpha=a,
         outline=INK, olw=7)
