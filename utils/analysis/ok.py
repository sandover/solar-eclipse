import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
import math, json
exec(open(ROOT / 'utils' / 'pal.py').read().split('# ---------- Solarized reference')[0])
exec(open(ROOT / 'utils' / 'pal.py').read().split('# ---------- OKLab')[1].split('\n',1)[1])

SOL={'fn':'#268bd2','str':'#2aa198','meta':'#6c71c4','kw':'#859900',
     'num':'#d33682','ty':'#b58900','err':'#dc322f','sp':'#cb4b16'}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
ORDER=['fn','str','meta','kw','num','ty','err','sp']

print("SOLARIZED: what I held constant (Lab C*) vs. what the eye reads (OKLab chroma)\n")
print(f"{'role':16}{'Lab C*':>9}{'OK chroma':>11}{'ratio':>8}")
sol=[]
for k in ORDER:
    _,C,_=lab2lch(hex2lab(SOL[k])); _,ok,_=hex2oklch(SOL[k])
    sol.append(ok)
    print(f"{NM[k]:16}{C:9.1f}{ok:11.3f}{ok/C*100:8.2f}")
print(f"\n  Lab C* spread:      {min(lab2lch(hex2lab(SOL[k]))[1] for k in ORDER):.0f} to {max(lab2lch(hex2lab(SOL[k]))[1] for k in ORDER):.0f}   ({max(lab2lch(hex2lab(SOL[k]))[1] for k in ORDER)/min(lab2lch(hex2lab(SOL[k]))[1] for k in ORDER):.2f}x)")
print(f"  OKLab spread:       {min(sol):.3f} to {max(sol):.3f}   ({max(sol)/min(sol):.2f}x)")

d=json.load(open(ROOT / 'schemes.json'))
FAV=['nocturne','aubergine','damson','verdigris','ashen']
print("\n\nMINE: OKLab chroma of the 'seen rarely' colours vs Solarized's\n")
print(f"{'system':12}{'type names':>12}{'errors':>10}{'preproc':>10}{'   worst vs Solarized'}")
sol_rare=max(hex2oklch(SOL[k])[1] for k in ('ty','err','sp'))
print(f"{'Solarized':12}"+"".join(f"{hex2oklch(SOL[k])[1]:>10.3f}  " for k in ('ty','err','sp')))
for s in d:
    if s['name'] not in FAV: continue
    vals=[hex2oklch(s['colors'][k])[1] for k in ('ty','err','sp')]
    print(f"{s['label'][:11]:12}"+"".join(f"{v:>10.3f}  " for v in vals)+
          f"   +{(max(vals)/sol_rare-1)*100:.0f}%")
print(f"\nSolarized's loudest colour anywhere: {max(hex2oklch(SOL[k])[1] for k in ORDER):.3f}")
allmine=[]
for s in d:
    if s['name'] not in FAV: continue
    for k in ORDER: allmine.append((hex2oklch(s['colors'][k])[1], s['label'], NM[k]))
allmine.sort(reverse=True)
print("My loudest five:")
for v,lab,role in allmine[:5]: print(f"   {v:.3f}  {lab} / {role}")
