# usage: python3 scripts/prep_voice.py <voiceover file> N [--start S --end E] [--keep-pauses]
# Voiceover-only reels: cuts the voice (optionally a stretch of it), tightens pauses, writes reel-NN/audio/voice.wav, transcribes.
import argparse, os, subprocess, sys
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("n", type=int)
ap.add_argument("--start", type=float); ap.add_argument("--end", type=float); ap.add_argument("--keep-pauses", action="store_true")
a = ap.parse_args(); d = f"reel-{a.n:02d}/audio"; os.makedirs(d, exist_ok=True)
cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y"] + (["-ss", str(a.start)] if a.start is not None else []) + (["-to", str(a.end)] if a.end is not None else []) + ["-i", a.src, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", f"{d}/raw.wav"]
subprocess.run(cmd, check=True)
if a.keep_pauses: os.replace(f"{d}/raw.wav", f"{d}/voice.wav")
else: subprocess.run([sys.executable, "-I", "scripts/tighten.py", f"{d}/raw.wav", f"{d}/voice.wav"], check=True)
subprocess.run([sys.executable, "-I", "scripts/transcribe.py", str(a.n)], check=True)
