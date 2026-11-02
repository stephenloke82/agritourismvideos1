"""Thumbnails A and B (1280x720), drawn at 1920x1080 and scaled down."""
import os, sys
import cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "kit"))  # shared kit
from gfx import *
from sets import season_bg
from flowers import flower_bucket, mason_jar, flower_row, ORANGE, MAGENTA, CORAL
from sarah import sarah
from kit088 import kitchen_bg
from beats import ROOT
from PIL import Image


def big_words(c, s, x, y, size, col, align="center"):
    text(c, s, x, y, size, DISPLAY, col, align, outline=INK, olw=size * 0.16)


def thumb_a(c):
    """$1 STEM -> $55 SEAT: the bucket of zinnias beside the same zinnias in a jar."""
    c.save(); c.rectangle(0, 0, 960, H); c.clip()
    season_bg(c, "summer", 2.0, tod="sunset", seed=31)
    flower_row(c, 900, 0.6, 0, ("zinnia", "cosmos"), seed=3, x0=-40, x1=980, gap=130)
    flower_bucket(c, 480, 1000, 2.2, 0, "zinnia", 11, seed=1, tag="$1")
    c.restore()
    c.save(); c.rectangle(960, 0, 960, H); c.clip()
    c.translate(960, 0)
    kitchen_bg(c, 0)
    c.restore()
    c.save(); c.rectangle(960, 0, 960, H); c.clip()
    mason_jar(c, 1440, 1000, 2.2, 0, (1, 1, 1, 1), seed=1, palette=[ORANGE, MAGENTA, CORAL])
    c.restore()
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), PAPER, 22)
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), INK, 8)
    big_words(c, "$1 STEM", 480, 220, 170, PAPER)
    big_words(c, "$55 SEAT", 1440, 220, 170, GOLD)
    circle(c, 960, 160, 70, TOMATO, 8)
    fill_ink(c, lambda: poly(c, [(925, 125), (1005, 160), (925, 195)]), PAPER, 0, shading=0)


def thumb_b(c):
    """SELL THE MORNING: Sarah with a jar bouquet in a zinnia row at golden hour."""
    season_bg(c, "summer", 2.0, tod="sunset", seed=38)
    flower_row(c, 820, 0.7, 0, ("zinnia", "cosmos", "dahlia"), seed=5, gap=130)

    def jar(c, hx_, hy):
        mason_jar(c, hx_ + 10, hy + 60, 0.7, 0, (1, 1, 1, 1), seed=2, palette=[ORANGE, MAGENTA, CORAL])
    sarah(c, 1240, 1100, 1.35, 0.0, 0.0, pose="present", hold=(1, jar))
    flower_row(c, 1080, 1.0, 0, ("zinnia", "cosmos", "zinnia"), seed=9, gap=170)
    big_words(c, "SELL THE", 90, 330, 200, PAPER, "left")
    big_words(c, "MORNING", 90, 540, 220, GOLD, "left")


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
