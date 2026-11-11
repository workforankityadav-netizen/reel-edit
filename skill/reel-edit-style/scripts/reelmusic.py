# Original upbeat loop per reel (seamless, numbered variations of tempo, chords and groove). usage: reelmusic.py out.wav N
import math, wave, array, random, sys
SR = 44100; n = int(sys.argv[2]); rnd = random.Random(100 + n)
PROG = [([[60,64,67,71],[55,59,62,67],[57,60,64,69],[53,57,60,65]],[36,43,45,41]),
        ([[57,60,64,67],[53,57,60,64],[60,64,67,71],[55,59,62,65]],[45,41,36,43]),
        ([[62,65,69,72],[58,62,65,69],[60,64,67,70],[57,60,64,67]],[38,46,36,45]),
        ([[53,57,60,64],[55,59,62,65],[57,60,64,67],[60,64,67,71]],[41,43,45,36]),
        ([[64,67,71,74],[60,64,67,71],[62,65,69,72],[59,62,67,71]],[40,36,38,43])]
BPM = [112, 106, 118, 110, 116, 104, 120, 108, 114, 122][(n-1) % 10]
chords, roots = PROG[(n-1) % 5]; pat = [[0,1,2,3,2,1,2,3],[0,2,1,3,0,2,1,3],[3,2,1,0,1,2,3,2],[0,1,3,2,0,1,3,2],[0,2,3,1,0,2,3,1]][(n*2) % 5]
beat = 60/BPM; bar = 4*beat; BARS = 8; N = int(BARS*bar*SR); buf = [0.0]*N
def mid(x): return 440*2**((x-69)/12)
def add(t0, dur, fn):
    a = int(t0*SR)
    for i in range(int(dur*SR)): buf[(a+i) % N] += fn(i/SR)
def ep(t0, f, d, amp): add(t0, d, lambda t: amp*math.exp(-t*5.5)*min(1,t*400)*(math.sin(2*math.pi*f*t)+0.25*math.sin(4*math.pi*f*t)*math.exp(-t*9)))
def pad(t0, f, d, amp): add(t0, d, lambda t: amp*min(1,t/0.5)*min(1,max(0,d-t)/0.5)*(math.sin(2*math.pi*f*t)+0.5*math.sin(2*math.pi*f*1.004*t)))
def sub(t0, f, d, amp): add(t0, d, lambda t: amp*min(1,t*200)*min(1,max(0,d-t)*40)*math.exp(-t*2.2)*math.sin(2*math.pi*f*t))
def noise(t0, d, amp, dec, hp=True):
    st = [0.0]
    def fn(t):
        x = rnd.uniform(-1,1); y = x-st[0] if hp else x; st[0] = x
        return amp*y*math.exp(-t*dec)
    add(t0, d, fn)
def kick(t0, amp):
    ph = [0.0]
    def fn(t):
        ph[0] += 2*math.pi*(48+80*math.exp(-t*30))/SR; return amp*math.sin(ph[0])*math.exp(-t*10)
    add(t0, 0.28, fn)
for b in range(BARS):
    t = b*bar; c = chords[b % 4]; r = roots[b % 4]
    for p in c: pad(t, mid(p), bar, 0.03)
    sub(t, mid(r), beat*1.8, 0.2); sub(t+2*beat, mid(r), beat*1.8, 0.16)
    for s in range(8): ep(t+s*beat/2, mid(c[pat[s]]+12), beat*1.2, 0.07 if s%2==0 else 0.05)
    for s in (0, 2): kick(t+s*beat, 0.22)
    for s in (1, 3): noise(t+s*beat, 0.12, 0.06, 30, False)
    for s in range(8): noise(t+s*beat/2, 0.06, 0.05 if s%2 else 0.03, 70)
pk = max(abs(x) for x in buf); g = 0.7/pk
w = wave.open(sys.argv[1],'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(array.array('h',(int(x*g*32767) for x in buf)).tobytes()); w.close()
print(n, BPM, "bpm", round(BARS*bar,1), "s")
