# Video 088 cartoon: How to Start a Flower Arranging Workshop on Your Farm

A fully AI-generated cartoon explainer for the Agritourism Success channel, built from the approved video-088 script
(Claude Doc: https://claude.ai/artifact/7LrKR2cz2xqDvZc48H4TaE). Every frame is drawn in code (Python + pycairo).
The only sound is the narration in Stephen's saved voice, **Young American Female Smooth** (Kokoro-82M ONNX; recipe in
`../../voices/young-american-female-smooth/VOICE.md`). No music, no sound effects. The host is **Sarah**.

| Path | What it is |
| --- | --- |
| `script/video-088-script.md` | Every beat: what we see, words on screen, spoken line |
| `output/video-088-flower-arranging-workshop.mp4` | The finished video (1920x1080, 30 fps, H.264 High, AAC 192 kb/s, faststart) |
| `output/video-088.srt` | Captions from the real narration timings |
| `output/thumbnail-a.png`, `output/thumbnail-b.png` | 1280x720 thumbnails ("$1 STEM → $55 SEAT", "SELL THE MORNING") |
| `output/contact-sheet.jpg` | One still from every scene |
| `output/checks-report.md` | Measured checks |
| `src/` | All source code |

## Rebuild

Set up the repo once (see the README at the repo root: packages, `models/`, fonts). Then from this folder:

```bash
python3 src/voice.py                    # narration, one mastered file per beat -> build/audio/
python3 src/audio.py                    # narration-only mix at -14 LUFS -> build/mix.wav
python3 src/render.py video --crf 16    # frames -> build/video_noaudio.mp4
python3 src/mux.py                      # final encode into output/
python3 src/captions.py                 # output/video-088.srt
python3 src/thumbs.py                   # thumbnails
python3 src/contact.py                  # contact sheet
python3 src/checks.py                   # output/checks-report.md
```

`python3 src/render.py still C06@5` renders one frame of a scene for a quick look.

## How it is put together

- The pipeline (`beats`, `timeline`, `voice`, `audio`, `render`, `mux`, `captions`, `contact`, `checks`, `thumbs`,
  `common`) is copied from video 008. `voice.py` adds hand phonemes for Benzakein, Skagit, Moulton, Ledbury,
  Tripadvisor and Eventbrite.
- New reusable props went into the shared kit as `../../kit/flowers.py`: zinnias, cosmos, dahlias, snapdragons,
  sweet peas on a trellis, branching sunflowers, mason jars with a four-layer arrangement (greens, stars, fillers,
  dancers), a vase, tin flower buckets, snips, name and care cards, a wrapped jar, the workshop table with guest
  stations, flower rows and an open-barn workshop.
- `kit088.py` holds this video's own pieces (cards, the five-step roadmap and tracker, the price board, the truck
  tailgate, ebook covers); `scenes088.py` has one function per beat.
- The How to Start a Flower Arranging Class ebook is not written yet: its cover shows the title only, and the
  narration says only that it is linked in the description.
