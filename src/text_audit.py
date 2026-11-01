"""Render every scene at its contact-sheet time and record every text size drawn.
Reports the smallest text per scene so the 54 px body / 120 px price rules can be checked."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx
REC = []
_orig = gfx.text


def rec_text(c, s, x, y, size, face=gfx.BODY, *a, **k):
    m = c.get_matrix()
    REC.append((size * m.xx, s, face, (k.get("alpha", a[3] if len(a) > 3 else 1.0))))
    return _orig(c, s, x, y, size, face, *a, **k)


gfx.text = rec_text
import timeline, render  # noqa
from contact import key_time
import cairo

scenes = timeline.build()
small = []
for S in scenes:
    REC.clear()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, gfx.W, gfx.H)
    c = cairo.Context(surf)
    render.draw_scene(c, S, key_time(S))
    for sz, s, face, a in REC:
        if sz < 54 and a > 0.05:
            small.append((S.id, round(sz), s))
seen = set()
for sid, sz, s in small:
    if (sid, s) not in seen:
        seen.add((sid, s))
        print(f"{sid}: {sz}px '{s}'")
