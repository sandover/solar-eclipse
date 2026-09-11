#!/usr/bin/env python3
"""Translate MarkText's built-in Solarized Dark theme into one of ours.

MarkText has no theme directory, only a Custom CSS override. Its solarized-dark
theme sets 79 variables on :root, so re-colouring those covers the app chrome,
not just the editor. Every colour in that block is mapped to its nearest
Solarized palette entry and replaced by our counterpart, keeping whatever
lightness offset the original had -- so a button-hover shade stays a shade.
"""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
import json, re, sys, math
exec(open(HERE / 'pal.py').read().split('# ---------- Solarized reference')[0])

SOL = {'base03':'#002b36','base02':'#073642','base01':'#586e75','base00':'#657b83',
       'base0':'#839496','base1':'#93a1a1','base2':'#eee8d5','base3':'#fdf6e3',
       'kw':'#859900','str':'#2aa198','fn':'#268bd2','ty':'#b58900',
       'num':'#d33682','err':'#dc322f','sp':'#cb4b16','meta':'#6c71c4'}

def nearest(hexv):
    L, a, b = hex2lab(hexv)
    best, bk = 1e9, None
    for k, v in SOL.items():
        L2, a2, b2 = hex2lab(v)
        d = math.sqrt((L-L2)**2 + (a-a2)**2 + (b-b2)**2)
        if d < best:
            best, bk = d, k
    return bk

def translate(hexv, target):
    """Move a colour onto the target palette, preserving its lightness offset."""
    k = nearest(hexv)
    Ls, _, _ = hex2lab(SOL[k])
    Lc, _, _ = hex2lab(hexv)
    La, Ca, Ha = lab2lch(hex2lab(target[k]))
    out, _ = lch2hex((max(0.0, min(100.0, La + (Lc - Ls))), Ca, Ha))
    return out

def rgb_of(hexv):
    r, g, b = hex2rgb(hexv)
    return f'{r}, {g}, {b}'

def build(block, target):
    hex_re = re.compile(r'#[0-9a-fA-F]{6}\b')
    rgba_re = re.compile(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)')
    def do_hex(m):
        return translate(m.group(0).lower(), target)
    def do_rgba(m):
        r, g, b, al = m.group(1), m.group(2), m.group(3), m.group(4)
        src = '#%02x%02x%02x' % (int(r), int(g), int(b))
        return f'rgba({rgb_of(translate(src, target))}, {al})'
    out = rgba_re.sub(do_rgba, block)
    out = hex_re.sub(do_hex, out)
    return out

# MarkText's own assignments follow Solarized's roles, and our schemes move the
# hues around per role -- so a heading that was red becomes our dimmest colour.
# These are re-pointed by prominence instead: h1 brightest, h6 quietest.
# MarkText-only correction. A markdown document is mostly headings and prose,
# so a warm mid-chroma accent that a code editor would spend on numbers ends up
# on every h2 and h3 here -- and drained warm hues read as skin, not restraint.
# Each offending colour keeps its brightness and vividness and moves to the
# coolest hue that stays clear of the rest. The palette itself is untouched.
WARM = (312, 90)
def decorpse(colors, roles=('fn','str','meta','kw','num','ty','err','sp')):
    """Merged roles share a hex, so work per distinct colour and move them together."""
    c = dict(colors)
    groups = {}
    for k in roles:
        groups.setdefault(c[k], []).append(k)
    hues = [lab2lch(hex2lab(h))[2] for h in groups
            if not (lab2lch(hex2lab(h))[2] >= WARM[0] or lab2lch(hex2lab(h))[2] <= WARM[1])]
    for hexv, keys in list(groups.items()):
        L, C, h = lab2lch(hex2lab(hexv))
        warm = h >= WARM[0] or h <= WARM[1]
        if not (warm and 8 <= C <= 45):
            continue
        best, bh = -1, None
        for cand in range(95, 310, 5):
            d = min(abs((cand - x + 180) % 360 - 180) for x in hues) if hues else 180
            if d > best:
                best, bh = d, cand
        moved, _ = lch2hex((L, C, bh))
        for k in keys:
            c[k] = moved
        hues.append(float(bh))
    return c

ROLE_OVERRIDE = {
    '--themeColor': 'str', '--linkColor': 'str', '--focusColor': 'str',
    '--headingColor': 'base1', '--strongColor': 'base1',
    '--h1Color': 'str',  '--h2Color': 'num', '--h3Color': 'kw',
    '--h4Color': 'meta', '--h5Color': 'fn',  '--h6Color': 'err',
    '--emColor': 'num', '--listMarkerColor': 'num', '--deleteColor': 'meta',
    '--blockquoteBorderColor': 'base01',
}

# Prism's token colours are hardcoded hexes in the bundle, not variables, so
# fenced code blocks need their own rules or they keep Solarized's palette.
PRISM = [
    ('comment,.token.block-comment,.token.prolog,.token.doctype,.token.cdata', 'base01'),
    ('punctuation', 'base00'),
    ('keyword,.token.atrule,.token.important', 'kw'),
    ('string,.token.char,.token.attr-value,.token.regex', 'str'),
    ('function,.token.function-name,.token.selector', 'fn'),
    ('number,.token.boolean,.token.constant,.token.symbol', 'num'),
    ('class-name,.token.builtin,.token.tag,.token.attr-name,.token.property', 'ty'),
    ('operator,.token.variable,.token.entity,.token.url', 'base0'),
    ('deleted', 'err'),
    ('inserted', 'kw'),
]

def prism_rules(c):
    out = ['', '/* fenced code blocks: Prism hardcodes these, so they are set here */',
           "code[class*='language-'], pre.ag-paragraph { color: %s; }" % c['base0'],
           # these two beat a plain .token.string on specificity, so they need saying
           ".language-css .token.string, .style .token.string { color: %s; }" % c['str']]
    for sel, role in PRISM:
        out.append('.token.%s { color: %s; background: none; }' % (sel, c[role]))
    return '\n'.join(out)


def shade(hexv, dL):
    L, C, H = lab2lch(hex2lab(hexv))
    return lch2hex((max(0.0, min(100.0, L + dL)), C, H))[0]


# The built-in theme sets these with literal hexes and no variable after them,
# so they survive the :root block and keep whatever base theme is selected
# showing through -- the title bar glyphs, the sidebar edge, the tab underline.
def leak_rules(c):
    edge = shade(c['base03'], -4.0)
    return '\n'.join([
        '', '/* the built-in theme hardcodes these, with no variable to override */',
        '.title-bar .frameless-titlebar-button > div > svg { fill: %s; }' % c['base0'],
        '.title-bar .frameless-titlebar-minimize:hover,',
        '.title-bar .frameless-titlebar-toggle:hover '
        '{ background-color: rgba(%s, 0.05); }' % rgb_of(c['base0']),
        '.side-bar { border-right: 1px solid %s !important; }' % edge,
        '.editor-tabs:after,',
        '.editor-tabs ul.tabs-container:after { border-bottom: 1px solid %s; }' % edge,
    ])


# The raw editor is CodeMirror, not Prism, and MarkText hands it the Railscasts
# theme for every dark scheme: a #2b2b2b box with red keywords and amber
# strings. None of it is a variable, so a code fence you are editing ignores
# the palette entirely until these are set.
CM = [
    ('', 'background: %(base02)s; color: %(base0)s;'),
    (' div.CodeMirror-selected', 'background: %(base01_dim)s !important;'),
    (' .CodeMirror-gutters', 'background: %(base02)s; border-right: 0;'),
    (' .CodeMirror-linenumber', 'color: %(base01)s;'),
    (' .CodeMirror-cursor', 'border-left: 1px solid %(base1)s !important;'),
    (' .CodeMirror-activeline-background', 'background: %(active)s;'),
    (' .CodeMirror-matchingbracket', 'text-decoration: underline; color: %(base1)s !important;'),
    (' span.cm-comment', 'color: %(base01)s;'),
    (' span.cm-atom', 'color: %(num)s;'),
    (' span.cm-number', 'color: %(num)s;'),
    (' span.cm-property, .cm-s-railscasts span.cm-attribute', 'color: %(ty)s;'),
    (' span.cm-keyword', 'color: %(kw)s;'),
    (' span.cm-string', 'color: %(str)s;'),
    (' span.cm-variable', 'color: %(base0)s;'),
    (' span.cm-variable-2', 'color: %(fn)s;'),
    (' span.cm-def', 'color: %(fn)s;'),
    (' span.cm-error', 'background: none; color: %(err)s;'),
    (' span.cm-bracket', 'color: %(base00)s;'),
    (' span.cm-tag', 'color: %(ty)s;'),
    (' span.cm-link', 'color: %(str)s;'),
]

def codemirror_rules(c):
    v = dict(c)
    v['active'] = shade(c['base02'], 2.0)
    v['base01_dim'] = shade(c['base02'], 4.0)
    out = ['', '/* the raw editor is CodeMirror, which MarkText still paints Railscasts */']
    for sel, body in CM:
        out.append('.cm-s-railscasts%s { %s }' % (sel, body % v))
    return '\n'.join(out)


if __name__ == '__main__':
    name = sys.argv[1]
    block = open(sys.argv[2] if len(sys.argv) > 2
                 else ROOT / 'marktext-colors-solar-eclipse' / '_base-vars.css',
                 encoding='utf-8').read()
    schemes = {s['name']: s for s in json.load(open(ROOT / 'schemes.json'))}
    s = schemes[name]
    palette = decorpse(s['colors'])
    css = build(block, palette)
    css = re.sub(r'/\*.*?\*/', '', css, count=1, flags=re.S)
    lines = []
    for l in css.splitlines():
        l = l.strip()
        if not l:
            continue
        var = l.split(':', 1)[0].strip()
        if var in ROLE_OVERRIDE:
            l = f"{var}: {palette[ROLE_OVERRIDE[var]]};"
        lines.append('  ' + l)
    body = (f"/* solar-eclipse-{name} for MarkText\n"
            f" * Paste into Preferences -> Theme -> Custom CSS.\n"
            f" * Overrides whichever built-in theme is selected. */\n"
            ":root {\n" + "\n".join(lines) + "\n}\n"
            + prism_rules(palette) + leak_rules(palette)
            + codemirror_rules(palette) + "\n")
    out = str(ROOT / 'marktext-colors-solar-eclipse' / f'Solar Eclipse {s["label"]}.css')
    open(out, 'w', encoding='utf-8').write(body)
    print(f'{out}: {len(body)} bytes, '
          f'{len(re.findall(r"--[a-zA-Z0-9]+\s*:", body))} variables')
