import subprocess,re,sys,json
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
src,out=sys.argv[1],sys.argv[2]
r=subprocess.run([FFMPEG,"-hide_banner","-nostats","-i",src,"-af","silencedetect=n=-40dB:d=0.18","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",r)]
dur=float(subprocess.run([FFPROBE,"-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
keep=[]; t=0.0; KEEP=0.16
for a,b in zip(st,en):
    if b-a>0.26:
        keep.append((t,a+KEEP/2)); t=b-KEEP/2
keep.append((t,dur))
fc=[]
for i,(a,b) in enumerate(keep):
    fc.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={b-a-0.004:.4f}:d=0.004[a{i}]")
fc.append("".join(f"[a{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1[o]")
subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-i",src,"-filter_complex",";".join(fc),"-map","[o]","-c:a","pcm_s16le",out],check=True)
newdur=sum(b-a for a,b in keep)
json.dump(keep,open(out+".keep.json","w", encoding="utf-8"))
print(f"{len(keep)} parts, {dur:.2f}s -> {newdur:.2f}s")
