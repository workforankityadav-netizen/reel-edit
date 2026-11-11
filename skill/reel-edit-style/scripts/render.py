# usage (from the project folder): python3 scripts/render.py N [N...]
# Renders reel-NN silently with Hyperframes, adds sound effects (skill sounds in scripts/sfx, overridden by any
# <project>/sfx/<name>.wav), an original music loop, mixes voice + ducked music + effects to -14 LUFS and writes
# exports/reel-NN.mp4. Works on macOS, Linux and Windows.
import glob, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import FFMPEG, FFPROBE, NPX, HF
ROOT = os.getcwd(); S = os.path.join(ROOT, "scripts"); PY = sys.executable
def run(c, **k): return subprocess.run(c, check=True, **k)
for n in map(int, sys.argv[1:]):
    d = os.path.join(ROOT, f"reel-{n:02d}")
    total = float(re.search(r'data-composition-id="main" data-start="0" data-duration="([\d.]+)"', open(os.path.join(d, "index.html"), encoding="utf-8").read()).group(1))
    with open(os.path.join(d, "render.log"), "w", encoding="utf-8") as log:
        r = subprocess.run([NPX] + HF + ["render", ".", "-o", "renders/video.mp4", "--fps", "30", "--quiet"], cwd=d, stdout=log, stderr=subprocess.STDOUT)
    if r.returncode: sys.exit(f"reel-{n:02d} RENDER FAILED, see {d}/render.log")
    a = os.path.join(d, "audio")
    run([PY, "-I", os.path.join(S, "sfx2.py"), a], stdout=subprocess.DEVNULL)              # built-in synth kit
    for f in glob.glob(os.path.join(S, "sfx", "*.wav")) + glob.glob(os.path.join(ROOT, "sfx", "*.wav")):   # skill sounds, then the user's own
        run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", f, "-ac", "1", "-ar", "44100", os.path.join(a, os.path.basename(f))])
    run([PY, "-I", os.path.join(S, "reelmusic.py"), os.path.join(a, "loop.wav"), str(n)], stdout=subprocess.DEVNULL)
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-stream_loop", "-1", "-i", os.path.join(a, "loop.wav"), "-t", str(total),
         "-af", f"afade=t=in:d=0.3,afade=t=out:st={max(0, total - 1.2):.2f}:d=1.2", "-ar", "44100", os.path.join(a, "music.wav")])
    run([PY, "-I", os.path.join(S, "mix.py"), ".", "cues.json", "final-mix.wav", str(total)], stdout=subprocess.DEVNULL, cwd=a)
    os.makedirs(os.path.join(ROOT, "exports"), exist_ok=True)
    out = os.path.join(ROOT, "exports", f"reel-{n:02d}.mp4")
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(d, "renders", "video.mp4"), "-i", os.path.join(a, "final-mix.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out])
    e = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    L = " ".join(re.findall(r"^\s+(?:I|Peak):\s+(\S+)", e, re.M)[-2:])
    D = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"reel-{n:02d} ok {D}s  LUFS/peak: {L}  -> {out}")
