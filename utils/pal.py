import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
import math, json

# ---------- sRGB <-> CIELAB (D65) ----------
WP = (0.95047, 1.00000, 1.08883)

def s2l(c):
    c = c/255.0
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def l2s(c):
    c = 12.92*c if c <= 0.0031308 else 1.055*(c**(1/2.4)) - 0.055
    return c

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def rgb2hex(r,g,b):
    return '#%02x%02x%02x' % (r,g,b)

def rgb2xyz(rgb):
    r,g,b = [s2l(v) for v in rgb]
    x = r*0.4124564 + g*0.3575761 + b*0.1804375
    y = r*0.2126729 + g*0.7151522 + b*0.0721750
    z = r*0.0193339 + g*0.1191920 + b*0.9503041
    return (x,y,z)

def xyz2rgb(xyz):
    x,y,z = xyz
    r =  x*3.2404542 + y*-1.5371385 + z*-0.4985314
    g =  x*-0.9692660 + y*1.8760108 + z*0.0415560
    b =  x*0.0556434 + y*-0.2040259 + z*1.0572252
    return (l2s(r), l2s(g), l2s(b))

def f(t):
    return t**(1/3) if t > 216/24389 else (841/108)*t + 4/29

def finv(t):
    return t**3 if t**3 > 216/24389 else (t - 4/29)*108/841

def xyz2lab(xyz):
    x,y,z = [xyz[i]/WP[i] for i in range(3)]
    fx,fy,fz = f(x),f(y),f(z)
    return (116*fy-16, 500*(fx-fy), 200*(fy-fz))

def lab2xyz(lab):
    L,a,b = lab
    fy = (L+16)/116
    fx = fy + a/500
    fz = fy - b/200
    return tuple(finv(v)*WP[i] for i,v in enumerate((fx,fy,fz)))

def hex2lab(h): return xyz2lab(rgb2xyz(hex2rgb(h)))

def lab2lch(lab):
    L,a,b = lab
    return (L, math.hypot(a,b), math.degrees(math.atan2(b,a)) % 360)

def lch2lab(lch):
    L,C,h = lch
    r = math.radians(h)
    return (L, C*math.cos(r), C*math.sin(r))

def in_gamut(rgb, eps=1e-4):
    return all(-eps <= v <= 1+eps for v in rgb)

def lch2hex(lch):
    """Convert LCh to hex, reducing chroma until in sRGB gamut."""
    L,C,h = lch
    lo, hi = 0.0, C
    if in_gamut(xyz2rgb(lab2xyz(lch2lab(lch)))):
        best = C
    else:
        for _ in range(40):
            mid = (lo+hi)/2
            if in_gamut(xyz2rgb(lab2xyz(lch2lab((L,mid,h))))):
                lo = mid
            else:
                hi = mid
        best = lo
    rgb = xyz2rgb(lab2xyz(lch2lab((L,best,h))))
    rgb = [min(1,max(0,v)) for v in rgb]
    return rgb2hex(*[round(v*255) for v in rgb]), best

def rel_lum(h):
    return rgb2xyz(hex2rgb(h))[1]

def contrast(a,b):
    la,lb = rel_lum(a), rel_lum(b)
    if la < lb: la,lb = lb,la
    return (la+0.05)/(lb+0.05)

# ---------- Solarized reference ----------
SOL = {
 'base03':'#002b36','base02':'#073642','base01':'#586e75','base00':'#657b83',
 'base0':'#839496','base1':'#93a1a1','base2':'#eee8d5','base3':'#fdf6e3',
 'yellow':'#b58900','orange':'#cb4b16','red':'#dc322f','magenta':'#d33682',
 'violet':'#6c71c4','blue':'#268bd2','cyan':'#2aa198','green':'#859900',
}
print(f"{'name':9} {'hex':9} {'L*':>6} {'a*':>6} {'b*':>6} {'C*':>6} {'h':>6}")
for k,v in SOL.items():
    L,a,b = hex2lab(v); _,C,h = lab2lch((L,a,b))
    print(f"{k:9} {v:9} {L:6.1f} {a:6.1f} {b:6.1f} {C:6.1f} {h:6.1f}")
print()
print("body text contrast  base0 on base03:", round(contrast(SOL['base0'],SOL['base03']),2))
print("emph  text contrast  base1 on base02:", round(contrast(SOL['base1'],SOL['base02']),2))
print("comment contrast    base01 on base03:", round(contrast(SOL['base01'],SOL['base03']),2))

# ---------- OKLab (Ottosson) : chroma is far more uniform across hues than CIELAB ----------
def rgb2oklab(rgb):
    r,g,b = [s2l(v) for v in rgb]
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_,m_,s_ = l**(1/3), m**(1/3), s**(1/3)
    return (0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
            1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
            0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_)
def hex2oklch(h):
    L,a,b = rgb2oklab(hex2rgb(h))
    return (L, math.hypot(a,b), math.degrees(math.atan2(b,a)) % 360)
