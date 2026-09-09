#!/usr/bin/env python3
"""Inline the generated palettes into the two HTML pages."""
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

build('tmpl.html', 'schemes.json', 'index.html', strip=('pair',))
build('howtmpl.html', 'refdata.json', 'how.html')
