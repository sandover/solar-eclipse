import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
exec(open(_P).read().split('# ---------- Solarized reference')[0])

def max_C(L,h):
    lo,hi=0.0,150.0
    for _ in range(40):
        mid=(lo+hi)/2
        r=xyz2rgb(lab2xyz(lch2lab((L,mid,h))))
        if all(-1e-4<=v<=1+1e-4 for v in r): lo=mid
        else: hi=mid
    return lo

SOL={'fn':'#268bd2','str':'#2aa198','meta':'#6c71c4','kw':'#859900',
     'num':'#d33682','ty':'#b58900','err':'#dc322f','sp':'#cb4b16'}
NAME={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
      'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
print("SOLARIZED: how much of the available colour each accent actually uses\n")
print(f"{'role':16}{'hue':>6}{'L*':>6}{'C* used':>9}{'C* available':>14}{'restraint':>11}")
sol_ratio={}
for k,v in SOL.items():
    L,C,h=lab2lch(hex2lab(v)); m=max_C(L,h)
    sol_ratio[k]=C/m
    print(f"{NAME[k]:16}{h:6.0f}{L:6.0f}{C:9.1f}{m:14.1f}{C/m:10.0%}")

d=json.load(open('schemes.json'))
print("\nMY SYSTEMS: same measurement, for the five you picked\n")
print(f"{'system':11}{'role':16}{'hue':>6}{'L*':>6}{'C*':>7}{'avail':>7}{'restraint':>11}   note")
FAV=['nocturne','aubergine','damson','verdigris','ashen']
for s in d:
    if s['name'] not in FAV: continue
    for k in ['kw','ty','err','sp','fn','str','num','meta']:
        L,C,h=lab2lch(hex2lab(s['colors'][k])); m=max_C(L,h)
        r=C/m
        note='' 
        if r>0.93: note='<- maxed out'
        print(f"{s['label'][:10]:11}{NAME[k]:16}{h:6.0f}{L:6.0f}{C:7.1f}{m:7.1f}{r:10.0%}   {note}")
    print()
avg_sol=sum(sol_ratio.values())/8
print(f"Solarized average restraint: {avg_sol:.0%}")
rs=[]
for s in d:
    if s['name'] not in FAV: continue
    for k in SOL:
        L,C,h=lab2lch(hex2lab(s['colors'][k])); rs.append(C/max_C(L,h))
print(f"My average restraint:        {sum(rs)/len(rs):.0%}")
