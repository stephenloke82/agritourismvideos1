"""All scenes of video 088, one function per beat of script/video-088-script.md."""
import math
import cairo
from gfx import *
from chars import person, bee, SKINS, HAIR, COATS
from props import barn, house, tree, fence, sign, stamp, ticket, gate
from sets import season_bg
from common import SCENES
from flowers import *
from kit088 import *

APRON = hx("e9d7b0")


# ---------------------------------------------------------------- shared shots and wrappers
def with_chapter(fn):
    """Show the chapter card for the first moments, then cut straight to the scene."""
    def wrap(c, t, S):
        if S.chapter and t < 1.7:
            chapter_card(c, t, S, *S.chapter)
            return
        fn(c, t, S)
        if S.step:
            tracker5(c, S.step, t)
    return wrap


def scene2(bid):
    def deco(fn):
        SCENES[bid] = with_chapter(fn)
        return fn
    return deco


def T0(S):
    """First moment after a chapter card."""
    return 1.7 if S.chapter else 0.0


def host(c, t, S, lines, starts=None, bg=None, pose="present", sx=340, s=1.0, cx=760, cy=150, size=66, **kw):
    (bg or flower_farm)(c, t)
    SAR(c, S, t, sx, 1010, s, pose=pose, **kw)
    if lines:
        st = starts or [P(S, i) for i in range(len(lines))]
        card(c, lines, cx, cy, t, st, size=size, maxw=1100)


def dawn_truck(c, t, bucket_y_off=0.0, tag=True):
    season_bg(c, "summer", t, tod="sunset", seed=31)
    flower_row(c, 820, 0.55, t, ("zinnia", "cosmos", "zinnia"), seed=31, gap=140)
    truck_tailgate(c, 960, 1060, 1.0, t)
    flower_bucket(c, 960, 745 + bucket_y_off, 1.35, t, "zinnia", 11, seed=1, tag="$1" if tag else None)


def kitchen_jar(c, t, x=760, s=1.7, ticket_a=1.0):
    kitchen_bg(c, t)
    mason_jar(c, x, 790, s, t, (1, 1, 1, 1), seed=1, palette=[ORANGE, MAGENTA, CORAL])
    if ticket_a > 0:
        c.save(); c.translate(1150, 760); c.rotate(-0.12)
        c.push_group()
        box(c, -130, -70, 260, 120, 14, GOLD, 5)
        text(c, "WORKSHOP", 0, -20, 34, DISPLAY, INK, "center")
        text(c, "$55", 0, 32, 48, DISPLAY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(ticket_a)
        c.restore()


def guest(c, x, y, s, t, seed, pose=((0.2, 0.2), (0.2, 0.2)), item=None, walk=None, **kw):
    """A workshop guest in an apron. item: None | 'bucket' | 'jar' | 'phone'."""
    def hold(c, hands):
        hxp, hyp = hands[1]
        if item == "bucket":
            flower_bucket(c, hxp, hyp + 70, 0.45, t, "mixed", 7, seed=seed)
        elif item == "jar":
            mason_jar(c, hxp - 10, hyp + 30, 0.45, t, (1, 1, 1, 1), seed=seed)
        elif item == "phone":
            box(c, hxp - 18, hyp - 50, 36, 64, 8, NAVY, 3)
    person(c, x, y, s, t, seed=seed, pose=pose, apron=APRON, walk=walk, hold=hold if item else None, **kw)


def pea_jar(c, x, y, s, t, seed=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = rng_for("peajar", seed)
    for k in range(9):
        ang = lerp(-0.7, 0.7, k / 8)
        L = r.uniform(120, 170)
        ex, ey = math.sin(ang) * L, -200 - math.cos(ang) * L
        stroke(c, lambda: (c.move_to(0, -190), c.line_to(ex, ey)), STEM_D, 3)
        sweet_pea(c, ex, ey, r.uniform(16, 22), PEA_COLS[k % len(PEA_COLS)], ang)
        if k % 3 == 1:
            tendril(c, ex * 0.6, -190 + (ey + 190) * 0.6, 0.8, ang)
    c.restore()
    mason_jar(c, x, y, s, t)


def gift_tag(c, x, y, s, txt, a=1.0):
    if a <= 0:
        return
    c.push_group()
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(0.15)
    stroke(c, lambda: (c.move_to(-40, -60), c.line_to(0, 0)), hx("8a6a3a"), 3)
    fill_ink(c, lambda: poly(c, [(0, -20), (150, -20), (170, 20), (150, 60), (0, 60)]), KRAFT, 4)
    circle(c, 20, 20, 7, PAPER, 3, shading=0)
    text(c, txt, 92, 32, 34, BODY, INK, "center")
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a)


def flip_bucket(c, x, y, s, t, p):
    """The Bucket-to-Bouquet Flip: a bucket of stems turns over and lands as a jar bouquet. p 0..1."""
    if p < 0.5:
        c.save(); c.translate(x, y - 120 * s); c.rotate(math.pi * ease(p * 2)); c.translate(-x, -(y - 120 * s))
        flower_bucket(c, x, y, s, t, "zinnia", 9, seed=2)
        c.restore()
    else:
        k = max(0.01, ease_back((p - 0.5) * 2))
        c.save(); c.translate(x, y); c.scale(k, k); c.translate(-x, -y)
        mason_jar(c, x, y, s * 1.1, t, (1, 1, 1, 1), seed=2, palette=[ORANGE, MAGENTA, CORAL])
        c.restore()


# ================================================================ Section 1: Hook
@scene2("H01")
def H01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.08, 960, 640)
    dawn_truck(c, t)
    c.restore()
    title(c, "50 STEMS.", W / 2, 170, t, P(S, 1), 110, col=GOLD)
    title(c, "ABOUT $1 EACH.", W / 2, 300, t, P(S, 2), 96)


@scene2("H02")
def H02(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    # florist's counter
    box(c, -20, 760, W + 40, 50, 10, WOOD)
    c.rectangle(0, 810, W, H - 810); setc(c, hx("e0c79a")); c.fill()
    sign(c, 1730, 470, "FLORIST", 64, CREAM, post=False)
    person(c, 1440, 760, 1.5, t, seed=9, coat=hx("e57399"), pose=((0.2, 0.2), (1.3, 0.5)))
    person(c, 360, 1010, 1.7, t, seed=4, hat="straw", pose=((1.2, 0.9), (0.2, 0.2)))
    bx = lerp(780, 1250, ease(prog(t, 0.6, 1.4)))
    flower_bucket(c, bx, 765, 1.25, t, "zinnia", 11, seed=1, tag="$1")
    # coins drop into the farmer's hand
    for k in range(3):
        p = prog(t, 1.4 + k * 0.35, 0.5)
        if p > 0:
            coin(c, 520 + k * 30, lerp(380, 600 - k * 12, ease_out(p)), 30)
    title(c, "Sold by the stem", W / 2, 200, t, P(S, 0) + 0.3, 100)


@scene2("H03")
def H03(c, t, S):
    c.save(); cam(c, t, S.dur, 1.04, 1.0, 760, 600)
    kitchen_jar(c, t, ticket_a=ease_out(prog(t, P(S, 3), 0.6)))
    c.restore()
    title(c, "$55 A SEAT", 1420, 640, t, P(S, 3), 104, col=GOLD)
    ease_text(c, "On a kitchen table in town", 1420, 900, 54, t, P(S, 1), BODY, INK, "center")


@scene2("H04")
def H04(c, t, S):
    c.save(); c.rectangle(0, 0, 960, H); c.clip()
    c.translate(-480, 0); dawn_truck(c, t); c.restore()
    c.save(); c.rectangle(960, 0, 960, H); c.clip()
    c.translate(400, 0); kitchen_jar(c, t, x=760, s=1.5, ticket_a=0); c.restore()
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), PAPER, 22)
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), INK, 8)
    card(c, ["Same flowers. Same field.", ("A very different check.", 72, DISPLAY, TOMATO)], W / 2, 60, t,
         [P(S, 0), P(S, 2)], size=60, anchor="tc")


@scene2("H05")
def H05(c, t, S):
    flower_farm(c, t, seed=5)
    workshop_table(c, 1200, 1030, 1150, 0.8, t, 5, items=1.0, jars_layers=(1, 1, 0, 0))
    x = lerp(-100, 330, ease_out(prog(t, 0.0, 1.6)))
    SAR(c, S, t, x, 1010, 1.0, pose="present" if t > 1.6 else "idle", walk=t * 6 if t < 1.6 else None)
    card(c, ["Flower arranging workshop", ("on your farm", 76, DISPLAY, LEAF)], 700, 90, t, [P(S, 0), P(S, 0) + 0.6],
         size=64)


@scene2("H06")
def H06(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 300, 1010, 0.95, pose="present")
    card(c, ["Craft class bookings on Tripadvisor", ("Jan to Jun 2026 vs Jan to Jun 2025", 40, BODY, GREY_D)], 620, 50,
         t, [P(S, 0), P(S, 0) + 0.4], size=54)
    base, x0, bw, maxh = 920, 760, 300, 480
    stroke(c, lambda: (c.move_to(x0 - 40, base), c.line_to(x0 + 2 * bw + 200, base)), INK, 6)
    st = P(S, 0) + 1.6
    for i, (lab, v, col) in enumerate((("2025", 100, GREY), ("2026", 188, LEAF))):
        vv = 100 + (v - 100) * ease_out(prog(t, P(S, 1), 1.4)) if i else 100
        a = ease_out(prog(t, st + i * 0.3, 0.6))
        if a <= 0:
            continue
        hh = maxh * vv / 188 * a
        bx = x0 + i * (bw + 140)
        box(c, bx, base - hh, bw, hh, 18, col, 6)
        text(c, lab, bx + bw / 2, base + 64, 52, BODY, INK, "center", alpha=a)
        if i and vv > 100.5:
            text(c, f"+{vv - 100:.0f}%", bx + bw / 2, base - hh - 30, 96, DISPLAY, INK, "center", outline=PAPER, olw=10)


@scene2("H07")
def H07(c, t, S):
    flower_farm(c, t, seed=7, rows=False)
    lay = (ease(prog(t, 0.3, 1.2)), ease(prog(t, 1.4, 1.2)), ease(prog(t, 2.6, 1.2)), ease(prog(t, 3.8, 1.2)))
    workshop_table(c, 960, 1080, 1600, 1.0, t, 5, guests=[3, 8, 12, 17, 22], items=1.0, jars_layers=lay,
                   names=["Ann", "Bea", "Cal", "Dee", "Eve"])
    card(c, ["People want to make something", ("with their hands.", 72, DISPLAY, LEAF)], W / 2, 50, t,
         [P(S, 0), P(S, 0) + 0.5], size=58, anchor="tc")


@scene2("H08")
def H08(c, t, S):
    flower_farm(c, t, seed=8)
    SAR(c, S, t, 330, 1010, 1.0, pose="count")
    for i, s in enumerate(["No florist's degree", "No fancy venue", "No big farm"]):
        pill(c, s, 1150, 260 + i * 180, t, P(S, i), size=64, mark="x")


@scene2("H09")
def H09(c, t, S):
    flower_farm(c, t, seed=9, tod="dusk")
    person(c, 520, 1000, 1.6, t, seed=4, hat="straw", pose=((0.6, 1.5), (0.2, 0.2)))
    thought(c, 900, 360, 360, 260, t, 0.3, lambda c, x, y: flower_bucket(c, x, y + 90, 0.6, t, "zinnia", 7, seed=4))
    card(c, ["“Who would pay to", "cut my flowers?”", ("I'm a grower, not a teacher.", 52, BODY, GREY_D)],
         1060, 120, t, [P(S, 0), P(S, 0) + 0.3, P(S, 2)], size=64, maxw=820)


@scene2("H10")
def H10(c, t, S):
    flower_farm(c, t, seed=10, rows=False)
    SAR(c, S, t, 330, 1010, 0.95, pose="present")
    card(c, ["Build it step by step", ("Pick, arrange, take home", 64, DISPLAY, LEAF)], 700, 330, t,
         [P(S, 1), P(S, 4)], size=62)
    roadmap(c, 0, t, P(S, 1), y=80, starts=[P(S, 4), P(S, 4) + 0.3, P(S, 5), P(S, 6), P(S, 7)])


@scene2("H11")
def H11(c, t, S):
    flower_farm(c, t, seed=10, rows=False)
    SAR(c, S, t, 330, 1010, 0.95, pose="point")
    roadmap(c, 0, t, -2, y=80, gold=4 if t > 0.4 else None)
    title(c, "Stay for No. 4", 1100, 520, t, P(S, 0) + 0.2, 110, col=GOLD)
    ease_text(c, "the one most farmers get wrong", 1100, 640, 60, t, P(S, 1), BODY, PAPER, "center", outline=INK, olw=8)


@scene2("H12")
def H12(c, t, S):
    flower_farm(c, t, seed=12)
    pose = "wave" if t < P(S, 1) else "finger"
    SAR(c, S, t, 380, 1010, 1.0, pose=pose, wave_amp=0.25 if pose == "wave" else 0)
    card(c, [("I'm Sarah.", 90, DISPLAY, INK), "Agritourism Success", ("by Stephen Loke", 50, BODY, INK)], 860, 70, t,
         [P(S, 0), P(S, 3), P(S, 3) + 0.3], size=60)
    card(c, ["Stephen grows durians in Malaysia", ("and welcomes visitors to his farm", 56, DISPLAY, LEAF)], 860, 520,
         t, [P(S, 4), P(S, 4) + 0.4], size=48)


@scene2("H13")
def H13(c, t, S):
    season_bg(c, "summer", t, tod="sunset", seed=13)
    for k, x in enumerate((180, 520, 1500, 1820)):
        tree(c, x, 820, 0.9, "leafy", t, seed=k + 3)
    for k in range(4):
        x = lerp(200 + k * 140, 900 + k * 140, t / S.dur)
        person(c, x, 990, 1.1, t, seed=30 + k, kid=(k == 3), walk=t * 6 + k)
    title(c, "They come for the morning.", W / 2, 230, t, P(S, 2), 104, col=GOLD)
    ease_text(c, "Not the crop.", W / 2, 340, 60, t, P(S, 1), BODY, PAPER, "center", outline=INK, olw=8)


# ================================================================ Section 2: The sweet peas
@scene2("S01")
def S01(c, t, S):
    season_bg(c, "spring", t, seed=21)
    for k, x in enumerate((140, 300, 1700, 1840)):
        tree(c, x, 860, 0.9, "pine", t, seed=k)
    sign(c, 1450, 560, "WASHINGTON STATE", 50, CREAM)
    person(c, 640, 1000, 1.5, t, seed=11, hair=hx("6b3f1f"), coat=hx("e57399"), look=0.3)
    card(c, ["A young mother in Washington State", ("Erin Benzakein", 84, DISPLAY, LEAF)], 860, 760, t,
         [P(S, 0) + T0(S), P(S, 1)], size=50)


@scene2("S02")
def S02(c, t, S):
    soft_bg(c, t, hx("f6e6ee"))
    # an old oval portrait frame
    c.save(); c.translate(560, 520)
    oval(c, 0, 0, 230, 290, WOOD, 8)
    oval(c, 0, 0, 190, 250, hx("efe0bf"), 5, shading=0)
    c.save(); ellipse(c, 0, 0, 190, 250); c.clip()
    person(c, 0, 300, 1.4, t, seed=2, hair=hx("d9d9d9"), coat=hx("8a6a9a"), face=True)
    c.restore(); c.restore()
    for k in range(5):
        sweet_pea(c, 830 + k * 34, 820 - k * 40, 26, PEA_COLS[k], 0.3 - k * 0.15)
    stroke(c, lambda: smooth(c, [(800, 900), (840, 840), (880, 780), (930, 700)], False), STEM_D, 5)
    card(c, ["Her great-grandmother's favorite:", ("sweet peas", 84, DISPLAY, MAGENTA)], 920, 160, t,
         [P(S, 0), P(S, 0) + 0.5], size=54, maxw=940)
    ease_text(c, "Planted in her memory", 1260, 760, 60, t, P(S, 2), DISPLAY, LEAF, "center")


@scene2("S03")
def S03(c, t, S):
    season_bg(c, "spring", t, seed=23)
    g = ease(prog(t, 0.3, max(1.0, S.dur - 1.5)))
    sweet_pea_trellis(c, 260, 980, 640, 620, t, 0.15 + 0.85 * g, seed=1)
    sweet_pea_trellis(c, 1000, 980, 640, 620, t, max(0.02, g * 1.1 - 0.1), seed=2)
    title(c, "They grew. And grew.", W / 2, 200, t, P(S, 1), 110, col=GOLD)


@scene2("S04")
def S04(c, t, S):
    season_bg(c, "spring", t, seed=24)
    sweet_pea_trellis(c, 80, 900, 420, 430, t, 1.0, seed=3)
    fence(c, -20, W + 20, 930, 1.0)

    def bunch(c, hands):
        hxp, hyp = hands[1]
        for k in range(5):
            sweet_pea(c, hxp + (k - 2) * 18, hyp - 40 - abs(k - 2) * 8, 18, PEA_COLS[k], 0)
    person(c, 760, 1010, 1.5, t, seed=11, hair=hx("6b3f1f"), coat=hx("e57399"), pose=((1.3, 0.4), (0.2, 0.2)), hold=bunch)
    for k, x in enumerate((1180, 1440, 1680)):
        a = ease_out(prog(t, P(S, k + 1) - 0.2, 0.6))
        if a > 0:
            c.push_group()
            person(c, x, 1010, 1.4, t, seed=40 + k, kid=(k == 2), pose=((1.2, 0.3), (0.2, 0.2)) if k == 0 else
                   ((0.2, 0.2), (0.2, 0.2)))
            c.pop_group_to_source(); c.paint_with_alpha(a)
    title(c, "Given away", W / 2, 190, t, P(S, 0), 110, col=GOLD)
    ease_text(c, "to neighbors, to friends, to anyone", W / 2, 300, 56, t, P(S, 1), BODY, PAPER, "center", outline=INK, olw=8)


@scene2("S05")
def S05(c, t, S):
    soft_bg(c, t, hx("eaf3e0"))
    pea_jar(c, 700, 900, 1.5, t, 1)
    gift_tag(c, 850, 760, 1.2, "for a friend", ease_out(prog(t, P(S, 0) + 0.3, 0.6)))
    a = ease_back(prog(t, P(S, 1), 0.6))
    if a > 0:
        c.save(); c.translate(1350, 900); c.scale(a, a); c.translate(-1350, -900)
        pea_jar(c, 1350, 900, 1.2, t, 2)
        c.restore()
    card(c, ["The first order:", ("one jar", 84, DISPLAY, MAGENTA)], W / 2, 50, t, [P(S, 0), P(S, 0) + 0.4], size=56,
         anchor="tc")
    ease_text(c, "Then another.", 1350, 380, 64, t, P(S, 1), DISPLAY, LEAF, "center")


@scene2("S06")
def S06(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 960, 700)
    season_bg(c, "summer", t, seed=26)
    house(c, 1500, 760, 0.8)
    flower_row(c, 800, 0.5, t, ("zinnia", "cosmos", "dahlia", "snap"), seed=26, gap=110)
    flower_row(c, 920, 0.7, t, ("cosmos", "zinnia", "dahlia"), seed=27, gap=140)
    c.restore()
    card(c, [("Floret", 100, DISPLAY, LEAF), "a family flower farm", ("Skagit Valley, Washington", 50, BODY, GREY_D)],
         W / 2, 90, t, [P(S, 0) + 0.3, P(S, 1), P(S, 2)], size=58, anchor="tc", align="center")


@scene2("S07")
def S07(c, t, S):
    flower_farm(c, t, seed=27)
    fence(c, -20, W + 20, 960, 1.0)
    person(c, 1500, 900, 1.2, t, seed=11, hair=hx("6b3f1f"), coat=hx("e57399"), pose=((0.6, 1.2), (0.2, 0.2)))
    for k, x in enumerate((240, 470, 700)):
        a = ease_out(prog(t, P(S, 1) + k * 0.3, 0.6))
        if a > 0:
            c.push_group()
            person(c, x, 1040, 1.5, t, seed=50 + k, pose=((2.0, 0.15), (0.2, 0.2)) if k == 1 else ((0.9, 0.6), (0.2, 0.2)),
                   look=0.4)
            c.pop_group_to_source(); c.paint_with_alpha(a)
    title(c, "They wanted to know how.", W / 2, 200, t, P(S, 3), 104, col=GOLD)


@scene2("S08")
def S08(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    box(c, 620, 140, 1100, 720, 30, PAPER, 7)
    text(c, "First workshop: tickets", 1170, 230, 60, DISPLAY, INK, "center")
    st = P(S, 2)
    for i in range(12):
        x, y = 680 + (i % 6) * 168, 310 + (i // 6) * 250
        p = ease_back(prog(t, st + i * 0.1, 0.35))
        box(c, x, y, 140, 200, 16, hx("efe8da"), 4, shading=0)
        if p > 0:
            c.save(); c.translate(x + 70, y + 100); c.scale(p, p)
            ticket(c, 0, 0, 0.9, GOLD, "SOLD", rot=-0.1)
            c.restore()
    if t > st + 1.6:
        stamp(c, 1170, 560, 2.2, "SOLD OUT", alpha=ease_out(prog(t, st + 1.6, 0.4)))
    ease_text(c, "within a couple of hours", 1170, 960, 64, t, st + 1.9, DISPLAY, TOMATO, "center")


@scene2("S09")
def S09(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    for i in range(3):
        a = 1.0 if i == 0 else ease_back(prog(t, P(S, 1) + (i - 1) * 0.5, 0.6))
        if a <= 0:
            continue
        x = 330 + i * 460
        c.save(); c.translate(x + 180, 560); c.scale(a, a); c.translate(-(x + 180), -560)
        box(c, x, 330, 360, 460, 30, PAPER, 7)
        box(c, x, 330, 360, 110, 30, TOMATO if i == 0 else LEAF, 7)
        text(c, "WORKSHOP", x + 180, 405, 54, DISPLAY, PAPER, "center")
        text(c, f"Session {i + 1}", x + 180, 560, 66, DISPLAY, INK, "center")
        if i == 0:
            stamp(c, x + 180, 680, 1.0, "SOLD OUT")
        else:
            text(c, "added", x + 180, 680, 54, BODY, LEAF, "center")
        c.restore()
    title(c, "+2 more sessions", W / 2, 200, t, P(S, 1), 110, col=GOLD)


@scene2("S10")
def S10(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    # notebook of fixes
    box(c, 180, 220, 640, 720, 20, PAPER, 7)
    for k in range(9):
        stroke(c, lambda: (c.move_to(220, 330 + k * 66), c.line_to(780, 330 + k * 66)), hx("bcd3ea"), 3)
    text(c, "What to fix", 500, 300, 60, DISPLAY, TOMATO, "center")
    for k, s in enumerate(("Name cards", "More buckets", "Shade", "Start on time")):
        st = P(S, 2) + k * 0.6
        ease_text(c, s, 300, 400 + k * 132, 52, t, st, BODY, INK)
        if t > st + 0.6:
            stroke(c, lambda: (c.move_to(230, 384 + k * 132), c.line_to(254, 404 + k * 132), c.line_to(284, 364 + k * 132)),
                   LEAF, 8, ease_out(prog(t, st + 0.6, 0.3)))
    # later: the lessons as online courses
    a = ease_out(prog(t, P(S, 5), 0.7))
    if a > 0:
        c.push_group()
        box(c, 980, 300, 760, 480, 24, NAVY, 7)
        box(c, 1010, 330, 700, 420, 12, PAPER, 0, shading=0)
        mason_jar(c, 1240, 700, 1.0, t, (1, 1, 1, 1), seed=4)
        circle(c, 1520, 520, 70, TOMATO, 6)
        fill_ink(c, lambda: poly(c, [(1500, 480), (1500, 560), (1560, 520)]), PAPER, 0, shading=0)
        fill_ink(c, lambda: poly(c, [(940, 780), (1780, 780), (1840, 840), (880, 840)]), GREY, 6)
        c.pop_group_to_source(); c.paint_with_alpha(a)
        ease_text(c, "Online courses today", 1360, 930, 60, t, P(S, 5), DISPLAY, LEAF, "center")
    title(c, "Rough at first. Better every time.", W / 2, 140, t, P(S, 0), 84)


@scene2("S11")
def S11(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    # left panel: future flower farmers with notebooks
    box(c, 40, 200, 740, 760, 30, hx("e2efd9"), 6)
    text(c, "Her guests:", 410, 290, 54, BODY, INK, "center")
    text(c, "future flower farmers", 410, 360, 56, DISPLAY, LEAF, "center")
    for k in range(3):
        person(c, 170 + k * 230, 900, 1.2, t, seed=60 + k, hat="cap" if k == 1 else None, pose=((1.0, 1.4), (0.2, 0.2)),
               hold=lambda c, h: box(c, h[1][0] - 30, h[1][1] - 40, 60, 74, 6, PAPER, 3))
    a = ease_out(prog(t, P(S, 2), 0.7))
    if a > 0:
        c.push_group()
        box(c, 1140, 200, 740, 760, 30, hx("fbe3e8"), 6)
        text(c, "Yours:", 1510, 290, 54, BODY, INK, "center")
        text(c, "families, friends, birthdays", 1510, 360, 48, DISPLAY, MAGENTA, "center")
        for k, (dx, kid) in enumerate(((1250, False), (1430, True), (1610, False), (1770, True))):
            if prog(t, P(S, 3 + k // 2), 0.4) > 0:
                person(c, dx, 900, 1.1, t, seed=70 + k, kid=kid)
        if t > P(S, 5):
            stroke(c, lambda: (c.move_to(1820, 700), c.curve_to(1830, 600, 1800, 560, 1810, 500)), INK, 3)
            oval(c, 1810, 460, 40, 50, TOMATO, 5)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    SAR(c, S, t, 960, 1010, 0.72, pose="idle")


@scene2("S12")
def S12(c, t, S):
    field_close(c, t, seed=12)
    SAR(c, S, t, 960, 1060, 1.05, pose="present")
    card(c, ["People will pay to stand", ("in your field and learn.", 72, DISPLAY, LEAF)], W / 2, 50, t,
         [P(S, 1), P(S, 1) + 0.5], size=62, anchor="tc")


# ================================================================ Section 3: The flip
@scene2("F01")
def F01(c, t, S):
    flower_farm(c, t, seed=14, rows=False)
    flip_bucket(c, 960, 900, 1.6, t, prog(t, T0(S) + 0.3, 1.6))
    title(c, "The Bucket-to-Bouquet Flip", W / 2, 200, t, T0(S) + 0.2, 110, col=GOLD)


def flip_panels(c, t, S, right=0.0, left_starts=None, right_starts=None):
    soft_bg(c, t, hx("f3e3c0"))
    box(c, 50, 40, 880, 1000, 30, hx("efe8da"), 6)
    text(c, "OLD WAY", 490, 130, 84, DISPLAY, GREY_D, "center")
    flower_bucket(c, 300, 720, 1.2, t, "zinnia", 9, seed=6)
    sign(c, 680, 500, "$1 a stem", 50, PAPER, post=False, rot=0.08)
    ls = left_starts or [-5, -5, -5, -5]
    for i, s in enumerate(["You cut", "You bucket", "You sell by the stem"]):
        ease_text(c, s, 120, 820 + i * 60, 50, t, ls[i], BODY, INK)
    ease_text(c, "The buyer sets the price", 120, 1010, 48, t, ls[3], DISPLAY, TOMATO)
    if right <= 0:
        return
    c.push_group()
    box(c, 990, 40, 880, 1000, 30, hx("fff1c4"), 6)
    text(c, "NEW WAY", 1430, 130, 84, DISPLAY, LEAF, "center")
    guest(c, 1230, 780, 1.4, t, 81, pose=((1.3, 0.6), (0.2, 0.2)))
    snips(c, 1330, 470, 1.6, 0.6, 0.4)
    mason_jar(c, 1560, 760, 1.0, t, (1, 1, 1, 1), seed=6)
    c.save(); c.translate(1720, 420); ticket(c, 0, 0, 1.2, GOLD, "SEAT", rot=0.15); c.restore()
    rs = right_starts or [-5, -5, -5, -5]
    for i, s in enumerate(["The guest cuts", "The guest arranges", "The guest takes it home"]):
        ease_text(c, s, 1060, 820 + i * 60, 50, t, rs[i], BODY, INK)
    ease_text(c, "You set the price", 1060, 1010, 48, t, rs[3], DISPLAY, LEAF)
    c.pop_group_to_source(); c.paint_with_alpha(right)


@scene2("F02")
def F02(c, t, S):
    flip_panels(c, t, S, 0.0, [P(S, 1), P(S, 2), P(S, 3), P(S, 4)])


@scene2("F03")
def F03(c, t, S):
    flip_panels(c, t, S, ease_out(prog(t, 0.0, 0.6)), None, [P(S, 1), P(S, 2), P(S, 3), P(S, 4)])
    a = ease_back(prog(t, P(S, 5), 0.6))
    if a > 0:
        c.save(); c.translate(W / 2, 250); c.scale(a, a)
        pill(c, "Paid for the morning, not the stem", 0, 0, t, -5, size=56, bg=GOLD)
        c.restore()


@scene2("F04")
def F04(c, t, S):
    flower_farm(c, t, seed=15, rows=False)
    SAR(c, S, t, 300, 1010, 0.95, pose="slate")
    box(c, 640, 180, 1160, 620, 20, WOOD, 7)
    box(c, 664, 204, 1112, 572, 12, hx("2d3a35"), 4)
    chalk = hx("f4f0e6")
    ease_text(c, "10 guests  ×  $55", 1220, 400, 100, t, P(S, 1), DISPLAY, chalk, "center")
    st = P(S, 3)
    if t > st:
        v = countup(550, t, st, 1.4)
        text(c, f"= ${v:,.0f}", 1220, 620, 140, DISPLAY, GOLD, "center", alpha=ease_out(prog(t, st, 0.4)))


@scene2("F05")
def F05(c, t, S):
    soft_bg(c, t, hx("eef2f6"))
    st = P(S, 1)
    n = int(countup(14, t, st, 2.4))
    for i in range(n):
        row = [0, 1, 2, 3, 4, 0, 1, 2, 3, 1, 2, 2, 1, 3][i]
        layer = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 2, 1][i]
        flower_bucket(c, 330 + row * 150 + layer * 75, 1000 - layer * 150, 0.8, t, "zinnia", 6, seed=i)
    v = countup(550, t, st, 2.4)
    box(c, 1200, 300, 600, 300, 30, PAPER, 7)
    text(c, f"{v:,.0f}", 1500, 470, 150, DISPLAY, TOMATO, "center")
    text(c, "stems to cut and sell", 1500, 550, 48, BODY, INK, "center")
    card(c, ["$550 ÷ about $1 a stem"], W / 2, 50, t, [P(S, 0)], size=70, anchor="tc")


@scene2("F06")
def F06(c, t, S):
    flower_farm(c, t, seed=16, rows=False)
    SAR(c, S, t, 330, 1010, 1.0, pose="point")
    flower_bucket(c, 900, 980, 1.3, t, "zinnia", 9, seed=7)
    mason_jar(c, 1450, 980, 1.3, t, (1, 1, 1, 1), seed=7)
    for x, st in ((900, P(S, 2)), (1450, P(S, 2) + 0.4)):
        a = ease_back(prog(t, st, 0.5))
        if a > 0:
            c.save(); c.translate(x + 150, 560); c.scale(a, a)
            circle(c, 0, 0, 56, LEAF, 6)
            stroke(c, lambda: (c.move_to(-26, 0), c.line_to(-6, 22), c.line_to(28, -22)), PAPER, 10)
            c.restore()
    card(c, ["NOT instead of florists.", ("AS WELL AS.", 84, DISPLAY, LEAF)], 760, 60, t, [P(S, 0), P(S, 2)], size=62)


@scene2("F07")
def F07(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    x0, y0, cw, ch = 360, 250, 170, 120
    box(c, x0 - 30, y0 - 130, cw * 7 + 60, ch * 5 + 170, 26, PAPER, 7)
    text(c, "JUNE", x0 + cw * 3.5, y0 - 50, 70, DISPLAY, TOMATO, "center")
    for d in range(30):
        col, row = d % 7, d // 7
        x, y = x0 + col * cw, y0 + row * ch
        box(c, x + 6, y + 6, cw - 12, ch - 12, 10, hx("f7f1e3"), 3, shading=0)
        text(c, str(d + 1), x + 26, y + 50, 36, BODY, INK)
        if col == 5 and d % 2 == 1:
            k = [5, 19, 33].index(d) if d in (5, 19, 33) else None
            st = P(S, 0) + 0.3 * (row)
            a = ease_out(prog(t, st, 0.5))
            if a > 0:
                stroke(c, lambda: ellipse(c, x + cw / 2, y + ch / 2, cw * 0.46, ch * 0.42), TOMATO, 7, a)
                mason_jar(c, x + cw / 2 + 20, y + ch - 14, 0.28, t, (1, 1, 1, 0), seed=d)
    card(c, ["One more way to sell the same field", ("on the days you choose", 60, DISPLAY, LEAF)], W / 2, 900, t,
         [P(S, 0), P(S, 1)], size=52, anchor="tc")


@scene2("F08")
def F08(c, t, S):
    flower_farm(c, t, seed=17)
    a = ease_back(prog(t, 0.2, 0.8))
    if a > 0:
        c.save(); c.translate(500, 520); c.scale(a, a); ebook_cover(c, 0, 0, 0.95, t); c.restore()
    card(c, [("Free ebook", 64, DISPLAY, LEAF), "150 Ways to Unlock", "Hidden Wealth From Your Farm",
             ("agritourismsuccess.com/150ways", 46, BODY, SKY)], 900, 200, t,
         [P(S, 1), P(S, 2), P(S, 2) + 0.3, P(S, 3)], size=58)


@scene2("F09")
def F09(c, t, S):
    flower_farm(c, t, seed=18, rows=False, barn_x=None)
    SAR(c, S, t, 330, 1010, 0.95, pose="present")
    title(c, "Five steps", 1150, 520, t, P(S, 1), 130, col=GOLD)
    roadmap(c, 0, t, 0.0, y=80, starts=[P(S, 1) + i * 0.15 for i in range(5)])


# ================================================================ Step 1
@scene2("A01")
def A01(c, t, S):
    host(c, t, S, ["Plant for the workshop,", ("not just the market", 70, DISPLAY, LEAF)],
         [P(S, 1) + T0(S) * 0, P(S, 2)], pose="present", cy=200)


@scene2("A02")
def A02(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 960, 800)
    field_close(c, t, seed=22)
    c.restore()
    for i, s in enumerate(["Tough", "Cheerful", "Plentiful"]):
        pill(c, s, 420 + i * 540, 160, t, P(S, i + 1), size=70, bg=PAPER)
    card(c, ["Cut-and-come-again flowers"], W / 2, 300, t, [P(S, 4)], size=60, anchor="tc")


@scene2("A03")
def A03(c, t, S):
    soft_bg(c, t, hx("eaf3e0"))
    c.rectangle(0, 860, W, H - 860); setc(c, hx("8a6a44")); c.fill()
    plants = [("Zinnias", lambda c, x: zinnia_plant(c, x, 860, 330, MAGENTA, t, 1, 1.35, 48)),
              ("Cosmos", lambda c, x: cosmos_plant(c, x, 860, 360, PINK, t, 2, 1.35, 46)),
              ("Snapdragons", lambda c, x: snapdragon(c, x, 860, 380, LEMON, t, 3, s=1.5)),
              ("Branching\nsunflowers", lambda c, x: branching_sunflower(c, x, 860, 380, t, 4, 1.35)),
              ("Dahlias", lambda c, x: dahlia_plant(c, x, 860, 320, PEACH, t, 5, 1.35, 62))]
    for i, (lab, fn) in enumerate(plants):
        st = P(S, i)
        a = ease_out(prog(t, st - 0.2, 0.6))
        if a <= 0:
            continue
        x = 220 + i * 370
        c.push_group(); c.translate(0, (1 - a) * 80); fn(c, x); c.pop_group_to_source(); c.paint_with_alpha(a)
        for k, part in enumerate(lab.split("\n")):
            text(c, part, x, 940 + k * 56, 50, DISPLAY, PAPER, "center", alpha=a, outline=INK, olw=8)
    card(c, ["The more you cut, the more they bloom."], W / 2, 40, t, [P(S, 5)], size=58, anchor="tc")


@scene2("A04")
def A04(c, t, S):
    soft_bg(c, t, hx("eaf3e0"))
    greens = [("Mint", MINT, "leafy"), ("Basil", hx("3f8f3a"), "leafy"), ("Herbs", SAGE, "leafy"),
              ("Hedgerow grasses", hx("b7a45a"), "grass")]
    for i, (lab, col, kind) in enumerate(greens):
        a = ease_out(prog(t, P(S, i + 1) - 0.1, 0.6))
        if a <= 0:
            continue
        x = 300 + i * 440
        c.push_group()
        for k in range(5):
            greens_sprig(c, x + (k - 2) * 26, 860, 300 - abs(k - 2) * 30, (k - 2) * 0.18, col, kind)
        c.pop_group_to_source(); c.paint_with_alpha(a)
        text(c, lab, x, 950, 54, DISPLAY, INK, "center", alpha=a)
    title(c, "Add greens", W / 2, 180, t, P(S, 0), 120, col=LEAF)


@scene2("A05")
def A05(c, t, S):
    kitchen_bg(c, t)
    g = ease(prog(t, 0.3, 2.0))
    mason_jar(c, 700, 800, 1.8, t, (g, 0, 0, 0), seed=3)
    card(c, ["Greens make a jar look full", ("and cost almost nothing", 64, DISPLAY, LEAF)], 1080, 160, t,
         [P(S, 0), P(S, 1)], size=56)


@scene2("A06")
def A06(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    st2 = P(S, 3)
    slide = ease(prog(t, st2, 1.0))
    x = lerp(560, 1360, slide)
    y = lerp(640, 470, slide)
    # a short, bent zinnia stem: the kind a florist turns down
    c.save(); c.translate(x, y)
    stroke(c, lambda: (c.move_to(0, 160), c.curve_to(30, 100, -40, 60, 10, 0)), INK, 12)
    stroke(c, lambda: (c.move_to(0, 160), c.curve_to(30, 100, -40, 60, 10, 0)), STEM, 7)
    zinnia_head(c, 10, -10, 70, ORANGE, t, 3, tilt=0.4)
    c.restore()
    mason_jar(c, 1360, 900, 1.7, t, (1, 0, 1, 1), seed=8)
    if t > P(S, 1):
        stamp(c, 560, 880, 1.6, "FLORIST: NO", alpha=1 - slide)
    pill(c, "GUEST: YES!", 1360, 980, t, st2 + 0.8, size=64, bg=GOLD, mark="v")
    card(c, ["Your seconds become", ("somebody's favorite", 70, DISPLAY, MAGENTA)], W / 2, 40, t,
         [P(S, 4), P(S, 4) + 0.4], size=56, anchor="tc")


# ================================================================ Step 2
@scene2("B01")
def B01(c, t, S):
    host(c, t, S, [("Set the table", 90, DISPLAY, SKY)], [P(S, 1)], pose="present", cy=200,
         bg=lambda c, t: flower_farm(c, t, seed=19, rows=False))
    workshop_table(c, 1260, 1030, 900, 0.75, t, 4, items=ease(prog(t, P(S, 1), 1.0)))


@scene2("B02")
def B02(c, t, S):
    flower_farm(c, t, seed=20, rows=False, barn_x=None)
    a1 = ease_out(prog(t, P(S, 2) - 0.2, 0.6))
    a2 = ease_out(prog(t, P(S, 3) - 0.2, 0.6))
    a3 = ease_out(prog(t, P(S, 4) - 0.2, 0.6))
    if a1 > 0:
        c.push_group()
        open_barn(c, 330, 880, 0.6, t, inside=lambda c: workshop_table(c, 0, 0, 560, 0.9, t, 3, extras=False))
        c.pop_group_to_source(); c.paint_with_alpha(a1)
        text(c, "A barn", 330, 970, 60, DISPLAY, PAPER, "center", alpha=a1, outline=INK, olw=8)
    if a2 > 0:
        c.push_group()
        box(c, 760, 560, 420, 320, 10, hx("8fa3b8"))
        fill_ink(c, lambda: poly(c, [(730, 570), (970, 440), (1210, 570)]), hx("6b7d90"))
        box(c, 860, 680, 220, 200, 6, hx("e6d2a8"))
        workshop_table(c, 970, 900, 380, 0.7, t, 2, extras=False)
        c.pop_group_to_source(); c.paint_with_alpha(a2)
        text(c, "A shed", 970, 970, 60, DISPLAY, PAPER, "center", alpha=a2, outline=INK, olw=8)
    if a3 > 0:
        c.push_group()
        tree(c, 1600, 890, 1.6, "leafy", t, seed=6)
        workshop_table(c, 1600, 900, 420, 0.7, t, 2, extras=False)
        c.pop_group_to_source(); c.paint_with_alpha(a3)
        text(c, "A shady tree", 1600, 970, 60, DISPLAY, PAPER, "center", alpha=a3, outline=INK, olw=8)
    card(c, ["You don't need a venue."], W / 2, 40, t, [P(S, 0)], size=62, anchor="tc")
    pill(c, "One station per guest", W / 2, 230, t, P(S, 6), size=58, bg=GOLD)


@scene2("B03")
def B03(c, t, S):
    soft_bg(c, t, hx("eef2f6"))
    box(c, 120, 760, 1680, 60, 12, WOOD)
    c.rectangle(140, 820, 1640, 30); setc(c, shade(WOOD, 0.25)); c.fill()
    items = [("Jar or vase", lambda: mason_jar(c, 300, 770, 1.2, t)),
             ("Bucket of water", lambda: (flower_bucket(c, 640, 770, 1.1, t, "zinnia", 0, seed=1),
                                          oval(c, 640, 770 - 105 * 1.1, 60, 9, hx("a6d4e8"), 0, shading=0))),
             ("Snips", lambda: snips(c, 960, 700, 2.0, 1.2, 0.35)),
             ("Apron", lambda: fill_ink(c, lambda: (c.move_to(1210, 520), c.line_to(1330, 520), c.line_to(1360, 760),
                                                    c.line_to(1180, 760), c.close_path()), APRON, 6)),
             ("Name card", lambda: name_card(c, 1600, 770, "Ruth", 2.0))]
    for i, (lab, fn) in enumerate(items):
        st = P(S, i)
        a = ease_out(prog(t, st - 0.1, 0.5))
        if a <= 0:
            continue
        x = [300, 640, 960, 1270, 1600][i]
        c.push_group(); c.translate(0, (1 - a) * -40); fn(); c.pop_group_to_source(); c.paint_with_alpha(a)
        lsz = fit_size(c, lab, DISPLAY, 50, 320, 30)
        text(c, lab, x, 930, lsz, DISPLAY, INK, "center", alpha=a)
    title(c, "One station", W / 2, 180, t, 0.2, 100, col=SKY)


@scene2("B04")
def B04(c, t, S):
    flower_farm(c, t, seed=21, rows=False)
    glow(c, 960, 740, 300, GOLD, 0.6 * ease(prog(t, P(S, 0), 0.8)))
    workshop_table(c, 960, 1040, 1500, 1.0, t, 5, items=1.0)
    card(c, ["Extras in the middle,", ("cut that morning", 66, DISPLAY, LEAF)], W / 2, 60, t, [P(S, 0), P(S, 1)],
         size=58, anchor="tc")


@scene2("B05")
def B05(c, t, S):
    flower_farm(c, t, seed=22, rows=False)
    n = int(countup(8, t, P(S, 1), 2.0))
    workshop_table(c, 960, 1060, 1800, 1.0, t, 8, guests=[91 + k for k in range(n)] if n else None, items=1.0,
                   extras=False)
    v = countup(12, t, P(S, 1) + 1.0, 1.6)
    card(c, [("8 to 12 guests", 90, DISPLAY, SKY)], W / 2, 50, t, [P(S, 1)], anchor="tc")
    ease_text(c, "plenty for one teacher", W / 2, 300, 56, t, P(S, 2), BODY, PAPER, "center", outline=INK, olw=8)


@scene2("B06")
def B06(c, t, S):
    flower_farm(c, t, seed=23, rows=False)
    up = ease(prog(t, P(S, 2), 0.8))
    poses = ((lerp(1.0, 2.5, up), lerp(0.6, 0.4, up)), (1.0, 0.6))
    workshop_table(c, 1180, 1060, 1400, 1.0, t, 5, extras=False, items=1.0, jars_layers=(1, 1, 1, 1))
    for k in range(5):
        x = 1180 - 700 + 280 * (k + 0.5) + 50
        if up > 0.05:
            guest(c, x, 990, 1.3, t, 101 + k, pose=(poses[0], (0.2, 0.2)), item="jar")
    SAR(c, S, t, 210, 1010, 0.9, pose="present")
    card(c, ["Everyone goes home", ("with something lovely", 70, DISPLAY, MAGENTA)], 560, 40, t, [P(S, 2), P(S, 2) + 0.4],
         size=58)


# ================================================================ Step 3
@scene2("C01")
def C01(c, t, S):
    flower_farm(c, t, seed=24, rows=False)
    SAR(c, S, t, 280, 1010, 0.9, pose="count")
    icons = [("Pick", lambda x, y: flower_bucket(c, x, y, 1.0, t, "mixed", 7, seed=2)),
             ("Arrange", lambda x, y: mason_jar(c, x, y, 0.9, t, (1, 1, 1, 1), seed=2)),
             ("Take home", lambda x, y: car_icon(c, x, y, t))]
    for i, (lab, fn) in enumerate(icons):
        st = P(S, 2 + i)
        a = ease_back(prog(t, st - 0.2, 0.6))
        if a <= 0:
            continue
        x = 760 + i * 440
        circle(c, x, 560, 190 * a, PAPER, 7)
        c.save(); c.translate(x, 560); c.scale(a, a); c.translate(-x, -560); fn(x, 650); c.restore()
        text(c, lab, x, 860, 66, DISPLAY, INK, "center", alpha=min(1, a), outline=PAPER, olw=10)
    title(c, "Three parts", 1200, 230, t, P(S, 1), 100, col=GOLD)


def car_icon(c, x, y, t):
    c.save(); c.translate(x, y)
    fill_ink(c, lambda: (rrect(c, -150, -120, 300, 90, 30)), TOMATO)
    fill_ink(c, lambda: poly(c, [(-90, -120), (-60, -190), (70, -190), (100, -120)]), TOMATO)
    box(c, -55, -178, 60, 52, 8, hx("bfe3f7"), 4)
    for wx in (-90, 90):
        circle(c, wx, -30, 34, hx("2d2f3a"), 5)
    c.restore()


@scene2("C02")
def C02(c, t, S):
    field_close(c, t, seed=25)
    off = t * 40
    for k in range(4):
        guest(c, 700 + k * 220 + off, 1000, 1.25, t, 111 + k, walk=t * 6 + k, item="bucket", pose=((0.6, 0.4), (0.2, 0.2)))
    SAR(c, S, t, 330 + off, 1010, 1.0, pose="point", walk=t * 6)
    title(c, "PICK", W / 2 + 300, 220, t, P(S, 0), 150, col=GOLD)


@scene2("C03")
def C03(c, t, S):
    soft_bg(c, t, hx("eaf3e0"))
    # a big zinnia stem, close: pairs of opposite leaves up the stem
    stem_line(c, 760, 1100, 780, 260, 16, 10)
    for yy, L in ((900, 150), (640, 130)):
        c.save(); c.translate(770, yy); c.scale(2.4, 2.4)
        from flowers import _leaf
        _leaf(c, 0, 0, L / 2.4, 18, 1.05, STEM); _leaf(c, 0, 0, L / 2.4, 18, -1.05, STEM)
        c.restore()
    cut = P(S, 1)
    drop = ease(prog(t, cut + 0.8, 0.8))
    c.save(); c.translate(0, drop * 30)
    zinnia_head(c, 780, 240, 130, MAGENTA, t, 2)
    c.restore()
    # snips close in just above the upper leaf pair
    sp = ease(prog(t, cut - 0.6, 0.8))
    snips(c, lerp(1200, 820, sp), 590, 3.0, 1.75, lerp(0.6, 0.0, ease(prog(t, cut + 0.3, 0.4))))
    a = ease_out(prog(t, cut, 0.5))
    if a > 0:
        stroke(c, lambda: (c.move_to(560, 560), c.line_to(720, 590)), TOMATO, 10, a)
        fill_ink(c, lambda: poly(c, [(720, 590), (690, 560), (680, 610)]), TOMATO, 0, alpha=a)
    card(c, ["Cut just above", ("a pair of leaves", 72, DISPLAY, LEAF)], 1100, 120, t, [P(S, 1), P(S, 1) + 0.4], size=60)
    ease_text(c, "It branches and blooms again", 1360, 900, 54, t, P(S, 2), BODY, INK, "center")


@scene2("C04")
def C04(c, t, S):
    field_close(c, t, seed=26)
    # a clock sweeping from 20 to 30 minutes
    cx, cy, r = 420, 380, 200
    circle(c, cx, cy, r, PAPER, 8)
    sweep = lerp(20, 30, ease(prog(t, P(S, 0), 2.0)))
    c.move_to(cx, cy); c.arc(cx, cy, r - 16, -math.pi / 2, -math.pi / 2 + sweep / 60 * 2 * math.pi); c.close_path()
    setc(c, GOLD, 0.7); c.fill()
    stroke(c, lambda: (c.move_to(cx, cy), c.line_to(cx + math.sin(sweep / 60 * 6.283) * (r - 30),
                                                    cy - math.cos(sweep / 60 * 6.283) * (r - 30))), INK, 10)
    text(c, f"{sweep:.0f} min", cx, cy + r + 90, 70, DISPLAY, INK, "center", outline=PAPER, olw=10)
    guest(c, 1300, 1020, 1.6, t, 121, pose=((2.2, 1.6), (2.2, 1.6)), item="phone")
    if int(t * 2) % 3 == 0 and t > P(S, 2):
        glow(c, 1330, 520, 160, WHITE, 0.7)
    card(c, ["This is the part", ("they'll photograph", 70, DISPLAY, MAGENTA)], 1050, 60, t, [P(S, 2), P(S, 2) + 0.4],
         size=56)


@scene2("C05")
def C05(c, t, S):
    flower_farm(c, t, seed=27, rows=False)
    box(c, -20, 820, W + 40, 50, 10, WOOD)
    c.rectangle(0, 870, W, H - 870); setc(c, CREAM); c.fill()
    mason_jar(c, 960, 840, 2.0, t)
    flower_bucket(c, 1500, 830, 1.1, t, "mixed", 9, seed=4)
    title(c, "ARRANGE", W / 2, 220, t, P(S, 0), 150, col=GOLD)
    ease_text(c, "one simple recipe", W / 2, 330, 64, t, P(S, 1), BODY, PAPER, "center", outline=INK, olw=8)


RECIPE = [("Greens", "a frame", SAGE), ("Stars", "three big blooms", WINE), ("Fillers", "around the stars", MAGENTA),
          ("Dancers", "light and airy", hx("b7a45a"))]


def recipe_list(c, x, y, t, starts, size=70):
    for i, ((w_, sub, col), st) in enumerate(zip(RECIPE, starts)):
        a = ease_out(prog(t, st, 0.6))
        if a <= 0:
            continue
        yy = y + i * 160
        c.push_group()
        box(c, x, yy, 600, 132, 30, PAPER, 6)
        circle(c, x + 66, yy + 66, 40, col, 5)
        text(c, str(i + 1), x + 66, yy + 88, 54, DISPLAY, PAPER, "center")
        text(c, w_, x + 130, yy + 70, size, DISPLAY, INK)
        text(c, sub, x + 132, yy + 114, 36, BODY, GREY_D)
        c.pop_group_to_source(); c.paint_with_alpha(a)


@scene2("C06")
def C06(c, t, S):
    flower_farm(c, t, seed=27, rows=False)
    box(c, -20, 820, W + 40, 50, 10, WOOD)
    c.rectangle(0, 870, W, H - 870); setc(c, CREAM); c.fill()
    st = [P(S, 0), P(S, 2), P(S, 4), P(S, 5)]
    lay = tuple(ease(prog(t, s_, 1.2)) for s_ in st)
    mason_jar(c, 640, 860, 1.65, t, lay, seed=1, palette=[WINE, ORANGE, PEACH])
    recipe_list(c, 1160, 150, t, st)


@scene2("C07")
def C07(c, t, S):
    flower_farm(c, t, seed=27, rows=False)
    box(c, -20, 820, W + 40, 50, 10, WOOD)
    c.rectangle(0, 870, W, H - 870); setc(c, CREAM); c.fill()
    mason_jar(c, 640, 860, 1.65, t, (1, 1, 1, 1), seed=1, palette=[WINE, ORANGE, PEACH])
    recipe_list(c, 1160, 150, t, [-5] * 4)
    pill(c, "Anyone can do it the first time", 1460, 840, t, P(S, 4), size=48, bg=GOLD)


@scene2("C08")
def C08(c, t, S):
    soft_bg(c, t, hx("f6ead8"))
    box(c, -20, 860, W + 40, 50, 10, WOOD)
    wrapped_jar(c, 640, 870, 1.5, t, ease(prog(t, P(S, 1), 1.2)), seed=2)
    a = ease_back(prog(t, P(S, 2), 0.6))
    if a > 0:
        c.save(); c.translate(1300, 600); c.scale(a * 1.6, a * 1.6); care_card(c, 0, 0, 1.0); c.restore()
    title(c, "TAKE HOME", W / 2, 200, t, P(S, 0), 140, col=GOLD)


@scene2("C09")
def C09(c, t, S):
    flower_farm(c, t, seed=28)

    def scr(c, sx, sy, sw, sh, tt):
        g = cairo.LinearGradient(0, sy, 0, sy + sh)
        g.add_color_stop_rgba(0, *hx("9fd0f0")); g.add_color_stop_rgba(1, *hx("f8e6b0"))
        c.rectangle(sx, sy, sw, sh); c.set_source(g); c.fill()
        c.save(); c.translate(sx + sw / 2, sy + sh * 0.95); c.scale(0.8, 0.8)
        guest(c, 0, 0, 1.5, tt, 131, pose=((1.2, 1.0), (1.2, 1.0)), item="jar")
        c.restore()
    guest(c, 520, 1010, 1.9, t, 131, pose=((1.2, 1.0), (1.2, 1.0)), item="jar")
    phone_frame(c, 1150, 150, 460, 800, scr, t, tilt=0.06)
    if t > P(S, 0) + 0.5 and t < P(S, 0) + 0.9:
        glow(c, 1380, 550, 500, WHITE, 0.8)
    card(c, ["That photo sells", ("your next class", 70, DISPLAY, MAGENTA)], 80, 60, t, [P(S, 1), P(S, 1) + 0.4], size=58)


# ================================================================ Step 4
@scene2("D01")
def D01(c, t, S):
    host(c, t, S, ["The one most farmers", ("get wrong", 90, DISPLAY, TOMATO)], [P(S, 1), P(S, 1) + 0.5], pose="hips",
         cy=200)


@scene2("D02")
def D02(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    # left: a tag on a single stem, crossed out
    zinnia_plant(c, 520, 950, 420, ORANGE, t, 1, 1.0, 60)
    box(c, 600, 640, 200, 110, 16, PAPER, 5)
    text(c, "$1", 700, 720, 70, DISPLAY, INK, "center")
    a = ease_out(prog(t, P(S, 0) + 0.3, 0.5))
    if a > 0:
        stroke(c, lambda: (c.move_to(560, 600), c.line_to(840, 790), c.move_to(840, 600), c.line_to(560, 790)), TOMATO, 16, a)
    # right: a sunrise on the new tag
    b = ease_back(prog(t, P(S, 1), 0.7))
    if b > 0:
        c.save(); c.translate(1340, 560); c.scale(b, b)
        box(c, -300, -200, 600, 400, 30, PAPER, 7)
        c.save(); rrect(c, -280, -180, 560, 360, 20); c.clip()
        g = cairo.LinearGradient(0, -180, 0, 180)
        g.add_color_stop_rgba(0, *hx("ffb27a")); g.add_color_stop_rgba(1, *hx("ffe6a6"))
        c.set_source(g); c.paint()
        circle(c, 0, 120, 110, hx("ffcf6a"), 0, shading=0)
        flower_row(c, 180, 0.4, t, ("zinnia", "cosmos"), seed=3, x0=-300, x1=300, gap=90)
        c.restore()
        c.restore()
    title(c, "Not the flowers.", 700, 200, t, P(S, 0), 96)
    title(c, "The morning.", 1340, 920, t, P(S, 1), 110, col=GOLD)


PRICES = [("Big Jim Farms", "New Mexico", "$35", "flowers + supplies included"),
          ("Moulton Farm", "New Hampshire", "$49.99", "1½ lb of pick-your-own flowers"),
          ("Land's Sake Farm", "Massachusetts", "$55", "flowers + jars included"),
          ("Dahlia bouquet class", "Ledbury, England", "£50", "hand-tied dahlias")]


def board(c, t, S, k, band=0.0):
    soft_bg(c, t, hx("eaf3e0"))
    starts = [-5] * k + [P(S, 0) + (0.6 if k == 0 else 0.1)] + [99] * (3 - k)
    if k == 0:
        starts[0] = P(S, 1)
    price_board(c, 160, 230, 1600, PRICES, t, starts, band)
    title(c, "What real farms charge", W / 2, 150, t, -5 if k else P(S, 0), 90, col=GOLD)


@scene2("D03")
def D03(c, t, S):
    board(c, t, S, 0)


@scene2("D04")
def D04(c, t, S):
    board(c, t, S, 1)


@scene2("D05")
def D05(c, t, S):
    board(c, t, S, 2)


@scene2("D06")
def D06(c, t, S):
    board(c, t, S, 3)


@scene2("D07")
def D07(c, t, S):
    board(c, t, S, 4, band=prog(t, P(S, 1), 0.6))
    for i, s in enumerate(["No counting stems", "No extra charge for the jar"]):
        pill(c, s, 560 + i * 800, 1010, t, P(S, 3 + i), size=50, mark="x")


@scene2("D08")
def D08(c, t, S):
    flower_farm(c, t, seed=30, rows=False)
    for k in range(6):
        x = 260 + k * 240
        box(c, x - 40, 860, 80, 120, 8, WOOD, 4)
        if t > P(S, 1) + k * 0.2:
            guest(c, x, 1000, 1.1, t, 141 + k)
    c.save(); c.translate(1600, 420); c.rotate(-0.1)
    box(c, -220, -110, 440, 220, 18, GOLD, 7)
    text(c, "WORKSHOP SEAT", 0, -20, 46, DISPLAY, INK, "center")
    text(c, "Sat 9 am", 0, 50, 44, BODY, INK, "center")
    c.restore()
    if t > P(S, 0) + 0.6:
        stamp(c, 1600, 440, 1.5, "PAID", alpha=ease_out(prog(t, P(S, 0) + 0.6, 0.3)))
    card(c, ["Sell tickets before the day.", ("Paid in advance means people turn up.", 50, BODY, LEAF)], 80, 60, t,
         [P(S, 0), P(S, 1)], size=62)


# ================================================================ Step 5
@scene2("E01")
def E01(c, t, S):
    host(c, t, S, [("Fill the seats", 90, DISPLAY, SKY)], [P(S, 1)], pose="present", cy=200,
         bg=lambda c, t: flower_farm(c, t, seed=31, rows=False))
    workshop_table(c, 1260, 1030, 900, 0.75, t, 4, guests=[151, 152, 153, 154][:int(countup(4, t, P(S, 1), 1.2))] or None)


@scene2("E02")
def E02(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))

    def scr(c, sx, sy, sw, sh, tt):
        c.rectangle(sx, sy, sw, 220); setc(c, hx("fbe3e8")); c.fill()
        mason_jar(c, sx + sw / 2, sy + 210, 0.6, tt, (1, 1, 1, 1), seed=3)
        text(c, "Flower Arranging", sx + 30, sy + 290, 44, DISPLAY, INK)
        text(c, "Workshop", sx + 30, sy + 340, 44, DISPLAY, INK)
        text(c, "Sat 14 June, 9 am", sx + 30, sy + 410, 36, BODY, GREY_D)
        text(c, "8 seats left", sx + 30, sy + 460, 36, BODY, LEAF)
        box(c, sx + 30, sy + 510, sw - 60, 90, 45, LEAF, 4)
        text(c, "Book now", sx + sw / 2, sy + 570, 46, DISPLAY, PAPER, "center")
    phone_frame(c, 260, 120, 500, 860, scr, t, tilt=-0.04)
    for i, s in enumerate(["Ticket Tailor", "Eventbrite"]):
        pill(c, s, 1300, 480 + i * 200, t, P(S, 3 + i), size=70)
    card(c, ["List each date on", ("a simple ticket page", 70, DISPLAY, SKY)], 900, 80, t, [P(S, 0), P(S, 0) + 0.4],
         size=58)


@scene2("E03")
def E03(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    for i, lab in enumerate(("TOURISM OFFICE", "CHAMBER OF COMMERCE")):
        a = ease_out(prog(t, P(S, i + 1) - 0.2, 0.6))
        if a <= 0:
            continue
        x = 220 + i * 780
        c.push_group()
        box(c, x, 300, 680, 520, 20, hx("c8955a"), 7)
        box(c, x + 30, 330, 620, 460, 10, hx("d9b88a"), 4, shading=0)
        lsz = fit_size(c, lab, DISPLAY, 50, 640, 30)
        text(c, lab, x + 340, 270, lsz, DISPLAY, INK, "center")
        # flyers pinned to the board, one is ours
        for k in range(3):
            box(c, x + 60 + k * 200, 380 + (k % 2) * 40, 160, 210, 6, PAPER if k != 1 else hx("fff1c4"), 4, shading=0)
            circle(c, x + 140 + k * 200, 392 + (k % 2) * 40, 9, TOMATO, 2, shading=0)
        mason_jar(c, x + 340, 560, 0.4, t, (1, 1, 1, 1), seed=i)
        text(c, "Workshop", x + 340, 600, 30, DISPLAY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    card(c, ["Moulton Farm's workshop is on", ("its regional chamber's events page", 52, DISPLAY, LEAF)], W / 2, 880,
         t, [P(S, 3), P(S, 3) + 0.4], size=46, anchor="tc")
    title(c, "Ask them to list it too", W / 2, 150, t, P(S, 0), 90, col=GOLD)


def wreath(c, x, y, r, t):
    for k in range(18):
        a = k * 2 * math.pi / 18
        c.save(); c.translate(x + math.cos(a) * r, y + math.sin(a) * r); c.rotate(a + 1.2)
        from flowers import _leaf
        _leaf(c, 0, 0, r * 0.5, r * 0.18, 0.0, hx("2f6b3a"), 3)
        c.restore()
    for k in range(8):
        a = k * 2 * math.pi / 8 + 0.2
        circle(c, x + math.cos(a) * r, y + math.sin(a) * r, r * 0.09, TOMATO, 3)


@scene2("E04")
def E04(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    cards = [("Spring blossoms", "spring", lambda x, y: tree(c, x, y + 120, 0.8, "blossom", t, seed=2)),
             ("Summer zinnias", "summer", lambda x, y: flower_bucket(c, x, y + 120, 1.0, t, "zinnia", 9, seed=3)),
             ("September dahlias", "fall", lambda x, y: dahlia_head(c, x, y - 30, 120, WINE, t, 2)),
             ("Winter wreaths", "winter", lambda x, y: wreath(c, x, y - 20, 110, t))]
    for i, (lab, season, fn) in enumerate(cards):
        st = P(S, i + 1)
        p = ease(prog(t, st - 0.3, 0.6))
        if p <= 0:
            continue
        x = 250 + i * 470
        c.save(); c.translate(x, 560); c.scale(max(0.02, abs(math.cos((1 - p) * math.pi / 2))), 1)
        box(c, -210, -330, 420, 640, 30, tint(SEASON_COL[season], 0.55), 7)
        fn(0, 0)
        lsz = fit_size(c, lab, DISPLAY, 46, 380, 28)
        text(c, lab, 0, 260, lsz, DISPLAY, INK, "center")
        c.restore()
    title(c, "Give each class a season", W / 2, 140, t, P(S, 0), 96, col=GOLD)


@scene2("E05")
def E05(c, t, S):
    flower_farm(c, t, seed=32)
    x = lerp(1900, 1200, ease(prog(t, 0.2, max(1.0, S.dur - 1.0))))
    guest(c, x, 1010, 1.5, t, 161, walk=t * 6 if x > 1210 else None, pose=((2.5, 0.5), (0.2, 0.2)))
    SAR(c, S, t, 500, 1010, 1.0, pose="wave", wave_amp=0.25)
    title(c, "A reason to come back", W / 2, 200, t, P(S, 0), 100, col=GOLD)


@scene2("E06")
def E06(c, t, S):
    soft_bg(c, t, hx("fbe3e8"))

    def scr(c, sx, sy, sw, sh, tt):
        g = cairo.LinearGradient(0, sy, 0, sy + sh)
        g.add_color_stop_rgba(0, *hx("9fd0f0")); g.add_color_stop_rgba(1, *hx("f8e6b0"))
        c.rectangle(sx, sy, sw, sh); c.set_source(g); c.fill()
        c.save(); c.translate(sx + sw / 2, sy + sh * 0.8); c.scale(0.75, 0.75)
        guest(c, 0, 0, 1.5, tt, 131, pose=((1.2, 1.0), (1.2, 1.0)), item="jar")
        c.restore()
        if tt > P(S, 4):
            text(c, "24 likes", sx + 30, sy + sh - 30, 44, DISPLAY, TOMATO)
    phone_frame(c, 720, 120, 480, 840, scr, t)
    for k, (x, y) in enumerate(((420, 300), (1500, 280), (350, 760), (1560, 760))):
        a = ease_back(prog(t, P(S, 4) + k * 0.25, 0.5))
        if a > 0:
            c.save(); c.translate(x, y); c.scale(a, a)
            circle(c, 0, 0, 100, PAPER, 6)
            c.save(); c.arc(0, 0, 94, 0, 6.3); c.clip()
            person(c, 0, 230, 0.9, t, seed=170 + k)
            c.restore()
            circle(c, 70, -70, 30, TOMATO, 4)
            c.restore()
    card(c, ["Their friends see it.", ("Their friends book.", 70, DISPLAY, MAGENTA)], W / 2, 40, t,
         [P(S, 4), P(S, 5)], size=56, anchor="tc")


# ================================================================ But I'm not a florist
@scene2("O01")
def O01(c, t, S):
    flower_farm(c, t, seed=33)
    person(c, 520, 1010, 1.7, t, seed=4, hat="straw", pose=((1.0, 1.4), (0.6, 2.0)))
    mason_jar(c, 900, 1000, 1.0, t, (1, 0, 0, 0), seed=1)
    card(c, ["“I'm a grower.", "I don't know how", "to arrange flowers.”"], 1150, 140, t,
         [P(S, 1), P(S, 2), P(S, 2) + 0.4], size=64)


@scene2("O02")
def O02(c, t, S):
    season_bg(c, "summer", t, seed=34)
    # left: a florist's shop front
    box(c, 80, 380, 620, 600, 12, hx("f4e6ee"))
    for k in range(6):
        fill_ink(c, lambda: poly(c, [(60 + k * 110, 380), (170 + k * 110, 380), (170 + k * 110, 450), (60 + k * 110, 450)]),
                 TOMATO if k % 2 else PAPER, 4, shading=0)
    text(c, "FLORIST", 390, 530, 70, DISPLAY, INK, "center")
    box(c, 140, 600, 240, 380, 8, hx("bfe3f7"))
    box(c, 430, 600, 220, 220, 8, hx("bfe3f7"))
    # right: the farmer in the field
    flower_row(c, 960, 0.8, t, ("zinnia", "cosmos", "dahlia"), seed=34, x0=1000, x1=1960, gap=150)
    person(c, 1500, 1000, 1.6, t, seed=4, hat="straw", pose=((2.5, 0.5), (0.2, 0.2)))
    for k in range(3):
        x = lerp(700, 1150 + k * 60, ease(prog(t, P(S, 1) + k * 0.2, 2.0)))
        person(c, x, 1040, 1.2, t, seed=180 + k, walk=t * 6 + k, back=False)
    title(c, "They want a farmer.", W / 2, 200, t, P(S, 2), 110, col=GOLD)


@scene2("O03")
def O03(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 1200, 600)
    season_bg(c, "summer", t, seed=35)
    for k in range(5):
        cosmos_plant(c, 1050 + k * 170, 980, 380 + (k % 2) * 40, COSMOS_COLS[k % 4], t, k, 1.2, 44)
    bx = 1400 + math.sin(t * 2.0) * 160
    by = 470 + math.sin(t * 3.1) * 50
    bee(c, bx, by, 1.6, t)
    person(c, 560, 1000, 1.7, t, seed=4, hat="straw", pose=((2.0, 0.15), (0.2, 0.2)), mouth=0.3)
    c.restore()
    card(c, ["Which flower you planted first.", ("Why the bees love the cosmos.", 56, DISPLAY, LEAF)], 80, 50, t,
         [P(S, 0), P(S, 1)], size=52)
    pill(c, "You know your field best", 560, 330, t, P(S, 2), size=54, bg=GOLD)


@scene2("O04")
def O04(c, t, S):
    kitchen_bg(c, t)
    for k in range(10):
        st = P(S, 5) + k * 0.25
        a = ease_back(prog(t, st, 0.4))
        if a > 0:
            x, y = 130 + (k % 5) * 190, 790 if k < 5 else 960
            c.save(); c.translate(x, y); c.scale(a, a)
            mason_jar(c, 0, 0, 0.55, t, (1, 1, 1, 1), seed=k, palette=[[WINE, ORANGE, PEACH], [CORAL, LEMON, PINK]][k % 2])
            c.restore()
    recipe_list(c, 1180, 80, t, [P(S, 1), P(S, 2), P(S, 3), P(S, 4)], size=62)
    ease_text(c, "Practice it 10 times", 1480, 900, 64, t, P(S, 5), DISPLAY, INK, "center")


@scene2("O05")
def O05(c, t, S):
    season_bg(c, "summer", t, seed=36)
    flower_row(c, 760, 0.55, t, ("zinnia", "cosmos", "zinnia"), seed=36, x0=300, x1=1100, gap=110)
    flower_row(c, 840, 0.65, t, ("dahlia", "zinnia", "cosmos"), seed=37, x0=300, x1=1100, gap=130)
    house(c, 1550, 800, 0.8)
    a = ease_out(prog(t, P(S, 3), 0.6))
    if a > 0:
        c.push_group()
        workshop_table(c, 960, 1060, 1300, 0.9, t, 5, guests=[191, 192, 193, 194, 195], jars_layers=(1, 1, 1, 0))
        c.pop_group_to_source(); c.paint_with_alpha(a)
    card(c, ["Floret: built on a two-acre farm"], W / 2, 50, t, [P(S, 1)], size=60, anchor="tc")
    title(c, "A few rows is enough.", W / 2, 300, t, P(S, 3), 96, col=GOLD)


# ================================================================ Close
@scene2("Z01")
def Z01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.08, 1.0, 960, 640)
    dawn_truck(c, t)
    c.restore()
    title(c, "Fifty zinnias.", W / 2, 170, t, P(S, 2), 104, col=GOLD)
    title(c, "About $1 a stem.", W / 2, 290, t, P(S, 3), 90)


@scene2("Z02")
def Z02(c, t, S):
    field_close(c, t, seed=37)
    later = t > P(S, 4)
    for k in range(10):
        x = 120 + k * 185 + (math.sin(k) * 30)
        y = 980 + (k % 2) * 60
        if later:
            guest(c, x + (t - P(S, 4)) * 30, y, 1.15, t, 201 + k, item="jar", pose=((1.0, 0.8), (0.2, 0.2)),
                  walk=t * 5 + k)
        elif t > P(S, 0) + k * 0.15:
            guest(c, x, y, 1.15, t, 201 + k, item="bucket", pose=((0.5, 0.3) if k % 2 else (1.2, 1.0), (0.2, 0.2)))
    title(c, "The Bucket-to-Bouquet Flip", W / 2, 180, t, P(S, 6), 104, col=GOLD)


@scene2("Z03")
def Z03(c, t, S):
    flower_farm(c, t, seed=38, tod="sunset")
    SAR(c, S, t, 960, 1030, 1.05, pose="present")
    card(c, ["Watching won't change anything.", ("Doing will.", 90, DISPLAY, LEAF)], W / 2, 50, t, [P(S, 0), P(S, 1)],
         size=60, anchor="tc", align="center")


@scene2("Z04")
def Z04(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    SAR(c, S, t, 280, 1010, 0.9, pose="point")
    box(c, 600, 200, 1220, 680, 30, PAPER, 7)
    text(c, "Homework", 660, 300, 70, DISPLAY, TOMATO)
    q = "Which 3 flowers could fill a guest's jar?"
    for k, ln in enumerate(wrap(c, q, DISPLAY, 60, 1120)):
        ease_text(c, ln, 660, 410 + k * 80, 60, t, P(S, 2) + k * 0.4, DISPLAY, INK)
    box(c, 660, 620, 1100, 110, 20, hx("f4f1ea"), 4, shading=0)
    reply = "Zinnias, cosmos, dahlias!"
    n = int(max(0, t - P(S, 3)) * 14)
    text(c, reply[:n], 690, 692, 50, BODY, INK)
    pill(c, "Tell Stephen in the comments", 1210, 810, t, P(S, 3), size=46, bg=GOLD)


@scene2("Z05")
def Z05(c, t, S):
    flower_farm(c, t, seed=39)
    a = ease_back(prog(t, 0.2, 0.8))
    if a > 0:
        c.save(); c.translate(500, 520); c.scale(a, a); flower_ebook_cover(c, 0, 0, 0.95, t); c.restore()
    card(c, [("For the full plan", 60, DISPLAY, LEAF), "How to Start a", "Flower Arranging Class",
             ("Link in the description", 48, BODY, SKY)], 900, 220, t, [P(S, 0), P(S, 1), P(S, 1) + 0.3, P(S, 2)], size=60)


@scene2("Z06")
def Z06(c, t, S):
    flower_farm(c, t, seed=40)
    a = ease_back(prog(t, 0.2, 0.8))
    if a > 0:
        c.save(); c.translate(500, 520); c.scale(a, a); ebook_cover(c, 0, 0, 0.95, t); c.restore()
    card(c, [("Free ebook", 64, DISPLAY, LEAF), "150 Ways to Unlock", "Hidden Wealth From Your Farm",
             ("agritourismsuccess.com/150ways", 50, BODY, SKY)], 900, 220, t, [P(S, 0), P(S, 1), P(S, 1) + 0.3, P(S, 1) + 0.8],
         size=58)


@scene2("Z07")
def Z07(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    box(c, 360, 140, 1200, 820, 20, PAPER, 7)
    for k in range(10):
        stroke(c, lambda: (c.move_to(400, 290 + k * 66), c.line_to(1520, 290 + k * 66)), hx("bcd3ea"), 3)
    ideas = ["Pick-your-own", "Farm tours", "Flower workshop", "Farm stay", "Seasonal festival", "Farm shop"]
    for k, s in enumerate(ideas):
        ease_text(c, f"{k + 1}. {s}", 440, 340 + k * 100, 56, t, 0.1 + k * 0.15, BODY, INK)
    a = ease_out(prog(t, P(S, 0) + 0.5, 0.6))
    if a > 0:
        stroke(c, lambda: ellipse(c, 700, 520, 330, 62), TOMATO, 8, a)
    title(c, "Find the one idea that fits your farm", W / 2, 110, t, P(S, 0), 70, col=GOLD)


@scene2("Z08")
def Z08(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))

    def body(c, x, y, w, h, t):
        text(c, "Get the free 150 Ways ebook", x + 60, y + 110, 60, DISPLAY, INK)
        for i, (lab, val) in enumerate((("Name", "Your name"), ("Email", "you@yourfarm.com"))):
            st = P(S, 1) + i * 0.8
            yy = y + 190 + i * 150
            text(c, lab, x + 60, yy, 40, BODYM, GREY_D)
            box(c, x + 60, yy + 20, w - 120, 80, 16, hx("f4f1ea"), 4, shading=0)
            n = int(max(0, t - st) * 16)
            text(c, val[:n], x + 90, yy + 76, 46, BODY, INK)
        a = ease_back(prog(t, P(S, 2), 0.5))
        if a > 0:
            c.save(); c.translate(x + w / 2, y + 570); c.scale(a, a)
            box(c, -220, -60, 440, 120, 60, LEAF, 6); text(c, "It's yours", 0, 22, 60, DISPLAY, PAPER, "center")
            c.restore()
    browser(c, 260, 120, 1400, 820, "agritourismsuccess.com/150ways", t, body)


def end_screen(c, t, S):
    flower_farm(c, t, seed=46, tod="sunset", rows=True)
    workshop_table(c, 1500, 1060, 700, 0.75, t, 3, jars_layers=(1, 1, 1, 1))
    SAR(c, S, t, 760, 1030, 0.8, pose="wave", wave_amp=0.25)


@scene2("Z09")
def Z09(c, t, S):
    end_screen(c, t, S)
    # top left is kept clear for YouTube's end-screen video card
    text(c, "Watch next", 120, 110, 60, DISPLAY, PAPER, outline=INK, olw=10, alpha=ease_out(prog(t, P(S, 0), 0.8)))


@scene2("Z10")
def Z10(c, t, S):
    end_screen(c, t, S)
    flip_bucket(c, 380, 1000, 0.9, t, prog(t, 0.3, 1.4))
    title(c, "Don't sell the stem.", W / 2, 230, t, P(S, 0), 100, col=PAPER)
    title(c, "Sell the morning.", W / 2, 360, t, P(S, 1), 110, col=GOLD)
