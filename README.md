# Agritourism Success cartoon videos

Fully AI-generated cartoon explainers for the Agritourism Success YouTube channel. Every frame is drawn in code
(Python + pycairo) and narrated with Stephen's saved Kokoro voices. One repo, one folder per video, one shared kit.

```
kit/      shared drawing kit: gfx, characters (Dot, Sarah, villagers, animals), props, season sets, icons, fonts
voices/   Stephen's saved voices: a VOICE.md recipe and a reference sample for each
videos/   one folder per video: script/, src/ (that video's scenes and pipeline), output/ (final MP4, captions,
          thumbnails, contact sheet, checks report)
models/   Kokoro model files, shared by every video (not committed; see below)
```

| Video | Host | Voice | Length |
| --- | --- | --- | --- |
| [video-045](videos/video-045): 30 Farm Event Ideas by Season, With Real Ticket Prices | Dot | Midwest Female Warm | 10:44 |
| [video-008](videos/video-008): Nobody Can Find My Farm Online | Sarah | Young American Female Smooth | 8:16 |

## Set up once

```bash
pip install pycairo numpy scipy soundfile pyloudnorm onnxruntime kokoro-onnx fonttools pillow spacy regex
pip install --no-deps misaki num2words
python3 -m spacy download en_core_web_sm
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python3 kit/fonts.py
```

Then build a video from inside its folder, for example `cd videos/video-008` and follow its README.

## Starting a new video

1. Make `videos/video-NNN/` with `script/`, `src/` and `output/`. Copy the pipeline files (`beats.py`, `timeline.py`,
   `voice.py`, `audio.py`, `render.py`, `mux.py`, `captions.py`, `contact.py`, `checks.py`, `thumbs.py`, `common.py`)
   from the latest video and change the names.
2. Write the beat script (`## ID | what we see | words on screen`, then the spoken line).
3. Write that video's scenes in `src/`, using the shared kit. Add new props or characters to `kit/` only when they
   are reusable.
4. Keep each final MP4 under about 95 MB (GitHub refuses files over 100 MB). When the repo nears 1 to 2 GB, keep final
   MP4s in Google Drive or Descript and commit only code, scripts and thumbnails.
5. Work on a branch and merge it into `main` when the video is approved.
