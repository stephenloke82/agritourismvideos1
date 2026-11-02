# Build brief: video-045 cartoon

Build "30 Farm Event Ideas by Season, With Real Ticket Prices" as a finished 1920x1080 cartoon explainer for the Agritourism Success YouTube channel. Everything is AI-generated. No stock footage, no sampled music.

`script/video-045-script.md` holds every beat: its scene idea, the words on screen and the spoken line. Do not change facts, prices, farm names or the spoken words. If a word cannot be voiced, fix the pronunciation, not the sentence.

## Narration

Follow `voice/VOICE.md` exactly. Compare a test line against `voice/Midwest-Female-Warm.mp3` for pace and tone before rendering the rest. Render one audio file per beat so scene timing comes from real durations. Hold the marked `(beat)` silences. If Kokoro cannot be obtained, stop and report it. Do not swap in another voice.

## Look

- A warm hand-drawn storybook cartoon, drawn in code (Python with pycairo, skia-python or Pillow, whichever renders fastest at this size). Thick soft ink outlines, flat colour with gentle shading, rounded shapes.
- Palette from the Open the Gate game: sky `#1b36a8`, gold `#f2b632`, tomato `#e2452f`, leaf `#3f8f3a`, cream `#fbf1d9`, paper `#fff8e8`, ink `#1b1f3a`, wood `#c8955a`. Never a black background.
- Host: Dot, a warm farmer woman in a gold straw hat with a tomato-red band, drawn in full body from the mentor portrait in Open the Gate. She blinks, gestures, walks in and out, and her mouth moves from the audio's loudness envelope. She is the same character in every scene.
- Season sets: winter (snow, bare trees, warm barn lights), spring (lambs, blossom, mud), summer (sun, sunflowers, long tables), fall (pumpkins, corn, gold light). Each is a layered background with slow parallax and weather (snow, petals, heat shimmer, leaves).
- Every one of the 30 events gets its own small illustrated vignette with visible motion: goats on yoga mats, a lamb being born under a heat lamp, sap dripping into a bucket. No two share a drawing.
- A wooden price tag swings in for each event with the price in very large type. Farm name and place sit below it in smaller type.
- A "No. X of 30" tracker stays top right during the list. A four-season wheel shows where we are.
- Colour-coded season chapter cards with a soft chime: winter sky blue, spring leaf green, summer gold, fall tomato.
- The Twelve-Month Gate is the running image: a wooden farm gate that opens, closes and returns at the close.

## Edit rules

- Something changes on screen every 3 to 6 seconds, with nothing on screen under 1.2 seconds.
- Straight cuts between scenes, soft fades only for build-ups. Words ease in slowly and stay, never pop.
- Big type for viewers over 40: body text at least 54 px, prices at least 120 px, high contrast, safe margins, no text touching a box edge.
- Count-up animation on key numbers.
- A hard stop or beat of silence before each turning point marked in the script.
- End screen: 20 seconds of Dot waving at the open gate, with blank space kept for YouTube's video and subscribe elements, the short URLs on screen, and a small line: "Narration and animation are AI-generated."

## Sound

- Original music synthesised in code: gentle acoustic-feeling folk (plucked strings, soft pads), one variation per season, ducked about 16 dB under the voice.
- Small synthesised sound effects (gate creak, chime, tag swing, snow crunch) kept quiet.
- Final mix about -14 LUFS, true peak under -1 dB, no clipping.

## Deliverables (commit these)

- `output/video-045-30-farm-event-ideas.mp4`: H.264 High, yuv420p, 30 fps, 1920x1080, AAC 192 kbps, with faststart. Keep it under 95 MB so it pushes to GitHub. Raise CRF rather than lowering the resolution.
- `output/video-045.srt`: captions from the beat timings, spoken words exactly.
- `output/thumbnail-a.png` and `output/thumbnail-b.png`: 1280x720, as described in the script file.
- `output/contact-sheet.jpg`: one still from every scene.
- All source code in `src/`, with a short `README.md` saying how to rebuild.

Do not commit raw frames, model files or caches. Add them to `.gitignore`.

## Checks before finishing

Actually run these and report the results:

- ffprobe: duration, resolution, streams.
- Measure loudness, true peak and any silence over 1.5 seconds that the script does not mark.
- Compare the spoken script word for word against what was sent to the voice, and list any word that needed hand phonemes.
- Look at every still in the contact sheet. Fix overflowing text, collisions and anything off-model.
- Check each of the 30 on-screen prices against the script.

You cannot hear audio, so say so, and say which checks were measured rather than heard. Push to `main` if allowed, otherwise to your branch, and report the branch name.
