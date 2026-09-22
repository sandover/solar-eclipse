"""Complete prose assignments; code accents remain independent.

Keep continuous text steady. Spend cool and warm color on the outline and
small navigation cues, with pale mineral tones for subordinate headings.
"""
# title, section, subheading, link, detail: selected together on each ground.
FAMILIES = {
    'solarized': ('#819fab', '#a39774', '#a0aaa7', '#7da6a6', '#92977d'),
    'verdigris': ('#6f9caf', '#9a9071', '#a3a39e', '#7eaaa6', '#8f9279'),
    'nocturne': ('#8ba9ba', '#a69a7c', '#a7afb1', '#829fae', '#8e9b9d'),
    'ashen': ('#98aab2', '#a79d87', '#adb0ab', '#8da5a7', '#969f92'),
    'umbra': ('#9aadb8', '#b0a083', '#b4afb5', '#97aaa9', '#a39b91'),
    'umbra-b': ('#9eafb7', '#b1a587', '#b5b6aa', '#9caeaa', '#a1a48f'),
    'umbra-d': ('#96abb4', '#b2a180', '#bab5a9', '#94aaa6', '#a49c86'),
    'totality': ('#829da8', '#9c9177', '#9fa8a6', '#7e9d9e', '#899789'),
    'solarized-green': ('#819fa9', '#a19670', '#a0aaa2', '#7da59b', '#909777'),
}


def prose(name, colors):
    title, section, minor, link, detail = FAMILIES[name]
    return dict(h1=title, h2=section, h3=minor, h4=minor, h5=colors['base1'],
                h6=colors['base1'], link=link, bold=colors['base1'],
                italic=colors['base0'], inline=detail, quote=colors['base0'],
                marker=detail, highlight=section+'28', selection=link+'38',
                success=link, warning=section, border=colors['base02'])
