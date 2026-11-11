# voice (padded to full length) + ducked music + SFX cues -> two-pass loudnorm to -14 LUFS / -1 dBTP
import subprocess,json,sys
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from tools import FFMPEG, FFPROBE, WHISPER, MODEL
d,cuesf,out,total=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4])
cfg=json.load(open(cuesf, encoding="utf-8")); cues=cfg["cues"]; lv=cfg["levels"]
inp=["-i","voice.wav","-i","music.wav"]; fc=[]
fc.append(f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,apad=whole_dur={total},asplit=2[vo][sc]")
fc.append("[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-19dB[mu0]")
fc.append("[mu0][sc]sidechaincompress=threshold=0.03:ratio=3:attack=40:release=400[mu]")
labels=["[vo]","[mu]"]
for k,(name,t) in enumerate(cues):
    inp+=["-i",f"{name}.wav"]; i=k+2
    fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,volume={lv[name]}dB,adelay={int(t*1000)}[s{i}]"); labels.append(f"[s{i}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{total}[mix]")
base=[FFMPEG,"-hide_banner","-y"]+inp+["-filter_complex"]
g=";".join(fc)+";[mix]"
r=subprocess.run(base+[g+"loudnorm=I=-14:TP=-1:LRA=9:print_format=json[o]","-map","[o]","-f","null","-"],capture_output=True,text=True,cwd=d)
j=json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}")+1])
ln=f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000"
subprocess.run(base+[g+ln+"[o]","-map","[o]","-ac","2","-c:a","pcm_s16le",out],check=True,capture_output=True,cwd=d)
print("ok", len(cues), "cues")
