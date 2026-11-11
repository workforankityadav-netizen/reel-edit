---
name: reel-edit-style
description: Edit 9:16 Instagram Reels / YouTube Shorts in the YT UNLOCKED reel style. Use when someone gives raw footage of a person talking, or a voiceover, and wants a reel, short, or vertical video: pauses removed with smooth cuts, the person in the bottom half with related images and motion graphics in the top half, 4–5 second full-screen 9:16 motion-graphic breaks, bold captions with yellow keywords throughout, pastel gradient look, whooshes, pops and music, mixed to -14 LUFS. Also use for "make a reel", "edit my short", "same reel style", "split-screen reel", or a voiceover-only graphics reel.
---

# Reel edit style

Pastel two-colour gradient with drifting blobs and a slowly turning starburst. White rounded cards with mock app UI. Bold condensed headlines with red keywords. A small black "topic" tag top-left. Captions in white with a thick black outline, keywords in yellow, a few words at a time. Fast zoom-blur cuts, a ribbon wipe (channel name, or the reel topic if no name is given, on a wavy band) at section changes, and a sound on every reveal. Full rules: `references/style.md`.

Two input types, one engine:

| Input | Mode | Layout |
|---|---|---|
| Raw footage of a person talking | `mode="footage"` | Pauses removed. The person sits in the **bottom half** (1080×960) and graphics or related images fill the **top half**. Every 10–15 s, one scene marked `full=True` hides the person for **4–5 s** and plays a full-screen 9:16 graphic. Captions run throughout, on the seam between the halves (or lower in full-screen breaks). |
| Voiceover only | `mode="voice"` | Full-screen 9:16 graphics the whole time, a new scene every 3–4 s. Pauses are tightened. |

## First time on a machine

Skills don't install software. Run the checker, which lists what is missing and installs it on request (macOS with Homebrew):

```bash
python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py            # check only
python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py --install  # brew-install ffmpeg/node/whisper-cpp + download the Whisper model
```

Needed: Python 3.9+ (standard library only), ffmpeg, Node 18+, whisper-cpp and its large-v3-turbo model (~550 MB). Hyperframes needs no install: `npx --yes hyperframes@0.9.7` fetches it on first run. Internet is needed at render time for Google Fonts and GSAP. Details and Windows/Linux notes: `references/setup.md`. Ask before installing anything for the user.

## Workflow

Run every command from the project folder. Reels are numbered: reel 1 lives in `reel-01/`. On Windows use `python` (or `py`) where these steps say `python3`.

1. **Make the project.** Run `python3 ~/.claude/skills/reel-edit-style/scripts/new_reel.py <project>`. It copies the scripts into `<project>/scripts`. Put the inputs in `<project>/raw/`. If the user supplies their own sound effects, rename them to `whoosh`, `swoosh`, `impact`, `pop`, `click`, `ding`, `riser` and `tick` (`.wav`) and put them in `<project>/sfx/`; they replace the default pack in `scripts/sfx/`.
2. **Prepare the audio.**
   - **Footage:**
     - If the clip is long, first transcribe the whole thing. Copy it to `reel-01/audio/voice.wav`, run `python3 scripts/transcribe.py 1`, then read `reel-01/audio/words.txt`.
     - Pick the strongest 30–60 s as `--ranges`.
     - Run `python3 scripts/cutpauses.py raw/<clip> 1 --ranges 12-41,55-70 --fx 0.5 --fy 0.35`.
     - The script removes every pause over 0.3 s, adds click-free 8 ms fades at each join, crops a 9:8 window around the person (`--fx`/`--fy` give the face position, 0–1) to `reel-01/assets/person.mp4`, writes `reel-01/audio/voice.wav`, and transcribes it.
     - Use `--audio <file>` when the voice was recorded separately.
   - **Voiceover:** run `python3 scripts/prep_voice.py raw/<file> 1`. It tightens pauses and transcribes. For one file holding several reels, run it once per reel with `--start`/`--end`.
   - Language: set `WHISPER_LANG=hi` (default), `en` or `auto`.
3. **Read the transcript** in `reel-NN/audio/words.txt`. If Whisper skipped a stretch (a gap over 2.5 s with speech), run `python3 scripts/fillgaps.py N`.
4. **Write the words** in `scripts/roman.py`, as `R[N]`. Write them exactly as spoken, in the caption language (Hindi speech is written in Roman Hinglish). Mark yellow caption keywords with `*word*`.
5. **Write the shot list** in `scripts/reels.py`, as `SPEC[N]`. See `references/widgets.md` for every graphic, with examples:
   - Each scene is `(spoken anchor, graphic, params)`. The anchor is the first words of the phrase where the scene starts, taken from `roman.py` (`None` for the first scene). Items inside a scene also appear on their spoken word (`*a` params such as `na`, `ha`, `sa`). **Graphics must land on the word, never before it.**
   - **Footage reels:** a new top-half graphic every 3–5 s. Every 10–15 s, add one `full=True` scene lasting 4–5 s, placed where an icon or number tells the point better than the face (a stat, a warning, a before/after). That scene must show something within 0.5 s of its start.
   - For related images, put the files in `reel-NN/assets/img/` and use `image` or `logos`. Use the user's own or properly licensed images, and never a third party's watermarked picture.
   - Ribbon wipe text: set `brand="Channel Name"` in `SPEC[N]` if the user gave a channel or brand name. Otherwise set `topic="Reel topic"`; if that is missing, the first scene's `topic` is used. With none of these, the ribbon has no text. Set `wipes=[i, ...]` for the scene indexes that open with it (section changes).
   - Also fill `COVERS[N]` and `TITLES[N]`.
6. **Build:** run `python3 scripts/make.py N`. Aim for a match of 93% or more. Fix every `WARN anchor` line, which means an item's word comes after its scene ends. Then run `npx --yes hyperframes@0.9.7 lint reel-NN`, which must report 0 errors.
7. **Look before rendering:** run `python3 scripts/snap.py N` and open `reel-NN/snap/contact-sheet*.jpg`. Check for:
   - text overlapping anything, or running outside its card;
   - a scene that is empty for over 1 s;
   - a face cut off in the bottom half (change `--fy` and re-run step 2);
   - captions covering the face.
   Fix, then rebuild.
8. **Render and mix:** run `python3 scripts/render.py N`. It renders, creates the effects and an original music loop, mixes voice + ducked music + effects at -14 LUFS, and writes `exports/reel-NN.mp4`. It takes about 1 minute per reel.
9. **Cover and title (optional):** `python3 scripts/covers.py` writes `covers/index.html`. Then run:
   ```bash
   cd covers && npx --yes hyperframes@0.9.7 snapshot . --at 0.5,1.5,... -o out --no-end && cd ..
   python3 scripts/finish.py
   ```
   This puts the cover on the first 0.4 s and saves `exports/<title>.mp4`.
10. **Report** the length, loudness and file path, and say what you could not check (you can't hear the audio).

## Rules that matter most

- **Sync:** every visual appears on its spoken word (the `make.py` anchors), never on a line start or a guess.
- **Pace:** a visual change every 3–4 s, and nothing on screen still for more than about 3 s.
- **Smooth:** no camera punch-zoom on every element. Scene cuts are short zoom-blurs, and the ribbon wipe is only for section changes.
- **Captions** are always on screen while someone speaks: 2–5 words, keywords in yellow, never over the face.
- **Footage:** cuts sit inside pauses (the script handles this). Never cut mid-word, and keep the person's eyes in the upper third of the bottom half.
- Full-screen breaks last **4–5 s**, roughly one per 10–15 s, and are never back to back.
- Don't invent facts. Numbers on screen must match what is said; if a number is wrong, show the correct one with a `*`.
- Use the user's own logos, thumbnails and images when possible. Label self-made mock screens "Illustration" when they could pass as real.

## Files

- `scripts/engine.py`: the graphics, icons, palettes and sound-cue rules. Add new graphics here as `g_name(c, t, p)`.
- `scripts/reel_template.html`: look, motion engine and footage split.
- `scripts/make.py`, `transcribe.py`, `fillgaps.py`, `prep_voice.py`, `cutpauses.py`, `tighten.py`.
- `scripts/render.py`, `snap.py`, `mix.py`, `sfx2.py`, `reelmusic.py`, `covers.py`, `finish.py`, `tools.py` (finds ffmpeg / npx / whisper on Mac, Linux and Windows).
- `scripts/sfx/`: the default sound pack (whoosh, swoosh, impact, pop, click, ding, riser, tick), used automatically. `scripts/sfx/extra/` holds more transitions (whip, thump, swell, drop, glitch, snap, chime, key, boom, riser_long); copy one into `<project>/sfx/` under a kit name to use it, e.g. `whip.wav` → `whoosh.wav`. Credits are in `scripts/sfx/CREDITS.md`.
- `scripts/examples/`: 10 real reels (`roman_example.py`, `reels_example.py`) to copy patterns from.
- `references/style.md` (look, motion, sound), `references/widgets.md` (graphics and params), `references/setup.md` (installing).
