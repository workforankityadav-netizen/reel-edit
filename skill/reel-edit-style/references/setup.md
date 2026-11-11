# Setup: what to install and what installs itself

A skill is only instructions and scripts. **Nothing installs automatically** when someone adds the skill. Run the checker once per machine:

```bash
python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py            # report
python3 ~/.claude/skills/reel-edit-style/scripts/check_setup.py --install  # macOS + Homebrew: installs what is missing
```

| Tool | Needed? | How it gets there | Used for |
|---|---|---|---|
| Python 3.9+ | yes | preinstalled on most Macs, or `brew install python` | every script (standard library only; no pip packages) |
| ffmpeg + ffprobe | yes | `brew install ffmpeg` | cutting pauses, cropping, mixing, loudness, muxing |
| Node.js 18+ | yes | `brew install node` | runs Hyperframes |
| **Hyperframes** 0.9.7 | yes | **automatic**: `npx --yes hyperframes@0.9.7` downloads it the first time it runs, along with its headless browser | renders the HTML animation to MP4, lint, snapshots |
| whisper.cpp (`whisper-cli`) | yes | Mac: `brew install whisper-cpp`. Windows: the installer downloads it from GitHub releases | word-level transcription |
| Whisper model `ggml-large-v3-turbo-q5_0.bin` (~550 MB) | yes | `check_setup.py --install` downloads it to `~/.whisper-models/`, or set `WHISPER_MODEL=/path` | Hindi + English; small models loop on Hindi |
| Internet at render time | yes | - | Google Fonts and GSAP load from CDNs |
| yt-dlp | optional | `brew install yt-dlp` | only for pulling reference videos or thumbnails |
| Remotion | **not used** | - | - |
| GitHub repos | **none** | - | the skill ships its own engine and scripts; nothing is cloned |

**Windows:** run `install-windows.ps1` from the repo. It installs Python, Node, FFmpeg, Git and yt-dlp with winget, plus whisper.cpp from its GitHub release and the model. Every script is Python, so no Bash is needed. Use `python` instead of `python3`.

**Linux:** install ffmpeg, nodejs (18+), python3, and whisper.cpp (build it from github.com/ggml-org/whisper.cpp so `whisper-cli` is on PATH). Then download the model from the URL in `check_setup.py`.

**Time and space:**
- First render: about 1–2 minutes while Hyperframes and its browser download.
- After that: about 1 minute per 40-second reel on an Apple Silicon Mac.
- Disk: about 1 GB for the model and caches.
