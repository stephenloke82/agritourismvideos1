"""Timeline: scene start/durations from the real narration durations, mouth envelopes, event data."""
import os, json, re
import numpy as np
import soundfile as sf
from beats import load_beats, ROOT

AUDIO = os.path.join(ROOT, "build", "audio")
FPS = 30

# Event data. rows = (small text above, BIG PRICE, small text below); joined they must equal the script.
EVENTS = {
    "H02": dict(n=None, season="winter", rows=[("", "£13.95", "per person")]),
    "W01": dict(n=1, season="winter", rows=[("", "$10", "a foot")]),
    "W02": dict(n=2, season="winter", rows=[("", "£6.50", "per car")]),
    "W03": dict(n=3, season="winter", rows=[("", "$17", "to"), ("", "$20", "")]),
    "W04": dict(n=4, season="winter", rows=[("", "£14.95", "per child")]),
    "W05": dict(n=5, season="winter", rows=[("", "$55", "per person")]),
    "W06": dict(n=6, season="winter", rows=[("", "£5", "per person")]),
    "W07": dict(n=7, season="winter", rows=[("", "$130", "per person")]),
    "W08": dict(n=8, season="winter", rows=[("", "£13.95", "per person")]),
    "S01": dict(n=9, season="spring", rows=[("", "$16", "adult"), ("", "$10", "child")]),
    "S02": dict(n=10, season="spring", rows=[("", "$50", "limit 10")]),
    "S03": dict(n=11, season="spring", rows=[("", "$50", "one hour")]),
    "S05": dict(n=12, season="spring", rows=[("", "£25", "to"), ("", "£195", "")]),
    "S06": dict(n=13, season="spring", rows=[("", "£17.50", "per person")]),
    "S07": dict(n=14, season="spring", rows=[("", "C$7", "per child")]),
    "S08": dict(n=15, season="spring", rows=[("", "$20", "to"), ("", "$25", "")]),
    "S09": dict(n=16, season="spring", rows=[("", "$10", "early"), ("", "$15", "at the gate")]),
    "U01": dict(n=17, season="summer", rows=[("", "$35", "per person")]),
    "U02": dict(n=18, season="summer", rows=[("", "$11.99", ""), ("bucket", "$19.99", "")]),
    "U03": dict(n=19, season="summer", rows=[("", "£7.75", "peak"), ("", "£5.75", "off-peak")]),
    "U04": dict(n=20, season="summer", rows=[("", "$375", "per child, per week")]),
    "U05": dict(n=21, season="summer", rows=[("", "$40", "")]),
    "U06": dict(n=22, season="summer", rows=[("", "$45", "to"), ("", "$95", "")]),
    "U07": dict(n=23, season="summer", rows=[("", "£105", "")]),
    "F01": dict(n=24, season="fall", rows=[("", "$12", "")]),
    "F02": dict(n=25, season="fall", rows=[("", "$18.52", "")]),
    "F03": dict(n=26, season="fall", rows=[("", "$26.99", "weekday"), ("", "$45.99", "weekend")]),
    "F04": dict(n=27, season="fall", rows=[("From", "$36", "")]),
    "F05": dict(n=28, season="fall", rows=[("", "C$90", "")]),
    "F06": dict(n=29, season="fall", rows=[("", "$10", "")]),
    "F07": dict(n=30, season="fall", rows=[("", "£60", "")]),
}
CHAPTERS = {"W00": "winter", "S00": "spring", "U00": "summer", "F00": "fall"}
CHAPTER_LEAD = 0.7  # chime before the voice on chapter cards
END_SCREEN = 20.0


def norm_price(s):
    return re.sub(r"\s+", " ", s.replace(",", " ")).strip()


def tag_text(rows):
    return " ".join(p for r in rows for p in r if p)


def season_of(bid):
    return {"W": "winter", "S": "spring", "U": "summer", "F": "fall"}.get(bid[0])


class Scene:
    pass


def mouth_env(path):
    x, sr = sf.read(path)
    hop = sr // FPS
    n = len(x) // hop + 1
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(x) else 0 for i in range(n)])
    ref = np.percentile(rms[rms > 1e-4], 90) if np.any(rms > 1e-4) else 1
    m = np.clip((rms / ref - 0.12) * 1.3, 0, 1)
    # slight smoothing, keep snappy
    m = np.convolve(m, [0.25, 0.5, 0.25], "same")
    return m


def build():
    beats = load_beats()
    timing = json.load(open(os.path.join(AUDIO, "timing.json")))
    scenes, t = [], 0.0
    list_on = False
    last_n, ev_n = 0, None
    for b in beats:
        S = Scene()
        S.id, S.beat = b["id"], b
        tm = timing[b["id"]]
        S.audio = os.path.join(AUDIO, b["id"] + ".wav")
        S.voice_off = CHAPTER_LEAD if b["id"] in CHAPTERS else 0.0
        S.voice_dur = tm["duration"]
        dur = S.voice_off + tm["duration"]
        if b["id"] == "C07":
            dur = max(dur, END_SCREEN)
        # frame-align
        S.frames = int(round(dur * FPS))
        S.dur = S.frames / FPS
        S.start_frame = int(round(t * FPS))
        S.start = S.start_frame / FPS
        t = S.start + S.dur
        S.ph = [p["start"] + S.voice_off for p in tm["phrases"]]
        S.ph_end = [p["end"] + S.voice_off for p in tm["phrases"]]
        S.ph_text = [p["text"] for p in tm["phrases"]]
        env = mouth_env(S.audio)
        off = int(round(S.voice_off * FPS))
        S.env = np.concatenate([np.zeros(off), env, np.zeros(max(0, S.frames - off - len(env)) + 2)])
        S.season = CHAPTERS.get(b["id"]) or season_of(b["id"])
        S.ev = EVENTS.get(b["id"])
        if b["id"] == "W00":
            list_on = True
        if b["id"] == "T01":
            list_on = False
        if b["id"] == "U00":
            list_on = True
        if b["id"] == "M01":
            list_on = False
        if S.ev and S.ev["n"]:
            last_n = S.ev["n"]
        S.tracker_n = last_n if (list_on and b["id"] not in CHAPTERS and last_n) else None
        scenes.append(S)
    return scenes


def mouth(S, t):
    i = int(t * FPS)
    if i < 0 or i >= len(S.env):
        return 0.0
    v = S.env[i]
    # cartoon quantise
    return 0.0 if v < 0.08 else 0.35 if v < 0.35 else 0.7 if v < 0.7 else 1.0


def total_duration(scenes):
    return scenes[-1].start + scenes[-1].dur


if __name__ == "__main__":
    sc = build()
    for S in sc:
        print(f"{S.id} {S.start:7.2f} {S.dur:6.2f} n={S.tracker_n}")
    print("total", total_duration(sc))
