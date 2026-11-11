# For Claude: installing this repo

This repo is a Claude Code skill (`skill/reel-edit-style`) plus installers. When the user asks to **install** it:

1. **Get the repo.** If you are not already inside a clone, `git clone <repo url>` into a temporary or working folder and `cd` into it. If git is missing on Windows, tell the user to run `winget install Git.Git` first, or download the repo ZIP and unzip it.
2. **Detect the OS** and tell the user, in one line, what will be installed: Python, FFmpeg, Node.js, whisper.cpp, the ~550 MB Whisper model, yt-dlp, and the skill. Ask for a yes before installing anything.
3. **Run the installer:**
   - macOS: `bash install-mac.sh`. Homebrew may ask the user for their Mac password in the terminal; tell them so, and never type passwords yourself.
   - Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File .\install-windows.ps1`. winget may show UAC prompts; the user approves them.
   - Linux: follow `skill/reel-edit-style/references/setup.md` by hand (apt + whisper.cpp build).
   These take several minutes (the model download is ~550 MB), so run them as long-running commands.
4. **Verify:** `python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py` (Windows: `python %USERPROFILE%\.claude\skills\reel-edit-style\scripts\check_setup.py`). Every required line must say OK. Fix anything missing using the command shown next to it.
5. **Tell the user** to restart Claude Code so the skill loads, and how to use it: "Make a reel from <file> using the reel-edit-style skill. Channel name: …".

To update later: `git pull` in the clone and run the installer again (it skips what is already installed and replaces the skill folder).
