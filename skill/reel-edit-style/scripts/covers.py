# usage: python3 scripts/covers.py  -> covers/index.html, one 1 s cover per reel; then snapshot it (see SKILL.md)
# B Sticker covers: three tilted strips (question), each reel's own gradient and theme graphic.
import sys
sys.path.insert(0, "scripts")
import engine
from engine import PAIRS, tile, icon, E
from reels import COVERS as C   # {N: (top line, BIG line, bottom line, icon, colour, crossed-out?)}
def fit(tx, cap, w=890): return int(min(cap, w / (len(tx) * 0.44)))
body = ""
for n, (a, b, c, ic, col, ban) in C.items():
    p = PAIRS[(n-1) % len(PAIRS)]
    g = tile(ic, col, 300) if ic != "yt" else tile("yt", "red", 280)
    if ban: g = f'<div class="bw">{g}<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#ff0033" stroke-width="9"/><path d="M19 19 L81 81" stroke="#ff0033" stroke-width="9"/></svg></div>'
    body += (f'<div id="c{n}" class="clip" data-start="{n-1}" data-duration="1" data-track-index="0" style="background:linear-gradient(160deg,{p[4]},#f5f2e6 55%,{p[5]})">'
             f'<div class="blob" style="left:-300px;top:-120px;background:{p[0]}"></div><div class="blob" style="right:-380px;top:800px;background:{p[1]}"></div>'
             f'<div class="col"><div class="s" style="background:#111;color:#fff;font-size:{fit(a,170)}px;transform:rotate(-3deg)">{E(a)}</div>'
             f'<div class="s" style="background:#ff0033;color:#fff;font-size:{fit(b,300)}px;transform:rotate(2deg)">{E(b)}</div>'
             f'<div class="s" style="background:#ffe14d;color:#111;font-size:{fit(c,170)}px;transform:rotate(-2deg)">{E(c)}</div><div class="g">{g}</div></div></div>')
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<link href="https://fonts.googleapis.com/css2?family=Anton&display=block" rel="stylesheet"/><script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#111}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.clip{{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden}}.blob{{position:absolute;width:950px;height:850px;border-radius:50%;filter:blur(60px)}}
.col{{position:absolute;left:0;right:0;top:250px;height:1420px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px}}
.s{{font-family:Anton;line-height:1.12;padding:6px 38px;white-space:nowrap;box-shadow:12px 12px 0 #111}}
.g{{margin-top:44px}}.ico{{width:1em;height:1em;display:block}}.tile{{display:flex;align-items:center;justify-content:center;color:#fff;box-shadow:0 22px 44px rgba(40,20,80,.3),0 0 0 6px rgba(255,255,255,.7)}}.tile.logo{{background:none;box-shadow:none;filter:drop-shadow(0 18px 28px rgba(40,20,80,.4))}}.tile.logo img{{object-fit:contain;display:block}}
.bw{{position:relative;width:360px;height:360px;display:flex;align-items:center;justify-content:center}}.bw > svg{{position:absolute;inset:-20px;width:400px;height:400px}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{len(C)}" data-width="1080" data-height="1920">{body}</div>
<script>const tl=gsap.timeline({{paused:true}});tl.set({{}},{{}},{len(C)});window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>'''
import os, json
os.makedirs("covers/assets", exist_ok=True)
for f in ("yt.svg", "studio.svg"): open(f"covers/assets/{f}", "w", encoding="utf-8").write(open(f"scripts/assets/{f}", encoding="utf-8").read())
json.dump({"id": "covers", "name": "covers"}, open("covers/meta.json", "w", encoding="utf-8"))
open("covers/index.html", "w", encoding="utf-8").write(html)
print("covers/index.html:", len(C), "covers")
