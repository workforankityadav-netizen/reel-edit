# usage: python3 scripts/finish.py   (after render.py and the cover snapshot)
# prepend each cover for 0.4 s (voice shifts by the same 0.4 s), export under SEO titles, save the cover image too
import subprocess, glob, os, sys
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
EXP = "exports"; COV = f"{EXP}/covers"; os.makedirs(COV, exist_ok=True)
sys.path.insert(0, "scripts")
from reels import TITLES   # {N: "English search-style YouTube title"}
frames = sorted(glob.glob("covers/out/frame-*.png"))
for n, t in TITLES.items():
    d = f"reel-{n:02d}"; cov = frames[sorted(TITLES).index(n)]; out = f"{EXP}/{t}.mp4"
    subprocess.run(["cp", cov, f"{COV}/{t}.png"], check=True)
    fc = "[0:v]fps=30,format=yuv420p,setsar=1,trim=end_frame=12,setpts=PTS-STARTPTS[c];[1:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v];[c][v]concat=n=2:v=1:a=0[o];[2:a]adelay=400:all=1,apad=pad_dur=0.1[a]"
    subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",cov,"-i",f"{d}/renders/video.mp4","-i",f"{d}/audio/final-mix.wav",
      "-filter_complex",fc,"-map","[o]","-map","[a]","-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",out],check=True)
    print(n, "ok")
