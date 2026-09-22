"""Starting points for the browser lab; never writes editor theme files."""
from make_vscode import theme_schemes, build as vscode_build, calm, verdigris_colors, READING_BASES
from make_obsidian import darken_toward_black, shade, alpha
from obsidian_reading import BASE_COLORS, SURROUNDS, reading_vars
from markdown_design import prose
from solarized_reference import palette, reading_colors, green_palette


def roles(c):
    return {**c, 'surround': 'base02', 'border': 'base02',
            'h1': 'base1', 'h2': 'str', 'h3': 'fn', 'h4': 'fn',
            'h5': 'base1', 'h6': 'base1', 'link': 'fn', 'bold': 'base1',
            'italic': 'base1', 'inline': 'base1', 'quote': 'base01',
            'marker': 'base01', 'highlight': c['ty'] + '35',
            'selection': c['fn'] + '40', 'success': 'kw', 'warning': 'ty'}


def review_data(schemes):
    result = []
    for s in schemes:
        result.append(dict(id='shared-'+s['name'], label=s['label'], source='Shared palette',
                           colors=reading_colors(palette()) if s['name'] == 'solarized' else roles(s['colors'])))
    for s in theme_schemes(schemes):
        c = {**s['colors'], **READING_BASES.get(s['name'], {})}
        if s['name'] == 'verdigris':
            c = verdigris_colors(c)
        c = calm(c)
        r = roles(c)
        theme = vscode_build(s)
        r.update(surround=theme['colors']['sideBar.background'],
                 h1='heading1' if 'heading1' in c else 'base1',
                 h2='heading2' if 'heading2' in c else 'str')
        result.append(dict(id='vscode-'+s['name'], label=s['label'], source='VS Code', colors=r))
    for s in schemes:
        if s['name'] == 'solarized':
            continue
        c = {**s['colors'], **BASE_COLORS.get(s['name'], {})}
        v = reading_vars(s['name'], c, alpha, shade)
        r = roles(c)
        r['surround'] = SURROUNDS.get(s['name'], darken_toward_black(c['base03'], 4))
        for key, css in dict(h1='h1-color', h2='h2-color', h3='h3-color', h4='h4-color',
                             h5='h5-color', h6='h6-color', link='link-color', bold='bold-color',
                             italic='italic-color', quote='blockquote-color', marker='list-marker-color',
                             highlight='text-highlight-bg', selection='text-selection',
                             success='checkbox-color').items():
            r[key] = v['--'+css]
        result.append(dict(id='obsidian-'+s['name'], label=s['label'], source='Obsidian', colors=r))
    e = next(p for p in result if p['id'] == 'vscode-verdigris')
    result.append(dict(id='candidate-verdigris-e', label='Verdigris · E / brighter H3',
                       source='Candidate (not installed)', colors={**e['colors'],
                       'h1': '#6f9caf', 'h2': '#9a9071', 'h3': '#a3a39e'}))
    result.append(dict(id='candidate-solarized-green', label='Solarized Green',
                       source='Candidate (not installed)', colors=reading_colors(green_palette())))
    for profile in result:
        name = profile['id'].split('-', 1)[1]
        if name == 'verdigris-e':
            name = 'verdigris'
        profile['colors'].update(prose(name, profile['colors']))
        profile['revision'] = 'prose-2026-09'
        profile['description'] = 'Reading composition: continuous prose, cool titles, muted gold sections, mineral subheadings.'
    solarized = next(p for p in result if p['id'] == 'shared-solarized')
    solarized['label'] = 'Solarized Dark · Reading'
    solarized['description'] = ('Solarized’s original ground and body text, with a prose-specific palette: '
                              'muted blue titles, soft gold sections, quiet emphasis and continuous lists.')
    result.append(dict(id='reference-vscode-solarized',
                       label='Solarized Dark · VS Code reference', source='Reference only',
                       colors=reading_colors(palette()), reference=True,
                       description='Unchanged VS Code 1.138.0 Markdown token assignments, rendered for comparison.'))
    return result
