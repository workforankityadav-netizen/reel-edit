# usage (from the project folder): python3 scripts/make.py N [N...]
# Aligns roman.py's script to Whisper's words, builds reel-NN/index.html and reel-NN/audio/cues.json.
import json, re, sys, os, shutil, subprocess
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
sys.path.insert(0, "scripts")
import engine
from roman import R
from reels import SPEC
V = {'क':'k','ख':'k','ग':'g','घ':'g','च':'c','छ':'c','ज':'j','झ':'j','ट':'t','ठ':'t','ड':'d','ढ':'d','ण':'n','त':'t','थ':'t','द':'d','ध':'d','न':'n','प':'p','फ':'f','ब':'b','भ':'b','म':'m','य':'y','र':'r','ल':'l','व':'v','श':'s','ष':'s','स':'s','ह':'h','ड़':'d','ढ़':'d','ं':'n','ँ':'n','ञ':'n','ङ':'n','ज़':'j','फ़':'f','ऱ':'r','क़':'k','ख़':'k','ग़':'g'}
def skel(w):
    w = w.lower(); out = ""
    if re.search(r'[ऀ-ॿ]', w):
        for ch in w:
            if ch in V: out += V[ch]
            elif ch.isdigit(): out += ch
    else:
        w = w.replace("ph","f").replace("sh","s").replace("ch","c").replace("th","t").replace("dh","d").replace("kh","k").replace("gh","g").replace("bh","b").replace("w","v").replace("z","j").replace("q","k").replace("x","ks").replace("ck","k").replace("c","k") if False else w
        w = w.replace("ph","f").replace("sh","s").replace("chh","c").replace("ch","c").replace("th","t").replace("dh","d").replace("kh","k").replace("gh","g").replace("bh","b").replace("w","v").replace("z","j").replace("q","k").replace("x","ks")
        for ch in w:
            if ch in "bcdfgjklmnprstvyh" or ch.isdigit(): out += ch
    return re.sub(r"(.)\1+", r"\1", out)
def sim(a, b):
    if not a or not b: return 0.0
    n, m = len(a), len(b); d = list(range(m + 1))
    for i in range(1, n + 1):
        p, d[0] = d[0], i
        for j in range(1, m + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j-1] + 1, p + (a[i-1] != b[j-1]))
    return 1 - d[m] / max(n, m)
def words_of(path):
    d = json.loads(open(path, "rb").read().decode("utf-8", "replace")); W = []
    for s in d["transcription"]:
        t = s["text"].strip()
        if t and not t.startswith("[") and "�" not in t: W.append((s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, t))
    # drop whisper's zero-width runs (hallucinated repeats)
    return [w for i, w in enumerate(W) if w[1] > w[0] or (i + 1 < len(W) and W[i+1][0] > w[0])]
def align(sc, W):
    """global alignment of script tokens to whisper tokens; unmatched tokens get interpolated times"""
    S = [skel(x) for x in sc]; T = [skel(x[2]) for x in W]; n, m = len(S), len(T)
    GAP = -0.25; prev = [j * GAP * 0.5 for j in range(m + 1)]; back = []
    for i in range(1, n + 1):
        cur = [i * GAP]; b = [0] * (m + 1)
        for j in range(1, m + 1):
            s = sim(S[i-1], T[j-1]); diag = prev[j-1] + (s * 2 - 0.7)
            up = prev[j] + GAP; left = cur[j-1] + GAP * 0.5
            best = max(diag, up, left); cur.append(best); b[j] = 0 if best == diag else (1 if best == up else 2)
        back.append(b); prev = cur
    times = [None] * n; i, j = n, m
    while i > 0 and j > 0:
        k = back[i-1][j]
        if k == 0:
            if sim(S[i-1], T[j-1]) >= 0.45: times[i-1] = W[j-1][0]
            i -= 1; j -= 1
        elif k == 1: i -= 1
        else: j -= 1
    # enforce monotonic, interpolate
    known = [(i, t) for i, t in enumerate(times) if t is not None]
    fixed = []; last = -1
    for i, t in known:
        if t >= last: fixed.append((i, t)); last = t
    pts = [(0, 0.0)] + fixed if not fixed or fixed[0][0] != 0 else fixed
    end = W[-1][1] if W else 1
    if pts[-1][0] != n - 1: pts.append((n - 1, end - 0.3))
    out = [0.0] * n
    for (i0, t0), (i1, t1) in zip(pts, pts[1:]):
        for i in range(i0, i1 + 1): out[i] = t0 + (t1 - t0) * (i - i0) / max(1, i1 - i0)
    return out, len(fixed) / n
def captions(tokens, times, total):
    caps = []; cur = []; on = False
    def flush(next_t):
        nonlocal cur
        if cur:
            tx = " ".join(c[1] for c in cur); caps.append([cur[0][0], next_t, tx]); cur = []
    for i, raw in enumerate(tokens):
        plain = raw.replace("*", "")
        marked = plain
        if raw.startswith("*"): on = True
        hl = on
        if raw.rstrip(".,!?:…").endswith("*"): on = False
        if hl: marked = f"<b>{engine.E(plain)}</b>"
        else: marked = engine.E(plain)
        chars = sum(len(re.sub("<.*?>", "", c[1])) + 1 for c in cur) + len(plain)
        if cur and (chars > 30 or len(cur) >= 5): flush(times[i])
        cur.append((times[i], marked))
        if re.search(r"[.,!?:]+$|\.\.\.$", plain) and len(cur) >= 2: flush(times[i+1] if i + 1 < len(tokens) else total)
    flush(total)
    return [[a, min(b, a + 4.0), t.replace("</b> <b>", " ")] for a, b, t in caps]
HF = {"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}, "media": {"autoProxy": True}}
for n in map(int, sys.argv[1:]):
    d = f"reel-{n:02d}"
    tokens = R[n].replace("\n", " ").split()
    W = words_of(f"{d}/audio/v.json")
    total = float(subprocess.run([FFPROBE,"-v","error","-show_entries","format=duration","-of","csv=p=0",f"{d}/audio/voice.wav"],capture_output=True,text=True).stdout)
    times, match = align(tokens, W)
    toks = [{"n": engine.norm(t), "a": a} for t, a in zip(tokens, times)]
    json.dump(toks, open(f"{d}/audio/toks.json", "w", encoding="utf-8"), ensure_ascii=False)
    caps = captions(tokens, times, total + 0.3)
    end = total + 0.6
    html_, cues = engine.build(n, SPEC[n], toks, end, caps)
    open(f"{d}/index.html", "w", encoding="utf-8").write(html_)
    json.dump(HF, open(f"{d}/hyperframes.json", "w", encoding="utf-8"), indent=2)
    json.dump({"name": d, "private": True, "type": "module"}, open(f"{d}/package.json", "w", encoding="utf-8"), indent=2)
    json.dump({"id": d, "name": d}, open(f"{d}/meta.json", "w", encoding="utf-8"))
    os.makedirs(f"{d}/assets/img", exist_ok=True)
    for f in ("yt.svg", "studio.svg"): shutil.copy(f"scripts/assets/{f}", f"{d}/assets/{f}")
    if SPEC[n].get("mode") == "footage" and not os.path.exists(f"{d}/assets/person.mp4"):
        print(f"  WARN {d}: footage mode but {d}/assets/person.mp4 is missing (run cutpauses.py)")
    lv = {"whoosh": -20, "swoosh": -25, "impact": -17, "pop": -26, "click": -21, "ding": -25, "riser": -27, "tick": -27}
    json.dump({"cues": cues, "levels": lv}, open(f"{d}/audio/cues.json", "w", encoding="utf-8"))
    print(d, f"dur {total:.1f}s match {match:.0%} scenes {len(SPEC[n]['scenes'])} caps {len(caps)} cues {len(cues)} ({len(cues)/total:.1f}/s)")
