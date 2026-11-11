# usage: python3 scripts/cutpauses.py <raw footage> N [--audio voice.wav] [--ranges 12.5-40.2,55-71] [--fx 0.5] [--fy 0.38] [--min-pause 0.3] [--pad 0.08]
# Raw footage of a person -> reel-NN/assets/person.mp4 (1080x960, the bottom half of the reel) + reel-NN/audio/voice.wav.
#  * --ranges keeps only those stretches of the raw file (pick the strongest lines from a first transcript).
#  * Every pause longer than --min-pause is removed; each cut keeps --pad of air and gets 8 ms audio fades, so joins
#    are click-free and sound continuous (smooth cuts). Cuts land inside measured silences, never mid-word.
#  * --fx/--fy: where the face/upper body sits in the source (0..1). The 9:8 crop is centred there.
import argparse, json, os, re, subprocess, sys
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("n", type=int)
ap.add_argument("--ranges", default=""); ap.add_argument("--fx", type=float, default=0.5); ap.add_argument("--fy", type=float, default=0.38)
ap.add_argument("--audio", help="separate voice recording, in sync with the video (use when the camera audio is bad or missing)"); ap.add_argument("--min-pause", type=float, default=0.3); ap.add_argument("--pad", type=float, default=0.08); ap.add_argument("--db", default="-35dB")
a = ap.parse_args(); R = f"reel-{a.n:02d}"; os.makedirs(f"{R}/assets", exist_ok=True); os.makedirs(f"{R}/audio", exist_ok=True)
pr = json.loads(subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", a.src], capture_output=True, text=True).stdout)
W, H = pr["streams"][0]["width"], pr["streams"][0]["height"]; DUR = float(pr["format"]["duration"])
ranges = [tuple(map(float, r.split("-"))) for r in a.ranges.split(",") if r] or [(0.0, DUR)]
ASRC = a.audio or a.src
has_a = run_ok = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", ASRC], capture_output=True, text=True).stdout.strip()
if not has_a: sys.exit(f"{ASRC} has no audio track. Pass the separately recorded voice with --audio <file>.")
AIN = "1:a" if a.audio else "0:a"
err = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", ASRC, "-vn", "-af", f"silencedetect=n={a.db}:d={a.min_pause}", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]))
keep = []
for r0, r1 in ranges:
    t = r0
    for s0, s1 in sil:
        if s1 <= r0 or s0 >= r1: continue
        s0, s1 = max(s0, r0), min(s1, r1)
        if s0 - t > 0.05: keep.append((t, min(r1, s0 + a.pad)))
        t = max(t, s1 - a.pad)
    if r1 - t > 0.05: keep.append((t, r1))
# drop slivers and leading/trailing air
keep = [(x, y) for x, y in keep if y - x > 0.12]
# 9:8 crop (1080x960) centred on the presenter
ar = 1080 / 960
cw, ch = (H * ar, H) if W / H > ar else (W, W / ar)
cx = min(max(a.fx * W - cw / 2, 0), W - cw); cy = min(max(a.fy * H - ch / 2, 0), H - ch)
vf = f"crop={int(cw)//2*2}:{int(ch)//2*2}:{int(cx)}:{int(cy)},scale=1080:960,setsar=1,fps=30"
fc = []
for i, (x, y) in enumerate(keep):
    d = y - x
    fc.append(f"[0:v]trim={x:.3f}:{y:.3f},setpts=PTS-STARTPTS,{vf}[v{i}]")
    fc.append(f"[{AIN}]atrim={x:.3f}:{y:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=mono,afade=t=in:d=0.008,afade=t=out:st={max(0, d - 0.008):.3f}:d=0.008[a{i}]")
fc.append("".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[v][a]")
open(f"{R}/audio/cut.fc", "w", encoding="utf-8").write(";".join(fc))
subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", a.src] + (["-i", a.audio] if a.audio else []) + ["-/filter_complex", f"{R}/audio/cut.fc", "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", f"{R}/assets/person.mp4",
                "-map", "[a]", "-c:a", "pcm_s16le", f"{R}/audio/voice.wav"], check=True)
json.dump(keep, open(f"{R}/audio/keep.json", "w", encoding="utf-8"))
new = sum(y - x for x, y in keep)
print(f"{R}: {len(keep)} pieces, {sum(r1 - r0 for r0, r1 in ranges):.1f}s -> {new:.1f}s (pauses removed); crop {int(cw)}x{int(ch)} at ({int(cx)},{int(cy)}) of {W}x{H}")
subprocess.run([sys.executable, "-I", "scripts/transcribe.py", str(a.n)], check=True)
