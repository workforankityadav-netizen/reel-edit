# Graphics (widgets) and their params

A scene is `(anchor, "widget", dict(...))`.

**Every scene accepts:**
- `topic="..."`: the small black tag at the top left.
- `full=True`: footage mode only. The scene goes full screen and the person is hidden.

**Words and anchors:**
- In `h` (headline) and `sub`, `*word*` turns that word red.
- Params ending in `a` (`ha`, `sa`, `na`, `ia`…) are spoken anchors. The first words of the phrase that reveals that part are searched from the scene's start. Leave one out and that part appears just after the scene starts.
- Anchors use the words in `roman.py`, lower-case, without punctuation. Numbers lose commas (`1,000` matches `1000`); keep `%` and `₹`.

**Shared values:**
- `col` (colours): `red`, `ink`, `green`, `blue`, `amber`, `purple`, `pink`, `teal`.
- `hs` (headline size): `""` (largest), `"md"`, `"sm"`, `"lg"`.
- `ic` (icons): `ad`, `alert`, `ban`, `bank`, `bell`, `bolt`, `cal`, `card`, `chart`, `chat`, `check`, `clock`, `copy`, `dollar`, `down`, `edit`, `eye`, `file`, `fire`, `ghost`, `globe`, `heart`, `hook`, `lock`, `mail`, `mic`, `moon`, `music`, `person`, `phone`, `play`, `refresh`, `robot`, `rupee`, `scissors`, `search`, `share`, `shield`, `skull`, `star`, `sun`, `swipe`, `sword`, `tag`, `target`, `trend`, `unlock`, `users`, `wifi`, `x`. Also `yt` (a red play logo) and `studio`.

| Widget | Params | Example |
|---|---|---|
| `head` | `ic`, `col`, `size`, `h`, `hs`, `kick`, `sub`, `sa` | `("lekin asli", "head", dict(ic="alert", col="amber", h="Asli *khatra?*", sub="sirf views rukna nahi", sa="sirf"))` |
| `stat` | `num`, `pre`, `suf`, `na`, `from`, `dur`, `ic`, `col`, `kick`, `h`, `ha`, `sub`, `sa` | `("aur woh", "stat", dict(num=10, suf=" SEC", na="10", h="Mein samajh aa jayega", ha="samajh"))` |
| `tiles` | `h`, `items=[(text, icon, colour, anchor)]`, `size` | `(None, "tiles", dict(topic="YouTube Secret", h="Apni video *khud* dekhte ho?", items=[("Apna phone", "phone", "ink", "phone"), ("Ghar ka Wi-Fi", "wifi", "blue", "wi-fi")]))` |
| `list` | `h`, `items=[(text, "ok"/"no"/icon, anchor)]` | `("aap soch", "list", dict(h="Aap sochte ho", items=[("Video kharab hai?", "alert", "video"), ("Channel shadowban?", "ban", "shadowban")]))` |
| `flow` | `h`, `items=[(text, icon, colour, anchor)]` (vertical steps with arrows) | `("jahan bina", "flow", dict(items=[("Bina original script", "file", "red", "bina"), ("Text copy-paste", "copy", "red", "copy-paste")]))` |
| `vs` | `no=dict(ic, h, s)`, `ok=dict(ic, h, s)`, `la`, `ra`, `h` | `("youtube ai", "vs", dict(no=dict(ic="copy", h="Inauthentic", s="copy-paste"), ok=dict(ic="robot", h="AI", s="koi nafrat nahi"), la="inauthentic", ra="youtube"))` |
| `ban` | `ic`, `col`, `ba` (when the red ban sign stamps), `h`, `hs`, `ha`, `sub`, `sa` | `("anjaani", "ban", dict(ic="play", col="red", ba="galti", h="Anjaani *galti*"))` |
| `lock` | `ic`, `col`, `la` (when it locks), `h`, `ha` | `("ek hi", "lock", dict(ic="eye", col="blue", la="freeze", h="Views *FREEZE*", ha="freeze"))` |
| `studio` | `rows=[(views, colour)]`, `ra`, `stamp`, `sa`, `h` (mock Studio content list) | `(None, "studio", dict(topic="Shorts Trap", rows=[("0","red")]*4, ra="achanak", stamp="0 VIEWS", sa="0"))` |
| `chart` | `title`, `kind="drop"/"cliff"/"rise"`, `da`, `dd`, `labs=[(text, x, y, colour, anchor)]`, `h`, `ha` | `("jo aapke", "chart", dict(title="CHANNEL HEALTH", kind="drop", da="channel", h="Chupchaap *khatam*", ha="khatam"))` |
| `bars` | `h`, `items=[(label, value text, 0–1, colour, anchor)]` | `("youtube studio", "bars", dict(h="Viewed vs Swiped", items=[("Viewed", "70%+", 0.72, "green", "70%"), ("Swiped Away", "kam rakho", 0.28, "red", "viewed")]))` |
| `meter` | `h`, `sa`, `to` (0–100 needle), `val` | `("rate", "meter", dict(h="Swipe-away rate", sa="40%", to=60, val="40%+ = DANGER"))` |
| `toggle` | `bar`, `q`, `opts=[a, b]`, `ca` (when the 2nd option is picked), `h`, `logo` | `("isliye apni", "toggle", dict(topic="Sahi tareeka", bar="YouTube Studio", q="Video kaise check karein?", opts=["Internal Preview", "Apne phone se play"], ca="internal", h="Hamesha *Internal Preview*"))` |
| `shortsphone` | `label`, `sa`, `h`, `ha`, `cls` | `("jab aap", "shortsphone", dict(sa="turant", label="TURANT BAND", h="Khud chalaya, *turant band*", ha="chalakar"))` |
| `crowd` | `h`, `pa`, `val`, `va`, `n`, `gone`, `ka` | `("youtube ka", "crowd", dict(topic="Algorithm ka test", h="*Seed Audience*", pa="har", val="100–500 viewers", va="100"))` |
| `cal` | `mon`, `day`, `yr`, `da`, `h`, `chips` | `("jo ki", "cal", dict(h="Rule badlega", mon="FEB", day="1", yr="2027", da="february"))` |
| `map` | `l=dict(tag, num, s, col)`, `r=dict(...)`, `la`, `ra`, `h` (two-panel compare) | `("youtube kuch", "map", dict(h="Minimum payment", l=dict(tag="TEST", num="$20", s="kuch users", col="green"), r=dict(tag="ABHI", num="$100", s="baaki sab", col="red"), la="20", ra="minimum"))` |
| `clock` | `h`, `hs`, `ha`, `ca` (when it spins), `sub`, `sa` | `("jahan algorithm", "clock", dict(h="Audience dhoondhne mein *mahine*", hs="md", ca="sahi", ha="audience"))` |
| `search` | `q` (typed query), `ta`, `td`, `items` | `("search karo", "search", dict(q="youtube shorts tips", ta="search"))` |
| `cta` | `text` (typed comment), `ta`, `td`, `sa` (subscribe button) | `("waise kya", "cta", dict(text="Haan, maine bhi ki hai!", ta="kya", td=1.2, sa="subscribe"))` |
| `image` | `img` (file in `reel-NN/assets/img/`), `ia`, `h`, `ha`, `hs`, `cap`, `ca`, `w`, `maxh` | `("yeh dekho", "image", dict(img="dashboard.png", ia="dekho", h="Studio *dashboard*", cap="real screenshot"))` |
| `logos` | `items=[(file in assets/img/, anchor)]`, `h`, `hs`, `lh` | `("maine kaam", "logos", dict(h="7 saal", items=[("adda.svg", "adda"), ("testbook.svg", "testbook")]))` |

**Spec-level keys:**
- `SPEC[N] = dict(mode="voice"|"footage", brand="Channel name (optional)", topic="Reel topic (optional)", wipes=[scene indexes], scenes=[...])`. Ribbon text = brand, else topic, else the first scene's topic, else blank.
- `COVERS[N] = (top line, BIG LINE, bottom line, icon, colour, crossed_out)`.
- `TITLES[N] = "English search-style title"`.

**Adding a graphic:**
- Write `def g_name(c, t, p):` in `engine.py`.
- It returns HTML. Wrap it in `<div class="stack">…</div>` to centre it.
- Use `A(time, fx)` for entrances. `fx` is `pop`, `up`, `rise`, `left`, `right`, `word`, `stamp`, `growx` or `growy`.
- Use `c.at("spoken words")` to get the time of a word.
- Sound cues are added automatically from the effects (`pop` → pop, `stamp` → impact, `left`/`up` → tick, and so on).
