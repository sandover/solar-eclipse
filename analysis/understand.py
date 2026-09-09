import pathlib
_P = str(pathlib.Path(__file__).resolve().parent.parent / 'pal.py')
import math
src=open(_P).read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])
def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)
def maxC(L,h):
    lo,hi=0.,150.
    for _ in range(30):
        m=(lo+hi)/2
        if all(-1e-4<=v<=1+1e-4 for v in xyz2rgb(lab2xyz(lch2lab((L,m,h))))): lo=m
        else: hi=m
    return lo

B=['base03','base02','base01','base00','base0','base1','base2','base3']
S={'base03':'#002b36','base02':'#073642','base01':'#586e75','base00':'#657b83',
   'base0':'#839496','base1':'#93a1a1','base2':'#eee8d5','base3':'#fdf6e3',
   'yellow':'#b58900','orange':'#cb4b16','red':'#dc322f','magenta':'#d33682',
   'violet':'#6c71c4','blue':'#268bd2','cyan':'#2aa198','green':'#859900'}
A=['blue','cyan','violet','green','magenta','yellow','red','orange']
lch={k:lab2lch(hex2lab(v)) for k,v in S.items()}

print("="*78)
print("A. THE MONOTONE RAMP")
print("="*78)
print(f"{'tone':8}{'hex':9}{'L*':>6}{'C*':>6}{'hue':>7}   step to next")
for i,k in enumerate(B):
    L,C,h=lch[k]
    st=f"{lch[B[i+1]][0]-L:+.1f}" if i<7 else ""
    print(f"{k:8}{S[k]:9}{L:6.1f}{C:6.1f}{h:7.0f}   {st}")
print("\nInversion symmetry -- swap the ends and the steps must mirror:")
for a,b in (('base03','base3'),('base02','base2'),('base01','base1'),('base00','base0')):
    print(f"  {a:7}{lch[a][0]:5.1f}   <->  {b:6}{lch[b][0]:5.1f}     sum {lch[a][0]+lch[b][0]:6.1f}")
print(f"\n  dark  end steps: base03->base02 {lch['base02'][0]-lch['base03'][0]:+.1f}"
      f"   base01->base00 {lch['base00'][0]-lch['base01'][0]:+.1f}")
print(f"  light end steps: base3 ->base2  {lch['base2'][0]-lch['base3'][0]:+.1f}"
      f"   base1 ->base0  {lch['base0'][0]-lch['base1'][0]:+.1f}")
print(f"  middle gap base02->base01: {lch['base01'][0]-lch['base02'][0]:+.1f}  (the empty band)")
print(f"\n  hue: dark end {lch['base03'][2]:.0f} deg -> light end {lch['base3'][2]:.0f} deg"
      f"  ({(lch['base03'][2]-lch['base3'][2])%360:.0f} deg apart)")
print("  the ramp is NOT one hue: it crosses from cool to warm through near-neutral")

print("\n  The two working pairs, in each mode:")
for mode,bg,hl,body,emp in (('dark','base03','base02','base0','base1'),
                            ('light','base3','base2','base00','base01')):
    print(f"    {mode:6} body {bg}:{body} = {contrast(S[bg],S[body]):.2f}:1"
          f"   highlighted {hl}:{emp} = {contrast(S[hl],S[emp]):.2f}:1"
          f"   dL* {abs(lch[bg][0]-lch[body][0]):.1f} / {abs(lch[hl][0]-lch[emp][0]):.1f}")

print("\n"+"="*78)
print("B. THE ACCENTS -- and the constraint I never tested: they serve BOTH grounds")
print("="*78)
print(f"{'accent':9}{'hex':9}{'L*':>6}{'C*':>6}{'hue':>6}{'  on DARK':>12}{'on LIGHT':>10}"
      f"{'  dark dE':>10}{'light dE':>10}{'  balance':>10}")
dk,lt=[],[]
for k in A:
    L,C,h=lch[k]
    cd,cl=contrast(S[k],S['base03']),contrast(S[k],S['base3'])
    dd,dl=okdE(S[k],S['base03']),okdE(S[k],S['base3'])
    dk.append(dd); lt.append(dl)
    print(f"{k:9}{S[k]:9}{L:6.1f}{C:6.1f}{h:6.0f}{cd:12.2f}{cl:10.2f}{dd:10.3f}{dl:10.3f}{dd/dl:10.2f}")
print(f"\n  distance from DARK ground : {min(dk):.3f} to {max(dk):.3f}   spread {max(dk)/min(dk):.2f}x")
print(f"  distance from LIGHT ground: {min(lt):.3f} to {max(lt):.3f}   spread {max(lt)/min(lt):.2f}x")
comb=[(dk[i]+lt[i])/2 for i in range(8)]
print(f"  average of the two        : {min(comb):.3f} to {max(comb):.3f}   spread {max(comb)/min(comb):.2f}x")
print(f"  contrast on dark : {min(contrast(S[k],S['base03']) for k in A):.2f} to {max(contrast(S[k],S['base03']) for k in A):.2f}")
print(f"  contrast on light: {min(contrast(S[k],S['base3']) for k in A):.2f} to {max(contrast(S[k],S['base3']) for k in A):.2f}")
print(f"  body text contrast for reference: dark {contrast(S['base0'],S['base03']):.2f}"
      f"  light {contrast(S['base00'],S['base3']):.2f}")

print("\n  Lightness banding (the spec rounds these to 50 / 55 / 60):")
for band in (50,55,60):
    mem=[k for k in A if abs(round(lch[k][0]/5)*5-band)<0.1]
    print(f"    L*{band}: {', '.join(mem)}")
print("\n  Gamut restraint -- how much of the available colour each accent takes:")
for k in A:
    L,C,h=lch[k]; m=maxC(L,h)
    print(f"    {k:9}{C/m*100:5.0f}%")
