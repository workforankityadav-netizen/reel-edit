# whisper sometimes skips a stretch: find silent-in-transcript gaps over 2.5 s and re-run just those in short windows
import json, re, subprocess, sys, os
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
M = MODEL
for n in sys.argv[1:]:
    d = f"reel-{int(n):02d}/audio"
    r = subprocess.run([FFMPEG,"-hide_banner","-nostats","-i",f"{d}/voice.wav","-af","silencedetect=n=-36dB:d=0.06","-f","null","-"],capture_output=True,text=True).stderr
    mids = [(float(a)+float(b))/2 for a, b in zip(re.findall(r"silence_start: ([0-9.]+)", r), re.findall(r"silence_end: ([0-9.]+)", r))]
    j = json.loads(open(f"{d}/v.json","rb").read().decode("utf-8","replace"))
    segs = [s for s in j["transcription"] if s["text"].strip() and not s["text"].strip().startswith("[")]
    segs.sort(key=lambda s: s["offsets"]["from"]); gaps = []
    for x, y in zip(segs, segs[1:]):
        if y["offsets"]["from"] - x["offsets"]["from"] > 2500: gaps.append((x["offsets"]["from"]/1000, y["offsets"]["from"]/1000))
    add = []
    for a, b in gaps:
        cut = [m for m in mids if a - 0.6 <= m <= b + 0.6]
        pts = [cut[0]] if cut else [a]
        for m in cut:
            if m - pts[-1] >= 5: pts.append(m)
        pts.append(cut[-1] if cut else b)
        pts = sorted(set(pts))
        segs = [s for s in segs if not (a < s["offsets"]["from"]/1000 < b)]
        for w0, w1 in zip(pts, pts[1:]):
            f = f"{d}/g"
            subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-ss",str(w0),"-to",str(w1),"-i",f"{d}/voice.wav","-ar","16000","-ac","1",f+".wav"],check=True)
            subprocess.run([WHISPER,"-m",M,"-f",f+".wav","-l",os.environ.get("WHISPER_LANG","hi"),"-mc","0","-ml","1","-sow","-ojf","-of",f,"-np","-t","8"],capture_output=True)
            g = json.loads(open(f+".json","rb").read().decode("utf-8","replace"))
            for s in g["transcription"]:
                s["offsets"]["from"] += int(w0*1000); s["offsets"]["to"] += int(w0*1000); add.append(s)
            os.remove(f+".wav"); os.remove(f+".json")
    segs += add; segs.sort(key=lambda s: s["offsets"]["from"])
    json.dump({"transcription": segs}, open(f"{d}/v.json","w", encoding="utf-8"), ensure_ascii=False)
    print(n, "gaps", [(round(a,1), round(b,1)) for a, b in gaps], "added", len(add))
