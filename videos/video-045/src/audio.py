"""Original music (synthesised in code), small sound effects, ducking and the final mix.

Music: Karplus-Strong plucked strings (guitar-like arpeggios + bass) over soft pads,
one variation per season. Ducked ~16 dB under the voice. Final mix -14 LUFS, TP < -1 dB.
Usage: python3 src/audio.py               -> narration only (current choice) -> build/mix.wav
       python3 src/audio.py --with-music  -> narration + music + effects
"""
import os, sys, math, json, subprocess
import numpy as np
import soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "kit"))  # shared kit
import timeline
import common
import vignettes, scenes_main  # noqa: registers scene sfx
from beats import ROOT

SR = 44100
BUILD = os.path.join(ROOT, "build")
rng = np.random.default_rng(11)

NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def hz(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave + 1) - 69) / 12)


CHORDS = {  # root, quality
    "G": ("G", [0, 4, 7]), "D": ("D", [0, 4, 7]), "Em": ("E", [0, 3, 7]), "C": ("C", [0, 4, 7]),
    "Bm": ("B", [0, 3, 7]), "A": ("A", [0, 4, 7]), "F#m": ("F#", [0, 3, 7]), "E": ("E", [0, 4, 7]),
    "Am": ("A", [0, 3, 7]), "F": ("F", [0, 4, 7]), "Dsus": ("D", [0, 5, 7]), "Cmaj7": ("C", [0, 4, 7, 11]),
}
THEMES = {
    "home":   dict(prog=["G", "D", "Em", "C"], bpm=92, pattern="arp", bright=0.5),
    "winter": dict(prog=["D", "Bm", "G", "A"], bpm=78, pattern="sparse", bright=0.8, bell=True),
    "spring": dict(prog=["G", "C", "Em", "D"], bpm=100, pattern="arp8", bright=0.7),
    "story":  dict(prog=["Am", "F", "C", "G"], bpm=74, pattern="sparse", bright=0.3),
    "summer": dict(prog=["A", "D", "F#m", "E"], bpm=104, pattern="strum", bright=0.6),
    "fall":   dict(prog=["Em", "C", "G", "D"], bpm=90, pattern="arp", bright=0.45),
}


def pluck(f, dur, bright=0.5, amp=1.0):
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    # soften the excitation for a warmer nylon-ish tone
    for _ in range(int(2 + (1 - bright) * 4)):
        buf = 0.5 * (buf + np.roll(buf, 1))
    out = np.zeros(n)
    decay = 0.996 + 0.003 * bright
    idx = 0
    b = buf.copy()
    for i in range(n):
        v = b[idx]
        out[i] = v
        nxt = (idx + 1) % p
        b[idx] = decay * 0.5 * (b[idx] + b[nxt])
        idx = nxt
    env = np.minimum(1, np.arange(n) / (0.003 * SR))
    return out * env * amp


_pl_cache = {}


def pluck_c(f, dur, bright, amp):
    key = (round(f, 2), round(dur, 2), round(bright, 2))
    if key not in _pl_cache:
        _pl_cache[key] = pluck(f, dur, bright, 1.0)
    return _pl_cache[key] * amp


def pad(freqs, dur, amp=0.1):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        for det in (-0.6, 0.6):
            ph = rng.uniform(0, 6.28)
            out += np.sin(2 * np.pi * (f + det) * t + ph) * 0.5 + 0.12 * np.sin(2 * np.pi * 2 * (f + det) * t + ph)
    att = min(0.8, dur / 3)
    env = np.minimum(1, t / att) * np.minimum(1, (dur - t) / att)
    return out * env * amp / len(freqs)


def bell(f, dur, amp=0.15):
    n = int(dur * SR)
    t = np.arange(n) / SR
    o = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.5 + k * 1.5)) / k for k in (1, 2.76, 5.4))
    return o * amp


def chord_freqs(name, octave=3):
    root, iv = CHORDS[name]
    base = hz(root, octave)
    return [base * 2 ** (i / 12) for i in iv]


def theme_audio(name, dur, seed=0):
    th = THEMES[name]
    beat = 60 / th["bpm"]
    bar = 4 * beat
    n = int(dur * SR) + SR * 3
    L = np.zeros(n); R = np.zeros(n)

    def add(sig, t0, pan=0.0):
        i = int(t0 * SR)
        if i >= n:
            return
        sig = sig[: n - i]
        L[i:i + len(sig)] += sig * (1 - max(0, pan))
        R[i:i + len(sig)] += sig * (1 + min(0, pan))
    nb = int(dur / bar) + 2
    for b in range(nb):
        ch = th["prog"][b % len(th["prog"])]
        t0 = b * bar
        fs = chord_freqs(ch, 3)
        add(pad([f * 2 for f in fs], bar + 0.6, 0.05), t0)
        # bass
        add(pluck_c(fs[0] / 2, bar * 0.9, 0.3, 0.32), t0, 0.0)
        add(pluck_c(fs[0] / 2 * (1.5 if b % 2 else 1), beat * 1.8, 0.3, 0.2), t0 + 2 * beat)
        notes = fs + [fs[0] * 2, fs[1] * 2]
        pat = th["pattern"]
        if pat in ("arp", "arp8"):
            step = beat / 2 if pat == "arp8" else beat / 2
            order = [0, 2, 1, 3, 2, 4, 3, 2]
            for k in range(8):
                f = notes[order[k] % len(notes)]
                add(pluck_c(f, 1.6, th["bright"], 0.16 if k % 2 == 0 else 0.11), t0 + k * step, pan=0.25 * (-1) ** k)
        elif pat == "sparse":
            for k in (0, 3, 5):
                f = notes[[0, 2, 4][[0, 3, 5].index(k)]]
                add(pluck_c(f, 2.4, th["bright"], 0.15), t0 + k * beat / 2, pan=-0.2)
            if th.get("bell") and b % 2 == 0:
                add(bell(notes[-1] * 2, 2.5, 0.05), t0 + beat * 2, pan=0.3)
        elif pat == "strum":
            for k, off in enumerate((0, 1.5, 2, 3)):
                for j, f in enumerate(notes[:5]):
                    add(pluck_c(f, 1.4, th["bright"], 0.07), t0 + off * beat + j * 0.012, pan=0.2)
    out = np.stack([L, R], 1)[: int(dur * SR)]
    return out


def theme_for(bid):
    p = bid[0]
    if bid in ("W00",) or p == "W":
        return "winter"
    if p == "S":
        return "spring"
    if p == "U":
        return "summer"
    if p == "F":
        return "fall"
    if p == "T":
        return "story"
    return "home"


# ---------------------------------------------------------------- sfx
def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def noise(n):
    return rng.uniform(-1, 1, n)


def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def bp(x, f, q=5):
    from scipy.signal import butter, sosfilt
    lo, hi = f / (1 + 1 / q), f * (1 + 1 / q)
    sos = butter(2, [max(20, lo), min(SR / 2 - 100, hi)], "bandpass", fs=SR, output="sos")
    return sosfilt(sos, x)


def sfx(name):
    t = lambda d: np.arange(int(d * SR)) / SR
    if name == "chime":
        return bell(hz("E", 6), 2.2, 0.35) + bell(hz("B", 6), 2.2, 0.2)
    if name in ("tag",):
        n = int(0.5 * SR)
        wh = bp(noise(n), 900, 2) * np.sin(np.linspace(0, np.pi, n)) * 0.5
        kn = np.sin(2 * np.pi * 320 * t(0.12)) * env_exp(int(0.12 * SR), 40)
        out = np.zeros(int(0.8 * SR)); out[:n] += wh; out[int(0.35 * SR):int(0.35 * SR) + len(kn)] += kn * 0.9
        return out * 0.5
    if name == "creak":
        tt = t(0.9)
        f = 260 + 90 * np.sin(2 * np.pi * 1.3 * tt) + 40 * np.sin(2 * np.pi * 7 * tt)
        ph = 2 * np.pi * np.cumsum(f) / SR
        saw = (ph / (2 * np.pi)) % 1 * 2 - 1
        return bp(saw, 700, 3) * np.sin(np.linspace(0, np.pi, len(tt))) * 0.5
    if name == "crunch":
        out = np.zeros(int(0.5 * SR))
        for k in range(6):
            i = int(rng.uniform(0, 0.4) * SR)
            g = bp(noise(1500), 2500, 1.5) * env_exp(1500, 60)
            out[i:i + 1500] += g * 0.6
        return out * 0.6
    if name == "thud":
        return (np.sin(2 * np.pi * 70 * t(0.5)) * env_exp(int(0.5 * SR), 9) + lp(noise(int(0.5 * SR)), 0.05) * env_exp(int(0.5 * SR), 20)) * 0.9
    if name == "car":
        tt = t(2.0)
        f = 55 + 20 * np.minimum(1, tt)
        ph = 2 * np.pi * np.cumsum(f) / SR
        return lp(np.sign(np.sin(ph)) * 0.5, 0.05) * np.sin(np.linspace(0, np.pi, len(tt))) * 0.5
    if name in ("baa", "moo"):
        d = 0.7 if name == "baa" else 1.1
        tt = t(d)
        f0 = (420 if name == "baa" else 130) * (1 + 0.04 * np.sin(2 * np.pi * 9 * tt))
        ph = 2 * np.pi * np.cumsum(f0) / SR
        saw = (ph / (2 * np.pi)) % 1 * 2 - 1
        v = bp(saw, 900 if name == "baa" else 450, 2) + 0.5 * bp(saw, 2400 if name == "baa" else 900, 3)
        return v * np.sin(np.linspace(0, np.pi, len(tt))) ** 0.5 * 0.45
    if name == "drip":
        tt = t(0.18)
        f = 1400 - 700 * tt / 0.18
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(len(tt), 25) * 0.35
    if name in ("snip", "click", "tick", "type"):
        n = int(0.05 * SR)
        g = bp(noise(n), 4000 if name != "tick" else 2500, 2) * env_exp(n, 120)
        if name == "snip":
            out = np.zeros(int(0.15 * SR)); out[:n] += g; out[int(0.08 * SR):int(0.08 * SR) + n] += g; return out * 0.6
        return g * 0.5
    if name in ("whoosh", "flip", "page", "paper", "poof", "wind"):
        d = {"whoosh": 0.6, "flip": 0.4, "page": 0.35, "paper": 0.5, "poof": 0.5, "wind": 2.5}[name]
        n = int(d * SR)
        fc = {"whoosh": 1200, "flip": 2500, "page": 3000, "paper": 2000, "poof": 600, "wind": 500}[name]
        return bp(noise(n), fc, 1.5) * np.sin(np.linspace(0, np.pi, n)) ** 2 * (0.5 if name != "wind" else 0.35)
    if name in ("coin", "ding"):
        f = hz("E", 7) if name == "coin" else hz("A", 6)
        return (np.sin(2 * np.pi * f * t(0.4)) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t(0.4))) * env_exp(int(0.4 * SR), 10) * 0.18
    if name == "ring":
        tt = t(1.4)
        on = (np.floor(tt * 6) % 2 == 0) & (tt % 0.7 < 0.55)
        return (np.sin(2 * np.pi * 1000 * tt) + np.sin(2 * np.pi * 1400 * tt)) * on * 0.08
    if name in ("hammer", "block", "drop"):
        f = {"hammer": 600, "block": 200, "drop": 300}[name]
        return np.sin(2 * np.pi * f * t(0.15)) * env_exp(int(0.15 * SR), 35) * 0.6
    if name == "boing":
        tt = t(0.5)
        f = 300 + 200 * np.sin(2 * np.pi * 6 * tt) * np.exp(-tt * 5)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(len(tt), 6) * 0.3
    if name in ("fork", "chalk", "scribble", "crackle", "tickets"):
        d = 0.6 if name != "crackle" else 2.0
        n = int(d * SR)
        out = np.zeros(n)
        for k in range(int(d * 30)):
            i = int(rng.uniform(0, d - 0.02) * SR)
            g = bp(noise(400), rng.uniform(1500, 5000), 3) * env_exp(400, 150)
            out[i:i + 400] += g
        return out * 0.35
    if name == "cluck":
        out = np.zeros(int(0.5 * SR))
        for k in range(3):
            i = int(k * 0.12 * SR)
            tt = t(0.07)
            out[i:i + len(tt)] += bp(np.sign(np.sin(2 * np.pi * 600 * tt)), 1200, 3) * env_exp(len(tt), 50)
        return out * 0.4
    if name == "buzz":
        tt = t(1.6)
        f = 210 + 12 * np.sin(2 * np.pi * 3 * tt)
        ph = 2 * np.pi * np.cumsum(f) / SR
        return bp((ph / (2 * np.pi)) % 1 * 2 - 1, 800, 2) * np.sin(np.linspace(0, np.pi, len(tt))) * 0.2
    if name == "boo":
        tt = t(1.4)
        f = 300 - 80 * tt
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.3 * np.sin(2 * np.pi * 5 * tt)) * np.sin(np.linspace(0, np.pi, len(tt))) * 0.18
    return np.zeros(10)


SFX_GAIN_DB = -20.0


VOICE_ONLY = "--with-music" not in sys.argv


def build_mix():
    scenes = timeline.build()
    total = timeline.total_duration(scenes)
    N = int(total * SR) + SR
    voice = np.zeros(N)
    for S in scenes:
        x, sr = sf.read(S.audio)
        assert sr == SR
        i = int(round((S.start + S.voice_off) * SR))
        voice[i:i + len(x)] += x
    # music: segments per theme with crossfades
    music = np.zeros((N, 2))
    segs = []
    for S in scenes:
        th = theme_for(S.id)
        if segs and segs[-1][0] == th:
            segs[-1][2] = S.start + S.dur
        else:
            segs.append([th, S.start, S.start + S.dur])
    xf = 1.5
    for k, (th, a, b) in enumerate(segs):
        a0 = max(0, a - (xf if k else 0))
        d = b - a0 + xf
        m = theme_audio(th, d, seed=k)
        n = len(m)
        env = np.ones(n)
        fi = int(xf * SR)
        if k:
            env[:fi] = np.linspace(0, 1, fi)
        env[-fi:] = np.linspace(1, 0, fi) if k < len(segs) - 1 else np.linspace(1, 0, fi)
        i = int(a0 * SR)
        music[i:i + n] += (m * env[:, None])[: N - i]
    # sfx
    fx = np.zeros(N)
    log = []
    for S in scenes:
        fn = common.SFX.get(S.id)
        if not fn:
            continue
        for (tt, name) in fn(S):
            if tt < 0 or tt > S.dur:
                continue
            s = sfx(name) * 10 ** (SFX_GAIN_DB / 20)
            i = int((S.start + tt) * SR)
            fx[i:i + len(s)] += s[: N - i]
            log.append((round(S.start + tt, 2), S.id, name))
    # ducking: music sits ~16 dB under the voice while she speaks
    from scipy.ndimage import maximum_filter1d
    venv = np.abs(voice)
    hop = 441
    frames = venv[: len(venv) // hop * hop].reshape(-1, hop).max(1)
    speaking = frames > 0.02
    speaking = maximum_filter1d(speaking.astype(float), size=130)  # hold ~1.3 s so short gaps do not pump
    # smooth attack/release
    g = np.zeros_like(speaking)
    acc = 0.0
    for i, s_ in enumerate(speaking):
        a = 0.35 if s_ > acc else 0.04
        acc += a * (s_ - acc)
        g[i] = acc
    duck_db = -9.0 * g  # extra dip during speech on top of the bed level
    gain = 10 ** (np.repeat(duck_db, hop) / 20)
    gain = np.concatenate([gain, np.full(N - len(gain), gain[-1])])
    # set the music bed level: during speech, music loudness = voice loudness - 16 dB
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    v_l = meter.integrated_loudness(voice[: int(total * SR)])
    sp_idx = np.repeat(g > 0.9, hop)[: int(total * SR)]
    mus_mono = music.mean(1)[: len(sp_idx)]
    m_l = meter.integrated_loudness(mus_mono[sp_idx] if sp_idx.sum() > SR * 5 else mus_mono)
    target = v_l - 16.0
    # account for the -9 dB duck that applies during speech
    base = 10 ** ((target - m_l + 9.0) / 20)
    music *= base * gain[:, None]
    if VOICE_ONLY:  # Stephen's choice (1 Nov 2026): narration only, no music or effects
        music[:] = 0
        fx[:] = 0
    mix = music.copy()
    mix[:, 0] += voice + fx
    mix[:, 1] += voice + fx
    mix = mix[: int(total * SR)]
    sf.write(os.path.join(BUILD, "premix.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
    sf.write(os.path.join(BUILD, "voice_track.wav"), voice[: int(total * SR)].astype(np.float32), SR, subtype="FLOAT")
    json.dump(log, open(os.path.join(BUILD, "sfx_log.json"), "w"))
    # report measured music-under-voice level
    mus_speech = meter.integrated_loudness(music.mean(1)[: len(sp_idx)][sp_idx]) if not VOICE_ONLY else None
    if not VOICE_ONLY:
        print(f"voice {v_l:.1f} LUFS, music under speech {mus_speech:.1f} LUFS (diff {v_l - mus_speech:.1f} dB)")
    # final loudness: two-pass loudnorm to -14 LUFS, TP -1.5 (headroom for AAC)
    src = os.path.join(BUILD, "premix.wav")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = ("loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:"
          "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}").format(**js)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af + ",alimiter=limit=0.72:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", os.path.join(BUILD, "mix.wav")], check=True)
    print("mix written", total)


if __name__ == "__main__":
    build_mix()
