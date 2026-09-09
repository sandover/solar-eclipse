import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)

EDITS={"err":[-2,0.7],"kw":[7.5,0.5],"meta":[-3.5,0.45],"num":[-4,0.7],"str":[8,1],"ty":[-6,0.8]}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
FREQ={'fn':'everywhere','str':'everywhere','meta':'occasional','kw':'common',
      'num':'occasional','ty':'occasional','err':'rare','sp':'rare'}
ORDER=['fn','str','meta','kw','num','ty','err','sp']

d=json.load(open('schemes.json'))
s=[x for x in d if x['name']=='nocturne'][0]
bg=s['colors']['base03']; body=s['colors']['base0']
bodyL=lab2lch(hex2lab(body))[0]

print(f"NOCTURNE, as you left it        body text sits at L*{bodyL:.1f}\n")
print(f"{'role':16}{'how often':12}{'was':9}{'now':9}{'bright':>9}{'vivid':>8}{'presence':>10}")
rows=[]
for k in ORDER:
    was=s['colors'][k]
    L,C,h=lab2lch(hex2lab(was))
    dl,cs=EDITS.get(k,[0,1.0])
    now,_=lch2hex((L+dl, C*cs, h))
    p0,p1=okdE(was,bg),okdE(now,bg)
    rows.append((k,was,now,L,L+dl,C,C*cs,p0,p1))
    mark=''
    if L+dl > bodyL+0.2: mark='  brighter than body text'
    print(f"{NM[k]:16}{FREQ[k]:12}{was:9}{now:9}{dl:+9.1f}{cs:8.2f}{p1-p0:+10.3f}{mark}")

print(f"\nPresence range before: {min(r[7] for r in rows):.3f} to {max(r[7] for r in rows):.3f}"
      f"   spread {max(r[7] for r in rows)/min(r[7] for r in rows):.2f}x")
print(f"Presence range after : {min(r[8] for r in rows):.3f} to {max(r[8] for r in rows):.3f}"
      f"   spread {max(r[8] for r in rows)/min(r[8] for r in rows):.2f}x")
print(f"(Solarized's own spread is 1.27x, its furthest 0.423)")

print("\nYour edits sorted by how often the colour appears:")
for grp in ('everywhere','common','occasional','rare'):
    ks=[k for k in ORDER if FREQ[k]==grp and k in EDITS]
    if not ks: 
        skip=[k for k in ORDER if FREQ[k]==grp]
        print(f"  {grp:12} untouched: {', '.join(NM[k] for k in skip)}")
        continue
    dl=sum(EDITS[k][0] for k in ks)/len(ks); cs=sum(EDITS[k][1] for k in ks)/len(ks)
    print(f"  {grp:12} brightness {dl:+5.1f}   saturation {cs:.2f}x   ({', '.join(NM[k] for k in ks)})")
