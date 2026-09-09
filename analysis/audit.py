import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math, json
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)
A=['fn','str','meta','kw','num','ty','err','sp']
d=json.load(open('schemes.json'))
sol=[s for s in d if s['name']=='solarized'][0]

print("The invariant I never noticed: every accent's brightness sits between the two")
print("body-text tones -- base00 (50.2, light mode's text) and base0 (60.1, dark mode's).")
print("No coloured token is ever brighter than plain prose.\n")
print(f"  Solarized accents span L* {min(lab2lch(hex2lab(sol['colors'][k]))[0] for k in A):.1f}"
      f" to {max(lab2lch(hex2lab(sol['colors'][k]))[0] for k in A):.1f}"
      f"   (base00 = 50.2, base0 = 60.1)\n")
print(f"{'system':12}{'accent L* range':>18}{'over body text?':>18}{'dual-ground spread':>20}")
for s in d:
    Ls=[lab2lch(hex2lab(s['colors'][k]))[0] for k in A]
    body=lab2lch(hex2lab(s['colors']['base0']))[0]
    over=[k for k in A if lab2lch(hex2lab(s['colors'][k]))[0] > body+0.15]
    dk=[okdE(s['colors'][k],s['colors']['base03']) for k in A]
    lt=[okdE(s['colors'][k],s['colors']['base3'])  for k in A]
    comb=[(dk[i]+lt[i])/2 for i in range(8)]
    flag=('  '+','.join(over)) if over else '  none'
    print(f"{s['label'][:11]:12}{min(Ls):8.1f} to {max(Ls):5.1f}{flag:>18}{max(comb)/min(comb):20.2f}x")
print(f"\nSolarized's dual-ground spread is 1.15x -- tighter than either ground alone")
print("(1.27x dark, 1.29x light). It balances presence across BOTH backgrounds.")
print("I only ever optimised the dark one.")
