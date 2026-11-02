# Video 008 cartoon: Nobody Can Find My Farm Online

A fully AI-generated cartoon explainer for the Agritourism Success channel, built from the approved video-008 script.
Every frame is drawn in code (Python + pycairo). The only sound is the narration in Stephen's saved voice,
**Young American Female Smooth** (Kokoro-82M ONNX; Stephen's saved recipe in `../../voices/young-american-female-smooth/VOICE.md`). No music, no sound effects.
The host is **Sarah**, a young farm host drawn in the same storybook style as the channel's earlier cartoons.

| Path | What it is |
| --- | --- |
| `script/video-008-script.md` | Every beat: what we see, words on screen, spoken line |
| `output/video-008-nobody-can-find-my-farm-online.mp4` | The finished video (1920x1080, 30 fps, H.264 High, AAC 192 kb/s, faststart) |
| `output/video-008.srt` | Captions from the real narration timings |
| `output/thumbnail-a.png`, `output/thumbnail-b.png` | 1280x720 thumbnails |
| `output/contact-sheet.jpg` | One still from every scene |
| `output/voice-comparison.wav` | Stephen's sample, then the saved recipe saying the same lines |
| `output/checks-report.md` | Measured checks |
| `src/` | All source code |

## Rebuild

Set up the repo once (see the README at the repo root: packages, `models/`, fonts). Then from this folder:

```bash
python3 src/voice.py                    # narration, one mastered file per beat -> build/audio/
python3 src/audio.py                    # narration-only mix at -14 LUFS -> build/mix.wav
python3 src/render.py video --crf 16    # frames -> build/video_noaudio.mp4
python3 src/mux.py                      # final encode into output/
python3 src/captions.py                 # output/video-008.srt
python3 src/thumbs.py                   # thumbnails
python3 src/contact.py                  # contact sheet
python3 src/checks.py                   # output/checks-report.md
python3 src/voice_compare.py            # output/voice-comparison.wav
```

`python3 src/render.py still K07@5` renders one frame of a scene for a quick look.

## How it is put together

- `beats.py` parses the script; `voice.py` renders the narration per beat following `voice/VOICE.md`
  (misaki G2P, two sentences per take, hand phonemes for names such as Kilgus and Fairbury).
- `timeline.py` times every scene from the real narration and builds the mouth envelope Sarah lip-syncs to.
- `kit/sarah.py` (shared) draws Sarah; `kit008.py` holds this video's props (phones, maps, ghost pin, listings, the phone gate,
  Jersey cows, the country store); `scenes008.py` has one function per beat.
- The shared drawing kit lives in `../../kit/`.
