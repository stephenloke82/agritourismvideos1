"""Timeline: scene start/durations from the real narration durations, plus mouth envelopes for lip-sync."""
import os, json
import numpy as np
import soundfile as sf
from beats import load_beats, ROOT

AUDIO = os.path.join(ROOT, "build", "audio")
FPS = 30

# Section-opening beats get a chapter card: the picture leads the voice slightly.
CHAPTERS = {"S01": ("The sweet peas", "leaf"),
            "F01": ("The Bucket-to-Bouquet Flip", "gold"),
            "A01": ("No. 1 Plant for the workshop", "leaf"),
            "B01": ("No. 2 Set the table", "sky"),
            "C01": ("No. 3 Pick, arrange, take home", "gold"),
            "D01": ("No. 4 Price the morning", "tomato"),
            "E01": ("No. 5 Fill the seats", "sky"),
            "O01": ("But I'm not a florist...", "tomato"),
            "Z01": ("Back to the bucket", "barn")}
CHAPTER_LEAD = 0.9
END_SCREEN = 18.0
STEP_OF = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}


class Scene:
    pass


def mouth_env(path):
    x, sr = sf.read(path)
    hop = sr // FPS
    n = len(x) // hop + 1
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(x) else 0 for i in range(n)])
    ref = np.percentile(rms[rms > 1e-4], 90) if np.any(rms > 1e-4) else 1
    m = np.clip((rms / ref - 0.12) * 1.3, 0, 1)
    return np.convolve(m, [0.25, 0.5, 0.25], "same")


def build():
    beats = load_beats()
    timing = json.load(open(os.path.join(AUDIO, "timing.json")))
    scenes, t = [], 0.0
    for b in beats:
        S = Scene()
        S.id, S.beat = b["id"], b
        tm = timing[b["id"]]
        S.audio = os.path.join(AUDIO, b["id"] + ".wav")
        S.voice_off = CHAPTER_LEAD if b["id"] in CHAPTERS else 0.0
        S.voice_dur = tm["duration"]
        dur = S.voice_off + tm["duration"]
        if b["id"] == "Z09":
            dur = max(dur, 10.0)
        if b["id"] == "Z10":
            dur = max(dur, END_SCREEN - 10.0)
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
        S.chapter = CHAPTERS.get(b["id"])
        S.step = STEP_OF.get(b["id"][0]) if b["id"][0] in STEP_OF and b["id"][1:].isdigit() else None
        scenes.append(S)
    return scenes


def mouth(S, t):
    i = int(t * FPS)
    if i < 0 or i >= len(S.env):
        return 0.0
    v = S.env[i]
    return 0.0 if v < 0.08 else 0.35 if v < 0.35 else 0.7 if v < 0.7 else 1.0


def total_duration(scenes):
    return scenes[-1].start + scenes[-1].dur


if __name__ == "__main__":
    sc = build()
    for S in sc:
        print(f"{S.id} {S.start:7.2f} {S.dur:6.2f} step={S.step}")
    print("total", total_duration(sc))
