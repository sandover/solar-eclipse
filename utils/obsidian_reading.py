from markdown_design import prose

"""Reading colors and layout for Obsidian, independent of code token roles."""

# Apply before deriving surfaces so controls and neutral ramps stay consistent.
# These adjustments belong to Obsidian; shared editor palettes stay unchanged.
BASE_COLORS = {
    # Smoky plum-gray gives the reading surface a hue beyond neutral charcoal.
    'umbra': {'base03': '#25222c', 'base02': '#302c38',
              'base01': '#6e6b78', 'base00': '#7c7886',
              'base0': '#9e9da1', 'base1': '#aba9ae'},
    'ashen': {'base0': '#8f9598', 'base1': '#9da4a7'},
    'nocturne': {'base03': '#0c1b28', 'base02': '#162735'},
    'totality': {'base03': '#0a1418', 'base02': '#142126'},
}

# Umbra's slate surround counterbalances the warmer reading surface.
SURROUNDS = {'umbra': '#191e28'}

# Each palette assigns color by its visible job.
PALETTES = {
    'verdigris': dict(heading='#b3beb3', minor='#a3b5b3', accent='#87b0c3',
                      detail='#aaa58d', warm='#c1af83', success='#91b3a2'),
    'umbra': dict(heading='#a2b9c5', minor='#adb2b8', accent='#8fabb3',
                  detail='#b2a3bd', warm='#b7a689', success='#91ac96'),
    'nocturne': dict(heading='#9caeb9', minor='#9ca6b0', accent='#829da9',
                     detail='#a397ad', warm='#b2a283', success='#879f94'),
    'ashen': dict(heading='#a1afb7', minor='#a0aaae', accent='#899fa7',
                  detail='#a0aca4', warm='#b2a38a', success='#8fa397'),
    'totality': dict(heading='#8e9fa7', minor='#89969c', accent='#7c939d',
                     detail='#928da2', warm='#a5967b', success='#80988b'),
}

# H1 through H6. Color families mark structure; lightness stays restrained.
# H3/H4 share a hue, as do H5/H6, rather than assigning six competing accents.
HEADINGS = {
    'umbra': ('#b7b3bb', '#a2b9c5', '#b0a5bb', '#a99ab1', '#aaa8af', '#aaa8af'),
    'verdigris': ('#b3beb3', '#98b3c1', '#b3ab93', '#aaa58d', '#9fada8', '#9fada8'),
    'ashen': ('#b0aca3', '#9daeba', '#a2aca0', '#98a68f', '#9fa6a6', '#9fa6a6'),
    'nocturne': ('#b3b4b5', '#8eafc2', '#aba4bd', '#a49ab5', '#a0a5ad', '#a0a5ad'),
    'totality': ('#a3a196', '#8e9fa7', '#9e93a5', '#958ba0', '#909a99', '#909a99'),
}


def reading_vars(name, colors, alpha, shade):
    """Return the reading overrides for a named theme."""
    r = prose(name, colors)
    p = PALETTES.get(name, dict(heading=r['h1'], minor=r['h3'],
                              accent=r['link'], detail=r['marker'],
                              warm=r['warning'], success=r['success']))
    accent, heading = p['accent'], p['heading']
    body, bg = colors['base0'], colors['base03']
    warning, error = p['warm'], '#be8d85'
    rgb = lambda color: ', '.join(str(int(color[i:i + 2], 16)) for i in (1, 3, 5))
    v = {
        '--h1-color': heading, '--h2-color': heading,
        '--h3-color': p['minor'], '--h4-color': p['minor'],
        '--h5-color': body, '--h6-color': body,
        '--inline-title-color': heading,
        '--h1-size': '1.75em', '--h2-size': '1.4em', '--h3-size': '1.18em',
        '--h4-size': '1.08em', '--h5-size': '1em', '--h6-size': '1em',
        '--h1-weight': '650', '--h2-weight': '600', '--h3-weight': '600',
        '--h4-weight': '600', '--h5-weight': '600', '--h6-weight': '600',
        '--h1-line-height': '1.25', '--h2-line-height': '1.3',
        '--heading-spacing': '1.65em',
        '--line-height-normal': '1.6', '--p-spacing': '1.05rem',
        '--list-spacing': '0.22em', '--file-line-width': '740px',
        '--bold-color': colors['base1'], '--bold-weight': '600',
        '--italic-color': p['minor'],
        '--link-color': accent, '--link-external-color': accent,
        '--link-color-hover': heading, '--link-external-color-hover': heading,
        '--link-unresolved-color': p['detail'],
        '--link-decoration-thickness': '1px',
        '--text-accent': accent, '--text-accent-hover': heading,
        '--color-accent': accent, '--color-accent-1': accent,
        '--color-accent-2': heading,
        '--interactive-accent': accent, '--interactive-accent-hover': heading,
        '--background-modifier-border-focus': accent,
        '--text-selection': alpha(accent, .25),
        '--text-highlight-bg': alpha(p['warm'], .23),
        '--list-marker-color': alpha(accent, .7),
        '--list-marker-color-collapsed': p['detail'],
        '--list-marker-color-hover': heading,
        '--indentation-guide-color': alpha(accent, .16),
        '--indentation-guide-color-active': alpha(accent, .38),
        '--blockquote-color': p['minor'],
        '--blockquote-border-color': alpha(p['detail'], .65),
        '--blockquote-background-color': alpha(p['detail'], .04),
        '--blockquote-border-thickness': '2px',
        '--callout-radius': '6px', '--callout-border-width': '1px',
        '--callout-border-opacity': '.18', '--callout-blend-mode': 'normal',
        '--tag-color': p['detail'], '--tag-color-hover': heading,
        '--tag-background': alpha(p['detail'], .08),
        '--tag-background-hover': alpha(p['detail'], .15),
        '--tag-border-color': alpha(p['detail'], .2),
        '--tag-border-color-hover': alpha(p['detail'], .35),
        '--tag-radius': '4px', '--tag-size': '.85em',
        '--checkbox-color': p['success'], '--checkbox-color-hover': heading,
        '--checkbox-marker-color': bg,
        '--checklist-done-color': colors['base00'],
        '--nav-item-color': shade(colors['base00'], 5),
        '--nav-item-color-active': heading, '--nav-item-color-selected': heading,
        '--nav-item-background-active': alpha(accent, .12),
        '--nav-item-background-selected': alpha(accent, .12),
        '--nav-item-background-hover': alpha(accent, .06),
        '--nav-indentation-guide-color': alpha(accent, .12),
        '--tab-text-color-focused-active': heading,
        '--tab-text-color-focused-active-current': heading,
        '--tab-text-color-active': heading,
        '--table-header-color': p['minor'],
        '--table-header-background': alpha(accent, .06),
        '--table-selection': alpha(accent, .12),
        '--table-selection-border-color': accent,
        '--text-warning': warning, '--text-error': error,
        '--text-success': p['success'],
        '--background-modifier-error': alpha(error, .18),
        '--background-modifier-error-hover': alpha(error, .25),
        '--background-modifier-error-rgb': rgb(error),
        '--background-modifier-success': alpha(p['success'], .18),
        '--background-modifier-success-rgb': rgb(p['success']),
    }
    # Status colors retain their meaning independently of syntax palette names.
    for names, color in (
        (('default', 'note', 'info', 'todo', 'abstract', 'summary', 'tldr'), accent),
        (('tip', 'hint', 'important', 'example'), p['detail']),
        (('success', 'check', 'done'), p['success']),
        (('question', 'help', 'faq', 'warning', 'caution', 'attention'), warning),
        (('failure', 'fail', 'missing', 'danger', 'error', 'bug'), error),
        (('quote', 'cite'), p['minor']),
    ):
        for role in names:
            # Current Obsidian mixes CSS colors directly, not RGB triples.
            v[f'--callout-{role}'] = color
    v['--inline-title-color'] = r['h1']
    for level, color in enumerate(HEADINGS.get(name, tuple(r[f'h{n}'] for n in range(1,7))), start=1):
        v[f'--h{level}-color'] = color
    r = prose(name, colors)
    for key, role in {'inline-title-color':'h1', 'bold-color':'bold',
                      'italic-color':'italic', 'link-color':'link',
                      'link-external-color':'link', 'blockquote-color':'quote',
                      'blockquote-border-color':'marker', 'list-marker-color':'marker',
                      'code-normal':'inline', 'text-highlight-bg':'highlight',
                      'text-selection':'selection'}.items():
        v['--'+key] = r[role]
    for level in range(1, 7):
        v[f'--h{level}-color'] = r[f'h{level}']
    return v


READING_CSS = """
/* Give links a quiet underline without weakening their text contrast. */
.theme-dark .markdown-rendered a,
.theme-dark .cm-s-obsidian span.cm-link,
.theme-dark .cm-s-obsidian span.cm-url {
  text-underline-offset: 0.16em;
  text-decoration-color: color-mix(in srgb, currentColor 40%, transparent);
}
.theme-dark .markdown-rendered a:hover {
  text-decoration-color: currentColor;
}

/* Group complete thoughts; nested lists keep the tighter shared rhythm. */
.theme-dark .markdown-rendered :is(ul, ol):not(li > ul, li > ol) > li + li {
  margin-top: 0.48em;
}

/* A small location cue, visible even on a quiet selection background. */
.theme-dark .nav-file-title.is-active {
  box-shadow: inset 2px 0 var(--interactive-accent);
}
"""
