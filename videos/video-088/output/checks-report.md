# Checks report: video-088 cartoon

## ffprobe
- duration: 493.23 s (8 min 13.2 s)
- file size: 56.69 MB
- video: h264 High 1920x1080 yuv420p 30/1 fps
- audio: aac 44100 Hz 2 ch, 169 kb/s
- faststart (moov before mdat): True

## Loudness and silence (measured with ffmpeg, not heard)
- integrated loudness: -14.0 LUFS (target -14)
- true peak: -2.5 dBTP (target under -1)
- loudness range: 2.3 LU
- silences over 1.5 s: 2
  - 477.44s to 485.51s (8.07s) in Z09
  - 487.40s to 493.24s (5.84s) in Z10

## Spoken script vs what was sent to the voice
- 84 beats, 1430 words compared, mismatches: 0 
- words given hand phonemes: Benzakein, Eventbrite, Ledbury, Moulton, Skagit, Tripadvisor, ebook
