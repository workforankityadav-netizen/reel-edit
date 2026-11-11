# reel-edit-style: a Claude Code skill

Turns raw talking-head footage or a voiceover into finished 9:16 reels in the YT UNLOCKED reel style:
- pauses cut with smooth joins;
- the person in the bottom half, with motion graphics and related images in the top half;
- 4–5 s full-screen graphic breaks;
- bold captions with yellow keywords;
- sound effects and music, mixed to -14 LUFS.

## Install
1. Unzip so this folder sits at `~/.claude/skills/reel-edit-style/` (Windows: `%USERPROFILE%\.claude\skills\reel-edit-style\`).
2. Run the setup checker once. It installs ffmpeg, Node, whisper.cpp and the Whisper model if they are missing (macOS + Homebrew):
   `python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py --install`
3. Hyperframes, the renderer, needs no install. It downloads itself on first use through `npx`.

## Use
Open Claude Code in any folder and say, for example: "Make a reel from raw/clip.mov in my reel style" or "Make a reel from this voiceover". Claude follows `SKILL.md`.

`references/setup.md` lists every dependency.
