# Reel 2 format as a builder: persistent two-colour gradient + starbursts, one graphic per line, zoom-blur cuts,
# ribbon wipes at section changes, outlined Hinglish subtitles with yellow keywords, fast SFX derived from the animation.
# build(n, spec, words, total) -> (html, cues). All times resolve from spoken-word anchors.
import html, json, math, re
E = html.escape
PAIRS = [  # rotating gradient per reel: (soft A, soft B, star A, star B, deep A, deep B)
 ("#c9b8f0", "#f2ee3a", "#f2ee3a", "#b9a4ee", "#ddd2f6", "#f6f29b"),
 ("#a9d8ff", "#ffc38a", "#ff9f4a", "#6bb8ff", "#d6ecff", "#ffe3c4"),
 ("#a8ecc8", "#ffe36b", "#ffd21f", "#52cf95", "#d9f6e6", "#fff3b8"),
 ("#ffb8d2", "#bcd2ff", "#ff7fae", "#7ea6ff", "#ffe0ec", "#dde8ff"),
 ("#ffd59a", "#c7f0a8", "#ffb347", "#8fdc5e", "#ffeccb", "#e4f8d2"),
 ("#b9c7ff", "#ffc2b0", "#ff9478", "#8297ff", "#dfe5ff", "#ffe1d8"),
 ("#a4eee4", "#d8bcff", "#b58cff", "#43d6c4", "#d6f7f2", "#ecdfff"),
 ("#fff08a", "#ffb3b3", "#ff8080", "#f5d800", "#fff9c9", "#ffdede"),
 ("#c2f2ff", "#e2ff9e", "#c5f03c", "#6fd6f5", "#def8ff", "#f2ffd2"),
 ("#ffc9f0", "#b5f0d5", "#5edba6", "#ff8fe0", "#ffe4f8", "#dcf9ec"),
]
IC = {
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>', "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>', "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>', "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
 "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', "unlock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/>',
 "play": '<path d="M7 4l13 8-13 8z" fill="currentColor"/>', "mail": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 7l10 7 10-7"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>', "heart": '<path d="M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z"/>',
 "users": '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M16 4a4 4 0 0 1 0 8M22 21a7 7 0 0 0-4-6.3"/>', "person": '<circle cx="12" cy="7" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "rupee": '<path d="M6 4h12M6 9h12M9 4c6 0 6 10 0 10H6l9 7"/>', "dollar": '<path d="M12 2v20M17 6.5C16 4.5 14 4 12 4 9 4 7 5.5 7 8s2 3.4 5 4 5 1.6 5 4-2 4-5 4c-2.200 0-4.200-.7-5-2.800"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>', "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "star": '<path d="M12 3l2.800 5.800 6.200.9-4.500 4.400 1 6.300L12 17.500 6.500 20.400l1-6.300L3 9.700l6.200-.9z"/>', "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
 "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.600 10.500l6.800-4M8.600 13.500l6.800 4"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>', "trend": '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>', "down": '<path d="M3 7l6 6 4-4 8 8M15 17h6v-6"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>', "phone": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>', "wifi": '<path d="M2 8.500a15 15 0 0 1 20 0M5.500 12.500a10 10 0 0 1 13 0M9 16.500a5 5 0 0 1 6 0"/><path d="M12 20h.01"/>',
 "shield": '<path d="M12 2l8 3v6c0 5-3.500 9-8 11-4.500-2-8-6-8-11V5z"/>', "robot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 13h.5M14.500 13h.5M9 17h6"/>',
 "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>', "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>', "ban": '<circle cx="12" cy="12" r="10"/><path d="M5 5l14 14"/>', "ghost": '<path d="M5 21V10a7 7 0 0 1 14 0v11l-2.300-2-2.400 2-2.300-2-2.300 2-2.400-2z"/><path d="M9.500 10h.01M14.500 10h.01"/>',
 "bell": '<path d="M6 16V10a6 6 0 0 1 12 0v6l2 2H4z"/><path d="M10 21h4"/>', "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/>', "hook": '<path d="M12 2v10a5 5 0 1 1-8 4"/><circle cx="12" cy="4" r="2"/>', "fire": '<path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 2-4 2-7 2 1 3 2 4-5z"/>',
 "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>', "file": '<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h7M9 17h7"/>', "tag": '<path d="M3 12V3h9l9 9-9 9z"/><path d="M7.500 7.500h.01"/>', "skull": '<path d="M12 2a8 8 0 0 0-5 14v3h10v-3a8 8 0 0 0-5-14z"/><path d="M9 11h.01M15 11h.01M10 22v-3M14 22v-3"/>',
 "bank": '<path d="M3 10l9-6 9 6M5 10v8M10 10v8M14 10v8M19 10v8M3 20h18"/>', "swipe": '<path d="M12 21V5M6 11l6-6 6 6"/>', "moon": '<path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10z"/>', "sun": '<circle cx="12" cy="12" r="5"/><path d="M12 1v3M12 20v3M1 12h3M20 12h3M4.200 4.200l2 2M17.800 17.800l2 2M4.200 19.800l2-2M17.800 6.200l2-2"/>',
 "ad": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 15l2.500-6L11 15M7 13h3M14 9v6h1.500a3 3 0 0 0 0-6z"/>', "sword": '<path d="M14 3h7v7L9 22l-7-7z"/><path d="M6 12l6 6"/>', "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.500 8.500L20 20M8.500 15.500L20 4"/>',
}
def icon(n, sw=2.2, cls=""):
    return f'<svg class="ico {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{IC[n]}</svg>'
LOGO = {"yt": "yt.svg", "studio": "studio.svg"}
TONE = {"red": "#ff0033", "ink": "#111111", "green": "#17a34a", "blue": "#2f6bff", "amber": "#f59e0b", "purple": "#7c3aed", "pink": "#ec4899", "teal": "#0d9488"}

class Ctx:
    def __init__(s, toks): s.toks, s.cur, s.base, s.end = toks, 0, None, 9e9
    def at(s, phrase):
        """first time of a spoken phrase. Scene starts search forward; inside a scene, search from the scene's start."""
        q = norm(phrase).split()
        i0 = s.cur if s.base is None else s.base
        for i in range(i0, len(s.toks) - len(q) + 1):
            if [t["n"] for t in s.toks[i:i+len(q)]] == q:
                if s.base is None: s.cur = i
                elif s.toks[i]["a"] > s.end: print(f"  WARN anchor {phrase!r} falls after its scene ends")
                return s.toks[i]["a"]
        raise ValueError(f"anchor not found: {phrase!r} after token {i0}: {' '.join(t['n'] for t in s.toks[i0:i0+12])}")
def norm(x): return re.sub(r"[^a-z0-9₹%\- ]", "", x.lower().replace("*", "").replace("...", " ")).strip()
def A(t, fx="pop", extra=""): return f'data-at="{t:.2f}" data-fx="{fx}"' + (" " + extra if extra else "")

def tile(ic, col="red", size=200, t=None, fx="pop"):
    a = " " + A(t, fx) if t is not None else ""
    if ic in LOGO:
        ar = 1.43 if ic == "yt" else 1
        return f'<div class="tile logo"{a}><img src="assets/{LOGO[ic]}" style="width:{size*ar:.0f}px;height:{size:.0f}px"></div>'
    return f'<div class="tile"{a} style="width:{size}px;height:{size}px;border-radius:{size*0.26:.0f}px;background:{TONE[col]};font-size:{size*0.58:.0f}px">{icon(ic, 2.3)}</div>'
def words(text, t, step=0.05):
    out = []; on = False; i = 0
    for li, line in enumerate(text.split("|")):
        if li: out.append("<br>")
        for w in line.split():
            if w.startswith("*"): on = True
            red = on
            if w.rstrip(".,!?").endswith("*"): on = False
            out.append(f'<span class="w{" red" if red else ""}" {A(t + i*step, "word")}>{E(w.replace("*", ""))}</span> ')
            i += 1
    return "".join(out)
def head(text, t, size=""): return f'<div class="hl {size}">{words(text, t)}</div>'
def chip(tx, t, ic=None, tone="", fx="pop"):
    i = (f'<span class="ci {tone}">{icon(ic)}</span>' if ic else "")
    return f'<div class="chip" {A(t, fx)}>{i}<span>{E(tx)}</span></div>'

# ---- graphics. c = Ctx, p = params; anchors resolve in spoken order ----
def g_head(c, t, p):
    h = ""
    if p.get("kick"): h += f'<div class="kick" {A(t+0.03)}>{E(p["kick"])}</div>'
    if p.get("ic"): h += tile(p["ic"], p.get("col", "red"), p.get("size", 230), t + 0.05)
    h += head(p["h"], t + 0.08, p.get("hs", ""))
    if p.get("sub"): h += f'<div class="sub" {A(c.at(p["sa"]) if p.get("sa") else t+0.5,"up")}>{E(p["sub"])}</div>'
    return f'<div class="stack">{h}</div>'
def g_stat(c, t, p):
    num = str(p["num"]); ca = c.at(p["na"]) if p.get("na") else t + 0.1
    h = ""
    if p.get("kick"): h += f'<div class="kick" {A(t+0.03)}>{E(p["kick"])}</div>'
    if p.get("ic"): h += tile(p["ic"], p.get("col", "red"), 170, t + 0.05)
    h += (f'<div class="stat" {A(ca,"stamp")}><span class="count" style="font-size:{min(290, int(1500/max(1,len(p.get("pre",""))+len(num))))}px" data-from="{p.get("from",0)}" data-to="{E(num)}" data-at="{ca:.2f}" data-dur="{p.get("dur",0.5)}" data-pre="{E(p.get("pre",""))}">{E(p.get("pre",""))}{E(num)}</span>'
          f'<small>{E(p.get("suf",""))}</small></div>')
    if p.get("h"): h += head(p["h"], c.at(p["ha"]) if p.get("ha") else ca + 0.15, "md")
    if p.get("sub"): h += f'<div class="sub" {A(c.at(p["sa"]) if p.get("sa") else ca+0.4,"up")}>{E(p["sub"])}</div>'
    return f'<div class="stack">{h}</div>'
def g_tiles(c, t, p):
    h = head(p["h"], t + 0.05, "md") if p.get("h") else ""
    cells = ""
    for tx, ic, col, an in p["items"]:
        a = c.at(an) if an else t + 0.2
        cells += f'<div class="cell" {A(a)}>{tile(ic, col, p.get("size",190))}<b>{E(tx)}</b></div>'
    return f'<div class="stack">{h}<div class="cells">{cells}</div></div>'
def g_list(c, t, p):
    h = head(p["h"], t + 0.05, "md") if p.get("h") else ""
    rows = ""
    for tx, kind, an in p["items"]:
        a = c.at(an) if an else t + 0.2
        ic = {"ok": "check", "no": "x"}.get(kind, kind); col = {"ok": "green", "no": "red"}.get(kind, "ink")
        rows += f'<div class="row2" {A(a,"left")}><span class="ri" style="background:{TONE[col]}">{icon(ic,2.8)}</span><span>{E(tx)}</span></div>'
    return f'<div class="stack">{h}<div class="ui list">{rows}</div></div>'
def g_flow(c, t, p):
    h = head(p["h"], t + 0.05, "md") if p.get("h") else ""
    st = ""
    for i, (tx, ic, col, an) in enumerate(p["items"]):
        a = c.at(an) if an else t + 0.15
        if i: st += f'<i class="farr" {A(a-0.08,"growy")}></i>'
        st += f'<div class="fstep" {A(a,"left")}><span class="fi" style="background:{TONE[col]}">{icon(ic)}</span><span>{E(tx)}</span></div>'
    return f'<div class="stack">{h}<div class="flow">{st}</div></div>'
def g_vs(c, t, p):
    a1 = c.at(p["la"]) if p.get("la") else t + 0.1
    a2 = c.at(p["ra"]) if p.get("ra") else t + 0.5
    def card(d, ok, a):
        return (f'<div class="ui vs {"ok" if ok else "no"}" {A(a,"left" if ok else "right")}>{tile(d["ic"], "green" if ok else "red", 120)}'
                f'<div><b>{E(d["h"])}</b><span>{E(d.get("s",""))}</span></div></div>')
    h = head(p["h"], t + 0.05, "md") if p.get("h") else ""
    return f'<div class="stack">{h}{card(p["no"], False, a1)}<div class="vsb" {A(a2-0.1)}>VS</div>{card(p["ok"], True, a2)}</div>'
def g_studio(c, t, p):
    rows = ""
    for i, (v, tone) in enumerate(p.get("rows", [("12", ""), ("8", ""), ("0", "red"), ("0", "red")])):
        rows += (f'<div class="srow" {A(t+0.12+i*0.08,"up")}><div class="sth th{i%4}">{icon("play")}</div><div class="sli"><i></i><i></i></div>'
                 f'<div class="svw {tone}" {A(c.at(p["ra"]) if p.get("ra") and tone else t+0.25+i*0.1,"pop")}>{E(v)}</div></div>')
    stamp = f'<div class="stampx" {A(c.at(p["sa"]),"stamp")}>{E(p["stamp"])}</div>' if p.get("stamp") else ""
    ttl = f'<div class="capt">{head(p["h"], t+0.1, "sm")}</div>' if p.get("h") else ""
    return (f'{ttl}<div class="ui studio" {A(t+0.02,"rise")}><div class="sbar"><img src="assets/studio.svg"><b>YouTube Studio</b></div>'
            f'<div class="stabs"><b>Videos</b><span>Shorts</span><span>Live</span></div>{rows}</div>{stamp}')
def g_chart(c, t, p):
    W, H = 900, 520; k = p.get("kind", "drop")
    d = {"drop": "M30 70 C 180 60, 260 70, 340 100 C 430 140, 470 330, 560 390 S 780 440, 870 450",
         "cliff": "M30 80 C 150 90, 240 100, 330 120 C 360 128, 380 150, 395 390 C 420 440, 700 450, 870 455",
         "rise": "M30 450 C 200 440, 320 430, 480 350 S 760 120, 870 50",
         "flat": "M30 400 C 200 402, 500 398, 870 402"}[k]
    col = "#17a34a" if k == "rise" else "#ff0033"
    a = c.at(p["da"]) if p.get("da") else t + 0.2
    labs = ""
    for tx, x, y, tone, an in p.get("labs", []):
        labs += f'<div class="clab {tone}" style="left:{x}px;top:{y}px" {A(c.at(an) if an else a+0.5,"pop")}>{E(tx)}</div>'
    grid = "".join(f'<line x1="30" y1="{y}" x2="870" y2="{y}" stroke="#eee" stroke-width="4"/>' for y in (110, 220, 330, 440))
    return (f'<div class="ui chart" {A(t+0.02,"rise")}><div class="cttl">{E(p["title"])}</div><svg viewBox="0 0 {W} {H}" style="width:{W}px;height:{H}px">{grid}'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="14" stroke-linecap="round" pathLength="1" {A(a,"draw", f"data-dur=\"{p.get("dd",1.1)}\"")}/></svg>{labs}</div>' +
            (f'<div class="under">{head(p["h"], c.at(p["ha"]) if p.get("ha") else a+0.8, "sm")}</div>' if p.get("h") else ""))
def g_bars(c, t, p):
    h = head(p["h"], t + 0.05, "md") if p.get("h") else ""
    bars = ""
    for tx, val, frac, col, an in p["items"]:
        a = c.at(an) if an else t + 0.2
        bars += (f'<div class="bar" {A(a,"up")}><div class="bl"><b>{E(tx)}</b><span style="color:{TONE[col]}">{E(val)}</span></div>'
                 f'<div class="bt"><i style="background:{TONE[col]};width:{frac*100:.0f}%" {A(a+0.08,"growx")}></i></div></div>')
    return f'<div class="stack">{h}<div class="ui bars">{bars}</div></div>'
def g_meter(c, t, p):
    a = c.at(p["sa"]) if p.get("sa") else t + 0.4
    return (f'<div class="stack">{head(p["h"], t+0.05, "md")}<svg class="meter" viewBox="0 0 600 340" {A(t+0.05)}>'
            f'<path d="M60 300 A 240 240 0 0 1 180 92" fill="none" stroke="#17a34a" stroke-width="46"/><path d="M180 92 A 240 240 0 0 1 420 92" fill="none" stroke="#f59e0b" stroke-width="46"/><path d="M420 92 A 240 240 0 0 1 540 300" fill="none" stroke="#ff0033" stroke-width="46"/>'
            f'<g class="needle" data-swing="{a:.2f}" data-to="{p["to"]}"><line x1="300" y1="300" x2="300" y2="86" stroke="#111" stroke-width="14" stroke-linecap="round"/></g><circle cx="300" cy="300" r="26" fill="#111"/></svg>'
            f'<div class="kick big" {A(a+0.25,"stamp")}>{E(p["val"])}</div></div>')
def g_toggle(c, t, p):
    a = c.at(p["ca"]); rows = ""
    for i, o in enumerate(p["opts"]):
        rows += f'<div class="opt{" sel" if i==p.get("sel",0) else ""}"><span class="rad"><i {A(a+0.06,"pop") if i==p.get("sel",0) else ""}></i></span>{E(o)}</div>'
    return (f'<div class="ui toggle" {A(t+0.02,"rise")}><div class="sbar">{("<img src=" + chr(34) + "assets/" + p.get("logo", "studio.svg") + chr(34) + ">") if p.get("logo", 1) else ""}<b>{E(p["bar"])}</b></div><div class="tq">{E(p["q"])}</div>{rows}</div>'
            f'<svg class="cursor" viewBox="0 0 40 40" {A(a-0.5,"cursor",f"data-click=\"{a:.2f}\"")} style="left:{p.get("cx",130)}px;top:{p.get("cy",640 if len(p["q"]) < 30 else 708)}px"><path d="M6 3 L33 18 L20 21 L14 34 Z" fill="#fff" stroke="#111" stroke-width="3" stroke-linejoin="round"/></svg>' +
            (f'<div class="under">{head(p["h"], a+0.2, "sm")}</div>' if p.get("h") else ""))
def g_shortsphone(c, t, p):
    a = c.at(p["sa"]) if p.get("sa") else t + 0.6
    sw = f'<div class="swipe" {A(a,"pop")}>{icon("swipe",3)}<b>{E(p.get("label","SWIPE"))}</b></div>'
    return (f'<div class="fphone" {A(t+0.02,"rise")}><div class="fscreen {p.get("cls","")}"><div class="fplay" data-out="{a:.2f}">{icon("play")}</div><div class="fside"><i>{icon("heart")}</i><i>{icon("chat")}</i><i>{icon("share")}</i></div>'
            f'<div class="fmeta"><i></i><i></i></div></div>{sw}</div>' + (f'<div class="fnote">{head(p["h"], c.at(p["ha"]) if p.get("ha") else t+0.15, "sm")}</div>' if p.get("h") else ""))
def g_crowd(c, t, p):
    n = p.get("n", 40); out = ""
    a = c.at(p["pa"]) if p.get("pa") else t + 0.15
    k = c.at(p["ka"]) if p.get("ka") else None
    for i in range(n):
        gone = p.get("gone", 0) and i % 10 < p["gone"] and k is not None
        out += f'<i class="dotp{" gone" if gone else ""}" {A(a+i*0.012,"pop")}{(f" data-fade=\"{k+i*0.008:.2f}\"") if gone else ""}>{icon("person",2.6)}</i>'
    return f'<div class="stack">{head(p["h"], t+0.05, "md")}<div class="crowd">{out}</div>' + (f'<div class="kick big" {A(c.at(p["va"]) if p.get("va") else a+0.6,"stamp")}>{E(p["val"])}</div>' if p.get("val") else "") + '</div>'
def g_lock(c, t, p):
    a = c.at(p["la"]) if p.get("la") else t + 0.6
    return (f'<div class="stack"><div class="lockw">{tile(p.get("ic","play"), p.get("col","blue"), 300, t+0.05)}<div class="chains" {A(a,"stamp")}></div><div class="lockb" {A(a+0.1,"stamp")}>{tile("lock","red",170)}</div></div>'
            f'{head(p["h"], c.at(p["ha"]) if p.get("ha") else a, "md")}</div>')
def g_ban(c, t, p):
    a = c.at(p["ba"]) if p.get("ba") else t + 0.5
    return (f'<div class="stack"><div class="banw">{tile(p["ic"], p.get("col","ink"), 320, t+0.05)}<svg class="bansvg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#ff0033" stroke-width="9" pathLength="1" {A(a,"draw","data-dur=\"0.3\"")}/><path d="M19 19 L81 81" stroke="#ff0033" stroke-width="9" pathLength="1" {A(a+0.2,"draw","data-dur=\"0.18\"")}/></svg></div>'
            f'{head(p["h"], c.at(p["ha"]) if p.get("ha") else a, "")}' + (f'<div class="sub" {A(c.at(p["sa"]) if p.get("sa") else a+.4,"up")}>{E(p["sub"])}</div>' if p.get("sub") else "") + '</div>')
def g_cta(c, t, p):
    ta = c.at(p["ta"]); sa = c.at(p["sa"]) if p.get("sa") else None
    sub = ""
    if sa is not None:
        conf = "".join(f'<i data-conf="{sa+0.1:.2f}" data-i="{i}" style="background:{["#ff0033","#f59e0b","#7c3aed","#111","#2f6bff"][i%5]}"></i>' for i in range(24))
        sub = f'<div class="subbtn" {A(sa,"stamp")}>{icon("bell",2.6)}SUBSCRIBE</div><div class="confetti">{conf}</div>'
    return (f'<div class="ui cbox" {A(t+0.02,"rise")}><div class="chdr">{icon("chat")}<b>Comments</b></div><div class="cin"><i class="cav">{icon("person")}</i><div class="cfield"><span class="type" data-text="{E(p["text"])}" data-at="{ta:.2f}" data-dur="{p.get("td",0.9)}"></span><i class="caret"></i></div></div></div>{sub}')
def g_cal(c, t, p):
    a = c.at(p["da"]) if p.get("da") else t + 0.4
    return (f'<div class="stack">{head(p["h"], t+0.05, "md")}<div class="ui calcard" {A(t+0.05,"rise")}><div class="calt">{E(p["mon"])}</div><div class="cald" {A(a,"stamp")}>{E(p["day"])}</div><div class="caly">{E(p["yr"])}</div></div>'
            f'<div class="chiprow">' + "".join(chip(x[0], c.at(x[1]) if x[1] else a+.3, x[2], x[3]) for x in p.get("chips", [])) + '</div></div>')
def g_map(c, t, p):
    a1, a2 = c.at(p["la"]), c.at(p["ra"])
    def side(d, a):
        return (f'<div class="ui mapc" {A(a,"up")}><div class="flag">{E(d["tag"])}</div><div class="mnum" style="color:{TONE[d["col"]]}">{E(d["num"])}</div><small>{E(d["s"])}</small></div>')
    return f'<div class="stack">{head(p["h"], t+0.05, "md")}<div class="cells2">{side(p["l"],a1)}{side(p["r"],a2)}</div></div>'
def g_search(c, t, p):
    ta = c.at(p["ta"]) if p.get("ta") else t + 0.2
    res = "".join(f'<div class="srow" {A(c.at(an) if an else ta+0.5+i*0.2,"left")}><div class="sth th{i%4}">{icon("play")}</div><div class="sli"><b>{E(tx)}</b><i></i></div></div>' for i, (tx, an) in enumerate(p["items"]))
    return (f'<div class="ui searchc" {A(t+0.02,"rise")}><div class="sbx"><img src="assets/yt.svg"><span class="type" data-text="{E(p["q"])}" data-at="{ta:.2f}" data-dur="{p.get("td",0.7)}"></span><i class="caret"></i></div>{res}</div>')
def g_clock(c, t, p):
    a = c.at(p["ca"]) if p.get("ca") else t + 0.1
    return (f'<div class="stack"><div class="clockw" {A(t+0.05)}><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="90" fill="#fff" stroke="#111" stroke-width="10"/><line class="hand" data-spin2="{a:.2f}" x1="100" y1="100" x2="100" y2="30" stroke="#ff0033" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="100" r="10" fill="#111"/></svg></div>'
            f'{head(p["h"], c.at(p["ha"]) if p.get("ha") else t+0.1, p.get("hs",""))}' + (f'<div class="sub" {A(c.at(p["sa"]) if p.get("sa") else t+.5,"up")}>{E(p["sub"])}</div>' if p.get("sub") else "") + '</div>')
def g_image(c, t, p):
    """a related photo / screenshot in a white card. img = file inside the reel's assets/img/ folder."""
    ia = c.at(p["ia"]) if p.get("ia") else t + 0.1
    h = head(p["h"], c.at(p["ha"]) if p.get("ha") else t + 0.05, p.get("hs", "md")) if p.get("h") else ""
    capt = f'<div class="sub" {A(c.at(p["ca"]) if p.get("ca") else ia + 0.4, "up")}>{E(p["cap"])}</div>' if p.get("cap") else ""
    w = p.get("w", 900)
    return (f'<div class="stack">{h}<div class="ui" {A(ia, "rise")} style="width:{w}px;padding:18px;border-radius:40px;background:#fff">'
            f'<img src="assets/img/{E(p["img"])}" style="display:block;width:100%;max-height:{p.get("maxh", 760)}px;object-fit:cover;border-radius:26px"></div>{capt}</div>')
def g_logos(c, t, p):
    """brand logos in white chips. items = [(file in assets/img/, anchor or None), ...]"""
    h = head(p["h"], t + 0.05, p.get("hs", "md")) if p.get("h") else ""
    cells = ""
    for f, an in p["items"]:
        a = c.at(an) if an else t + 0.2
        cells += f'<div class="ui" {A(a)} style="padding:30px 44px;border-radius:34px;background:#fff"><img src="assets/img/{E(f)}" style="display:block;height:{p.get("lh", 110)}px"></div>'
    return f'<div class="stack">{h}<div style="display:flex;flex-wrap:wrap;gap:30px;justify-content:center">{cells}</div></div>'
G = {k[2:]: v for k, v in globals().items() if k.startswith("g_")}

def ribbon_text(spec):
    """ribbon wipe text: the channel/brand name if given, else the reel's topic, else nothing"""
    t = spec.get("brand") or spec.get("topic") or next((s[2].get("topic") for s in spec["scenes"] if s[2].get("topic")), "")
    return t.strip().upper()
def build(n, spec, toks, total, caps, tpl_path="scripts/reel_template.html"):
    """mode "voice": full 9:16 graphics.  mode "footage": person video in the bottom half, graphics in the top half,
    and any scene with full=True takes the whole 9:16 frame (person hidden) for its length."""
    mode = spec.get("mode", "voice")
    pal = PAIRS[(n - 1) % len(PAIRS)]
    c = Ctx(toks); scenes = []; S = spec["scenes"]
    starts = []
    for sc in S:   # resolve scene starts first, in spoken order
        c_start = c.at(sc[0]) if sc[0] else 0.0
        starts.append(c_start)
    c = Ctx(toks); body = []; cue = []; fulls = []
    wipes = [starts[i] for i in spec.get("wipes", [])]
    for i, sc in enumerate(S):
        t = starts[i]; end = starts[i+1] if i + 1 < len(S) else total
        p = dict(sc[2])
        if "from_" in p: p["from"] = p.pop("from_")
        c.base = None
        if sc[0]: c.at(sc[0])
        c.base, c.end = c.cur, end
        inner = G[sc[1]](c, t, p)
        topic = ""
        if p.get("topic"):
            topic = f'<div class="topic" {A(t+0.05,"left")}><span class="dot">{icon("bolt",2.4)}</span><span class="tbody">{E(p["topic"])}</span></div>'
        full = mode == "footage" and p.get("full")
        if full: fulls.append((t, end))
        if mode == "footage" and not full: inner, topic = f'<div class="fit">{topic}{inner}</div>', ""
        body.append(f'<div id="s{i}" class="clip scene{" full" if full else ""}" data-start="{max(0,t-0.05):.2f}" data-duration="{end-t+0.3:.2f}" data-track-index="1" data-in="{t:.2f}" data-out="{end:.2f}"><div class="cam">{topic}{inner}</div></div>')
    wipe_html = "".join(f'<div class="clip wipe" data-wipe="{w:.2f}" data-start="{max(0,w-0.4):.2f}" data-duration="1.1" data-track-index="4"></div>' for w in wipes)
    capsh = "".join(f'<div class="cap" data-in="{a:.2f}" data-out="{b:.2f}">{tx}</div>' for a, b, tx in caps)
    tpl = open(tpl_path, encoding="utf-8").read()
    person = ""
    if mode == "footage":
        person = f'<video id="pv" class="clip" src="assets/person.mp4" muted playsinline data-start="0" data-duration="{total:.2f}" data-media-start="0" data-track-index="3"></video>'
    out = (tpl.replace("%BRAND%", E(ribbon_text(spec))).replace("%MODE%", mode).replace("%PERSON%", person).replace("%FULLS%", json.dumps([[round(a, 2), round(b, 2)] for a, b in fulls]))
           .replace("%TOTAL%", f"{total:.2f}").replace("%SCENES%", "\n".join(body)).replace("%WIPES%", wipe_html).replace("%CAPS%", capsh)
           .replace("%A%", pal[0]).replace("%B%", pal[1]).replace("%SA%", pal[2]).replace("%SB%", pal[3]).replace("%DA%", pal[4]).replace("%DB%", pal[5]))
    # sound design comes straight from the animation so every effect lands on a visual
    ev = []
    for w in wipes: ev.append(("riser", max(0, w - 1.8))); ev.append(("whoosh", max(0, w - 0.3)))
    for fa, fb in fulls: ev.append(("whoosh", max(0, fa - 0.2))); ev.append(("swoosh", max(0, fb - 0.2)))
    for i, t in enumerate(starts):
        if t > 0 and t not in wipes: ev.append((("swoosh", "whoosh")[i % 3 == 0], max(0, t - 0.12)))
    for m in re.finditer(r'data-at="([\d.]+)" data-fx="(\w+)"', out):
        a, fx = float(m.group(1)), m.group(2)
        if fx == "pop": ev.append(("pop", a))
        elif fx == "stamp": ev.append(("impact", a))
        elif fx in ("left", "up"): ev.append(("tick", a))
        elif fx == "rise": ev.append(("swoosh", a))
        elif fx == "word": ev.append(("pop", a))
        elif fx == "draw": ev.append(("swoosh", a))
        elif fx == "cursor": pass
    for m in re.finditer(r'data-click="([\d.]+)"', out): ev.append(("click", float(m.group(1))))
    for m in re.finditer(r'class="subbtn" data-at="([\d.]+)"', out): ev.append(("ding", float(m.group(1)) + 0.1))
    ev.sort(key=lambda x: x[1]); gap = {"pop": 0.5, "tick": 0.3, "click": 0.1, "ding": 0.5, "impact": 0.8, "swoosh": 0.3, "whoosh": 0.3, "riser": 3}
    last = {}; kept = []
    for nm, a in ev:
        if a >= total - 0.1: continue
        if a - last.get(nm, -9) >= gap[nm]: kept.append([nm, round(a, 3)]); last[nm] = a
    return out, kept
