"""Measured comparison of a rendered beat against voice/Midwest-Female-Warm.mp3.
Pitch (autocorrelation F0), syllable-nucleus rate, pause ratio, spectral centroid, loudness."""
import sys, os, subprocess, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import find_peaks, butter, sosfilt

def load(p):
    tmp = p + ".cmp.wav"
    subprocess.run(["ffmpeg","-y","-v","error","-i",p,"-ar","16000","-ac","1",tmp],check=True)
    x, sr = sf.read(tmp); os.remove(tmp); return x, sr

def stats(p):
    x, sr = load(p)
    loud = pyln.Meter(sr).integrated_loudness(x)
    hop, win = 160, 640
    f0s, ens = [], []
    for i in range(0, len(x)-win, hop):
        f = x[i:i+win]*np.hanning(win); e = np.sqrt(np.mean(f**2)); ens.append(e)
        ac = np.correlate(f, f, "full")[win-1:]
        lo, hi = sr//400, sr//120
        k = lo + np.argmax(ac[lo:hi])
        if ac[0] > 0 and ac[k]/ac[0] > 0.45 and e > 0.01: f0s.append(sr/k)
    ens = np.array(ens); voiced = ens > 0.1*ens.max()
    sos = butter(2, [300, 2500], "bandpass", fs=sr, output="sos")
    env = np.abs(sosfilt(sos, x)); env = np.convolve(env, np.ones(400)/400, "same")[::160]
    pk, _ = find_peaks(env, height=0.15*env.max(), distance=10, prominence=0.05*env.max())
    speech_t = voiced.sum()*hop/sr
    spec = np.abs(np.fft.rfft(x)); fr = np.fft.rfftfreq(len(x), 1/sr)
    return dict(dur=len(x)/sr, f0_median=np.median(f0s), f0_iqr=np.subtract(*np.percentile(f0s,[75,25])),
                syl_per_speech_s=len(pk)/speech_t, speech_ratio=speech_t/(len(x)/sr),
                centroid=float((spec*fr).sum()/spec.sum()), lufs=loud)

for p in sys.argv[1:]:
    s = stats(p); print(os.path.basename(p).ljust(28), "  ".join(f"{k}={v:.2f}" for k, v in s.items()))
