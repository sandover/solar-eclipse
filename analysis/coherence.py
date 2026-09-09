import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)

SOL={'blue':'#268bd2','cyan':'#2aa198','violet':'#6c71c4','green':'#859900',
     'magenta':'#d33682','yellow':'#b58900','red':'#dc322f','orange':'#cb4b16'}
# what you get if you just pick eight colours off the wheel without thinking
NAIVE={'blue':'#0000ff','cyan':'#00ffff','violet':'#8000ff','green':'#00ff00',
       'magenta':'#ff00ff','yellow':'#ffff00','red':'#ff0000','orange':'#ff8000'}

def report(name,P,bg):
    Ls=[lab2lch(hex2lab(v))[0] for v in P.values()]
    Cs=[lab2lch(hex2lab(v))[1] for v in P.values()]
    ds=[okdE(v,bg) for v in P.values()]
    print(f"{name:22}{min(Ls):5.0f} to{max(Ls):4.0f}{max(Ls)-min(Ls):9.0f}"
          f"{max(ds)/min(ds):11.2f}x{max(Cs)/min(Cs):10.2f}x")

print("The three things a colour can vary. A palette coheres when only ONE of them does.\n")
print(f"{'palette':22}{'lightness span':>19}{'presence spread':>12}{'chroma spread':>13}")
report("Solarized accents",SOL,'#002b36')
report("Eight raw wheel hues",NAIVE,'#002b36')
print()
print("Lightness is the unifier. Solarized holds its eight accents inside an 11-point")
print("band; picking hues straight off the wheel spreads them over 65 points. Since")
print("lightness is what the eye uses to build shape and hierarchy, a wide spread reads")
print("as a jumble of different-importance things. Hue alone carries the distinctions.\n")

print("Where that 11-point band sits is not arbitrary either:")
for k,v in sorted(SOL.items(), key=lambda x: lab2lch(hex2lab(x[1]))[0]):
    L=lab2lch(hex2lab(v))[0]
    print(f"   {k:9}{L:6.1f}")
print(f"   {'base01':9}{45.0:6.1f}  <- comments, the dimmest text")
print(f"   {'base0':9}{60.1:6.1f}  <- body text, the brightest normal text")
print("\nEvery accent lands between those two. No coloured token is ever brighter than")
print("the prose it sits in, and none is dimmer than a comment. Colour changes what a")
print("token IS, never how loud it is.\n")

print("Second unifier: the ground and the text are tinted the SAME way, so everything")
print("shares one atmosphere. This is the part that stops a tinted background looking")
print("like a filter laid over neutral text:")
for k,v in (('base03','#002b36'),('base02','#073642'),('base01','#586e75'),
            ('base00','#657b83'),('base0','#839496'),('base1','#93a1a1')):
    L,C,h=lab2lch(hex2lab(v))
    print(f"   {k:8}{v}  L*{L:5.1f}  chroma{C:5.1f}  hue{h:5.0f}")
print("   every one of them tinted, none neutral, all within 31 degrees of hue")
