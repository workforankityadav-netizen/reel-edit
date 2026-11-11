# usage: python3 <skill>/scripts/new_reel.py <project-folder>
# Creates a reel project: copies this skill's scripts into <project>/scripts and writes blank roman.py / reels.py.
import os, shutil, sys
if len(sys.argv) != 2: sys.exit(__doc__ or "usage: new_reel.py <project-folder>")
P = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(P, exist_ok=True)
dst = os.path.join(P, "scripts")
shutil.copytree(HERE, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "new_reel.py"))
for d in ("raw", "exports", "sfx"): os.makedirs(os.path.join(P, d), exist_ok=True)
if not os.path.exists(f"{dst}/roman.py"):
    open(f"{dst}/roman.py", "w", encoding="utf-8").write('''# The words of each reel in Hinglish Roman, word for word as spoken. *word(s)* = yellow keyword in the captions.
R = {
1: """Paste the reel's spoken words here, *keyword* marked.""",
}
''')
if not os.path.exists(f"{dst}/reels.py"):
    open(f"{dst}/reels.py", "w", encoding="utf-8").write('''# Shot lists. Scene = (spoken anchor where it starts or None for the first, graphic, params).
# mode="voice": full 9:16 graphics.  mode="footage": person bottom half, graphics top half; full=True on a scene = full-screen break.
# See references/widgets.md for every graphic and its params, examples/reels_example.py for 10 real reels.
SPEC = {
1: dict(mode="voice", brand="", topic="", wipes=[], scenes=[
 (None, "head", dict(topic="Topic", ic="play", col="red", h="Big *headline*")),
]),
}
COVERS = {1: ("TOP LINE", "BIG WORD", "BOTTOM LINE?", "play", "red", False)}
TITLES = {1: "English Search Style YouTube Title"}
''')
print(f"project ready: {P}\n  put raw footage / voiceover in {P}/raw, optional own sound effects in {P}/sfx (whoosh/swoosh/impact/pop/click/ding/riser/tick .wav)")
