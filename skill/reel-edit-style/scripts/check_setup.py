# usage: python3 <skill>/scripts/check_setup.py [--install]
# Checks every tool this skill needs. With --install (macOS + Homebrew) it installs what is missing and downloads
# the Whisper model. Nothing is installed without --install.
import os, shutil, subprocess, sys, urllib.request, platform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import find, MODEL as _M
WIN = platform.system() == "Windows"
MODEL = _M
MODEL_URL = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin"
INSTALL = "--install" in sys.argv
def run(c): return subprocess.run(c, capture_output=True, text=True)
def ver(c):
    c = [find(c[0]) or c[0]] + c[1:]
    try: r = run(c); return (r.stdout or r.stderr).strip().splitlines()[0][:70]
    except Exception: return None
rows = []
def check(name, ok, how, why):
    rows.append((name, ok, how, why))
py_ok = sys.version_info >= (3, 9)
check("Python 3.9+", py_ok, "winget install Python.Python.3.12" if WIN else "brew install python", "runs every script (standard library only, no pip packages)")
check("ffmpeg + ffprobe", bool(find("ffmpeg") and find("ffprobe")), "winget install Gyan.FFmpeg" if WIN else "brew install ffmpeg", "cutting, cropping, pause removal, mixing, loudness")
node = ver(["node", "--version"])
node_ok = bool(node) and int(node.lstrip("v").split(".")[0]) >= 18
check("Node.js 18+ (npx)", node_ok and bool(find("npx")), "winget install OpenJS.NodeJS.LTS" if WIN else "brew install node", "runs Hyperframes; `npx --yes hyperframes@0.9.7` downloads it by itself on first use")
check("whisper-cli (whisper.cpp)", bool(find("whisper-cli", [os.path.join(os.path.expanduser("~"), ".reel-tools", "whisper"), os.path.join(os.path.expanduser("~"), ".reel-tools", "whisper", "Release")])), "run install-windows.ps1 from the repo" if WIN else "brew install whisper-cpp", "word-level transcription for captions and timing")
check("Whisper model large-v3-turbo", os.path.exists(MODEL), f"download to {MODEL} (~550 MB)", "Hindi + English speech; small models loop on Hindi")
chrome = any(os.path.exists(p) for p in ("/Applications/Google Chrome.app", "/Applications/Chromium.app")) or bool(shutil.which("google-chrome") or shutil.which("chromium"))
check("Chrome (optional)", True, "Hyperframes downloads its own headless browser if Chrome is missing", "frame rendering")
check("yt-dlp (optional)", True if find("yt-dlp") else None, "winget install yt-dlp.yt-dlp" if WIN else "brew install yt-dlp", "only to pull reference videos / thumbnails")
check("Internet at render time", True, "-", "Google Fonts + GSAP load from CDN when a reel renders")
w = max(len(r[0]) for r in rows)
missing = []
for name, ok, how, why in rows:
    mark = "OK " if ok else ("-- " if ok is None else "MISSING")
    print(f"{mark:8} {name:<{w}}  {why}")
    if ok is False: missing.append((name, how))
if not missing: print("\nAll required tools are present."); sys.exit(0)
print("\nMissing:"); [print(f"  {n}: {h}") for n, h in missing]
if not INSTALL: print("\nRun again with --install to install them (macOS, Homebrew), or install by hand."); sys.exit(1)
if WIN: sys.exit("On Windows run install-windows.ps1 from the repo (PowerShell) to install everything.")
if not shutil.which("brew"): sys.exit("Homebrew not found. Install it from https://brew.sh, then re-run with --install.")
pk = {"ffmpeg + ffprobe": "ffmpeg", "Node.js 18+ (npx)": "node", "whisper-cli (whisper.cpp)": "whisper-cpp", "Python 3.9+": "python"}
for n, _ in missing:
    if n in pk: print(f"brew install {pk[n]} ..."); subprocess.run(["brew", "install", pk[n]], check=False)
if not os.path.exists(MODEL):
    os.makedirs(os.path.dirname(MODEL), exist_ok=True); print(f"downloading Whisper model to {MODEL} ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL + ".part"); os.replace(MODEL + ".part", MODEL)
print("done. Re-run without --install to confirm.")
