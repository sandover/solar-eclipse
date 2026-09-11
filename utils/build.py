#!/usr/bin/env python3
"""Inline the generated palettes into the two HTML pages."""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
import json
from html import escape

def build(template, data, out, strip=()):
    d = json.load(open(data, encoding='utf-8'))
    if strip and isinstance(d, list):
        for s in d:
            for k in strip:
                s.pop(k, None)
    t = open(template, encoding='utf-8').read()
    assert '__DATA__' in t, template + ' has no __DATA__ placeholder'
    open(out, 'w', encoding='utf-8').write(
        t.replace('__DATA__', json.dumps(d, separators=(',', ':'))))
    print(f'{out}: {len(open(out, encoding="utf-8").read())} bytes')

build(str(ROOT / 'tmpl.html'), str(ROOT / 'schemes.json'), str(ROOT / 'index.html'), strip=('pair',))
build(str(ROOT / 'howtmpl.html'), str(ROOT / 'refdata.json'), str(ROOT / 'how.html'))


def preview_svg():
    schemes = json.load(open(ROOT / 'schemes.json', encoding='utf-8'))
    width, card_w, card_h = 1200, 568, 246
    margin, gap = 28, 24
    rows = (len(schemes) + 1) // 2
    height = margin * 2 + rows * card_h + (rows - 1) * gap
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Solar Eclipse colour schemes</title>',
        '<desc id="desc">Six dark colour schemes shown as editor windows with neutral and accent colour ramps.</desc>',
        '<rect width="100%" height="100%" fill="#131417"/>',
    ]

    def text(value):
        return escape(str(value), quote=True)

    for i, scheme in enumerate(schemes):
        c = scheme['colors']
        b0 = c['base0']
        b01 = c['base01']
        x = margin + (i % 2) * (card_w + gap)
        y = margin + (i // 2) * (card_h + gap)
        parts += [
            f'<g transform="translate({x} {y})">',
            f'<rect width="{card_w}" height="{card_h}" rx="4" fill="{c["base03"]}" stroke="#3a3e47"/>',
            f'<text x="20" y="28" fill="{c["base1"]}" font-family="system-ui,sans-serif" font-size="18" font-weight="600">{text(scheme["label"])}</text>',
            f'<text x="{card_w - 20}" y="27" text-anchor="end" fill="{c["base01"]}" font-family="ui-monospace,monospace" font-size="11">{scheme["c_body"]:.2f}:1</text>',
            f'<rect x="20" y="46" width="{card_w - 40}" height="116" rx="2" fill="{c["base03"]}" stroke="{c["base02"]}"/>',
            f'<rect x="20" y="46" width="{card_w - 40}" height="22" fill="{c["base02"]}"/>',
            f'<circle cx="34" cy="57" r="4" fill="{c["err"]}"/><circle cx="47" cy="57" r="4" fill="{c["ty"]}"/><circle cx="60" cy="57" r="4" fill="{c["kw"]}"/>',
            f'<text x="76" y="61" fill="{c["base01"]}" font-family="ui-monospace,monospace" font-size="10">palette.ts</text>',
            f'<g font-family="ui-monospace,monospace" font-size="12">',
            f'<text x="34" y="88" fill="{b01}">01</text><text x="65" y="88" fill="{c["kw"]}">const</text><text x="107" y="88" fill="{b0}"> scheme = </text><text x="180" y="88" fill="{c["str"]}">"{text(scheme["name"])}"</text>',
            f'<text x="34" y="110" fill="{b01}">02</text><text x="65" y="110" fill="{c["kw"]}">return</text><text x="114" y="110" fill="{b0}"> contrast &gt; </text><text x="202" y="110" fill="{c["num"]}">4.75</text>',
            f'<text x="34" y="132" fill="{b01}">#</text><text x="65" y="132" fill="{scheme.get("markdown_title", c["str"])}" font-family="system-ui,sans-serif" font-size="14" font-weight="600">Palette notes</text>',
            '</g>',
            '<g transform="translate(20 177)">',
        ]
        for j, key in enumerate(('base03', 'base02', 'base01', 'base00', 'base0', 'base1', 'base2', 'base3')):
            parts.append(f'<rect x="{j * 66}" width="65" height="20" fill="{c[key]}"/>')
        parts.append('</g><g transform="translate(20 202)">')
        for j, key in enumerate(('fn', 'str', 'meta', 'kw', 'num', 'err', 'sp')):
            parts.append(f'<rect x="{j * 75}" width="74" height="20" fill="{c[key]}"/>')
        parts += ['</g></g>']

    parts.append('</svg>')
    out = ROOT / 'assets' / 'solar-eclipse-preview.svg'
    out.parent.mkdir(exist_ok=True)
    out.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    print(f'{out}: {out.stat().st_size} bytes')


preview_svg()


# The canonical table lives in the README, the way Solarized does it -- but
# generated from schemes.json rather than hand-maintained, so ports cannot drift.
def readme_table():
    import json
    NAME = {'base03':'background','base02':'highlight','base01':'comments',
            'base00':'faint text','base0':'body text','base1':'bright text',
            'base2':'pale','base3':'palest','fn':'function names','str':'strings',
            'meta':'special','kw':'keywords','num':'numbers','ty':'type names',
            'err':'errors','sp':'preprocessor'}
    ORDER = ['base03','base02','base01','base00','base0','base1','base2','base3',
             'fn','str','meta','kw','num','ty','err','sp']
    d = [s for s in json.load(open(ROOT / 'schemes.json')) if s['name'] != 'solarized']
    rows = ['| role | ' + ' | '.join(s['label'] for s in d) + ' |',
            '| --- | ' + ' | '.join('---' for _ in d) + ' |']
    for k in ORDER:
        rows.append(f'| {NAME[k]} | ' +
                    ' | '.join(f"`{s['colors'][k]}`" for s in d) + ' |')
    rows += ['', '| | ' + ' | '.join(s['label'] for s in d) + ' |',
             '| --- | ' + ' | '.join('---' for _ in d) + ' |',
             '| text contrast | ' + ' | '.join(f"{s['c_body']}:1" for s in d) + ' |']
    return '\n'.join(rows)

r = ROOT / 'README.md'
txt = r.read_text()
a, b = '<!-- palettes:start -->', '<!-- palettes:end -->'
if a in txt and b in txt:
    head, rest = txt.split(a, 1)
    _, tail = rest.split(b, 1)
    r.write_text(head + a + '\n\n' + readme_table() + '\n\n' + b + tail)
    print('README.md: palette table regenerated')
