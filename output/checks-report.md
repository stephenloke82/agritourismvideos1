# Checks report: video-045

## ffprobe
- duration: 643.80 s (10 min 43.8 s)
- file size: 80.61 MB (80614047 bytes)
- video: h264 High 1920x1080 yuv420p 30/1 fps, 798 kb/s
- audio: aac LC 48000 Hz 2 ch, 195 kb/s
- faststart (moov before mdat): True

## Loudness and silence (measured with ffmpeg, not heard)
- integrated loudness: -14.0 LUFS (target -14)
- true peak: -1.4 dBTP (target under -1)
- loudness range: 1.4 LU
- sample peak (per channel / overall): -1.575012, -1.589042, -1.575012 dBFS
- silences over 1.5 s in the final mix (below -50 dB): 0 
- gaps over 1.5 s in the narration track (music still plays under them): 1
  - 630.24s to 643.8s (13.56s) in C07: end screen (20 s, marked in BUILD.md)

## Spoken script vs what was sent to the voice
- 70 beats, 1576 words compared, mismatches: 0
- words given hand phonemes (29 spellings): Agritourism /ˈæɡɹɪtˌʊɹɪzəm/, Angus /ˈæŋɡəs/, Baylham /bˈAləm/, Buford /bjˈufəɹd/, Chazy /ʃAzˈi/, Cotley /kˈɑtli/, Crieff /kɹˈif/, Elburn /ˈɛlbɜɹn/, Kuipers /kˈIpəɹz/, Lennox /lˈɛnəks/, Lomond /lˈOmənd/, Loretto /ləɹˈɛɾO/, Lunan /lˈunən/, Maybury /mˈAbəɹi/, Maybury's /mˈAbəɹi/, McDougal /məkdˈuɡᵊl/, McDougal's /məkdˈuɡᵊl/, Nicholson /nˈɪkᵊlsən/, Niki's /nˈɪki/, Ormsby /ˈɔɹmzbi/, Pineland /pˈInlˌænd/, Ramon /ɹəmˈOn/, Santa /sˈæntə/, Schaefer /ʃˈAfəɹ/, Springville /spɹˈɪŋvˌɪl/, Vala's /vˈælə/, agritourism /ˈæɡɹɪtˌʊɹɪzəm/, ebook /ˈibˌʊk/, schoolchildren /skˈulʧˌɪldɹᵊn/

## On-screen prices vs script
- H02 (hook): script '£13.95 per person' | tag '£13.95 per person' | OK
- W01 (No. 1): script '$10 a foot' | tag '$10 a foot' | OK
- W02 (No. 2): script '£6.50 per car' | tag '£6.50 per car' | OK
- W03 (No. 3): script '$17 to $20' | tag '$17 to $20' | OK
- W04 (No. 4): script '£14.95 per child' | tag '£14.95 per child' | OK
- W05 (No. 5): script '$55 per person' | tag '$55 per person' | OK
- W06 (No. 6): script '£5 per person' | tag '£5 per person' | OK
- W07 (No. 7): script '$130 per person' | tag '$130 per person' | OK
- W08 (No. 8): script '£13.95 per person' | tag '£13.95 per person' | OK
- S01 (No. 9): script '$16 adult, $10 child' | tag '$16 adult $10 child' | OK
- S02 (No. 10): script '$50, limit 10' | tag '$50 limit 10' | OK
- S03 (No. 11): script '$50, one hour' | tag '$50 one hour' | OK
- S05 (No. 12): script '£25 to £195' | tag '£25 to £195' | OK
- S06 (No. 13): script '£17.50 per person' | tag '£17.50 per person' | OK
- S07 (No. 14): script 'C$7 per child' | tag 'C$7 per child' | OK
- S08 (No. 15): script '$20 to $25' | tag '$20 to $25' | OK
- S09 (No. 16): script '$10 early, $15 at the gate' | tag '$10 early $15 at the gate' | OK
- U01 (No. 17): script '$35 per person' | tag '$35 per person' | OK
- U02 (No. 18): script '$11.99, bucket $19.99' | tag '$11.99 bucket $19.99' | OK
- U03 (No. 19): script '£7.75 peak, £5.75 off-peak' | tag '£7.75 peak £5.75 off-peak' | OK
- U04 (No. 20): script '$375 per child, per week' | tag '$375 per child, per week' | OK
- U05 (No. 21): script '$40' | tag '$40' | OK
- U06 (No. 22): script '$45 to $95' | tag '$45 to $95' | OK
- U07 (No. 23): script '£105' | tag '£105' | OK
- F01 (No. 24): script '$12' | tag '$12' | OK
- F02 (No. 25): script '$18.52' | tag '$18.52' | OK
- F03 (No. 26): script '$26.99 weekday, $45.99 weekend' | tag '$26.99 weekday $45.99 weekend' | OK
- F04 (No. 27): script 'From $36' | tag 'From $36' | OK
- F05 (No. 28): script 'C$90' | tag 'C$90' | OK
- F06 (No. 29): script '$10' | tag '$10' | OK
- F07 (No. 30): script '£60' | tag '£60' | OK
- prices checked: 31, mismatches: 0

## Layout checks (measured)
- smallest price size used: 128px (rule: at least 120px)
- tag/banner/tracker overflow or collision problems: 0
