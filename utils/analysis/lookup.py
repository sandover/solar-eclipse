import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
import math, json
src=open(ROOT / 'utils' / 'pal.py').read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)
d=json.load(open(ROOT / 'schemes.json'))
BY={s['name']:s for s in d}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
R=['fn','str','meta','kw','num','ty','err','sp']
NOTES=[('nocturne','#ad40ca','tone down'),('nocturne','#d75d23','satisfying, use more often'),
       ('aubergine','#e34b1f','tone down'),('aubergine','#759c30','tone down'),
       ('aubergine','#888e29','tone down'),('damson','#d0348f','tone down'),
       ('damson','#3aa5a1','weird'),('damson','#38a883','weird'),
       ('verdigris','#b43ac5','weird'),('ashen','#6aa131','too loud')]
print(f"{'system':11}{'hex':9}{'role':16}{'L*':>6}{'C*':>6}{'hue':>6}{'reach':>7}{'used':>6}   note")
for sysn,hx,note in NOTES:
    s=BY[sysn]; hit=[k for k in R if s['colors'][k].lower()==hx.lower()]
    if not hit:
        near=min(((okdE(hx,s['colors'][k]),k) for k in R))
        hit=[near[1]]; note+=f"  (nearest: {s['colors'][near[1]]}, dE {near[0]:.3f})"
    k=hit[0]; L,C,h=lab2lch(hex2lab(s['colors'][k]))
    print(f"{s['label'][:10]:11}{s['colors'][k]:9}{NM[k]:16}{L:6.1f}{C:6.1f}{h:6.0f}"
          f"{s['roles'][k]['reach']:7.3f}{s['roles'][k]['used']:5}%   {note}")

print("\n\nADJACENT ACCENTS: are neighbouring colours actually distinguishable?")
print("Equal steps in hue degrees are NOT equal steps in how different two colours look.\n")
print(f"{'system':11}{'closest pair':34}{'deg apart':>10}{'how different':>15}")
for s in [BY['solarized']]+[BY[n] for n in ('nocturne','aubergine','damson','verdigris','ashen')]:
    pairs=[]
    for i in range(len(R)):
        for j in range(i+1,len(R)):
            a,b=R[i],R[j]
            ha=lab2lch(hex2lab(s['colors'][a]))[2]; hb=lab2lch(hex2lab(s['colors'][b]))[2]
            pairs.append((okdE(s['colors'][a],s['colors'][b]),
                          abs((ha-hb+180)%360-180), NM[a], NM[b]))
    pairs.sort()
    for p in pairs[:2]:
        print(f"{s['label'][:10]:11}{p[2]+' / '+p[3]:34}{p[1]:10.0f}{p[0]:15.3f}")
    print()
