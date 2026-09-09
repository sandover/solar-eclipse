import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)
GREEN=(80,170)          # olive through green-teal
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
ORDER=['fn','str','meta','kw','num','ty','err','sp']
d=json.load(open('schemes.json')); BY={s['name']:s for s in d}

def isgreen(h): return GREEN[0] <= h <= GREEN[1]

print("Where the green comes from\n")
for nm in ('damson','aubergine'):
    s=BY[nm]; g=s['ground']
    print(f"  {s['label']}  ground {g}deg")
    for k in ORDER:
        h=s['roles'][k]['hue']; dist=abs((h-g+180)%360-180)
        print(f"     {NM[k]:15}hue {h:4}  {dist:4}deg from ground  {'GREEN' if isgreen(h) else ''}")
    print(f"     -> the ground's opposite is {(g+180)%360}deg, which is green. The roles that")
    print(f"        sit furthest from the ground have nowhere else to be.\n")

print("="*74)
print("If green is banned outright, how much room is left?\n")
def spacing(hues, L=55.0, C=55.0):
    """smallest visible gap between neighbouring accents, at matched brightness"""
    hx=[lch2hex((L,C,h))[0] for h in hues]
    worst=9
    for i in range(len(hues)):
        for j in range(i+1,len(hues)):
            worst=min(worst, okdE(hx[i],hx[j]))
    return worst

SOLHUES=[266,188,294,111,355,84,34,48]
print(f"  Solarized, 8 accents over the whole wheel : closest pair {spacing(SOLHUES):.3f}")

for nm in ('damson','aubergine'):
    s=BY[nm]; g=s['ground']
    # usable arc: not green, and not within 30 deg of the ground
    ok=[h for h in range(360) if not isgreen(h) and abs((h-g+180)%360-180)>=30]
    # split into runs, then spread n accents evenly across the total usable span
    runs=[]; cur=[ok[0]]
    for h in ok[1:]:
        if h==cur[-1]+1: cur.append(h)
        else: runs.append(cur); cur=[h]
    runs.append(cur)
    if len(runs)>1 and runs[0][0]==0 and runs[-1][-1]==359:
        runs[0]=runs[-1]+runs[0]; runs.pop()
    total=sum(len(r) for r in runs)
    print(f"\n  {s['label']}: {total} degrees usable ({len(runs)} arcs), out of 360")
    for n in (8,7,6):
        hues=[]; step=total/n; pos=step/2
        for _ in range(n):
            acc=0
            for r in runs:
                if pos < acc+len(r): hues.append(r[int(pos-acc)]%360); break
                acc+=len(r)
            pos+=step
        print(f"     {n} accents -> {[h for h in hues]}")
        print(f"        closest pair {spacing(hues):.3f}"
              f"   {'holds up' if spacing(hues)>=0.050 else 'too crowded, colours blur'}")
