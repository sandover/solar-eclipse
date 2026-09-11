import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
import math, json
src=open(HERE / 'pal.py').read()
exec(src.split('# ---------- Solarized reference')[0])
exec(src.split('# ---------- OKLab')[1].split('\n',1)[1])

def okdE(a,b):
    L1,a1,b1=rgb2oklab(hex2rgb(a)); L2,a2,b2=rgb2oklab(hex2rgb(b))
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)

SOLACC={'fn':'#268bd2','str':'#2aa198','meta':'#6c71c4','kw':'#859900',
        'num':'#d33682','ty':'#b58900','err':'#dc322f','sp':'#cb4b16'}
ROLES=[('fn','function names','everywhere',36),('str','strings','everywhere',-42),
       ('meta','special','occasional',64),('kw','keywords','common',-119),
       ('num','numbers','occasional',125),('ty','type names','occasional',-146),
       ('err','errors','rare',164),('sp','preprocessor','rare',178)]
# how far each role sits from the background in Solarized -- the thing to hold constant
TARGET={k:okdE(SOLACC[k],'#002b36') for k,_,_,_ in ROLES}
ROLE_C={k:lab2lch(hex2lab(v))[1] for k,v in SOLACC.items()}   # Solarized's own chroma, per role
GREEN_DAMP=(95,140,0.85)   # his ear, not a law: greens have read loud three rounds running
LADDER=[('base03',11.5,14.5),('base02',16.5,15.6),('base01',45.0,9.2),('base00',50.2,9.3),
        ('base0',60.1,6.4),('base1',65.2,5.2),('base2',92.0,10.0),('base3',97.0,10.0)]
DRIFT={'base0':21,'base1':31}; PAPER=135; CEIL=0.85

def max_C(L,h):
    lo,hi=0.0,150.0
    for _ in range(30):
        mid=(lo+hi)/2
        r=xyz2rgb(lab2xyz(lch2lab((L,mid,h))))
        if all(-1e-4<=v<=1+1e-4 for v in r): lo=mid
        else: hi=mid
    return lo

def place(h, target, bg, role, cscale, Llo=49.0, Lhi=60.1):
    """Chroma is fixed by the role, the way Solarized fixes it. Lightness is the free
       variable, chosen so the colour lands the right distance from the background."""
    want=ROLE_C[role]*cscale
    glo,ghi,f=GREEN_DAMP
    if glo<=h<=ghi: want*=f
    best=(1e9,54.0,0.0,0.0)
    L=Llo
    while L<=Lhi+0.001:
        C=min(want, CEIL*max_C(L,h))
        hx,_=lch2hex((L,C,h))
        err=abs(okdE(hx,bg)-target)
        if err<best[0]: best=(err,L,C,okdE(hx,bg))
        L+=0.25
    return best[1],best[2],best[3]

MERGE={'nt':('num','ty'), 'ea':('err','sp')}
ROLES6=[('fn','function names','everywhere'),('str','strings','everywhere'),
        ('meta','special','occasional'),('kw','keywords','common'),
        ('nt','numbers and types','occasional'),('ea','errors and preprocessor','rare')]

GROUND_L={'ashen':7.5, 'nocturne':8.5, 'umbra':10.0, 'totality':3.0}
# how far the whole text ladder drops with the ground, per scheme. 6.0 is the
# most it can drop while body text stays inside the 4.75-5.7:1 he has lived with
# and comments stay above Solarized's own 2.79:1 floor.
LEVEL={'totality':6.0}
def universe(G,mirror=1,cm=1.0,swap=False,ban=None,six=False,gL=None,lvl=0.0):
    cols={}; meta={}
    gl=(G-mirror*PAPER)%360
    for k,L,C in LADDER:
        if gL is not None and k=='base03': L=gL
        elif gL is not None and k=='base02': L=gL+5.0
        elif lvl: L=max(2.0, L-lvl)
        if k in ('base2','base3'): h,c=gl,C
        elif k in DRIFT:           h,c=(G-mirror*DRIFT[k])%360, C*(1+(cm-1)*0.5)
        else:                      h,c=G, C*cm
        cols[k],_=lch2hex((L,c,h))
    bg=cols['base03']
    refbg,_=lch2hex((15.5 if gL is None else gL+4.0,
                     lab2lch(hex2lab(bg))[1], lab2lch(hex2lab(bg))[2]))
    gc=lab2lch(hex2lab(bg))[1]
    cscale=min(1.0,(gc/14.5)**0.5)
    OFF={k:o for k,_l,_f,o in ROLES}
    if swap: OFF['kw'],OFF['num']=OFF['num'],OFF['kw']
    HUE={}
    if ban or six:
        lo,hi = ban if ban else (None,None)
        def banned(x):
            if ban is None: return False
            return (lo<=x or x<=hi) if lo>hi else (lo<=x<=hi)
        ok=[x for x in range(360)
            if not banned(x) and abs((x-G+180)%360-180)>=30]
        runs=[];cur=[ok[0]]
        for x in ok[1:]:
            if x==cur[-1]+1: cur.append(x)
            else: runs.append(cur);cur=[x]
        runs.append(cur)
        if len(runs)>1 and runs[0][0]==0 and runs[-1][-1]==359:
            runs[0]=runs[-1]+runs[0]; runs.pop()
        nacc=len(ROLES6) if six else len(ROLES)
        total=sum(len(r) for r in runs); step=total/nacc; pos=step/2
        placed=[]
        for _ in range(nacc):
            acc=0
            for r in runs:
                if pos<acc+len(r): placed.append(r[int(pos-acc)]%360); break
                acc+=len(r)
            pos+=step
        # nearest hue to the ground takes the role Solarized keeps nearest, and so on
        placed.sort(key=lambda x: abs((x-G+180)%360-180))
        want=ROLES6 if six else ROLES
        rank=lambda r: (sum(abs(OFF[m]) for m in MERGE[r[0]])/2.0) if r[0] in MERGE else abs(OFF[r[0]])
        # keep each system's character: every role takes the free slot nearest
        # to where the unmerged ring would have put it
        free=list(placed[:len(want)])
        # strings is the one bright, saturated colour, so it decides the scheme's
        # character. He likes it blue (Nocturne 230, Ashen 190); put it there first.
        # ...unless the ground is itself blue, in which case anything but green:
        # a bright green standout is the thing he keeps objecting to.
        # The standout may sit at the ground's own hue. Tested: at brightness 68
        # against a ground at 12, hue distance from the ground changes separation
        # by 0.011 -- below noticing. Solarized's own body text is 21 deg off its
        # ground. Lightness does the separating, not hue.
        cand=free+[int(round(G))%360]
        notgreen=[x for x in cand if not (95<=x<=175)]
        pool=notgreen if notgreen else cand
        blue=min(pool,key=lambda x: abs((x-215+180)%360-180))
        HUE['str']=blue
        if blue in free: free.remove(blue)
        for r in sorted(want,key=rank):
            if r[0]=='str': continue
            off = OFF[MERGE[r[0]][0]] if r[0] in MERGE else OFF[r[0]]
            ideal=(G+mirror*off)%360
            best=min(free,key=lambda x: abs((x-ideal+180)%360-180))
            HUE[r[0]]=best; free.remove(best)
    gh=lab2lch(hex2lab(bg))[2]
    for row in (ROLES6 if six else ROLES):
        key=row[0]
        if key in MERGE:
            mem=MERGE[key]
            TARGET[key]=sum(TARGET[m] for m in mem)/len(mem)
            ROLE_C[key]=sum(ROLE_C[m] for m in mem)/len(mem)
        h=HUE.get(key, (G+mirror*OFF.get(key,0))%360)
        L,C,got=place(h,TARGET[key],refbg,key,cscale,49.0-lvl,60.1-lvl)
        hx,_=lch2hex((L,C,h))
        for slot in (MERGE[key] if key in MERGE else (key,)):
            cols[slot]=hx
            meta[slot]=dict(hue=round(h),dist=round(abs((h-gh+180)%360-180)),
                            L=round(L),C=round(C),reach=round(got,3),
                            used=round(C/max_C(L,h)*100),
                            merged=(row[1] if key in MERGE else ''))
    return cols,meta,round(gl)

SOL={'base03':'#002b36','base02':'#073642','base01':'#586e75','base00':'#657b83',
     'base0':'#839496','base1':'#93a1a1','base2':'#eee8d5','base3':'#fdf6e3'}
SOL.update(SOLACC)

SPECS=[
 ('solarized','Solarized Dark','control',230,1,1.00,0,'',
  'The original, unmodified. Lightest ground of the four, which is what separates it.',
  None,False,None),

 # Blend of Nocturne, Aubergine and Aubergine-no-green: they shared this ground
 # already, so the blend is a per-role pick -- no greens, the standout stays the
 # sky blue he tuned by hand, and the colour seen most is the quietest.
 ('nocturne','Nocturne','purple',262,1,1.10,1,'',
  'Violet. Sky blue is the one bright colour; everything else is nearly drained.',
  None,True,
  {'fn':'#85969e','str':'#55b2ce','meta':'#7a5955','kw':'#a08e77',
   'nt':'#5d8f85','ea':'#725d60'}),

 # Cove, Malachite and Verdigris all converged on the same palette, so they are
 # one scheme. Verdigris's ground, Cove's blue standout, Verdigris's orange in
 # place of Cove's pink, Malachite's violet in place of the green.
 ('verdigris','Verdigris','green',199,1,0.85,1,'',
  'Weathered copper. No green, no pink, no red.',
  None,True,
  {'fn':'#84939d','str':'#53b3c5','meta':'#546490','kw':'#9f9179',
   'nt':'#937668','ea':'#6d707e'}),

 ('ashen','Ashen','neutral',250,1,0.40,1,'',
  'Colour drained almost out, and the darkest of the four, so it recedes.',
  None,True,None),

 # Near-neutral charcoal with a trace of warmth, at the same lightness.
 ('umbra','Umbra','warm',65,1,0.12,1,'',
  'Warm charcoal: nearly neutral, with just a trace of brown.',
  (312,90),True,None),

 # The ground-hue plane is full: five schemes already tile it, and every new
 # position lands inside 0.03 of one of them, under the 0.05 where two grounds
 # read as clearly different. So this one separates on level instead. Ground at
 # L*3 and the whole text ladder down with it, which keeps the gentle contrast
 # rather than turning a black ground into a glare. Hue sits on the daylight
 # axis exactly, the most receding place there is -- which at this depth is the
 # point: it is the only ground in the set that reads as absence rather than
 # as a colour.
 ('totality','Totality','neutral',225,1,1.30,1,'',
  'One stop down from everything else: near-black, with the text dimmed to match so it never glares.',
  None,True,None),
]

prev={s['name']:s['colors'] for s in json.load(open(ROOT / 'schemes.json'))}
schemes=[]
for name,label,fam,G,mir,cm,fav,note,blurb,ban,six,picked in SPECS:
    if name=='solarized':
        cols=dict(SOL); meta={}
        for key,_l,_f,off in ROLES:
            L,C,h=lab2lch(hex2lab(SOL[key]))
            meta[key]=dict(hue=round(h),dist=abs(off),L=round(L),C=round(C),
                           reach=round(okdE(SOL[key],SOL['base03']),3),
                           used=round(C/max_C(L,h)*100), merged='')
        gl=round(lab2lch(hex2lab(SOL['base3']))[2])
    else:
        cols,meta,gl=universe(G,mir,cm,swap=(name=='nocturne'),ban=ban,six=six,
                              gL=GROUND_L.get(name),lvl=LEVEL.get(name,0.0))
    if picked:
        ent_picked=set()
        for slot,hx in picked.items():
            for m in (MERGE[slot] if slot in MERGE else (slot,)):
                ent_picked.add(m)
                cols[m]=hx
                L_,C_,h_=lab2lch(hex2lab(hx))
                meta[m]=dict(hue=round(h_),dist=round(abs((h_-lab2lch(hex2lab(cols['base03']))[2]+180)%360-180)),
                             L=round(L_),C=round(C_),reach=round(okdE(hx,cols['base03']),3),
                             used=round(C_/max_C(L_,h_)*100),
                             merged=('numbers and types' if slot=='nt' else
                                     'errors and preprocessor' if slot=='ea' else ''))
    gh=lab2lch(hex2lab(cols['base03']))[2]
    reach=[meta[k]['reach'] for k,_,_,_ in ROLES]
    schemes.append(dict(name=name,label=label,family=fam,fav=fav,
        picked=sorted(ent_picked) if picked else [],
        note=note.encode().decode('unicode_escape'),
        blurb=blurb.encode().decode('unicode_escape'),
        colors=cols,prev=prev.get(name,cols),roles=meta,ground=round(gh),paper=gl,mirror=mir,
        clear=round(min(abs((lab2lch(hex2lab(cols[k]))[2]-gh+180)%360-180) for k,_,_,_ in ROLES)),
        peak=max(m['used'] for m in meta.values()),
        far=round(max(reach),3), spreadr=round(max(reach)/min(reach),2),
        c_body=round(contrast(cols['base0'],cols['base03']),2),
        c_cmt=round(contrast(cols['base01'],cols['base03']),2)))

KEYS16=['base03','base02','base01','base00','base0','base1','base2','base3',
        'fn','str','meta','kw','num','ty','err','sp']
# Read back off the artifact after he called Nocturne restful. Per role rather than
# per frequency, because he treats the two "everywhere" roles oppositely: strings is
# the one bright, colourful thing on the page, function names is nearly grey.
SHAPE={'fn':(3.5,0.25), 'str':(8.0,1.00), 'meta':(-8.0,0.585), 'kw':(1.0,0.275),
       'num':(-4.5,0.5525), 'ty':(-4.5,0.5525), 'err':(-9.5,0.14), 'sp':(-9.5,0.14)}
FAVS=set()
# Warm hues are the only ones a screen lets run to chroma 90+, so whatever lands
# there arrives loud. He reads anything saturated between rose and terracotta as
# "too red". Cap it; his own favourites already sit at 11 and 18, so they don't move.
WARM=(312,80); WARM_CAP=15.0
def iswarm(h): return h>=WARM[0] or h<=WARM[1]

# Text tuning is independent of ground saturation. L*, chroma, hue:
# keep ordinary text neutral; spend colour on distinct syntax roles.
TEXT_LCH = {'nocturne': {'base0': (60, 4, 240),
              'base1': (65, 3, 240),
              'fn': (59, 12, 245),
              'str': (62, 27, 225),
              'kw': (59, 23, 85),
              'num': (56, 24, 165),
              'ty': (56, 24, 165),
              'meta': (53, 23, 310),
              'err': (54, 16, 355),
              'sp': (54, 16, 355)},
 'verdigris': {'base0': (60, 3, 190),
               'base1': (65, 3, 190),
               'fn': (59, 14, 260),
               'str': (61, 27, 235),
               'kw': (59, 19, 205),
               'num': (56, 20, 255),
               'ty': (56, 20, 255),
               'meta': (54, 18, 265),
               'err': (55, 21, 250),
               'sp': (55, 21, 250)},
 'ashen': {'base0': (64, 3, 250),
           'base1': (69, 3, 250),
           'fn': (62, 10, 230),
           'str': (64, 22, 200),
           'kw': (62, 16, 215),
           'num': (59, 18, 195),
           'ty': (59, 18, 195),
           'meta': (57, 12, 235),
           'err': (59, 19, 245),
           'sp': (59, 19, 245)},
 'umbra': {'base0': (65, 2, 95),
           'base1': (70, 2, 95),
           'fn': (62, 10, 240),
           'str': (65, 22, 235),
           'kw': (63, 16, 255),
           'num': (60, 17, 225),
           'ty': (60, 17, 225),
           'meta': (58, 12, 250),
           'err': (61, 20, 260),
           'sp': (61, 20, 260)},
 'totality': {'base0': (55, 4, 225),
              'base1': (60, 4, 225),
              'fn': (54, 16, 265),
              'str': (56, 25, 220),
              'kw': (54, 22, 115),
              'num': (52, 23, 335),
              'ty': (52, 23, 335),
              'meta': (50, 25, 295),
              'err': (50, 25, 40),
              'sp': (50, 25, 40)}}

for s in schemes:
    if s['name']=='solarized': continue          # the control stays untouched
    for k,_l,_f,_o in ROLES:
        if k in s.get('picked',[]): continue     # hand-picked colours are final
        dl,cs=SHAPE[k]
        L,C,h=lab2lch(hex2lab(s['colors'][k]))
        C=C*cs
        if iswarm(h): C=min(C, WARM_CAP)
        s['colors'][k],_=lch2hex((L+dl, C, h))
    for k, lch in TEXT_LCH.get(s['name'], {}).items():
        s['colors'][k], _ = lch2hex(lch)
    # Recompute diagnostics from the final colours, after all text tuning.
    bg = s['colors']['base03']
    gh = lab2lch(hex2lab(bg))[2]
    for k, _, _, _ in ROLES:
        L, C, h = lab2lch(hex2lab(s['colors'][k]))
        s['roles'][k].update(hue=round(h), dist=round(abs((h-gh+180)%360-180)),
            L=round(L), C=round(C), reach=round(okdE(s['colors'][k], bg), 3),
            used=round(C/max_C(L, h)*100))
    reaches = [m['reach'] for m in s['roles'].values()]
    s['far'] = round(max(reaches), 3)
    s['spreadr'] = round(max(reaches)/min(reaches), 2)
    s['peak'] = max(m['used'] for m in s['roles'].values())
    s['c_body'] = round(contrast(s['colors']['base0'], bg), 2)
    s['c_cmt'] = round(contrast(s['colors']['base01'], bg), 2)
    # starting point for every colour, so the page can recompute it live
    s['lch']={k:[round(v,2) for v in lab2lch(hex2lab(s['colors'][k]))] for k in KEYS16}
    for junk in ('tune','btune','tdef'):
        s.pop(junk,None)

def dE(a,b):
    L1,a1,b1=hex2lab(a); L2,a2,b2=hex2lab(b)
    return math.sqrt((L1-L2)**2+(a1-a2)**2+(b1-b2)**2)
ref=schemes[0]['colors']['base03']
for s in schemes:
    s['dE']=round(dE(s['colors']['base03'],ref),1)
    s['pair']={t['name']:round(dE(s['colors']['base03'],t['colors']['base03']),1) for t in schemes}
json.dump(schemes,open(ROOT / str(ROOT / 'schemes.json'),'w'),indent=1)

sol=schemes[0]
print(f"Solarized's furthest accent from its own background: {sol['far']:.3f}   spread {sol['spreadr']}x\n")
print(f"{'system':12}{'furthest':>10}{'spread':>8}{'over?':>8}   brightness of the rare colours")
for s in schemes:
    over='' if s['far']<=sol['far']+0.002 else 'OVER'
    Ls=[s['roles'][k]['L'] for k in ('err','sp','ty')]
    print(f"{s['label'][:11]:12}{s['far']:10.3f}{s['spreadr']:8.2f}{over:>8}   errors L{Ls[0]}  preproc L{Ls[1]}  types L{Ls[2]}")
print("\nWhat moved in your five (brightness, then colour):")
for s in schemes:
    if not s['fav']: continue
    print(f"  {s['label']}")
    for k in ('err','sp','ty'):
        L0,C0,_=lab2lch(hex2lab(s['prev'][k])); L1,C1,_=lab2lch(hex2lab(s['colors'][k]))
        print(f"    {k:5}{s['prev'][k]}  L{L0:.0f} C{C0:.0f}   ->   {s['colors'][k]}  L{L1:.0f} C{C1:.0f}")
print(f"\nUnchanged: contrast {min(s['c_body'] for s in schemes)}-{max(s['c_body'] for s in schemes)}"
      f"   comments {min(s['c_cmt'] for s in schemes)}-{max(s['c_cmt'] for s in schemes)}"
      f"   clear space {min(s['clear'] for s in schemes)}-{max(s['clear'] for s in schemes)} deg")
