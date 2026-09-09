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
def band(h):
    if 340<=h or h<25: return 'red'
    if 25<=h<70: return 'orange'
    if 70<=h<95: return 'gold'
    if 95<=h<175: return 'green'
    if 175<=h<255: return 'blue'
    if 255<=h<310: return 'violet'
    return 'pink'
R=['fn','str','meta','kw','num','ty','err','sp']
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
LIKE={'nocturne':'LIKES','ashen':'LIKES','aubergine-clear':'LIKES',
      'verdigris':'pink annoying','cove':'too green','sloe':'too red, too bright'}
d=json.load(open(ROOT / 'schemes.json'))
print("The standout: whichever accent sits furthest from the ground.\n")
print(f"{'system':22}{'ground':>8}{'standout role':>16}{'its band':>9}{'dist':>7}   verdict")
for s in d:
    if s['name']=='solarized': continue
    bg=s['colors']['base03']
    far=max(R, key=lambda k: okdE(s['colors'][k],bg))
    h=s['roles'][far]['hue']
    print(f"{s['label']:22}{s['ground']:8}{NM[far]:>16}{band(h):>9}"
          f"{okdE(s['colors'][far],bg):7.3f}   {LIKE.get(s['name'],'')}")
print("\n\nEvery accent, by band, per scheme:\n")
for s in d:
    if s['name']=='solarized': continue
    seen=[]
    for k in R:
        hx=s['colors'][k]
        if hx not in [x[0] for x in seen]: seen.append((hx,s['roles'][k]['hue'],k))
    bands=[band(h) for _,h,_ in seen]
    tag=LIKE.get(s['name'],'')
    print(f"  {s['label']:22}{', '.join(bands):46}{tag}")
print("\n\nWhere strings (the one bright colour) lands:\n")
for s in d:
    if s['name']=='solarized': continue
    h=s['roles']['str']['hue']; L,C,_=lab2lch(hex2lab(s['colors']['str']))
    print(f"  {s['label']:22}{s['colors']['str']}  hue {h:4} {band(h):8} bright {L:4.0f} vivid {C:3.0f}   {LIKE.get(s['name'],'')}")
