# Video 045: 30 Farm Event Ideas by Season, With Real Ticket Prices

A fully AI-generated cartoon explainer for the Agritourism Success channel. Every frame is drawn in code
(Python + pycairo), every sound is synthesised in code, and the narration is the saved voice
**Midwest Female Warm** (Kokoro-82M ONNX, `af_heart` 0.6 + `af_sarah` 0.4, speed 0.97).

## What's here

| Path | What it is |
| --- | --- |
| `BUILD.md` | The build brief |
| `script/video-045-script.md` | Every beat: what we see, words on screen, spoken line (final, not edited) |
| `voice/VOICE.md`, `voice/Midwest-Female-Warm.mp3` | Voice recipe and reference sample |
| `output/video-045-30-farm-event-ideas.mp4` | The finished video (1920x1080, 30 fps, H.264 High, AAC 192 kb/s, faststart) |
| `output/video-045.srt` | Captions from the real narration timings, spoken words exactly |
| `output/thumbnail-a.png`, `output/thumbnail-b.png` | 1280x720 thumbnails as described in the script |
| `output/contact-sheet.jpg` | One still from every scene (70 scenes) |
| `output/checks-report.md` | Results of the checks listed in BUILD.md |
| `src/` | All source code |

## Rebuild

Needs Python 3.11+, ffmpeg, and about 2 GB of disk. From the repo root:

```bash
pip install pycairo numpy scipy soundfile pyloudnorm onnxruntime kokoro-onnx fonttools pillow spacy num2words regex
pip install --no-deps misaki
python3 -m spacy download en_core_web_sm
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python3 src/fonts.py            # Fredoka + Nunito (OFL) static cuts into ~/.fonts
python3 src/voice.py            # narration, one mastered file per beat -> build/audio/
python3 src/audio.py            # music, sound effects, ducking, -14 LUFS mix -> build/mix.wav
python3 src/render.py video --crf 16   # frames -> high-quality intermediate build/video_noaudio.mp4 (4 workers)
python3 src/mux.py              # final encode into output/, raising CRF until under 92 MB
python3 src/captions.py         # output/video-045.srt
python3 src/thumbs.py           # output/thumbnail-a.png, thumbnail-b.png
python3 src/contact.py          # output/contact-sheet.jpg
python3 src/checks.py           # output/checks-report.md
```

`python3 src/render.py still W01@4.5` renders one frame of a scene for a quick look.

## How it is put together

- `beats.py` parses the script. `voice.py` follows `voice/VOICE.md`: misaki G2P (full engine with spaCy),
  phrases split at commas and sentence ends, style row `voice[min(len(tokens), 510) - 1]`, trim at 2% of the
  240-sample envelope peak with 40 ms padding, seeded pauses (seed 7), 0.8 s for each `(beat)`, then the
  ffmpeg mastering chain. Words missing from misaki's dictionaries are listed in `HAND` with hand-written phonemes.
- `timeline.py` builds the scene list from the real narration durations and the mouth envelope Dot lip-syncs to.
- `gfx.py`, `chars.py`, `props.py`, `sets.py`, `icons.py` are the drawing kit: Dot (drawn from her portrait),
  villagers, animals, the gate, price tags, the tracker and season wheel, the four season sets with parallax and weather.
- `vignettes.py` holds the 30 event scenes; `scenes_main.py` holds everything else.
- `audio.py` writes the music (Karplus-Strong plucked strings and pads, one variation per season), the sound effects
  and the mix. Music sits about 16 dB under the voice while she speaks.

Model files, fonts, frames and intermediate audio live in `build/` and `models/` and are not committed.
