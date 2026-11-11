# Install on Mac

**Needs:** macOS 12+ and about 2 GB of free disk space. Apple Silicon or Intel both work.

## Option A: let Claude Code do it
Open Claude Code and say:
> Install this skill: https://github.com/<your-username>/reel-edit-style

Approve the steps Claude shows. Homebrew may ask for your Mac password in the terminal; type it there yourself.

## Option B: by hand
1. Open **Terminal**.
2. Get the repo:
   ```bash
   git clone https://github.com/<your-username>/reel-edit-style.git ~/reel-edit-style
   ```
   (If `git` is missing, macOS will offer to install the Command Line Tools. Accept, then run the command again. Or download the ZIP from GitHub and unzip it to `~/reel-edit-style`.)
3. Run the installer:
   ```bash
   cd ~/reel-edit-style && bash install-mac.sh
   ```
   It installs, skipping anything you already have:
   1. Homebrew, if missing.
   2. python, ffmpeg, node, whisper-cpp and yt-dlp.
   3. The Whisper model (~550 MB) into `~/.whisper-models/`.
   4. The skill, copied to `~/.claude/skills/reel-edit-style`.
   5. The Hyperframes renderer, warmed up.
   6. A final check that shows OK for every tool.
4. **Restart Claude Code.**

## Check it any time
```bash
python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py
```

## Update
```bash
cd ~/reel-edit-style && git pull && bash install-mac.sh
```

## Remove
```bash
rm -rf ~/.claude/skills/reel-edit-style ~/.whisper-models
```
(The brew tools can stay; other apps use them too.)
