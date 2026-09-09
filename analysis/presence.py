import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])

SOL={'fn':'#268bd2','str':'#2aa198','meta':'#6c71c4','kw':'#859900',
     'num':'#d33682','ty':'#b58900','err':'#dc322f','sp':'#cb4b16'}
NM={'fn':'function names','str':'strings','meta':'special','kw':'keywords',
    'num':'numbers','ty':'type names','err':'errors','sp':'preprocessor'}
ORDER=['fn','str','meta','kw','num','ty','err','sp']
BG='#002b36'

def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)

def spread(v): return max(v)/min(v)

print("SOLARIZED: candidate measures of how much each accent 'pops' off the background\n")
print(f"{'role':16}{'L*':>6}{'Lab C*':>8}{'contrast':>10}{'OK dist from bg':>17}")
cols={'L':[],'C':[],'ct':[],'ok':[]}
for k in ORDER:
    L,C,h=lab2lch(hex2lab(SOL[k]))
    ct=contrast(SOL[k],BG); ok=okdE(SOL[k],BG)
    cols['L'].append(L); cols['C'].append(C); cols['ct'].append(ct); cols['ok'].append(ok)
    print(f"{NM[k]:16}{L:6.0f}{C:8.1f}{ct:10.2f}{ok:17.3f}")
print(f"\n{'':16}{'spread:':>6}{spread(cols['C']):8.2f}x{spread(cols['ct']):9.2f}x{spread(cols['ok']):16.2f}x")

# correlation between lightness and chroma
n=len(ORDER); mx=sum(cols['L'])/n; my=sum(cols['C'])/n
r=(sum((cols['L'][i]-mx)*(cols['C'][i]-my) for i in range(n))/
   math.sqrt(sum((x-mx)**2 for x in cols['L'])*sum((y-my)**2 for y in cols['C'])))
print(f"\nLightness vs chroma correlation in Solarized: r = {r:+.2f}")

d=json.load(open('schemes.json'))
FAV=['nocturne','aubergine','damson','verdigris','ashen']
print("\n\nDistance from own background, OKLab. Solarized's range is "
      f"{min(cols['ok']):.3f} to {max(cols['ok']):.3f}\n")
print(f"{'system':12}{'min':>8}{'max':>8}{'spread':>9}   loudest role")
allrows=[]
for s in d:
    if s['name'] not in FAV: continue
    bg=s['colors']['base03']
    vals=[(okdE(s['colors'][k],bg),k) for k in ORDER]
    vals.sort()
    print(f"{s['label'][:11]:12}{vals[0][0]:8.3f}{vals[-1][0]:8.3f}{vals[-1][0]/vals[0][0]:9.2f}x   "
          f"{NM[vals[-1][1]]} {vals[-1][0]:.3f}")
    allrows += [(v,s['label'],k) for v,k in vals]
print(f"\nSolarized's loudest accent sits {max(cols['ok']):.3f} from its background.")
over=[x for x in allrows if x[0]>max(cols['ok'])]
over.sort(reverse=True)
print(f"Mine that exceed it: {len(over)} of {len(allrows)}")
for v,lab,k in over[:10]: print(f"   {v:.3f}  {lab} / {NM[k]}")
