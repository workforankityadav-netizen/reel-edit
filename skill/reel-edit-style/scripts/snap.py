# usage (from the project folder): python3 scripts/snap.py N  -> reel-NN/snap/contact-sheet*.jpg, one frame per scene near its end
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import NPX, HF
for n in map(int, sys.argv[1:]):
    d = f"reel-{n:02d}"; h = open(f"{d}/index.html", encoding="utf-8").read()
    ts = ",".join(f"{max(0.2, float(b) - 0.35):.2f}" for a, b in re.findall(r'data-in="([\d.]+)" data-out="([\d.]+)"><div class="cam"', h))
    shutil.rmtree(f"{d}/snap", ignore_errors=True)
    subprocess.run([NPX] + HF + ["snapshot", ".", "--at", ts, "--no-end", "-o", "snap", "--timeout", "120000"], cwd=d, capture_output=True)
    print(d, "->", f"{d}/snap/", len([f for f in os.listdir(f"{d}/snap") if f.startswith("contact")]) if os.path.isdir(f"{d}/snap") else 0, "contact sheets")
