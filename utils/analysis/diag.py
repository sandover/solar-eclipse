import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
import math
exec(open(ROOT / 'utils' / 'pal.py').read().split('# ---------- Solarized reference')[0])
SOL={'base03':'#002b36','yellow':'#b58900','orange':'#cb4b16','red':'#dc322f',
 'magenta':'#d33682','violet':'#6c71c4','blue':'#268bd2','cyan':'#2aa198','green':'#859900'}
A={k:lab2lch(hex2lab(v)) for k,v in SOL.items()}
G=A['base03'][2]
acc=sorted([(v[2],k,v[1]) for k,v in A.items() if k!='base03'])

print("Solarized accent ring, by CIELAB hue angle:\n")
print(f"{'accent':9}{'hue':>7}{'C*':>7}{'gap to next':>13}{'dist to ground':>16}")
for i,(h,k,c) in enumerate(acc):
    nh = acc[(i+1)%len(acc)][0]
    gap = (nh-h) % 360
    d = abs((h-G+180)%360-180)
    print(f"{k:9}{h:7.0f}{c:7.0f}{gap:13.0f}{d:16.0f}")

gaps=[((acc[(i+1)%len(acc)][0]-h)%360, acc[i][1], acc[(i+1)%len(acc)][1], h) for i,(h,k,c) in enumerate(acc)]
gaps.sort(reverse=True)
print("\nWidest gaps in the ring:")
for g,a,b,h in gaps[:4]:
    print(f"  {g:5.0f} deg  between {a} and {b}   midpoint {(h+g/2)%360:5.0f}")
print(f"\nGround sits at {G:.0f}.  Nearest accent is {min(acc,key=lambda t:abs((t[0]-G+180)%360-180))[1]} "
      f"at {min(abs((h-G+180)%360-180) for h,k,c in acc):.0f} deg clearance.")

print("\nChroma vs. distance-from-ground (is accent C* a function of how far it sits from the ground?)")
pts=[(abs((h-G+180)%360-180), c, k) for h,k,c in acc]
n=len(pts); sx=sum(p[0] for p in pts); sy=sum(p[1] for p in pts)
sxx=sum(p[0]**2 for p in pts); sxy=sum(p[0]*p[1] for p in pts)
B=(n*sxy-sx*sy)/(n*sxx-sx*sx); Aa=(sy-B*sx)/n
mx=sx/n; my=sy/n
r=sum((p[0]-mx)*(p[1]-my) for p in pts)/math.sqrt(sum((p[0]-mx)**2 for p in pts)*sum((p[1]-my)**2 for p in pts))
for d,c,k in sorted(pts):
    print(f"  {k:9} d={d:5.0f}  C*={c:5.1f}   fit={Aa+B*d:5.1f}")
print(f"\n  C* = {Aa:.1f} + {B:.3f} * distance      r = {r:.3f}")
