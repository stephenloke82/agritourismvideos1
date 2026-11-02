"""The 30 event vignettes (plus the shared lambing barn). Each is its own drawing with motion."""
import math
import cairo
from gfx import *
from chars import dot, person, sheep, goat, reindeer, cow, chicken, chick, dog, bee, limb, limb2, wool, SKINS, HAIR, COATS
from props import *
from sets import season_bg, weather, sepia
from common import *


# ---------------------------------------------------------------- shared helpers
def seated(c, x, y, s=1.0, t=0.0, seed=0, mouth=0.0, coat=None, hat=None, eat=False):
    """Upper body of a diner seated behind a table whose top is at y."""
    c.save()
    c.translate(x, y + math.sin(t * 1.3 + seed) * 1.5)
    c.scale(s, s)
    c.translate(0, 112)
    pose = ((0.45 + (0.35 * max(0, math.sin(t * 2 + seed)) if eat else 0), 0.9), (0.45, 0.9))
    person(c, 0, 0, 1.0, t, seed=seed, coat=coat, hat=hat, mouth=mouth, pose=pose)
    c.restore()


def interior(c, wall=hx("c98d5a"), floor=hx("a8743f"), plank=True, floor_y=820, lights=True, t=0.0):
    setc(c, wall); c.paint()
    if plank:
        for i in range(0, W, 120):
            stroke(c, lambda: (c.move_to(i, 0), c.line_to(i, floor_y)), shade(wall, 0.12), 4)
    c.rectangle(0, floor_y, W, H - floor_y)
    setc(c, floor); c.fill()
    stroke(c, lambda: (c.move_to(0, floor_y), c.line_to(W, floor_y)), INK, 6, 0.8)
    for i in range(0, W, 160):
        stroke(c, lambda: (c.move_to(i, floor_y), c.line_to(i - 120, H)), shade(floor, 0.12), 3)
    if lights:
        lantern_string(c, -40, 1180, 90, 90, 12, t)


def window(c, x, y, w, h, scene_fn, t):
    box(c, x - 16, y - 16, w + 32, h + 32, 10, WOOD, 6)
    c.save(); rrect(c, x, y, w, h, 6); c.clip()
    c.translate(x, y)
    scene_fn(c, w, h, t)
    c.restore()
    stroke(c, lambda: (c.move_to(x + w / 2, y), c.line_to(x + w / 2, y + h)), WOOD, 12)
    stroke(c, lambda: (c.move_to(x, y + h / 2), c.line_to(x + w, y + h / 2)), WOOD, 12)
    stroke(c, lambda: rrect(c, x, y, w, h, 6), INK, 6)


def mini_snow_view(c, w, h, t):
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgba(0, *hx("2b3f9a")); g.add_color_stop_rgba(1, *hx("8fa8e0"))
    c.set_source(g); c.paint()
    c.rectangle(0, h * 0.7, w, h); setc(c, SNOW); c.fill()
    weather(c, "snow", t, 30, region=(0, 0, w, h))


def steam(c, x, y, t, s=1.0, seed=0, a=0.6):
    for i in range(3):
        ph = (t * 0.6 + i / 3 + seed * 0.1) % 1
        yy = y - ph * 90 * s
        xx = x + math.sin(ph * 6 + i + seed) * 10 * s
        c.arc(xx, yy, (8 + ph * 14) * s, 0, 6.3)
        setc(c, WHITE, a * (1 - ph)); c.fill()


def flame(c, x, y, s=1.0, t=0.0, seed=0):
    f = 1 + 0.15 * math.sin(t * 13 + seed) + 0.1 * math.sin(t * 7.7 + seed)
    glow(c, x, y - 20 * s, 120 * s, hx("ffb04a"), 0.45)
    fill_ink(c, lambda: (c.move_to(x - 22 * s, y), c.curve_to(x - 30 * s, y - 30 * s * f, x - 4 * s, y - 50 * s * f,
                                                             x + math.sin(t * 9 + seed) * 6 * s, y - 70 * s * f),
                         c.curve_to(x + 8 * s, y - 46 * s * f, x + 30 * s, y - 30 * s * f, x + 22 * s, y), c.close_path()),
             hx("ff8a2a"), 4 * s, shading=0)
    fill_ink(c, lambda: (c.move_to(x - 10 * s, y), c.curve_to(x - 14 * s, y - 20 * s * f, x, y - 30 * s * f, x + 2 * s,
                                                             y - 40 * s * f),
                         c.curve_to(x + 6 * s, y - 24 * s * f, x + 14 * s, y - 16 * s * f, x + 10 * s, y), c.close_path()),
             hx("ffe27a"), 0, shading=0)


def candle(c, x, y, t, seed=0):
    box(c, x - 12, y - 80, 24, 80, 5, CREAM, 4)
    f = 1 + 0.2 * math.sin(t * 15 + seed)
    glow(c, x, y - 100, 70, hx("ffcf6a"), 0.5)
    oval(c, x + math.sin(t * 9 + seed) * 2, y - 98, 8, 16 * f, hx("ffd24a"), 3, shading=0)


def kneel(c, x, y, s, t, seed=0, coat=DENIM, reach=0.0, hold=None, hat=None):
    """A crouching/kneeling person (feet hidden)."""
    c.save(); c.translate(x, y + 70 * s); c.scale(s, s)
    person(c, 0, 0, 1.0, t, seed=seed, coat=coat, hat=hat,
           pose=((1.2 + reach * 0.3, 0.5 + math.sin(t * 2) * 0.1), (1.0 + reach * 0.3, 0.6)), hold=hold)
    c.restore()


# ---------------------------------------------------------------- lambing barn (H02 + W08)
def lambing_barn(c, t, close=False, birth_t=None, gallery_crowd=True):
    interior(c, wall=hx("b97a4a"), floor=hx("d9b25a"), floor_y=760, lights=False, t=t)
    # roof beams + warm lamps
    for bx in (200, 700, 1200, 1700):
        stroke(c, lambda: (c.move_to(bx, 0), c.line_to(bx, 300)), shade(hx("b97a4a"), 0.3), 26)
        glow(c, bx, 120, 220, hx("ffcf6a"), 0.35)
        circle(c, bx, 120, 18, hx("ffe9a0"), 4)
    # viewing gallery (raised walkway with families)
    gy = 470
    if gallery_crowd:
        for i in range(9):
            px = 90 + i * 125
            person(c, px, gy, 0.72, t, seed=i + 2, kid=(i % 3 == 1), mouth=0.6 * max(0, math.sin(t * 2 + i)) ** 4,
                   hat=["beanie", None, "cap", "bun"][i % 4], scarf=[TOMATO, GOLD, LEAF][i % 3],
                   look=math.sin(t * 0.5 + i) * 0.5)
    box(c, -20, gy - 10, 1240, 34, 6, WOOD, 6)
    for i in range(14):
        box(c, i * 90, gy, 16, 120, 3, shade(WOOD, 0.1), 4)
    box(c, -20, gy + 110, 1240, 40, 6, shade(WOOD, 0.15), 6)
    # pen
    px0 = 160 if not close else 120
    fence(c, px0, px0 + 840, 960, 0.9, WOOD)
    # straw
    r = rng_for("straw", 1)
    for i in range(60):
        sx, sy = r.uniform(0, 1200), r.uniform(800, 1060)
        stroke(c, lambda: (c.move_to(sx, sy), c.line_to(sx + r.uniform(-30, 30), sy + r.uniform(-8, 8))), hx("f2d27a"), 5)
    # heat lamp
    lx, ly = 640, 560
    stroke(c, lambda: (c.move_to(lx, 160), c.line_to(lx, ly - 40)), INK, 4)
    glow(c, lx, ly + 220, 330, hx("ff6a3a"), 0.32 + 0.04 * math.sin(t * 3))
    fill_ink(c, lambda: (c.move_to(lx - 60, ly), c.line_to(lx - 30, ly - 50), c.line_to(lx + 30, ly - 50),
                         c.line_to(lx + 60, ly), c.close_path()), hx("8c8f9e"))
    oval(c, lx, ly, 52, 12, hx("ff7a4a"), 4)
    # ewe + lamb
    sheep(c, 520, 900, 1.0, t, seed=3, bleat=0.6 * max(0, math.sin(t * 1.5)) ** 8)
    if birth_t is not None:
        p = ease_out(prog(t, birth_t, 1.2))
        if p > 0:
            stand = ease_back(prog(t, birth_t + 1.6, 1.4))
            wob = math.sin(t * 9) * 0.06 * (1 - prog(t, birth_t + 3.5, 2))
            c.save(); c.translate(770, 900); c.rotate(wob); c.scale(p, p)
            sheep(c, 0, 0, 0.9 + 0.1 * stand, t, lamb=True, flip=True, seed=5, legs=stand > 0.3)
            c.restore()
    else:
        sheep(c, 770, 900, 1.0, t, lamb=True, flip=True, seed=5)


# ---------------------------------------------------------------- WINTER
@scene("W01", sfx=lambda S: tag_sfx(S) + [(1.0, "crunch"), (3.0, "crunch"), (5.0, "crunch")])
def w01(c, t, S):
    def world(c, t, S):
        season_bg(c, "winter", t, seed=1)
        for i, x in enumerate((90, 330, 560)):
            tree(c, x, 850, 0.9, "pine", t, seed=i, snow=True)
        # tape measure tree
        tx, ty = 860, 960
        tree(c, tx, ty, 1.45, "pine", t, seed=9, snow=True)
        p = ease(prog(t, P(S, 2), 3.0))
        th = 470 * p
        box(c, tx + 26, ty - 60, 70, 56, 12, GOLD, 5)
        circle(c, tx + 61, ty - 32, 14, INK, 0)
        if th > 4:
            fill_ink(c, lambda: rrect(c, tx + 40, ty - 60 - th, 26, th, 3), hx("ffe04a"), 4, shading=0)
            for k in range(int(th / 24)):
                yy = ty - 66 - k * 24
                stroke(c, lambda: (c.move_to(tx + 42, yy), c.line_to(tx + (56 if k % 4 == 0 else 50), yy)), INK, 3)
        # family pulling a sled with a cut tree
        x, walking = walk_x(t, 0.0, -100, 560, 140)
        ph = t * 7 if walking else None
        sx = x - 300
        stroke(c, lambda: (c.move_to(x - 40, 900), c.line_to(sx + 150, 1000)), hx("6b4a2a"), 4)
        c.save(); c.translate(sx, 1010)
        box(c, -170, -26, 330, 26, 10, TOMATO, 5)
        stroke(c, lambda: (c.move_to(-190, 6), c.line_to(170, 6), c.curve_to(200, 6, 205, -20, 190, -30)), INK, 7)
        c.save(); c.translate(-10, -60); c.rotate(-math.pi / 2 + 0.02)
        tree(c, 0, 180, 0.7, "pine", 0, seed=4, snow=True, sway=0)
        c.restore()
        c.restore()
        person(c, x, 1010, 1.0, t, seed=1, hat="beanie", scarf=TOMATO, walk=ph,
               pose=((1.1, -0.4), (0.3, 0.2)) if walking else ((1.0, -0.3), (0.2, 0.2)))
        person(c, x - 120, 1030, 0.95, t, seed=4, hat="cap", scarf=GOLD, walk=ph + 1.5 if ph else None)
        person(c, x + 110, 1040, 0.95, t, seed=6, kid=True, hat="beanie", walk=ph + 0.7 if ph else None,
               look=0.6)
        weather(c, "snow", t)
    event_scene(c, t, S, world)


@scene("W02", sfx=lambda S: tag_sfx(S) + [(0.3, "car")])
def w02(c, t, S):
    def world(c, t, S):
        season_bg(c, "winter", t, seed=2)
        tree(c, 1060, 840, 0.8, "pine", t, snow=True)
        barn(c, 760, 860, 0.95, snow=True, lit=0.4)
        fence(c, 420, 1100, 1000, 0.8, snow=True)
        reindeer(c, 730, 990, 0.95, t, flip=True, chew=max(0, math.sin(t * 6)) if t > P(S, 3) else 0)
        reindeer(c, 960, 960, 0.7, t + 1, flip=False, seed=2)
        cx_ = lerp(-420, 170, ease_out(prog(t, 0.2, 3.2)))
        car(c, cx_, 1050, 0.95, SKY, t, moving=1 - prog(t, 2.6, 0.8))
        # child holds out feed
        kx = 470
        if t > 3.0:
            a = ease(prog(t, 3.0, 0.8))
            person(c, kx, 1060, 1.0, t, seed=3, kid=True, hat="beanie", scarf=GOLD, look=1,
                   pose=((lerp(0.2, 1.5, a), 0.1), (0.2, 0.2)))
        else:
            person(c, kx, 1060, 1.0, t, seed=3, kid=True, hat="beanie", scarf=GOLD, look=1)
        weather(c, "snow", t, 80)
    event_scene(c, t, S, world)


@scene("W03", sfx=tag_sfx)
def w03(c, t, S):
    def world(c, t, S):
        season_bg(c, "winter", t, tod="night", seed=3)
        lantern_string(c, -40, 1200, 160, 110, 14, t, (GOLD, TOMATO, hx("8fd0ff")))
        cols = [TOMATO, GOLD, hx("e86aa6"), hx("8fd0ff"), WHITE, hx("b36ae8")]
        for row in range(6):
            yy = 830 + row * 42
            s = 0.6 + row * 0.18
            for i in range(26 - row * 2):
                x = -20 + i * (1240 / (26 - row * 2)) + (row % 2) * 20
                k = (i + row) % len(cols)
                tw_ = 0.5 + 0.5 * math.sin(t * 2.5 + i * 0.8 + row)
                sweep_x = (t - P(S, 3) - 3.0) * 420
                if 0 < sweep_x < 1700 and abs(x - sweep_x) < 160:
                    tw_ = 1.0 + 0.8 * (1 - abs(x - sweep_x) / 160)
                tulip(c, x, yy, s, cols[k], t, seed=i + row * 7, glow_=tw_)
        # path + couple walking
        x, w_ = walk_x(t, 0.5, -200, 700, 90)
        person(c, x, 1010, 0.9, t, seed=7, hat="beanie", scarf=TOMATO, walk=t * 5 if w_ else None, look=0.5)
        person(c, x + 110, 1020, 0.88, t, seed=8, hat="bun", scarf=GOLD, walk=t * 5 + 1 if w_ else None, look=-0.3)
    event_scene(c, t, S, world)


@scene("W04", sfx=tag_sfx)
def w04(c, t, S):
    def world(c, t, S):
        interior(c, t=t)
        window(c, 860, 200, 240, 200, mini_snow_view, t)
        for (x, y) in ((140, 820), (280, 820), (210, 760)):
            hay_bale(c, x, y + 60, 1.0)
        glow(c, 620, 600, 420, hx("ffcf6a"), 0.3)
        # Santa on a chair
        box(c, 520, 600, 200, 300, 20, TOMATO, 6)
        box(c, 500, 780, 240, 60, 14, shade(TOMATO, 0.15), 6)
        c.save(); c.translate(620, 900)
        person(c, 0, 0, 1.05, t, seed=11, coat=TOMATO, hat="santa", skin=SKINS[0], hair=WHITE, bottom=TOMATO,
               pose=((0.6 + 0.5 * max(0, math.sin(t * 3)) * prog(t, 3, 1), 1.2), (0.5, 0.8)), mouth=0.5 * max(0, math.sin(t * 4)) ** 6)
        fill_ink(c, lambda: smooth(c, [(-44, -262), (-20, -252), (0, -256), (20, -252), (44, -262), (40, -222), (0, -196), (-40, -222)]), WHITE, 5)
        oval(c, 0, -258, 12, 6, hx("7a1f2b"), 3, shading=0)
        c.restore()
        # child with a toy walks up
        x, w_ = walk_x(t, 0.6, -150, 380, 110)

        def teddy(c, hands):
            hx_, hy_ = hands[1]
            circle(c, hx_ + 6, hy_ - 4, 22, hx("b07a4a"), 4)
            circle(c, hx_ + 6, hy_ - 36, 16, hx("b07a4a"), 4)
            circle(c, hx_ - 6, hy_ - 48, 6, hx("b07a4a"), 3)
            circle(c, hx_ + 18, hy_ - 48, 6, hx("b07a4a"), 3)
        person(c, x, 1010, 1.0, t, seed=5, kid=True, hat="bun", walk=t * 6 if w_ else None, look=1,
               pose=((0.2, 0.2), (1.0, 1.3)), hold=teddy, coat=hx("8e5aa8"))
    event_scene(c, t, S, world)


@scene("W05", sfx=tag_sfx)
def w05(c, t, S):
    def world(c, t, S):
        season_bg(c, "winter", t, tod="dusk", seed=5)
        tree(c, 1080, 860, 0.9, "pine", t, snow=True)
        tent(c, 560, 1060, 1.3, 1.0)
        # diners behind the long table inside the tent
        for i in range(7):
            seated(c, 170 + i * 128, 960, 0.62, t, seed=i + 20, eat=True,
                   mouth=0.5 * max(0, math.sin(t * 2.2 + i * 1.3)) ** 6, hat=["beanie", None, None, "bun"][i % 4])
        table(c, 560, 1070, 980, 1.0, CREAM, plates=7)
        for i in range(7):
            steam(c, 170 + i * 128 + 20, 940, t, 0.9, seed=i)
        # patio heater
        box(c, 1120, 800, 18, 240, 4, hx("8c8f9e"), 5)
        flame(c, 1129, 800, 0.8, t)
        weather(c, "snow", t, 90)
    event_scene(c, t, S, world)


@scene("W06", sfx=lambda S: tag_sfx(S) + [(1.2, "crunch"), (4.0, "crunch")])
def w06(c, t, S):
    def world(c, t, S):
        season_bg(c, "winter", t, seed=6)
        for i, x in enumerate((120, 460, 820, 1100)):
            tree(c, x, 870, 1.0 + 0.1 * (i % 2), "bare", t, seed=i, snow=True)
        r = rng_for("snowdrops", 2)
        for i in range(140):
            x, y = r.uniform(-20, 1200), r.uniform(880, 1070)
            s = 0.5 + (y - 880) / 300
            nod = math.sin(t * 1.6 + i) * 0.15
            c.save(); c.translate(x, y); c.scale(s, s)
            stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -30, 8, -46, 16, -42)), LEAF, 4)
            c.translate(16, -40); c.rotate(nod)
            fill_ink(c, lambda: (c.move_to(-8, 0), c.curve_to(-12, 20, 12, 20, 8, 0), c.close_path()), WHITE, 3)
            c.restore()
        x, w_ = walk_x(t, 0.3, -150, 760, 85)
        ph = t * 4.5 if w_ else None
        # guide with a flag
        person(c, x, 990, 0.85, t, seed=12, hat="straw", walk=ph, pose=((2.4, 0.2), (0.2, 0.2)) if True else None,
               coat=LEAF)
        stroke(c, lambda: (c.move_to(x + 70, 760 + 80), c.line_to(x + 80, 640)), INK, 6)
        fill_ink(c, lambda: poly(c, [(x + 80, 640), (x + 150 + math.sin(t * 6) * 6, 660), (x + 80, 690)]), GOLD, 4)
        for k in range(4):
            person(c, x - 130 - k * 105, 1000 + (k % 2) * 25, 0.8, t, seed=13 + k, walk=ph + k if ph else None,
                   hat=["beanie", "bun", "cap", None][k], scarf=[TOMATO, GOLD, SKY, LEAF][k])
    event_scene(c, t, S, world)


@scene("W07", sfx=tag_sfx)
def w07(c, t, S):
    def world(c, t, S):
        interior(c, wall=hx("7a2f45"), floor=hx("5a2a3a"), plank=False, floor_y=900, lights=False, t=t)
        # heart garland
        for i in range(9):
            x = 60 + i * 130
            y = 110 + math.sin(i * 0.9) * 20 + math.sin(t * 2 + i) * 4
            c.save(); c.translate(x, y); c.scale(0.7, 0.7)
            fill_ink(c, lambda: (c.move_to(0, 30), c.curve_to(-50, -4, -20, -44, 0, -16), c.curve_to(20, -44, 50, -4, 0, 30)),
                     [TOMATO, hx("f29ab0")][i % 2], 5)
            c.restore()
        stroke(c, lambda: (c.move_to(0, 100), c.curve_to(400, 160, 800, 60, 1200, 120)), GOLD, 3)
        # table
        box(c, -40, 640, 2000, 60, 10, hx("f6e7d0"), 6)
        fill_ink(c, lambda: (c.move_to(-40, 680), c.line_to(1960, 680), c.line_to(1960, 1080), c.line_to(-40, 1080),
                             c.close_path()), hx("f6e7d0"))
        for x in (120, 1040):
            candle(c, x, 640, t, seed=x)
        # champagne glasses with bubbles
        for gx in (240, 900):
            fill_ink(c, lambda: (c.move_to(gx - 30, 470), c.line_to(gx + 30, 470), c.line_to(gx + 22, 580),
                                 c.line_to(gx - 22, 580), c.close_path()), (1, 0.93, 0.6, 0.85), 5, shading=0)
            stroke(c, lambda: (c.move_to(gx, 580), c.line_to(gx, 630)), INK, 5)
            oval(c, gx, 636, 30, 8, (1, 1, 1, 0.8), 4)
            for b in range(6):
                ph = (t * 0.7 + b / 6) % 1
                c.arc(gx - 14 + (b * 7) % 28, 575 - ph * 95, 3.5, 0, 6.3); setc(c, WHITE, 0.9 * (1 - ph)); c.fill()
        # seven plates arriving in turn
        n = 1 + int(clamp((t - 0.6) / max(S.dur - 2.5, 1)) * 7)
        n = min(7, max(0, n if t > 0.6 else 0))
        foods = [hx("e4a95a"), LEAF, TOMATO, hx("b36ae8"), GOLD, hx("8a5a3a"), hx("f29ab0")]
        for i in range(n):
            st = 0.6 + i * (S.dur - 2.5) / 7
            p = ease_out(prog(t, st, 0.6))
            px = 160 + i * 140
            py = 790 if i % 2 == 0 else 900
            px_ = lerp(1300, px, p)
            oval(c, px_, py, 62, 22, WHITE, 5)
            oval(c, px_, py - 6, 30, 12, foods[i], 4)
        text(c, f"{n} of 7", 1040, 1040, 54, BODY, hx("7a2f45"), "center", alpha=prog(t, 1.0, 0.6))
    event_scene(c, t, S, world)


@scene("W08", sfx=lambda S: tag_sfx(S) + [(P(S, 1), "baa")])
def w08(c, t, S):
    def world(c, t, S):
        lambing_barn(c, t, close=True, birth_t=0.4, gallery_crowd=True)
    event_scene(c, t, S, world, zoom=(1.08, 1.14), focus=(620, 780))


# ---------------------------------------------------------------- SPRING
def mud(c, seed=1, n=6):
    r = rng_for("mud", seed)
    for i in range(n):
        oval(c, r.uniform(0, 1150), r.uniform(900, 1060), r.uniform(70, 150), r.uniform(14, 26), MUD, 4, shading=0.1)


@scene("S01", sfx=lambda S: tag_sfx(S) + [(1.4 + k * 1.6, "drip") for k in range(int(S.dur / 1.6))])
def s01(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=11)
        mud(c, 3, 4)
        for x in (60, 1060):
            tree(c, x, 880, 1.0, "bare", t, seed=int(x))
        # maple with tap + bucket
        mx = 330
        tree(c, mx, 1000, 1.5, "bare", t, seed=21, sway=0.3)
        box(c, mx + 22, 760, 40, 12, 4, hx("9aa0b0"), 4)
        bucket(c, mx + 56, 900, 0.9)
        ph = (t * 0.62) % 1
        dy = 772 + ph ** 2 * 64
        if ph < 0.92:
            oval(c, mx + 58, dy, 6, 9, hx("e8b65a"), 3, shading=0)
        lvl = clamp(t / S.dur)
        oval(c, mx + 56, 840 + 10 * (1 - lvl), 38, 7, hx("e8b65a"), 0, shading=0)
        # griddle + pancakes flipping
        gx = 820
        box(c, gx - 220, 860, 440, 30, 8, WOOD, 5)
        for lx in (gx - 190, gx + 190):
            box(c, lx - 8, 890, 16, 150, 3, shade(WOOD, 0.2), 4)
        box(c, gx - 170, 830, 340, 30, 8, hx("4a4a5a"), 5)
        for i, px in enumerate((gx - 100, gx + 10, gx + 110)):
            fp = ((t + i * 0.9) % 3.0) / 3.0
            lift = math.sin(min(fp, 0.4) / 0.4 * math.pi) * 150 if fp < 0.4 else 0
            ang = min(fp, 0.4) / 0.4 * math.pi
            c.save(); c.translate(px, 822 - lift); c.scale(1, abs(math.cos(ang)) * 0.9 + 0.1)
            oval(c, 0, 0, 46, 12, hx("e4a95a"), 4)
            c.restore()
        steam(c, gx, 800, t, 1.2)
        # stack + syrup
        for k in range(4):
            oval(c, gx + 260, 860 - k * 14, 44, 11, hx("e4a95a"), 4)
        person(c, gx - 260, 1040, 1.0, t, seed=31, hat="cap", apron=WHITE, coat=hx("2f8f8a"),
               pose=((1.3 + 0.3 * math.sin(t * 3), 0.6), (0.3, 0.2)))
        weather(c, "petals", t, 18)
    event_scene(c, t, S, world)


@scene("S02", sfx=lambda S: tag_sfx(S) + [(1.5 + k * 1.3, "snip") for k in range(int((S.dur - 2) / 1.3))])
def s02(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=12)
        trees = [(180, 870), (560, 870), (940, 870)]
        for i, (x, y) in enumerate(trees):
            tree(c, x, y, 0.95, "blossom" if i == 1 else "bare", t, seed=40 + i)
        # tag tied on a branch
        bx, by = 610, 600
        ang = math.sin(t * 2.2) * 0.25
        c.save(); c.translate(bx, by); c.rotate(ang)
        stroke(c, lambda: (c.move_to(0, 0), c.line_to(0, 50)), INK, 3)
        box(c, -24, 50, 48, 64, 8, GOLD, 4)
        circle(c, 0, 62, 5, WHITE, 2)
        c.restore()
        # ten people with pruners, two rows
        for k in range(10):
            row = k // 5
            x = 90 + (k % 5) * 230 + row * 110
            y = 960 + row * 70
            snip = max(0, math.sin(t * 5 + k)) ** 4
            person(c, x, y, 0.62 + row * 0.08, t, seed=50 + k, hat=["straw", "cap", None, "bun", "beanie"][k % 5],
                   pose=((2.0 + 0.2 * snip, 0.4), (0.3, 0.2)), look=0.3)
        # falling twigs
        for k in range(4):
            ph = (t * 0.5 + k / 4) % 1
            x = 200 + k * 260
            c.save(); c.translate(x + ph * 30, 640 + ph * 300); c.rotate(ph * 5)
            stroke(c, lambda: (c.move_to(-20, 0), c.line_to(20, 0), c.move_to(5, 0), c.line_to(15, -10)), hx("7a5236"), 5,
                   1 - ph)
            c.restore()
    event_scene(c, t, S, world)


@scene("S03", sfx=lambda S: [(P(S, 0), "flip"), (P(S, 2) - 0.05, "chime"), (tag_time(S), "tag"),
                             (P(S, 5) + 0.3, "thud")])
def s03(c, t, S):
    t_cut = P(S, 2) - 0.05
    if t < t_cut:
        # mystery card flips, then a hard stop (the beat)
        setc(c, hx("3f8f3a")); c.paint()
        season_bg(c, "spring", t, seed=13, layers=(0, 1, 2, 3))
        c.set_source_rgba(0.1, 0.12, 0.23, 0.35); c.paint()
        fp = prog(t, P(S, 0) + 0.2, 0.7)
        sx = abs(math.cos(fp * math.pi))
        c.save(); c.translate(960, 560); c.scale(max(sx, 0.02), 1)
        box(c, -260, -340, 520, 680, 34, PAPER if fp < 0.5 else GOLD, 8)
        if fp < 0.5:
            text(c, "No. 11", 0, -150, 110, DISPLAY, INK, "center")
            text(c, "?", 0, 180, 300, DISPLAY, TOMATO, "center")
        else:
            text(c, "No. 11", 0, -150, 110, DISPLAY, INK, "center")
            from icons import icon
            icon(c, 10, 0, 110, 150, ring=False)
        c.restore()
        overlay_tracker(c, t, S)
        return

    def world(c, t, S):
        tt = t
        season_bg(c, "spring", tt, seed=14)
        greenhouse(c, 560, 880, 1.6)
        # table with soil trays, seed packets and labels
        box(c, 40, 760, 1080, 40, 10, WOOD, 6)
        for lx in (80, 1080):
            box(c, lx - 10, 800, 20, 240, 4, shade(WOOD, 0.2), 5)
        for i in range(4):
            x = 110 + i * 230
            box(c, x, 690, 200, 74, 10, hx("6b4a2a"), 5)
            for j in range(4):
                sp = ease_back(prog(t, P(S, 3) + 0.5 + i * 0.8 + j * 0.3, 0.7))
                if sp > 0:
                    sx_ = x + 30 + j * 46
                    stroke(c, lambda: (c.move_to(sx_, 692), c.line_to(sx_, 692 - 34 * sp)), LEAF, 5)
                    oval(c, sx_ - 9 * sp, 692 - 34 * sp, 10 * sp, 5 * sp, LEAF, 3)
                    oval(c, sx_ + 9 * sp, 692 - 38 * sp, 10 * sp, 5 * sp, LEAF, 3)
        for i, col in enumerate((TOMATO, GOLD, LEAF)):
            c.save(); c.translate(230 + i * 300, 860); c.rotate(-0.1 + i * 0.1)
            box(c, -50, -70, 100, 130, 8, col, 5)
            box(c, -34, -46, 68, 50, 6, PAPER, 3)
            c.restore()
        # labels (plant markers)
        for i in range(4):
            box(c, 270 + i * 230, 640, 22, 60, 4, PAPER, 3)
        # hands planting seeds
        hx_ = 300 + ((t * 120) % 700)
        hy_ = 600 + math.sin(t * 4) * 10
        limb2(c, [(hx_ + 90, hy_ - 230), (hx_ + 30, hy_ - 70), (hx_, hy_)], 40, hx("2f8f8a"), 6)
        circle(c, hx_, hy_, 28, SKIN, 5)
        for k in range(3):
            ph = (t * 1.5 + k / 3) % 1
            circle(c, hx_ + k * 6 - 6, 630 + ph * 60, 5, hx("6b4a2a"), 2)
        if t > P(S, 5) + 0.3:
            k = clamp((t - P(S, 5) - 0.3) / 0.25)
            stamp(c, 600, 420, lerp(2.2, 1.25, ease_out(k)), "SOLD OUT", alpha=k)
    event_scene(c, t, S, world, banner_ph=2)


@scene("S05", sfx=lambda S: tag_sfx(S) + [(1.0, "baa")])
def s05(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=15)
        house(c, 920, 860, 0.9)
        # farmhouse lunch with six places
        box(c, 700, 900, 400, 26, 8, CREAM, 5)
        for i in range(6):
            x = 730 + i * 66
            pp = ease_back(prog(t, P(S, 3) + i * 0.12, 0.4))
            if pp <= 0:
                continue
            box(c, x - 14 * pp, 930, 28 * pp, 50, 4, WOOD, 3)
            oval(c, x, 896, 24 * pp, 7 * pp, WHITE, 3)
            steam(c, x, 880, t, 0.5, seed=i, a=0.5)
        sheep(c, 200, 1010, 1.0, t, seed=9, bleat=0.6 * max(0, math.sin(t * 1.2)) ** 10)

        def lamb_hold(c, hands):
            (rx, ry), (lx, ly) = hands[1], hands[-1]
            sheep(c, (rx + lx) / 2 + 10, max(ry, ly) + 50, 0.62, t, lamb=True, flip=True, seed=4)
        reach = ease(prog(t, P(S, 2) + 3.5, 1.0))
        kneel(c, 470 - 40 * reach, 1010, 1.0, t, seed=17, coat=DENIM, hold=lamb_hold, hat="cap", reach=reach)
        if t > P(S, 2) + 3.0:
            fx_, w_ = walk_x(t, P(S, 2) + 3.0, 1250, 760, 120)
            person(c, fx_, 1060, 0.95, t, seed=19, hat="straw", coat=LEAF, walk=t * 5 if w_ else None, look=-1)
        weather(c, "petals", t, 20)
    event_scene(c, t, S, world)


@scene("S06", sfx=lambda S: tag_sfx(S) + [(2.0, "baa")])
def s06(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=16)
        fence(c, 0, 1160, 860, 0.7)
        coats = [TOMATO, GOLD, SKY]
        for i, x in enumerate((180, 540, 900)):
            laugh = 0.3 + 0.7 * max(0, math.sin(t * 5 + i)) ** 2
            person(c, x, 1010, 0.95, t, seed=60 + i, mouth=laugh, pose=((1.2, 1.0), (1.2, 1.0)),
                   hat=[None, "straw", "beanie"][i], look=0.4 * (-1) ** i)
            hay_bale(c, x, 1050, 1.25)
            hop = abs(math.sin(t * 2.2 + i * 1.3)) * 50
            goat(c, x + (40 if i % 2 else -40), 965 - hop, 0.72, t, coat=coats[i], seed=i, flip=i % 2 == 1)
        gx, _ = walk_x(t, 0.5, 1150, 900, 60)
        goat(c, gx, 1070, 0.85, t, coat=LEAF, seed=0, flip=True, pose="trot")
        weather(c, "petals", t, 16)
    event_scene(c, t, S, world)


@scene("S07", sfx=tag_sfx)
def s07(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=17)
        barn(c, 980, 860, 0.7, lit=0.0)
        oval(c, 560, 990, 620, 110, hx("f2d27a"), 5, shading=0.06)
        r = rng_for("straw2", 3)
        for i in range(70):
            sx, sy = r.uniform(0, 1150), r.uniform(900, 1080)
            stroke(c, lambda: (c.move_to(sx, sy), c.line_to(sx + r.uniform(-24, 24), sy + r.uniform(-6, 6))), hx("e8c15a"), 4)
        eggs = [(160, 960, hx("8fd0f0")), (330, 1030, hx("f29ab0")), (620, 950, GOLD), (760, 1040, hx("b36ae8")),
                (920, 980, LEAF), (1080, 1050, TOMATO)]
        for i, (x, y, col) in enumerate(eggs):
            found = t > 1.5 + i * 1.4
            if not found:
                oval(c, x, y, 18, 24, col, 4)
                stroke(c, lambda: (c.move_to(x - 16, y), c.line_to(x - 4, y - 6), c.line_to(x + 6, y + 4), c.line_to(x + 16, y - 4)),
                       WHITE, 3)

        def basket(n):
            def h(c, hands):
                hx_, hy_ = hands[1]
                for k in range(n):
                    oval(c, hx_ - 18 + k * 12, hy_ - 6, 10, 13, eggs[k][2], 3)
                fill_ink(c, lambda: (c.move_to(hx_ - 36, hy_ - 6), c.line_to(hx_ + 36, hy_ - 6), c.line_to(hx_ + 26, hy_ + 30),
                                     c.line_to(hx_ - 26, hy_ + 30), c.close_path()), hx("c8955a"), 4)
                stroke(c, lambda: c.arc(hx_, hy_ - 6, 34, math.pi, 2 * math.pi), hx("8a5a3a"), 5)
            return h
        nfound = sum(1 for i in range(6) if t > 1.5 + i * 1.4)
        x1, w1 = walk_x(t, 0.4, -100, 640, 70)
        person(c, x1, 1030, 1.0, t, seed=70, kid=True, hat="bun", walk=t * 6 if w1 else None,
               pose=((0.4, 0.4), (0.3, 0.2)), hold=basket((nfound + 1) // 2), coat=hx("f29ab0"))
        x2, w2 = walk_x(t, 1.0, 1250, 860, 60)
        person(c, x2, 1060, 1.0, t, seed=71, kid=True, hat="cap", walk=t * 6 if w2 else None,
               pose=((0.4, 0.4), (0.3, 0.2)), hold=basket(nfound // 2))
        chicken(c, 260, 900, 0.9, t, seed=1)
        for k in range(5):
            chick(c, 340 + k * 40, 930 + (k % 2) * 16, 0.9, t, seed=k)
    event_scene(c, t, S, world)


@scene("S08", sfx=tag_sfx)
def s08(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=18, layers=(0, 1))
        cols = [TOMATO, GOLD, hx("e86aa6"), WHITE, hx("b36ae8"), TOMATO, GOLD]
        hz = 690
        for i in range(7):
            y0, y1 = hz + i * (H - hz) / 7, hz + (i + 1) * (H - hz) / 7
            c.rectangle(-10, y0, 1940, y1 - y0)
            setc(c, cols[i]); c.fill()
            c.rectangle(-10, y1 - 10, 1940, 10); setc(c, hx("5a8f3a")); c.fill()
            s = 0.4 + i * 0.25
            for k in range(int(40 - i * 4)):
                tulip(c, k * (1940 / (40 - i * 4)) + (i % 2) * 20, y1 - 4, s, cols[i], t, seed=k + i)
        # picker with a basket filling
        n = int(clamp(t / S.dur) * 9)

        def basket(c, hands):
            hx_, hy_ = hands[-1]
            for k in range(n):
                tulip(c, hx_ - 30 + k * 8, hy_ - 4, 0.6, cols[k % 5], 0)
            fill_ink(c, lambda: (c.move_to(hx_ - 50, hy_), c.line_to(hx_ + 50, hy_), c.line_to(hx_ + 36, hy_ + 50),
                                 c.line_to(hx_ - 36, hy_ + 50), c.close_path()), hx("c8955a"), 5)
        person(c, 560, 1060, 1.2, t, seed=81, hat="straw", coat=hx("8fd0f0"),
               pose=((1.3 + 0.4 * max(0, math.sin(t * 2.5)) ** 2, 0.2 + 0.4 * max(0, math.sin(t * 2.5))), (0.9, 1.0)),
               hold=basket)
        weather(c, "petals", t, 14)
    event_scene(c, t, S, world)


@scene("S09", sfx=tag_sfx)
def s09(c, t, S):
    def world(c, t, S):
        season_bg(c, "spring", t, seed=19)
        barn(c, 1020, 860, 0.7)
        # sheepdog circling
        a = t * 0.9
        dx, dy = 560 + math.cos(a) * 420, 880 + math.sin(a) * 40
        dog(c, dx, dy, 0.8, t, flip=math.sin(a) > 0, run=1)
        wl = 1 - 0.6 * ease(prog(t, 1.0, S.dur - 2))
        sheep(c, 420, 1020, 1.4, t, wool_amt=wl, seed=6)
        # wool falling away
        for k in range(6):
            ph = (t * 0.45 + k / 6) % 1
            if t > 1.0:
                wool(c, 330 + k * 40 + ph * 30, 900 + ph * 140, 24, 15, CREAM, n=6, lw=4)
        person(c, 700, 1040, 1.05, t, seed=91, hat="cap", coat=hx("2f8f8a"),
               pose=((1.3, 0.9 + 0.3 * math.sin(t * 6)), (1.0, 0.8)))
        box(c, 590, 860 + math.sin(t * 6) * 10, 50, 22, 6, hx("8c8f9e"), 4)
    event_scene(c, t, S, world)


# ---------------------------------------------------------------- SUMMER
def tabletop(c, x, y, s, t, seed, coat):
    """Person in table pose on a yoga mat."""
    c.save(); c.translate(x, y); c.scale(s, s)
    skin = SKINS[(seed * 3 + 2) % len(SKINS)]
    limb2(c, [(-60, -100), (-62, -14), (-150, -14)], 30, hx("39457a"), 5)
    limb2(c, [(70, -110), (76, -8)], 26, coat, 5)
    circle(c, 80, -8, 13, skin, 4)
    fill_ink(c, lambda: rrect(c, -90, -140, 190, 64, 32), coat)
    circle(c, 110, -100, 36, skin, 5)
    fill_ink(c, lambda: (c.new_sub_path(), c.arc(110, -100, 36, math.pi * 1.1, math.pi * 1.9)), HAIR[seed % 6], 4)
    circle(c, 122, -96, 3.5, INK, 0)
    c.restore()


@scene("U01", sfx=tag_sfx)
def u01(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, seed=21)
        mats = [(220, 900, hx("8e5aa8")), (600, 910, hx("2f8f8a")), (960, 900, TOMATO), (400, 1010, GOLD), (790, 1020, SKY)]
        for i, (x, y, col) in enumerate(mats):
            fill_ink(c, lambda: (c.move_to(x - 150, y), c.line_to(x + 150, y), c.line_to(x + 170, y + 30),
                                 c.line_to(x - 170, y + 30), c.close_path()), col, 5)
            tabletop(c, x - 10, y + 10, 0.9, t, i, [CREAM, LEAF, hx("f29ab0"), WHITE, GOLD][i])
        # goats hopping from back to back
        for g in range(2):
            seq = [0, 1, 2, 4, 3] if g == 0 else [3, 4, 1, 0, 2]
            per = 2.4
            k = int((t + g * 1.2) / per) % len(seq)
            u = ((t + g * 1.2) % per) / per
            a, b = mats[seq[k]], mats[seq[(k + 1) % len(seq)]]
            if u < 0.7:
                gx, gy = a[0], a[1] - 118
                goat(c, gx, gy, 0.75, t, seed=g, flip=g == 1)
            else:
                v = (u - 0.7) / 0.3
                gx = lerp(a[0], b[0], v)
                gy = lerp(a[1], b[1], v) - 118 - math.sin(v * math.pi) * 70
                goat(c, gx, gy, 0.75, t, seed=g, flip=b[0] < a[0], pose="trot")
        weather(c, "heat", t)
    event_scene(c, t, S, world)


@scene("U02", sfx=lambda S: tag_sfx(S) + [(2.0 + k * 1.8, "snip") for k in range(int((S.dur - 3) / 1.8))])
def u02(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, seed=22, layers=(0, 1, 2))
        cols = [hx("e86aa6"), GOLD, TOMATO, hx("f6f0e0"), hx("b36ae8"), hx("ff9a3a")]
        hz = 760
        for i in range(6):
            y = hz + i * 60
            c.rectangle(-10, y, 1940, 70); setc(c, hx("5a9a3a")); c.fill()
            r = rng_for("ff", i)
            for k in range(int(38 - i * 3)):
                x = k * 1940 / (38 - i * 3) + r.uniform(-10, 10)
                s = 0.45 + i * 0.16
                sw = math.sin(t * 1.4 + k + i) * 3
                c.save(); c.translate(x + sw, y + 50); c.scale(s, s)
                for p in range(6):
                    a = p * math.pi / 3
                    circle(c, math.cos(a) * 14, -40 + math.sin(a) * 14, 10, cols[(k + i) % 6], 2)
                circle(c, 0, -40, 8, GOLD, 2)
                c.restore()
        n = int(clamp((t - 1) / (S.dur - 2)) * 8)

        def bkt(c, hands):
            hx_, hy_ = hands[-1]

            def fl(c):
                for k in range(n):
                    circle(c, -30 + (k % 4) * 20, -80 - (k // 4) * 18, 14, cols[k % 6], 3)
            bucket(c, hx_, hy_ + 80, 0.8, fill=fl)
        person(c, 560, 1060, 1.15, t, seed=101, hat="straw", coat=hx("2f8f8a"),
               pose=((1.6 + 0.3 * math.sin(t * 2), 0.3), (0.3, 0.1)), hold=bkt)
        weather(c, "heat", t, 14)
    event_scene(c, t, S, world)


@scene("U03", sfx=lambda S: tag_sfx(S) + [(1.0, "buzz")])
def u03(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, seed=23, layers=(0, 1))
        vx, vy = 600, 640
        for i in range(-9, 10):
            c.move_to(vx + i * 8, vy)
            c.line_to(560 + i * 170, H + 20)
            c.line_to(560 + i * 170 + 110, H + 20)
            c.line_to(vx + i * 8 + 5, vy)
            c.close_path()
            setc(c, hx("8e6ad8") if i % 2 == 0 else hx("6aa84a")); c.fill()
        c.rectangle(0, vy - 6, W, 12); setc(c, hx("7a5ac8")); c.fill()
        # picnic bench
        bx = 860
        box(c, bx - 170, 900, 340, 26, 8, WOOD, 5)
        box(c, bx - 190, 970, 380, 20, 6, WOOD, 5)
        for lx in (bx - 140, bx + 140):
            stroke(c, lambda: (c.move_to(lx, 926), c.line_to(lx - 20, 1060)), INK, 14)
            stroke(c, lambda: (c.move_to(lx, 926), c.line_to(lx - 20, 1060)), WOOD, 8)
        person(c, bx - 90, 1000, 0.9, t, seed=111, hat="straw", pose=((1.2, 1.4), (0.5, 0.3)), mouth=0.4 * max(0, math.sin(t * 3)) ** 4)
        person(c, bx + 90, 1000, 0.9, t, seed=112, hat="bun", pose=((0.5, 0.3), (1.2, 1.4)), look=-0.6)
        fill_ink(c, lambda: rrect(c, bx - 40, 860, 80, 44, 8), hx("c8955a"))
        stroke(c, lambda: c.arc(bx, 862, 34, math.pi, 2 * math.pi), hx("8a5a3a"), 5)
        for k in range(5):
            bee(c, 200 + k * 180 + math.sin(t * 2 + k) * 50, 780 + math.sin(t * 3 + k * 2) * 40, 1.0, t + k)
        weather(c, "heat", t, 10)
    event_scene(c, t, S, world)


@scene("U04", sfx=lambda S: tag_sfx(S) + [(1.5, "cluck")])
def u04(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, seed=24)
        # hay wagon with waving kids passes behind
        wx = lerp(-500, 1300, (t / max(S.dur, 1)))
        c.save(); c.translate(wx, 860)
        box(c, -240, -90, 380, 70, 10, hx("e8c15a"), 5)
        for k in range(4):
            person(c, -200 + k * 90, -80, 0.5, t, seed=120 + k, kid=True, hat="straw",
                   pose=((2.6, 0.4 + 0.4 * math.sin(t * 8 + k)), (0.3, 0.2)))
        box(c, -250, -40, 400, 30, 6, WOOD, 5)
        for wx_ in (-180, 80):
            circle(c, wx_, 0, 34, INK, 4); circle(c, wx_, 0, 14, hx("c9c6c0"), 3)
        box(c, 170, -110, 150, 90, 14, TOMATO, 5)
        circle(c, 280, 0, 44, INK, 4); circle(c, 190, 10, 30, INK, 4)
        c.restore()
        # kids in hats feeding chickens
        for k in range(3):
            x = 220 + k * 300
            throw = max(0, math.sin(t * 2.5 + k * 2))
            person(c, x, 1040, 1.0, t, seed=130 + k, kid=True, hat="straw" if k != 1 else "cap",
                   pose=((0.8 + throw * 0.7, 0.2), (0.6, 1.4)), look=0.6, mouth=0.3 * throw)
            for g in range(5):
                ph = ((t * 1.2 + g / 5 + k * 0.3) % 1)
                c.arc(x + 60 + ph * 90, 930 + ph * ph * 140, 4, 0, 6.3); setc(c, GOLD); c.fill()
        for k in range(6):
            chicken(c, 330 + k * 140 + math.sin(t * 0.7 + k) * 20, 1050 - (k % 2) * 30, 0.95, t, seed=k,
                    flip=k % 2 == 0, col=[CREAM, hx("c4692c"), WHITE][k % 3])
        weather(c, "heat", t, 10)
    event_scene(c, t, S, world)


@scene("U05", sfx=tag_sfx)
def u05(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, tod="sunset", seed=25)
        cols = [hx("e86aa6"), GOLD, TOMATO, WHITE]
        wx = lerp(-200, 650, ease(prog(t, 0, S.dur)))
        c.save(); c.translate(wx, 1010)
        # wagon + friends with buckets of blooms
        box(c, -380, -110, 560, 80, 12, hx("e8c15a"), 5)
        for k in range(4):
            def bk(c, hands, k=k):
                hx_, hy_ = hands[1]
                bucket(c, hx_ + 4, hy_ + 50, 0.55,
                       fill=lambda c: [circle(c, -20 + j * 20, -80, 14, cols[(j + k) % 4], 3) for j in range(3)])
            person(c, -320 + k * 140, -100, 0.75, t, seed=140 + k, hat=[None, "straw", "bun", None][k],
                   pose=((1.0, 1.0), (0.3, 0.2)), hold=bk, mouth=0.5 * max(0, math.sin(t * 3 + k)) ** 6)
        box(c, -400, -50, 600, 34, 6, WOOD, 5)
        for x_ in (-300, 100):
            circle(c, x_, -6, 40, INK, 4); circle(c, x_, -6, 16, hx("c9c6c0"), 3)
        box(c, 230, -150, 190, 120, 18, TOMATO, 5)
        box(c, 300, -230, 90, 90, 10, hx("ffdca0"), 5)
        circle(c, 380, 0, 52, INK, 4); circle(c, 260, 10, 36, INK, 4)
        c.restore()
        for k in range(16):
            x = k * 80
            sunflower(c, x, 1080, 0.55, t, seed=k)
    event_scene(c, t, S, world)


@scene("U06", sfx=lambda S: tag_sfx(S) + [(0.5, "buzz")])
def u06(c, t, S):
    def world(c, t, S):
        season_bg(c, "summer", t, seed=26)
        # hives
        for k, hx_ in enumerate((180, 760)):
            for j in range(3):
                box(c, hx_ - 90, 1000 - (j + 1) * 80, 180, 80, 6, [CREAM, GOLD, CREAM][j], 5)
            box(c, hx_ - 104, 1000 - 3 * 80 - 24, 208, 28, 6, WOOD, 5)
        # frame being lifted
        lift = ease(prog(t, 1.0, 2.0)) * 220
        fx, fy = 500, 760 - lift
        box(c, fx - 120, fy - 70, 240, 140, 6, WOOD, 6)
        c.save(); rrect(c, fx - 104, fy - 56, 208, 112, 4); c.clip()
        setc(c, hx("f6c03a")); c.paint()
        for i in range(10):
            for j in range(6):
                cx_ = fx - 100 + i * 24 + (j % 2) * 12
                cy_ = fy - 54 + j * 20
                poly(c, [(cx_ + 10 * math.cos(a), cy_ + 10 * math.sin(a)) for a in [k * math.pi / 3 for k in range(6)]])
                setc(c, hx("c9871a"), 0.7); c.set_line_width(2); c.stroke()
        c.restore()

        def frame_hold(c, hands):
            pass
        person(c, 380, 1060, 1.15, t, seed=151, coat=CREAM, bottom=CREAM, hat="bee",
               pose=((1.7 - lift / 400, 0.6), (1.5 - lift / 400, 0.6)))
        # tasting spoon with honey drip
        c.save(); c.translate(960, 760); c.rotate(-0.3)
        stroke(c, lambda: (c.move_to(-120, 0), c.line_to(40, 0)), INK, 16)
        stroke(c, lambda: (c.move_to(-120, 0), c.line_to(40, 0)), hx("c9c6c0"), 10)
        oval(c, 70, 0, 40, 22, hx("c9c6c0"), 6)
        oval(c, 70, -2, 30, 14, hx("f6a91a"), 0, shading=0)
        c.restore()
        ph = (t * 0.8) % 1
        oval(c, 1028, 770 + ph * 120, 8, 12 + ph * 6, hx("f6a91a"), 3, shading=0)
        for k in range(9):
            bee(c, 300 + math.sin(t * 1.3 + k * 1.7) * 330, 700 + math.cos(t * 1.7 + k) * 140, 1.0, t + k)
    event_scene(c, t, S, world)


@scene("U07", sfx=tag_sfx)
def u07(c, t, S):
    def world(c, t, S):
        setc(c, hx("e9f0ee")); c.paint()
        for i in range(0, W, 80):
            for j in range(0, 820, 80):
                c.rectangle(i + 3, j + 3, 74, 74); setc(c, hx("dfe8e6")); c.fill()
        c.rectangle(0, 820, W, H); setc(c, hx("9aa0b0")); c.fill()
        stroke(c, lambda: (c.move_to(0, 820), c.line_to(W, 820)), INK, 6)
        # vat
        box(c, 80, 560, 460, 300, 30, hx("c9cfdb"), 7)
        oval(c, 310, 566, 228, 30, hx("fdf8ec"), 6)
        a = t * 2
        stroke(c, lambda: (c.move_to(310 + math.cos(a) * 140, 566 + math.sin(a) * 18), c.line_to(330 + math.cos(a) * 60, 360)),
               WOOD, 14)
        for k in range(3):
            oval(c, 310 + math.cos(a + k * 2) * 120, 566 + math.sin(a + k * 2) * 14, 30, 6, hx("efe6cf"), 0, shading=0)
        # cheese cloth hanging, dripping
        stroke(c, lambda: (c.move_to(600, 160), c.line_to(1000, 160)), WOOD, 14)
        fill_ink(c, lambda: (c.move_to(700, 160), c.curve_to(680, 260, 720, 360, 780, 380), c.curve_to(840, 360, 880, 260,
                                                                                                      860, 160)), CREAM, 5)
        ph = (t * 0.9) % 1
        oval(c, 780, 400 + ph * 140, 6, 9, hx("dfe8f6"), 3, shading=0)
        # wheels of cheese stacking up
        n = 1 + int(clamp(t / (S.dur - 1)) * 6)
        for k in range(min(n, 7)):
            st = k * (S.dur - 1) / 6
            p = ease_back(prog(t, st, 0.5))
            yy = 800 - k * 52
            oval(c, 920 + (k % 2) * 6, yy - (1 - p) * 120, 120 * p if p > 0 else 0.1, 26 * max(p, 0.01), hx("f6d36a"), 5)
            box(c, 800 + (k % 2) * 6, yy - 26 - (1 - p) * 120, 240, 26, 4, hx("f6d36a"), 0, shading=0)
            oval(c, 920 + (k % 2) * 6, yy - 26 - (1 - p) * 120, 120, 26, hx("fbe48a"), 5)
        # person carrying a wheel home
        x, w_ = walk_x(t, 2.0, 600, 1300, 90)

        def wheel(c, hands):
            hx_, hy_ = hands[1]
            oval(c, hx_ - 30, hy_ - 16, 64, 22, hx("f6d36a"), 5)
        person(c, x, 1050, 1.0, t, seed=161, coat=WHITE, hat="cap", walk=t * 5 if w_ else None,
               pose=((1.3, 1.2), (1.3, 1.2)), hold=wheel)
    event_scene(c, t, S, world)


# ---------------------------------------------------------------- FALL
@scene("F01", sfx=tag_sfx)
def f01(c, t, S):
    def world(c, t, S):
        season_bg(c, "fall", t, tod="night", seed=31, layers=(0, 1))
        # constellation drawn progressively
        pts = [(260, 200), (380, 160), (500, 230), (620, 180), (720, 290), (860, 250)]
        p = prog(t, 2.0, 3.0) * (len(pts) - 1)
        for i in range(len(pts) - 1):
            k = clamp(p - i)
            if k > 0:
                a, b = pts[i], pts[i + 1]
                stroke(c, lambda: (c.move_to(*a), c.line_to(lerp(a[0], b[0], k), lerp(a[1], b[1], k))), hx("fff1c4"), 3, 0.7)
        for i, (x, y) in enumerate(pts):
            star(c, x, y, 13 + 3 * math.sin(t * 3 + i), hx("fff1c4"))
        # shooting star
        sp = (t % 6) / 1.2
        if sp < 1:
            sx, sy = 1000 - sp * 500, 120 + sp * 180
            stroke(c, lambda: (c.move_to(sx, sy), c.line_to(sx + 120, sy - 44)), WHITE, 4, 1 - sp)
        # dark hill
        c.move_to(0, H); c.line_to(0, 820); c.curve_to(300, 700, 800, 700, 1250, 840); c.line_to(1250, H); c.close_path()
        setc(c, hx("22306e")); c.fill_preserve(); setc(c, INK, 0.8); c.set_line_width(6); c.stroke()
        # telescope on tripod
        tx, ty = 520, 820
        for dx in (-50, 0, 50):
            stroke(c, lambda: (c.move_to(tx, ty - 110), c.line_to(tx + dx, ty)), INK, 8)
        c.save(); c.translate(tx, ty - 120); c.rotate(-0.6)
        box(c, -90, -26, 220, 52, 18, hx("c9cfdb"), 6)
        box(c, 110, -32, 34, 64, 8, GOLD, 5)
        c.restore()
        person(c, 330, 900, 1.0, t, seed=171, coat=hx("6b6b9a"), hat="beanie",
               pose=((2.6 + 0.1 * math.sin(t * 2), 0.1), (0.3, 0.2)), mouth=0.4 * max(0, math.sin(t * 3)) ** 4, look=0.5)
        person(c, 730, 930, 0.9, t, seed=172, kid=True, hat="beanie", look=-0.5, scarf=GOLD)
        person(c, 860, 940, 0.95, t, seed=173, hat="bun", look=-0.6, scarf=TOMATO)
    event_scene(c, t, S, world)


@scene("F02", sfx=tag_sfx)
def f02(c, t, S):
    def world(c, t, S):
        setc(c, hx("b88a3a")); c.paint()
        # overhead maze: corn blocks with paths
        x0, y0, cs = 40, 170, 62
        grid = ["################",
                "#....#.....#...#",
                "#.##.#.###.#.#.#",
                "#.#..#...#...#.#",
                "#.#.####.#####.#",
                "#.#......#.....#",
                "#.######.#.###.#",
                "#......#...#...#",
                "#.####.###.#.###",
                "#.............. ",
                "################"]
        for j, row in enumerate(grid):
            for i, ch in enumerate(row):
                x, y = x0 + i * cs, y0 + j * cs
                if ch == "#":
                    box(c, x + 2, y + 2, cs - 4, cs - 4, 10, hx("d9b24a"), 3, shading=0.12)
                    for k in range(3):
                        circle(c, x + 14 + k * 20, y + 20 + (k % 2) * 26, 7, hx("e8c86a"), 0)
                else:
                    c.rectangle(x, y, cs, cs); setc(c, hx("8a6a3a")); c.fill()
        # hay wagon circling the outer path
        per = 14.0
        u = (t % per) / per
        path = [(x0 - 40, y0 - 40), (x0 + 16 * cs + 40, y0 - 40), (x0 + 16 * cs + 40, y0 + 11 * cs + 40),
                (x0 - 40, y0 + 11 * cs + 40)]
        L_ = [abs(path[(i + 1) % 4][0] - path[i][0]) + abs(path[(i + 1) % 4][1] - path[i][1]) for i in range(4)]
        d = u * sum(L_)
        i = 0
        while d > L_[i]:
            d -= L_[i]; i += 1
        a, b = path[i], path[(i + 1) % 4]
        k = d / L_[i]
        wx, wy = lerp(a[0], b[0], k), lerp(a[1], b[1], k)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        c.save(); c.translate(wx, wy); c.rotate(ang)
        box(c, -90, -32, 120, 64, 8, hx("e8c15a"), 5)
        for q in range(3):
            circle(c, -66 + q * 34, 0, 13, SKINS[q], 3)
        box(c, 40, -26, 60, 52, 10, TOMATO, 5)
        c.restore()
        # a few visitors in the maze
        for q, (gx, gy) in enumerate(((1, 5), (8, 3), (12, 7), (5, 9))):
            ph = (t * 0.3 + q * 0.25) % 1
            px = x0 + (gx + 0.5) * cs + math.sin(ph * 6.28) * 20
            py = y0 + (gy + 0.5) * cs
            circle(c, px, py, 18, COATS[q], 4)
            circle(c, px, py, 9, HAIR[q], 0)
        weather(c, "leaves", t, 16)
    event_scene(c, t, S, world, zoom=(1.0, 1.04))


@scene("F03", sfx=lambda S: tag_sfx(S) + [(P(S, 3), "flip")])
def f03(c, t, S):
    def world(c, t, S):
        season_bg(c, "fall", t, seed=33)
        r = rng_for("pump", 1)
        for i in range(40):
            y = r.uniform(860, 1070)
            pumpkin(c, r.uniform(-20, 1180), y, 0.5 + (y - 860) / 300, [hx("ef8a1d"), hx("e8761a"), hx("f2a03a")][i % 3])
            stroke(c, lambda: (c.move_to(r.uniform(0, 1150), y + 10), c.line_to(r.uniform(0, 1150), y + 14)), LEAF, 4)
        # sign flipping between weekday and weekend
        fp = prog(t, P(S, 3), 0.6)
        sx = abs(math.cos(fp * math.pi))
        lbl = "WEEKDAY" if fp < 0.5 else "WEEKEND"
        c.save(); c.translate(820, 760)
        box(c, -12, -40, 24, 210, 4, WOOD, 5)
        c.scale(1, max(sx, 0.04))
        box(c, -190, -130, 380, 110, 16, CREAM if fp < 0.5 else GOLD, 6)
        text(c, lbl, 0, -48, 66, DISPLAY, INK, "center")
        c.restore()
        # family with wagon
        x, w_ = walk_x(t, 0.5, -200, 380, 80)
        box(c, x - 260, 990, 150, 60, 8, TOMATO, 5)
        pumpkin(c, x - 185, 995, 0.7)
        for wx_ in (x - 240, x - 130):
            circle(c, wx_, 1056, 18, INK, 3)
        stroke(c, lambda: (c.move_to(x - 110, 1010), c.line_to(x - 40, 960)), INK, 5)
        person(c, x, 1050, 1.0, t, seed=181, hat="cap", walk=t * 5 if w_ else None, scarf=GOLD)
        person(c, x + 110, 1060, 1.0, t, seed=182, kid=True, hat="beanie", walk=t * 5 + 1 if w_ else None)
        weather(c, "leaves", t, 22)
    event_scene(c, t, S, world)


@scene("F04", sfx=lambda S: tag_sfx(S) + [(1.5, "boo")])
def f04(c, t, S):
    def world(c, t, S):
        season_bg(c, "fall", t, tod="night", seed=34, layers=(0, 1))
        moon(c, 900, 230, 110)
        # corn rows
        for i in range(30):
            corn(c, -20 + i * 42, 880, 1.2, t, seed=i, col=hx("8a7a4a"))
        # friendly ghosts bob up from the corn
        for k, gx in enumerate((180, 560, 980)):
            up = max(0, math.sin(t * 1.1 + k * 2.1))
            gy = 760 - up * 150
            c.save(); c.translate(gx, gy + math.sin(t * 3 + k) * 6)
            fill_ink(c, lambda: (c.move_to(-50, 60), c.line_to(-50, -10), c.curve_to(-50, -90, 50, -90, 50, -10),
                                 c.line_to(50, 60), c.line_to(30, 44), c.line_to(10, 60), c.line_to(-10, 44), c.line_to(-30, 60),
                                 c.close_path()), (1, 1, 1, 0.92), 5)
            circle(c, -16, -16, 7, INK, 0); circle(c, 16, -16, 7, INK, 0)
            oval(c, 0, 8, 10, 12 * up + 3, INK, 0)
            c.restore()
        for i in range(30):
            corn(c, i * 42, 930, 1.0, t, seed=i + 40, col=hx("a08a4a"))
        # hay wagon with riders
        wx = lerp(-300, 900, ease(prog(t, 0, S.dur)))
        c.save(); c.translate(wx, 1040)
        box(c, -300, -100, 440, 70, 10, hx("c9a64a"), 5)
        for k in range(4):
            sc = max(0, math.sin(t * 1.1 + k * 2.1 - 0.5)) ** 3
            person(c, -260 + k * 100, -90, 0.55, t, seed=190 + k, mouth=sc, pose=((1.0 + sc * 1.4, 0.6), (1.0 + sc, 0.6)),
                   hat=["beanie", None, "cap", "bun"][k])
        box(c, -320, -40, 480, 30, 6, WOOD, 5)
        circle(c, -230, 0, 32, INK, 4); circle(c, 80, 0, 32, INK, 4)
        c.restore()
    event_scene(c, t, S, world)


@scene("F05", sfx=tag_sfx)
def f05(c, t, S):
    def world(c, t, S):
        interior(c, wall=hx("e3c79a"), floor=hx("a8743f"), plank=True, floor_y=860, lights=True, t=t)

        def farm_view(c, w, h, t):
            g = cairo.LinearGradient(0, 0, 0, h)
            g.add_color_stop_rgba(0, *hx("e9a25e")); g.add_color_stop_rgba(1, *hx("ffe6b4"))
            c.set_source(g); c.paint()
            c.move_to(0, h * 0.6); c.curve_to(w * 0.3, h * 0.45, w * 0.7, h * 0.7, w, h * 0.55); c.line_to(w, h); c.line_to(0, h)
            setc(c, hx("c27a36")); c.fill()
            for k in range(4):
                tree(c, 30 + k * w / 3.5, h * 0.75, 0.25, "autumn", t, seed=k)
        for wx_ in (100, 440, 780):
            window(c, wx_, 180, 260, 230, farm_view, t)
        # chalkboard
        box(c, 1000, 200, 150, 200, 8, hx("2d3a35"), 6)
        # long table + diners
        for i in range(7):
            seated(c, 140 + i * 145, 790, 0.62, t, seed=200 + i, eat=True, mouth=0.5 * max(0, math.sin(t * 2 + i)) ** 6)
        table(c, 590, 900, 1080, 1.0, hx("fdf3e0"))
        # four courses arriving
        course = min(4, 1 + int(clamp(t / (S.dur - 1)) * 4))
        foods = [hx("e8b65a"), LEAF, hx("8a5a3a"), hx("e4a95a")]
        for i in range(7):
            oval(c, 140 + i * 145 + 30, 790, 34, 9, WHITE, 3)
            oval(c, 140 + i * 145 + 30, 786, 16, 6, foods[course - 1], 2)
        for k in range(4):
            circle(c, 1040 + (k % 2) * 60, 260 + (k // 2) * 70, 22, foods[k] if k < course else hx("4a5a55"), 3)

    event_scene(c, t, S, world)


@scene("F06", sfx=lambda S: tag_sfx(S) + [(1.0, "crackle")])
def f06(c, t, S):
    def world(c, t, S):
        season_bg(c, "fall", t, tod="night", seed=36, layers=(0,))
        moon(c, 560, 420, 300)
        c.move_to(0, H); c.line_to(0, 860); c.curve_to(400, 780, 800, 800, 1250, 880); c.line_to(1250, H); c.close_path()
        setc(c, hx("2a2f6a")); c.fill_preserve(); setc(c, INK, 0.8); c.set_line_width(6); c.stroke()
        # walkers along the ridge
        for k in range(6):
            x = ((t * 55 + k * 150) % 1400) - 200
            y = 860 - 70 * math.sin(clamp(x / 1250) * math.pi) * 0.9 + 20
            person(c, x, y, 0.62, t, seed=210 + k, walk=t * 5 + k, coat=hx("3a3f7a"), hair=hx("2a2a4a"),
                   skin=hx("4a4f8a"), bottom=hx("2a2f5a"), face=False, hat=["beanie", None, "cap"][k % 3])
        # firepit waiting
        fx, fy = 980, 1020
        for k in range(7):
            a = k * math.pi / 3.5
            circle(c, fx + math.cos(a) * 90, fy + math.sin(a) * 18, 18, hx("8c8f9e"), 4)
        flame(c, fx, fy, 1.4, t)
        for k in range(5):
            ph = (t * 0.8 + k / 5) % 1
            circle(c, fx + math.sin(ph * 8 + k) * 30, fy - 90 - ph * 160, 3, hx("ffcf6a"), 0, alpha=1 - ph)
        box(c, 760, 1000, 140, 26, 10, WOOD, 4)
    event_scene(c, t, S, world)


@scene("F07", sfx=lambda S: tag_sfx(S) + [(2.0, "moo")])
def f07(c, t, S):
    def world(c, t, S):
        season_bg(c, "fall", t, seed=37)
        barn(c, 1020, 860, 0.75, col=hx("b8452a"))
        brush = math.sin(t * 4)
        cow(c, 330, 1000, 1.25, t, brush=brush * 0.5)
        person(c, 140, 1040, 1.0, t, seed=221, hat="beanie", scarf=GOLD, pose=((1.5, 0.3 + brush * 0.3), (0.3, 0.2)), look=1)
        box(c, 210 + brush * 30, 830 + brush * 6, 60, 24, 8, hx("8a5a3a"), 4)
        # table with a wreath being built
        box(c, 640, 900, 440, 30, 8, WOOD, 5)
        for lx in (680, 1040):
            box(c, lx - 8, 930, 16, 120, 3, shade(WOOD, 0.2), 4)
        prog_w = clamp(t / (S.dur - 1))
        wx, wy = 860, 860
        n = int(prog_w * 18)
        for k in range(n):
            a = k * 2 * math.pi / 18
            oval(c, wx + math.cos(a) * 70, wy + math.sin(a) * 26, 26, 14, [LEAF, hx("2f6f3a")][k % 2], 3)
        if prog_w > 0.8:
            fill_ink(c, lambda: (c.move_to(wx, wy + 26), c.line_to(wx - 30, wy + 6), c.line_to(wx - 30, wy + 46), c.close_path(),
                                 c.move_to(wx, wy + 26), c.line_to(wx + 30, wy + 6), c.line_to(wx + 30, wy + 46), c.close_path()),
                     TOMATO, 4)
        person(c, 860, 1070, 0.95, t, seed=222, hat="bun", coat=hx("8e5aa8"),
               pose=((1.3 + 0.2 * math.sin(t * 3), 1.0), (1.3, 1.0)))
        weather(c, "leaves", t, 20)
    event_scene(c, t, S, world)
