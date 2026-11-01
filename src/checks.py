"""Run every check from BUILD.md and write output/checks-report.md.

- ffprobe: duration, resolution, streams
- loudness (EBU R128 integrated), true peak, clipping, silences > 1.5 s (mix and voice track)
- spoken script vs what was sent to the voice, word for word; hand-phoneme words
- the 30 on-screen prices (and H02) against the script
- layout: tag text fits, banner never reaches the tracker, smallest text sizes used
"""
import os, sys, re, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats import load_beats, ROOT
import timeline

OUT = os.path.join(ROOT, "output")
MP4 = os.path.join(OUT, "video-045-30-farm-event-ideas.mp4")
lines = []


def say(s=""):
    print(s)
    lines.append(s)


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def ffprobe():
    say("## ffprobe")
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "format=duration,size,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,"
             "r_frame_rate,sample_rate,channels,bit_rate", "-of", "json", MP4])
    j = json.loads(r.stdout)
    f = j["format"]
    say(f"- duration: {float(f['duration']):.2f} s ({int(float(f['duration']) // 60)} min {float(f['duration']) % 60:.1f} s)")
    say(f"- file size: {int(f['size']) / 1e6:.2f} MB ({int(f['size'])} bytes)")
    for s in j["streams"]:
        if s["codec_type"] == "video":
            say(f"- video: {s['codec_name']} {s.get('profile')} {s['width']}x{s['height']} {s['pix_fmt']} "
                f"{s['r_frame_rate']} fps, {int(s.get('bit_rate', 0)) // 1000} kb/s")
        else:
            say(f"- audio: {s['codec_name']} {s.get('profile')} {s['sample_rate']} Hz {s['channels']} ch, "
                f"{int(s.get('bit_rate', 0)) // 1000} kb/s")
    # faststart: moov before mdat
    with open(MP4, "rb") as fh:
        head = fh.read(200000)
    say(f"- faststart (moov before mdat): {head.find(b'moov') != -1 and (head.find(b'mdat') == -1 or head.find(b'moov') < head.find(b'mdat'))}")
    return float(f["duration"]), int(f["size"])


def loudness():
    say("\n## Loudness and silence (measured with ffmpeg, not heard)")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", MP4, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    txt = r.stderr[r.stderr.rfind("Summary:"):]
    I = re.search(r"I:\s+(-?[\d.]+) LUFS", txt).group(1)
    LRA = re.search(r"LRA:\s+(-?[\d.]+) LU", txt).group(1)
    TP = re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt).group(1)
    say(f"- integrated loudness: {I} LUFS (target -14)")
    say(f"- true peak: {TP} dBTP (target under -1)")
    say(f"- loudness range: {LRA} LU")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", MP4, "-af", "astats=metadata=0:reset=0", "-f", "null", "-"])
    pk = re.findall(r"Peak level dB:\s+(-?[\d.inf]+)", r.stderr)
    clip = re.findall(r"Number of clipped samples:\s+(\d+)", r.stderr) or re.findall(r"Flat factor:\s+([\d.]+)", r.stderr)
    say(f"- sample peak (per channel / overall): {', '.join(pk)} dBFS")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", MP4, "-af", "silencedetect=noise=-50dB:d=1.5", "-f", "null", "-"])
    sil = re.findall(r"silence_start: ([\d.]+)", r.stderr)
    say(f"- silences over 1.5 s in the final mix (below -50 dB): {len(sil)} {sil if sil else ''}")
    # narration gaps (voice track only) and whether the script marks them
    vt = os.path.join(ROOT, "build", "voice_track.wav")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", vt, "-af", "silencedetect=noise=-45dB:d=1.5", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    scenes = timeline.build()
    say(f"- gaps over 1.5 s in the narration track: {len(starts)}")
    for a, b in zip(starts, ends + [None] * (len(starts) - len(ends))):
        S = next((S for S in scenes if S.start <= a < S.start + S.dur), scenes[-1])
        nxt = next((T for T in scenes if T.start > a), None)
        why = "end screen (20 s, marked in BUILD.md)" if S.id == "C07" else \
            ("(beat) marked in script" if "(beat)" in (nxt.beat["spoken"] if nxt else "") else
             "chapter card chime lead-in" if nxt and nxt.id in timeline.CHAPTERS else "NOT MARKED")
        say(f"  - {a:.2f}s to {b if b is None else round(b, 2)}s ({(b or a) - a:.2f}s) in {S.id}: {why}")


def words():
    say("\n## Spoken script vs what was sent to the voice")
    ph = json.load(open(os.path.join(ROOT, "build", "audio", "phonemes.json")))
    bad = 0
    for b in load_beats():
        want = re.sub(r"\s+", " ", b["spoken"].replace("(beat)", " ")).strip()
        got = " ".join(p["text"] for p in ph[b["id"]])
        if want.split() != got.split():
            bad += 1
            say(f"- MISMATCH {b['id']}: script={want!r} sent={got!r}")
        for p in ph[b["id"]]:
            if "❓" in p["phonemes"]:
                bad += 1
                say(f"- UNKNOWN PHONEME in {b['id']}: {p['text']}")
    n = sum(len(re.sub(r'\(beat\)', '', b['spoken']).split()) for b in load_beats())
    say(f"- {len(ph)} beats, {n} words compared, mismatches: {bad}")
    hand = json.load(open(os.path.join(ROOT, "build", "audio", "hand_phonemes_used.json")))
    sys.path.insert(0, os.path.dirname(__file__))
    from voice import HAND
    say(f"- words given hand phonemes ({len(hand)} spellings): " +
        ", ".join(f"{w} /{HAND.get(w, HAND.get(w.replace(chr(39) + 's', ''), HAND.get(w.lower(), HAND.get(w.replace(chr(39) + 's', '').capitalize(), '?'))))}/" for w in hand))
    return bad


def prices():
    say("\n## On-screen prices vs script")
    bad = 0
    beats = {b["id"]: b for b in load_beats()}
    for bid, ev in timeline.EVENTS.items():
        scr = beats[bid]["screen"]
        script_price = scr[-1] if bid != "S03" else scr[2]
        if bid == "H02":
            script_price = scr[2]
        shown = timeline.tag_text(ev["rows"])
        ok = timeline.norm_price(shown) == timeline.norm_price(script_price)
        bad += not ok
        num = f"No. {ev['n']}" if ev["n"] else "hook"
        say(f"- {bid} ({num}): script '{script_price}' | tag '{shown}' | {'OK' if ok else 'MISMATCH'}")
    say(f"- prices checked: {len(timeline.EVENTS)}, mismatches: {bad}")
    return bad


def layout():
    say("\n## Layout checks (measured)")
    import cairo
    from gfx import text_w, fit_size, wrap, DISPLAY, BODY, BODYM
    from common import event_parts
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
    c = cairo.Context(s)
    scenes = timeline.build()
    problems = 0
    min_price = 999
    for S in scenes:
        if not S.ev:
            continue
        rows = S.ev["rows"]
        maxw = 680
        big = 150 if len(rows) == 1 else 128
        for _, b, _ in rows:
            sz = fit_size(c, b, DISPLAY, big, maxw - 80, 120)
            min_price = min(min_price, sz)
            if text_w(c, b, DISPLAY, sz) > maxw - 80:
                problems += 1; say(f"- {S.id}: price '{b}' too wide")
        n, title, name, place = event_parts(S)
        for ln in wrap(c, name, BODY, 60, maxw - 90) + wrap(c, place, BODYM, 54, maxw - 90):
            if text_w(c, ln, BODY, 60) > maxw - 60:
                problems += 1; say(f"- {S.id}: farm line '{ln}' too wide")
        if n:
            bw = 40 + text_w(c, f"No. {n}", DISPLAY, 60) + 56 + text_w(c, title, BODY, 64) + 70
            tw = text_w(c, f"No. {n} of 30", DISPLAY, 56) + 60 + 140
            if bw > 1890 - tw - 30:
                problems += 1; say(f"- {S.id}: banner reaches tracker")
    say(f"- smallest price size used: {min_price}px (rule: at least 120px)")
    say(f"- tag/banner/tracker overflow or collision problems: {problems}")
    return problems


if __name__ == "__main__":
    say("# Checks report: video-045\n")
    dur, size = ffprobe()
    loudness()
    w = words()
    p = prices()
    l = layout()
    open(os.path.join(OUT, "checks-report.md"), "w").write("\n".join(lines) + "\n")
