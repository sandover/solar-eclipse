#!/usr/bin/env python3
"""Inline the generated palettes into the two HTML pages."""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
import json

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
