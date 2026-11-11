# Finds the command-line tools on macOS, Linux and Windows (npx is npx.cmd on Windows; whisper-cli may live in
# ~/.reel-tools/whisper after the Windows installer).
import os, shutil, sys
HOME = os.path.expanduser("~")
def find(name, extra=()):
    env = os.environ.get(name.upper().replace("-", "_"))
    if env and os.path.exists(env): return env
    p = shutil.which(name) or shutil.which(name + ".exe") or shutil.which(name + ".cmd")
    if p: return p
    for d in extra:
        for n in (name, name + ".exe"):
            q = os.path.join(d, n)
            if os.path.exists(q): return q
    return None
FFMPEG = find("ffmpeg") or "ffmpeg"
FFPROBE = find("ffprobe") or "ffprobe"
NPX = find("npx") or "npx"
WHISPER = find("whisper-cli", [os.path.join(HOME, ".reel-tools", "whisper"), os.path.join(HOME, ".reel-tools", "whisper", "Release")]) or "whisper-cli"
MODEL = os.environ.get("WHISPER_MODEL", os.path.join(HOME, ".whisper-models", "ggml-large-v3-turbo-q5_0.bin"))
HF = ["--yes", "hyperframes@0.9.7"]
