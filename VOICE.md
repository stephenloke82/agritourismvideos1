# Midwest Female Warm: voice recipe

Stephen's saved AI voice. Every narration in this repo uses it. `Midwest-Female-Warm.mp3` in this folder is a reference sample of the voice (rebuilt 1 Nov 2026), so compare against it.

## Saved settings (original, 29 Oct 2026)

- Engine: Kokoro-82M (royalty-free), ONNX version
- Voice blend: `af_heart` 0.6 + `af_sarah` 0.4 (weighted sum of the two voice style arrays)
- Speed: 0.97
- Language: American English (en-us)
- Mastering: about -16 LUFS
- Export: 192 kbps mono MP3

## Model files

- https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
- https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin (numpy .npz, each voice 510 x 1 x 256)

## Pronunciation

Best: the full misaki engine (`pip install "misaki[en]"`), or `pip install kokoro-onnx`.

Fallback when those cannot be installed: clone https://github.com/hexgrad/misaki and https://github.com/thewh1teagle/kokoro-onnx, then look words up in `misaki/data/us_silver.json` with `us_gold.json` over it (gold overrides silver, use a dict value's `DEFAULT`). Token vocab is `src/kokoro_onnx/config.json` key `vocab`. Overrides: `a` -> `ɐ`, `the` -> `ðə`. Any word missing from the dictionaries must get phonemes by hand, never be dropped.

## Rendering

- Split at commas and sentence ends, synthesise each phrase separately.
- Style vector: `voice[min(len(tokens), len(voice)) - 1]`. Input `[[0, *tokens, 0]]`, `speed` 0.97.
- Trim each phrase to its speech: moving-average envelope of 240 samples, threshold 2% of peak, keep 40 ms padding.
- Pause after a comma: random 0.12 to 0.20 s. After a sentence end: random 0.30 to 0.45 s. Seed 7.
- Lead-in 0.25 s, tail 0.30 s. Normalise peak to 0.9. Model output is 24 kHz.

## Mastering (ffmpeg)

```
-af bass=g=2:f=180,treble=g=-2:f=7000,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120,loudnorm=I=-16:TP=-1.5:LRA=7
-ar 44100 -ac 1 -b:a 192k
```

Pause values and the dictionary method date from the 1 Nov 2026 rebuild, not the original notes, so a new script matches that rebuild and may not match the 29 Oct file sound for sound.
