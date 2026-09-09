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
ED={"err":[-7.5,0.2],"fn":[-4.5,0.25],"kw":[-6.5,0.55],"meta":[-3.5,0.9],
    "num":[0,0.85],"sp":[-7.5,0.2],"ty":[0,0.85]}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
R=['fn','str','meta','kw','num','ty','err','sp']
SOL={'fn':'#268bd2','str':'#2aa198','meta':'#6c71c4','kw':'#859900',
     'num':'#d33682','ty':'#b58900','err':'#dc322f','sp':'#cb4b16'}
d=json.load(open(ROOT / 'schemes.json')); s=[x for x in d if x['name']=='nocturne'][0]
bg=s['colors']['base03']
b01=lab2lch(hex2lab(s['colors']['base01']))[0]
b0 =lab2lch(hex2lab(s['colors']['base0']))[0]

print("NOCTURNE as you have it now\n")
print(f"  ground     {bg}")
print(f"  body text  {s['colors']['base0']}\n")
print(f"  {'role':22}{'hex':9}{'bright':>8}{'vivid':>7}{'distance out':>14}")
seen=set(); rows=[]
for k in R:
    dl,cs = ED.get(k,[0,1.0])
    L,C,h = s['lch'][k]
    hx,_ = lch2hex((L+dl, C*cs, h))
    if hx in seen: continue
    seen.add(hx)
    share=[NM[x] for x in R if x!=k and ED.get(x,[0,1])==ED.get(k,[0,1]) and s['lch'][x][:1]==s['lch'][k][:1] and lch2hex((s['lch'][x][0]+ED.get(x,[0,1])[0], s['lch'][x][1]*ED.get(x,[0,1])[1], s['lch'][x][2]))[0]==hx]
    lab=NM[k]+(' + '+share[0] if share else '')
    rows.append((hx,L+dl,C*cs,okdE(hx,bg)))
    flag=' below comments' if L+dl < b01 else ''
    print(f"  {lab[:22]:22}{hx:9}{L+dl:8.1f}{C*cs:7.0f}{okdE(hx,bg):14.3f}{flag}")

sv=[lab2lch(hex2lab(v))[1] for v in SOL.values()]
sd=[okdE(v,'#002b36') for v in SOL.values()]
print(f"\n  vividness   yours {min(r[2] for r in rows):.0f} to {max(r[2] for r in rows):.0f}"
      f"      Solarized {min(sv):.0f} to {max(sv):.0f}")
print(f"  brightness  yours {min(r[1] for r in rows):.0f} to {max(r[1] for r in rows):.0f}"
      f"      Solarized 49 to 60   (comments {b01:.0f}, body text {b0:.0f})")
print(f"  distance    yours {min(r[3] for r in rows):.3f} to {max(r[3] for r in rows):.3f}"
      f"   Solarized {min(sd):.3f} to {max(sd):.3f}")
print(f"\n  Average vividness: yours {sum(r[2] for r in rows)/len(rows):.0f}, "
      f"Solarized {sum(sv)/len(sv):.0f}  ->  {(1-(sum(r[2] for r in rows)/len(rows))/(sum(sv)/len(sv)))*100:.0f}% less colourful")
print(f"  Average distance : yours {sum(r[3] for r in rows)/len(rows):.3f}, "
      f"Solarized {sum(sd)/len(sd):.3f}")
