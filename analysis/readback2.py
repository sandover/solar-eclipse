import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
POLICY={'everywhere':(8.0,1.00),'common':(7.5,0.50),'occasional':(-4.5,0.65),'rare':(-2.0,0.70)}
FREQ={'fn':'everywhere','str':'everywhere','meta':'occasional','kw':'common',
      'num':'occasional','ty':'occasional','err':'rare','sp':'rare'}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
EDITS={
 'nocturne':{"err":[-4,0.55],"fn":[0,0.45],"kw":[-6.5,0.55],"sp":[-4,0.55]},
 'aubergine':{"err":[-8,0.7],"kw":[-5.5,0.7],"num":[-8,0.9],"sp":[-8,0.7],
              "str":[-3.5,1.05],"ty":[-8,0.9]},
 'damson':{"fn":[-8,1]},
}
d=json.load(open('schemes.json')); BY={s['name']:s for s in d}
floors=0
for nm,ed in EDITS.items():
    s=BY[nm]
    print(f"{s['label']}\n")
    print(f"  {'role':16}{'baseline':>10}{'yours':>10}{'bright':>8}{'vivid':>7}   vs before my policy")
    done=set()
    for k,(dl,cs) in sorted(ed.items()):
        if s['colors'][k] in done: continue
        done.add(s['colors'][k])
        L,C,h=lab2lch(hex2lab(s['colors'][k]))
        new,_=lch2hex((L+dl, C*cs, h))
        pdl,pcs=POLICY[FREQ[k]]
        net_dl, net_cs = pdl+dl, pcs*cs
        hit=' (slider floor)' if dl<=-8 else ''
        floors += 1 if dl<=-8 else 0
        share=[NM[x] for x in NM if s['colors'][x]==s['colors'][k] and x!=k and x in ed]
        label=NM[k]+(' + '+share[0] if share else '')
        print(f"  {label[:16]:16}{s['colors'][k]:>10}{new:>10}{dl:+8.1f}{cs:7.2f}"
              f"   {net_dl:+.1f} bright, {net_cs:.2f}x vivid{hit}")
    print()
print(f"Sliders bottomed out {floors} times. The brightness range only goes to -8.")
