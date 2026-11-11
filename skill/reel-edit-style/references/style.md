# Look, motion and sound

## Canvas
- 1080×1920 at 30 fps, H.264 plus AAC.
- Loudness -14 LUFS integrated, true peak at or below -1 dBTP.

## Background
- A two-colour pastel gradient with two large blurred blobs that drift on every cut, plus a starburst that turns slowly. It stays the same for the whole reel.
- Ten palettes rotate by reel number (`PAIRS` in `engine.py`), so a batch doesn't look identical.

## Type
- **Headlines:** Roboto Condensed 800. Black ink, with keywords in red (`*word*`).
- **Topic tag:** Space Mono in a white pill with a black bolt dot, top left.
- **Captions:**
  - Roboto Condensed 800, about 86 px, white with a 14 px black outline. Keywords are yellow (#ffe14d).
  - 2–5 words or about 30 characters per caption. Each caption pops in, and they follow the voice word by word.
  - Hindi speech is captioned in Roman Hinglish, because the font has no Devanagari.
- **Covers:** Anton. Three tilted strips (black, red, yellow) with a short question and one icon.

## Footage mode layout
- **Top half (0–960 px):** graphics, scaled to 74% so a full graphic fits, or related images and logos in white cards.
- **Bottom half (960–1920 px):** the person, cropped 9:8 around the face, with a white line and a soft shade at the seam.
- **Captions:** on the seam (top 830 px), so they never cover the face.
- **Full-screen break (`full=True`):** the person slides down and fades out, the graphic takes the whole frame for 4–5 s, and the captions drop to 1350 px. Then the person slides back.
- **Cuts:** every pause over 0.3 s is removed. Joins sit inside silences, with 80 ms of air and 8 ms fades, so speech flows with no clicks.

## Motion
- **Scene cuts:**
  - A 0.3 s zoom-blur in (0.9 → 1 scale, 14 px blur) and a 0.2 s zoom-blur out.
  - A ribbon wipe only at section changes. The wavy band shows the channel or brand name if given, otherwise the reel topic, otherwise no text.
  - Each scene drifts slowly (scale 1 → 1.05).
- **Entrances:** pop (back-out), up, rise, left, right, word-by-word, stamp (for big numbers, with a white flash), and grow bars.
- **Timing:** everything appears on its spoken word. Expect a new visual every 3–4 s, and nothing still for more than about 3 s.
- **No:** punch-zoom on every element, long static cards, or visuals that come before the voice.

## Sound
- **Effects:** the kit has whoosh, swoosh, impact, pop, click, ding, riser and tick. They come from the animation automatically: pop on pops, impact on stamps, tick on slide-ins, whoosh/swoosh on cuts, a riser before ribbon wipes, and a whoosh in and out of full-screen breaks. Cues of the same type have a minimum gap, so the mix doesn't get dense.
- **Music:** an original 8-bar loop per reel (`reelmusic.py`) at -19 dB, sidechain-ducked under the voice.
- **Voice:** high-pass, light compression and loudnorm. The final mix is two-pass loudnorm to -14 LUFS.
- **User sound effects:** files in `<project>/sfx/` named after a kit sound replace that sound.
