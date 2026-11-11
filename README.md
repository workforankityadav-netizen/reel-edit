# Reel Edit Style: a Claude Code skill for 9:16 reels

Turn **raw talking-head footage** or a **voiceover** into finished Instagram Reels / YouTube Shorts:

- **Pauses removed**, with smooth click-free cuts.
- **Split screen:** you in the bottom half, motion graphics or related images in the top half.
- **Full-screen 9:16 motion-graphic breaks** of 4–5 s, every 10–15 s.
- **Bold captions** throughout, with yellow keywords, timed to each spoken word.
- **Look:** pastel gradient, white UI cards, and a ribbon wipe showing your channel name (or the reel topic).
- **Sound:** whoosh, pop, click and riser sound effects plus an original music loop, mixed to -14 LUFS.
- **Voiceover-only mode:** full-screen graphic reels.

## Install: the easy way (Claude Code does it)

1. Open **Claude Code**.
2. Paste this repo's link and say:
   > **Install this skill: https://github.com/<your-username>/reel-edit-style**

Claude clones the repo, detects Mac or Windows, runs the right installer and checks everything. Then restart Claude Code.

## Install by hand

- **Mac:** follow [INSTALL-MAC.md](INSTALL-MAC.md). It comes down to:
  ```bash
  git clone https://github.com/<your-username>/reel-edit-style.git && cd reel-edit-style && bash install-mac.sh
  ```
- **Windows:** follow [INSTALL-WINDOWS.md](INSTALL-WINDOWS.md). In PowerShell:
  ```bash
  git clone https://github.com/<your-username>/reel-edit-style.git; cd reel-edit-style; powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
  ```

## What gets installed

| Tool | Why |
|---|---|
| Python 3 | runs every script (no pip packages) |
| FFmpeg | cutting pauses, cropping, mixing, loudness |
| Node.js 18+ | runs Hyperframes, the renderer (it downloads itself on first use) |
| whisper.cpp + the large-v3-turbo model (~550 MB) | word-level captions in Hindi and English |
| yt-dlp | optional, for reference videos |
| The skill | copied to `~/.claude/skills/reel-edit-style` |

The sound effects ship inside the skill (`skill/reel-edit-style/scripts/sfx/`); see the credits there. Remotion and other repos are not needed.

## Use

In Claude Code, from any folder:

> Make a reel from `clip.mov` using the reel-edit-style skill. Channel name: **My Channel**.

> Make a voiceover reel from `voice.mp3` using the reel-edit-style skill.

Your reel is saved to `<project>/exports/reel-01.mp4`. To use your own sound effects, put `whoosh.wav`, `pop.wav` and similar files in the project's `sfx/` folder.

## Folder map

```
install-mac.sh            Mac installer (Homebrew)
install-windows.ps1       Windows installer (winget + GitHub release)
INSTALL-MAC.md            Mac guide
INSTALL-WINDOWS.md        Windows guide
CLAUDE.md                 instructions Claude follows when asked to install
skill/reel-edit-style/    the skill itself: SKILL.md, scripts, sound pack, references
```
