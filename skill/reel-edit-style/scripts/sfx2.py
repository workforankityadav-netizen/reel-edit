# Synthesized, original SFX kit: whoosh, swoosh, impact, pop, click, ding, riser, tick.
import math,wave,array,random,sys
SR=44100; out=sys.argv[1]; rnd=random.Random(11)
def save(n,b,peak=0.85):
    pk=max(abs(x) for x in b) or 1
    w=wave.open(f"{out}/{n}.wav",'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(array.array('h',(int(x/pk*peak*32767) for x in b)).tobytes()); w.close()
def bp_noise(dur,f_of_t,env,r=0.97):
    n=int(dur*SR); y1=y2=0; b=[]
    for i in range(n):
        t=i/n; w0=2*math.pi*f_of_t(t)/SR; x=rnd.uniform(-1,1)
        y=x*(1-r)+2*r*math.cos(w0)*y1-r*r*y2; y2=y1; y1=y; b.append(y*env(t))
    return b
save("whoosh",bp_noise(0.6,lambda t:300+2900*math.sin(math.pi*t)**1.5,lambda t:math.sin(math.pi*t)**2))
save("swoosh",bp_noise(0.26,lambda t:900+3200*t,lambda t:math.sin(math.pi*t)**1.5,0.95))
save("riser",bp_noise(1.8,lambda t:250+3500*t**2,lambda t:(t**1.6)*min(1,(1-t)*12),0.98))
# impact: pitched thump + short noise crack
n=int(0.45*SR); b=[]; ph=0
for i in range(n):
    t=i/SR; f=46+90*math.exp(-t*25); ph+=2*math.pi*f/SR
    b.append(math.sin(ph)*math.exp(-t*7)+0.35*rnd.uniform(-1,1)*math.exp(-t*60))
save("impact",b)
n=int(0.07*SR); b=[]; ph=0
for i in range(n):
    t=i/SR; f=420+600*math.exp(-t*60); ph+=2*math.pi*f/SR
    b.append(math.sin(ph)*math.exp(-t*45)*min(1,t*2000))
save("pop",b)
n=int(0.03*SR); b=[]
for i in range(n):
    t=i/SR; b.append((0.6*math.sin(2*math.pi*2600*t)+rnd.uniform(-1,1)*0.5)*math.exp(-t*220))
save("click",b)
n=int(0.9*SR); b=[]
for i in range(n):
    t=i/SR; e=math.exp(-t*5)*min(1,t*800)
    b.append(e*(math.sin(2*math.pi*1318.5*t)+0.5*math.sin(2*math.pi*1975.5*t)*math.exp(-t*3)+0.25*math.sin(2*math.pi*2637*t)))
save("ding",b)
n=int(0.018*SR); b=[]
for i in range(n):
    t=i/SR; b.append(rnd.uniform(-1,1)*math.exp(-t*400))
save("tick",b)

# tape stop: chord whose pitch and speed sag to zero
n=int(0.7*SR); b=[]; ph=[0,0,0]
for i in range(n):
    t=i/n; sp=(1-t)**2
    v=0
    for k,f in enumerate((220,277.2,329.6)):
        ph[k]+=2*math.pi*f*sp/SR; v+=math.sin(ph[k])+0.3*math.sin(2*ph[k])
    b.append(v*min(1,(1-t)*6)*min(1,i/200))
save("tapestop",b,0.7)
# soft sub boom hit (1.6 s)
n=int(1.6*SR); b=[]; ph=0; lp=0
for i in range(n):
    t=i/SR; f=38+55*math.exp(-t*12); ph+=2*math.pi*f/SR
    lp+=0.05*(rnd.uniform(-1,1)-lp)
    b.append(math.sin(ph)*math.exp(-t*2.4)+1.5*lp*math.exp(-t*5))
save("hit",b)
print("sfx kit ok")
