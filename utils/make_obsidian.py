#!/usr/bin/env python3
"""Build Obsidian theme folders from schemes.json.

Obsidian has no single-extension model like VS Code: each theme is its own
folder under .obsidian/themes/<name>/ with a manifest.json and a theme.css,
and they show up together in Appearance -> Themes. So this generates one
folder per scheme, the same five as the other ports.

Obsidian is prose, like MarkText, not code like VS Code -- a note is mostly
headings and paragraphs, so the same correction applies: a warm mid-chroma
accent that a code editor spends on numbers would otherwise sit on every
heading, and a drained warm hue reads as skin rather than restraint. Moved
to the coolest hue clear of the rest, same as the MarkText port.
"""
import pathlib, json, re, math
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
exec(open(HERE / 'pal.py').read().split('# ---------- Solarized reference')[0])

def shade(hexv, dL):
    L, C, h = lab2lch(hex2lab(hexv))
    return lch2hex((max(0.0, min(100.0, L + dL)), C, h))[0]

# A flat -4 L* darkening clips to solid black once the ground itself is
# already near L*3 (Totality), which reads as a rendering error rather than
# a chrome layer. Scale the darkening by the ground's own headroom instead.
def darken_toward_black(hexv, dL):
    L = hex2lab(hexv)[0]
    return shade(hexv, -min(abs(dL), L * 0.45))

def alpha(hexv, a):
    return hexv + format(int(round(a * 255)), '02x')

def rgb_of(hexv):
    r, g, b = hex2rgb(hexv)
    return f'{r}, {g}, {b}'

def hex2hsl(hexv):
    r, g, b = (v / 255 for v in hex2rgb(hexv))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r: h = (g - b) / d + (6 if g < b else 0)
        elif mx == g: h = (b - r) / d + 2
        else: h = (r - g) / d + 4
        h *= 60
    return h, s * 100, l * 100

def hsl_triple(hexv):
    h, s, l = hex2hsl(hexv)
    return f'{h:.0f}, {s:.0f}%, {l:.0f}%'

def lab2hex_clamped(L, a, b):
    r, g, bl = xyz2rgb(lab2xyz((L, a, b)))
    rgb = [min(1, max(0, v)) for v in (r, g, bl)]
    return rgb2hex(*[round(v * 255) for v in rgb])

# Obsidian's neutral scale runs --color-base-00 (background) to --color-base-100
# (brightest text-like tone) at these eleven uneven steps. Rather than invent a
# fresh grey ramp, this walks the ramp already latent in the palette -- base03
# through base1 are already six points along the scheme's own hue, lightening
# in the same steps Solarized's are -- so plugins that reach for --color-base-60
# get a tone that belongs to the scheme instead of a generic grey.
BASE_STEPS = (0, 5, 10, 20, 25, 30, 35, 40, 50, 60, 70, 100)

def base_ramp(c):
    anchors = sorted((c['base03'], c['base02'], c['base01'],
                       c['base00'], c['base0'], c['base1']),
                      key=lambda h: hex2lab(h)[0])
    labs = [hex2lab(h) for h in anchors]
    L_lo, L_hi = labs[0][0], labs[-1][0]
    out = {}
    for s in BASE_STEPS:
        L = L_lo + (s / 100.0) * (L_hi - L_lo)
        lo_i = len(labs) - 2
        for i in range(len(labs) - 1):
            if labs[i][0] <= L <= labs[i + 1][0]:
                lo_i = i
                break
        L0, a0, b0 = labs[lo_i]
        L1, a1, b1 = labs[lo_i + 1]
        t = 0.0 if L1 == L0 else (L - L0) / (L1 - L0)
        out[s] = lab2hex_clamped(L, a0 + t * (a1 - a0), b0 + t * (b1 - b0))
    return out

# Same warm-corpse correction as the MarkText port: a drained warm hue in the
# 8-45 chroma band, 312-90 degrees off the wheel, reads as skin rather than
# restraint once it is dense on the page instead of sparse in code.
WARM = (312, 90)

def decorpse(colors, roles=('fn', 'str', 'meta', 'kw', 'num', 'ty', 'err', 'sp')):
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

# Only h1 carries an accent hue. A note is mostly headings, the densest,
# most-scanned structure on the screen, so colouring every level the way a
# code editor colours its (rare) token types would put the most colour where
# the "brightness carries the distinction, not hue" rule matters most. h2-h6
# separate by size and weight instead, all on the same bright neutral tone --
# same choice VS Code already makes for markdown inside a code file.
HEADING_ROLE = {1: 'str', 2: 'base1', 3: 'base1', 4: 'base1', 5: 'base1', 6: 'base1'}

# Obsidian's extended palette expects eight named hues; the schemes use six
# accents for eight roles (numbers share type names, errors share the
# preprocessor marker), so red=orange and yellow=pink land on the same value.
# That is the same "six accents, not eight" restraint as the other ports, not
# a bug in this generator.
EXTENDED = {'red': 'err', 'orange': 'sp', 'yellow': 'ty', 'green': 'kw',
            'cyan': 'str', 'blue': 'fn', 'purple': 'meta', 'pink': 'num'}

CALLOUT = {
    'default': 'base00', 'note': 'fn', 'abstract': 'str', 'summary': 'str', 'tldr': 'str',
    'info': 'fn', 'todo': 'fn', 'tip': 'str', 'hint': 'str', 'important': 'str',
    'success': 'kw', 'check': 'kw', 'done': 'kw',
    'question': 'ty', 'help': 'ty', 'faq': 'ty',
    'warning': 'sp', 'caution': 'sp', 'attention': 'sp',
    'failure': 'err', 'fail': 'err', 'missing': 'err',
    'danger': 'err', 'error': 'err', 'bug': 'err',
    'example': 'meta', 'quote': 'base01', 'cite': 'base01',
}

def build_vars(s):
    c = decorpse(s['colors'])
    ramp = base_ramp(c)
    bg, hl = c['base03'], c['base02']
    chrome = darken_toward_black(bg, 4.0)
    over = shade(bg, +3.2)
    accent = c['str']

    v = {}
    for step, hexv in ramp.items():
        v[f'--color-base-{step:02d}'] = hexv
    for name, role in EXTENDED.items():
        v[f'--color-{name}'] = c[role]
        v[f'--color-{name}-rgb'] = rgb_of(c[role])
    h, s_, l_ = hex2hsl(accent)
    v['--accent-h'] = f'{h:.0f}'
    v['--accent-s'] = f'{s_:.0f}%'
    v['--accent-l'] = f'{l_:.0f}%'
    v['--color-accent'] = accent
    v['--color-accent-1'] = accent
    v['--color-accent-2'] = shade(accent, +6)

    v.update({
        '--background-primary': bg,
        '--background-primary-alt': hl,
        '--background-secondary': chrome,
        '--background-secondary-alt': shade(chrome, +2.0),
        '--background-modifier-hover': alpha(c['base1'], .06),
        '--background-modifier-active-hover': alpha(c['base1'], .1),
        '--background-modifier-border': shade(hl, +6),
        '--background-modifier-border-hover': shade(hl, +10),
        '--background-modifier-border-focus': accent,
        '--background-modifier-error': alpha(c['err'], .2),
        '--background-modifier-error-hover': alpha(c['err'], .3),
        '--background-modifier-error-rgb': rgb_of(c['err']),
        '--background-modifier-success': alpha(c['kw'], .2),
        '--background-modifier-success-rgb': rgb_of(c['kw']),
        '--background-modifier-message': over,
        '--background-modifier-form-field': shade(bg, -1.0),

        '--text-normal': c['base0'],
        '--text-muted': c['base00'],
        '--text-faint': c['base01'],
        '--text-on-accent': bg,
        '--text-on-accent-inverted': c['base3'],
        '--text-success': c['kw'],
        '--text-warning': c['ty'],
        '--text-error': c['err'],
        '--text-accent': accent,
        '--text-accent-hover': shade(accent, +6),
        '--text-selection': alpha(accent, .25),
        '--text-highlight-bg': alpha(c['ty'], .35),
        '--caret-color': c['base1'],

        '--interactive-normal': over,
        '--interactive-hover': shade(over, +2.0),
        '--interactive-accent': accent,
        '--interactive-accent-hsl': hsl_triple(accent),
        '--interactive-accent-hover': shade(accent, +6),

        '--code-background': hl,
        '--code-normal': c['base0'],
        '--code-comment': c['base01'],
        '--code-function': c['fn'],
        '--code-important': c['err'],
        '--code-keyword': c['kw'],
        '--code-operator': c['base0'],
        '--code-property': c['ty'],
        '--code-punctuation': c['base00'],
        '--code-string': c['str'],
        '--code-tag': c['meta'],
        '--code-value': c['num'],

        '--heading-formatting': c['base01'],
        '--blockquote-background-color': 'transparent',
        '--blockquote-border-color': c['base01'],
        '--blockquote-color': c['base00'],

        '--link-color': accent,
        '--link-color-hover': shade(accent, +6),
        '--link-external-color': c['fn'],
        '--link-external-color-hover': shade(c['fn'], +6),
        '--link-unresolved-color': c['err'],

        '--tag-color': c['fn'],
        '--tag-color-hover': shade(c['fn'], +6),
        '--tag-background': alpha(c['fn'], .12),
        '--tag-background-hover': alpha(c['fn'], .2),
        '--tag-border-color': alpha(c['fn'], .3),
        '--tag-border-color-hover': alpha(c['fn'], .5),

        '--list-marker-color': c['base01'],
        '--list-marker-color-hover': accent,
        '--list-marker-color-collapsed': c['base01'],

        '--checkbox-color': accent,
        '--checkbox-color-hover': shade(accent, +6),
        '--checkbox-marker-color': bg,
        '--checkbox-border-color': c['base01'],
        '--checkbox-border-color-hover': c['base00'],
        '--checklist-done-color': c['base01'],

        '--table-background': bg,
        '--table-border-color': shade(hl, +6),
        '--table-header-background': chrome,
        '--table-header-background-hover': shade(chrome, +2.0),
        '--table-header-color': c['base1'],
        '--table-text-color': c['base0'],
        '--table-column-alt-background': alpha(c['base1'], .03),
        '--table-row-background-hover': alpha(c['base1'], .04),
        '--table-row-alt-background': alpha(c['base1'], .02),
        '--table-row-alt-background-hover': alpha(c['base1'], .05),
        '--table-selection': alpha(accent, .12),
        '--table-selection-border-color': accent,
        '--table-drag-handle-background': chrome,
        '--table-drag-handle-color': c['base00'],

        '--divider-color': shade(hl, +6),
        '--divider-color-hover': shade(hl, +10),

        '--scrollbar-bg': 'transparent',
        '--scrollbar-thumb-bg': alpha(c['base1'], .12),
        '--scrollbar-active-thumb-bg': alpha(c['base1'], .2),

        '--titlebar-background': chrome,
        '--titlebar-background-focused': chrome,
        '--titlebar-text-color': c['base00'],
        '--titlebar-text-color-focused': c['base1'],

        '--ribbon-background': chrome,
        '--ribbon-background-collapsed': chrome,

        '--status-bar-background': chrome,
        '--status-bar-border-color': shade(hl, +6),
        '--status-bar-text-color': c['base00'],

        '--tab-container-background': chrome,
        '--tab-background-active': bg,
        '--tab-text-color': c['base01'],
        '--tab-text-color-active': c['base1'],
        '--tab-text-color-focused': c['base01'],
        '--tab-text-color-focused-active': c['base1'],
        '--tab-text-color-focused-highlighted': c['base1'],
        '--tab-text-color-focused-active-current': c['base1'],

        '--nav-item-color': c['base00'],
        '--nav-item-color-hover': c['base1'],
        '--nav-item-color-active': c['base1'],
        '--nav-item-color-selected': c['base1'],
        '--nav-item-background-hover': alpha(c['base1'], .06),
        '--nav-item-background-active': alpha(accent, .14),
        '--nav-item-background-selected': alpha(accent, .14),
        '--nav-indentation-guide-color': shade(hl, +6),
        '--nav-collapse-icon-color': c['base01'],
        '--nav-collapse-icon-color-collapsed': c['base01'],
        '--nav-heading-color': c['base00'],
        '--nav-heading-color-hover': c['base1'],
    })

    for lvl, role in HEADING_ROLE.items():
        v[f'--h{lvl}-color'] = c[role]

    for name, role in CALLOUT.items():
        v[f'--callout-{name}'] = rgb_of(c[role])

    v['--h1-color'] = s.get('markdown_title', c['str'])
    if s['name'] == 'umbra':
        # Large selection surfaces stay neutral.
        selection = shade(hl, 4.0)
        for key in ('--nav-item-background-active', '--nav-item-background-selected',
                    '--text-selection', '--table-selection'):
            v[key] = selection
    return v

def render_css(s, v):
    lines = [
        f'/* Solar Eclipse {s["label"]} for Obsidian',
        ' * Dark only -- install alongside the other Solar Eclipse ports.',
        ' * Generated by utils/make_obsidian.py, do not edit by hand. */',
        '',
        '.theme-dark {',
    ]
    for k in sorted(v):
        lines.append(f'  {k}: {v[k]};')
    lines.append('}')
    lines.append('')
    return '\n'.join(lines)

def manifest(s):
    return {
        'name': f'Solar Eclipse {s["label"]}',
        'version': '1.0.0',
        'minAppVersion': '1.0.0',
        'author': 'Brandon Harvey',
    }

if __name__ == '__main__':
    out = ROOT / 'obsidian-colors-solar-eclipse'
    schemes = [s for s in json.load(open(ROOT / 'schemes.json')) if s['name'] != 'solarized']
    for s in schemes:
        name = f'Solar Eclipse {s["label"]}'
        theme_dir = out / name
        theme_dir.mkdir(parents=True, exist_ok=True)
        v = build_vars(s)
        (theme_dir / 'theme.css').write_text(render_css(s, v), encoding='utf-8')
        json.dump(manifest(s), open(theme_dir / 'manifest.json', 'w', encoding='utf-8'), indent=2)
        print(f'{name}: {len(v)} variables')
