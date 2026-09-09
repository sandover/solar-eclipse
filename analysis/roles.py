import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math
exec(open(_P).read().split('# ---------- Solarized reference')[0])
SOL={'green':'#859900','cyan':'#2aa198','blue':'#268bd2','yellow':'#b58900',
     'magenta':'#d33682','red':'#dc322f','orange':'#cb4b16','violet':'#6c71c4'}
ROLE={'green':'keywords','cyan':'strings','blue':'function names','yellow':'type names',
      'magenta':'numbers','red':'errors','orange':'preprocessor','violet':'special'}
FREQ={'blue':'everywhere','cyan':'everywhere','violet':'occasional','green':'common',
      'magenta':'occasional','yellow':'occasional','red':'rare','orange':'rare'}
G=lab2lch(hex2lab('#002b36'))[2]
rows=[]
for k,v in SOL.items():
    L,C,h=lab2lch(hex2lab(v))
    d=abs((h-G+180)%360-180)
    rows.append((d,k,L,C,h))
rows.sort()
print("How far each text colour sits from the background, nearest first:\n")
print(f"{'role':16}{'how often':13}{'distance':>9}{'vividness':>11}{'brightness':>12}")
for d,k,L,C,h in rows:
    print(f"{ROLE[k]:16}{FREQ[k]:13}{d:8.0f}{chr(176)}{C:11.0f}{L:12.0f}")
print("\nSigned offsets from the background (this is the shape to rebuild):")
print("  "+", ".join(f"{ROLE[k]}:{((h-G+180)%360-180):+.0f}" for d,k,L,C,h in rows))
