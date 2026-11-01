"""Thumbnails A and B (1280x720), drawn at 1920x1080 and scaled down."""
import os, sys, math
import cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx import *
from props import gate, latch_point, price_tag, chapter_wheel, barn, fence, season_wheel
from chars import person, sheep
from sets import season_bg, weather
from scenes_main import feb_yard
from beats import ROOT
from PIL import Image


def big_words(c, lines, x, y, size, cols, align="left"):
    for i, (s, col) in enumerate(zip(lines, cols)):
        text(c, s, x, y + i * size * 1.02, size, DISPLAY, col, align, outline=INK, olw=size * 0.16)


def thumb_a(c):
    season_bg(c, "fall", 2.0, seed=7)
    # four-season wheel behind the gate
    chapter_wheel(c, 1470, 430, 330, 0, None, None, 0)
    gx, gy, gs = 1040, 830, 1.0
    gate(c, gx, gy, gs, open_=0.0)
    lx, ly = latch_point(gx, gy, gs, 0.0)
    c.save(); c.translate(lx + 6, ly); c.rotate(-0.12)
    price_tag(c, 0, 0, [("", "$", "")], "", "", 1.0, 0.0, swing=False, maxw=300)
    c.restore()
    big_words(c, ["30 EVENTS.", "REAL PRICES."], 50, 300, 160, [PAPER, GOLD])


def thumb_b(c):
    # left: snowy, empty barnyard; right: packed
    c.save(); c.rectangle(0, 0, 960, H); c.clip(); c.translate(-250, 0)
    feb_yard(c, 1.0)
    c.restore()
    c.save(); c.rectangle(960, 0, 960, H); c.clip(); c.translate(960, 0)
    season_bg(c, "winter", 1.0, tod="dusk", seed=8)
    barn(c, 520, 880, 1.15, lit=1.0, snow=True, doors_open=0.7)
    for k in range(16):
        person(c, 40 + (k % 8) * 125 + (k // 8) * 50, 930 + (k // 8) * 110, 0.8, 1.0 + k, seed=k + 3, kid=k % 3 == 0,
               hat=["beanie", None, "bun", "cap"][k % 4], scarf=[TOMATO, GOLD, LEAF][k % 3], mouth=0.6)
    weather(c, "snow", 1.0, 50, region=(0, 0, 960, H))
    c.restore()
    weather(c, "snow", 2.0, 40, region=(0, 0, 960, H))
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), PAPER, 22)
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), INK, 8)
    text(c, "EMPTY?", 480, 250, 210, DISPLAY, PAPER, "center", outline=INK, olw=34)
    text(c, "SELL", 1440, 210, 190, DISPLAY, GOLD, "center", outline=INK, olw=30)
    text(c, "TICKETS", 1440, 400, 190, DISPLAY, GOLD, "center", outline=INK, olw=30)


def render(fn, out):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(s)
    fn(c)
    s.write_to_png(out + ".tmp.png")
    Image.open(out + ".tmp.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(out)
    os.remove(out + ".tmp.png")
    print(out)


if __name__ == "__main__":
    od = os.path.join(ROOT, "output"); os.makedirs(od, exist_ok=True)
    render(thumb_a, os.path.join(od, "thumbnail-a.png"))
    render(thumb_b, os.path.join(od, "thumbnail-b.png"))
