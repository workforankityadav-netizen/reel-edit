# Install on Windows 10 / 11

**Needs:** Windows 10 (21H2+) or 11, about 2 GB of free disk space, and **winget** (preinstalled on Windows 11; on Windows 10 get "App Installer" from the Microsoft Store).

## Option A: let Claude Code do it
Open Claude Code and say:
> Install this skill: https://github.com/<your-username>/reel-edit-style

Approve the steps Claude shows, and click **Yes** on any Windows permission (UAC) pop-ups.

## Option B: by hand
1. Open **PowerShell** (Start → type "PowerShell").
2. If you don't have Git:
   ```bash
   winget install --id Git.Git -e
   ```
   Then close and reopen PowerShell.
3. Get the repo:
   ```bash
   git clone https://github.com/<your-username>/reel-edit-style.git $HOME\reel-edit-style
   ```
   (Or download the ZIP from GitHub and unzip it to `C:\Users\<you>\reel-edit-style`.)
4. Run the installer:
   ```bash
   cd $HOME\reel-edit-style; powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
   ```
   It installs, skipping anything you already have:
   1. Python 3.12, Node.js LTS, FFmpeg, Git and yt-dlp, with winget.
   2. whisper.cpp (`whisper-cli.exe`) from its official GitHub release into `%USERPROFILE%\.reel-tools\whisper`, added to your PATH.
   3. The Whisper model (~550 MB) into `%USERPROFILE%\.whisper-models`.
   4. The skill, copied to `%USERPROFILE%\.claude\skills\reel-edit-style`.
   5. The Hyperframes renderer, warmed up.
   6. A final check.
5. **Close and reopen Claude Code** so it picks up the new PATH and the skill.

## Check it any time
```bash
python $HOME\.claude\skills\reel-edit-style\scripts\check_setup.py
```

## Notes
- Use `python` (not `python3`) on Windows. The skill's scripts work the same way on Windows and Mac; no Bash or WSL is needed.
- If `whisper-cli` is not found after installing, open a **new** PowerShell window (PATH updates only apply to new windows).
- Antivirus may scan `whisper-cli.exe` on first run. That's normal.

## Update
```bash
cd $HOME\reel-edit-style; git pull; powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```
