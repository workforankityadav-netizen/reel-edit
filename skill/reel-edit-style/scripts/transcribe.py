# usage: python3 scripts/transcribe.py N [N...]   (env WHISPER_LANG=hi|en|auto, WHISPER_MODEL=path)
# Transcribes reel-NN/audio/voice.wav in ~15 s windows that start inside pauses (whole-file runs drift and drop
# stretches), writes reel-NN/audio/v.json (whisper-cli JSON) and reel-NN/audio/words.txt (time + word, readable).
import json, re, subprocess, sys, os
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
M = MODEL
LANG = os.environ.get("WHISPER_LANG", "hi")
if not os.path.exists(M): sys.exit(f"Whisper model not found: {M}  (run scripts/check_setup.py --install)")
for n in sys.argv[1:]:
    d = f"reel-{int(n):02d}/audio"
    r = subprocess.run([FFMPEG,"-hide_banner","-nostats","-i",f"{d}/voice.wav","-af","silencedetect=n=-36dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
    mids = [(a+b)/2 for a, b in zip(st, en)]
    dur = float(subprocess.run([FFPROBE,"-v","error","-show_entries","format=duration","-of","csv=p=0",f"{d}/voice.wav"],capture_output=True,text=True).stdout)
    cuts = [0.0]
    while dur - cuts[-1] > 19:
        c = [m for m in mids if cuts[-1] + 11 <= m <= cuts[-1] + 18]
        cuts.append(c[-1] if c else cuts[-1] + 15)
    cuts.append(dur); out = []
    for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
        f = f"{d}/w{i}"
        subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-ss",str(a),"-to",str(b),"-i",f"{d}/voice.wav","-ar","16000","-ac","1",f+".wav"],check=True)
        subprocess.run([WHISPER,"-m",M,"-f",f+".wav","-l",LANG,"-mc","0","-ml","1","-sow","-ojf","-of",f,"-np","-t","8"],capture_output=True)
        j = json.loads(open(f+".json","rb").read().decode("utf-8","replace"))
        for s in j["transcription"]:
            s["offsets"]["from"] += int(a*1000); s["offsets"]["to"] += int(a*1000); out.append(s)
        os.remove(f+".wav"); os.remove(f+".json")
    json.dump({"transcription": out}, open(f"{d}/v.json","w", encoding="utf-8"), ensure_ascii=False)
    with open(f"{d}/words.txt", "w", encoding="utf-8") as fw:
        row, cur = [], 0
        for s in out:
            a = s["offsets"]["from"] / 1000; w = s["text"].strip()
            if not w or w.startswith("["): continue
            if int(a // 5) != cur and row: fw.write(f"[{cur*5:>4}s] " + " ".join(row) + "\n"); row = []
            cur = int(a // 5); row.append(f"{a:.1f}:{w}")
        if row: fw.write(f"[{cur*5:>4}s] " + " ".join(row) + "\n")
    print(f"reel-{int(n):02d}: {len(cuts)-1} windows, {len(out)} words -> {d}/v.json, {d}/words.txt")
