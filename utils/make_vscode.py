#!/usr/bin/env python3
"""Build a VS Code colour-theme extension from schemes.json.

Unlike MarkText, VS Code installs real themes: a folder under ~/.vscode/extensions
with a package.json declaring them. One extension carries all schemes, so
they appear together in the theme picker.

The warm accent is left where it is here. In a markdown editor it lands on every
heading and reads as pallor; in a code editor it lands on numbers and constants,
which are sparse, so it reads as intended.
"""
import pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
exec(open(HERE / 'pal.py').read().split('# ---------- Solarized reference')[0])

def shade(hexv, dL):
    L, C, h = lab2lch(hex2lab(hexv))
    return lch2hex((max(0.0, min(100.0, L + dL)), C, h))[0]

def alpha(hexv, a):
    return hexv + format(int(round(a * 255)), '02x')

# In a code editor the token colours cover the screen, so the invariant that
# matters most is Solarized's: no coloured token brighter than the prose. Our
# shape deliberately breaks it for strings -- which is fine in a markdown file
# where strings are rare, and wrong in a JSON file where they are everything.
def calm(colors, roles=('fn','str','meta','kw','num','ty','err','sp')):
    c = dict(colors)
    bodyL = lab2lch(hex2lab(c['base0']))[0]
    seen = {}
    for k in roles:
        if c[k] in seen:
            c[k] = seen[c[k]]
            continue
        src = c[k]
        L, C, h = lab2lch(hex2lab(src))
        if L > bodyL or C > CHROMA_CAP:
            out, _ = lch2hex((min(L, bodyL), min(C, CHROMA_CAP), h))
            seen[src] = out
            c[k] = out
        else:
            seen[src] = src
    return c

CHROMA_CAP = 24.0

def verdigris_colors(colors):
    """Relate the reading scale and accents to the established green ground.

    CIELAB D65 / LCh: supporting neutrals follow the ground; body text moves
    toward a warmer near-neutral. Accent hues occupy a neighboring arc.
    Lightness stays near the body scale rather than increasing saturation
    and brightness together. This is a visual candidate, not a harmony proof.
    """
    c = dict(colors)
    ground_lightness, ground_chroma, ground_hue = lab2lch(hex2lab(c['base03']))
    roles = {
        'base02': (ground_lightness + 5, ground_chroma, 0),
        'base01': (45, 8, 0), 'base00': (50, 8, 0),
        'base1': (61, 8, -90),
        'base2': (74, 6, -35), 'base3': (80, 6, -35),
        'fn': (59, 14, 30), 'str': (60, 16, 0),
        'kw': (59, 16, -30), 'meta': (57, 16, -60),
        'num': (58, 22, -105), 'ty': (58, 18, -90),
        'err': (58, 22, -145), 'sp': (60, 22, -145),
        'bracket_olive': (59, 18, -70),
        'heading1': (65, 18, -30), 'heading2': (62, 12, 10),
    }
    # User-selected A1 is the exact reading reference. calm() brings syntax
    # lightness down with it; heading candidates remain a separate exploration.
    c['base0'] = '#878779'
    for role, (lightness, chroma, offset) in roles.items():
        c[role], used_chroma = lch2hex((lightness, chroma, (ground_hue + offset) % 360))
        if used_chroma < chroma - .01:
            raise ValueError(f'Verdigris {role} needs explicit gamut review')
    return c

def verdigris_workbench(c):
    """Extend the full workbench with roles that otherwise inherit vivid defaults."""
    v = workbench(c)
    v.pop('editorIndentGuide.activeIndentGuide1', None)
    bg, surface = c['base03'], c['base02']
    text, bright, dim = c['base0'], c['base1'], c['base00']
    accent, gold, error = c['str'], c['ty'], c['err']
    border, raised = shade(surface, 6), shade(bg, 3.2)
    v.update({
        'foreground': text, 'descriptionForeground': dim,
        'disabledForeground': c['base01'], 'icon.foreground': dim,
        'errorForeground': error, 'selection.background': alpha(accent, .25),
        'textPreformat.foreground': bright, 'textPreformat.background': surface,
        'editorIndentGuide.activeBackground1': c['base01'],
        'editorBracketHighlight.unexpectedBracket.foreground': error,
        'editorWarning.foreground': gold,
        'editorOverviewRuler.errorForeground': alpha(error, .7),
        'editorOverviewRuler.warningForeground': alpha(gold, .7),
        'editorOverviewRuler.infoForeground': alpha(accent, .7),
        'editorOverviewRuler.addedForeground': alpha(c['kw'], .7),
        'editorOverviewRuler.modifiedForeground': alpha(gold, .7),
        'editorOverviewRuler.deletedForeground': alpha(error, .7),
        'editorInlayHint.foreground': dim, 'editorInlayHint.background': surface,
        'editorCodeLens.foreground': dim, 'editorLink.activeForeground': bright,
        'editorLightBulb.foreground': gold,
        'editorLightBulbAutoFix.foreground': accent,
        'editorGhostText.foreground': c['base01'],
        'notifications.background': raised, 'notifications.foreground': text,
        'notifications.border': border, 'notificationCenterHeader.background': surface,
        'notificationsErrorIcon.foreground': error,
        'notificationsWarningIcon.foreground': gold,
        'notificationsInfoIcon.foreground': accent,
        'quickInput.background': raised, 'quickInput.foreground': text,
        'quickInputList.focusBackground': surface,
        'quickInputList.focusForeground': bright,
        'menu.selectionBackground': surface, 'menu.selectionForeground': bright,
        'menu.separatorBackground': border, 'menu.border': border,
        'button.secondaryBackground': surface, 'button.secondaryForeground': text,
        'button.secondaryHoverBackground': shade(surface, 3),
        'checkbox.background': surface, 'checkbox.foreground': accent,
        'checkbox.border': border,
        'inputValidation.errorBackground': alpha(error, .12),
        'inputValidation.errorBorder': error,
        'inputValidation.warningBackground': alpha(gold, .12),
        'inputValidation.warningBorder': gold,
        'inputValidation.infoBackground': alpha(accent, .12),
        'inputValidation.infoBorder': accent,
        'settings.headerForeground': bright,
        'settings.modifiedItemIndicator': gold,
        'settings.focusedRowBackground': alpha(accent, .05),
        'list.focusHighlightForeground': accent,
        'list.inactiveSelectionForeground': text,
        'list.hoverForeground': bright,
        'terminal.selectionBackground': alpha(accent, .22),
        'terminal.findMatchBackground': alpha(gold, .28),
        'terminal.findMatchHighlightBackground': alpha(gold, .12),
    })
    # Terminal labels are protocol names. Magenta uses olive here deliberately.
    for name, role in {'Red': 'err', 'Green': 'kw', 'Yellow': 'num',
                       'Blue': 'fn', 'Magenta': 'meta', 'Cyan': 'str',
                       'White': 'base0', 'Black': 'base02'}.items():
        v[f'terminal.ansi{name}'] = c[role]
        v[f'terminal.ansiBright{name}'] = c['base01'] if name == 'Black' else shade(c[role], 4)
    for level in range(1, 7):
        color = (c['num'], c['bracket_olive'], c['kw'])[(level - 1) % 3]
        v[f'editorBracketHighlight.foreground{level}'] = color
        v[f'editorBracketPairGuide.background{level}'] = alpha(color, .12)
        v[f'editorBracketPairGuide.activeBackground{level}'] = alpha(color, .30)
    return v

# VS Code-specific tuning keeps other app ports independent.
READING_BASES = {
    'nocturne': {'base03': '#0c1b28', 'base02': '#162735', 'str': '#829da9'},
    'ashen': {'base0': '#8f9598', 'base1': '#9da4a7', 'str': '#899fa7'},
    'totality': {'base03': '#0a1418', 'base02': '#142126', 'str': '#7c939d'},
    'umbra': {'base03': '#25222c', 'base02': '#302c38',
              'base0': '#9e9da1', 'base1': '#aba9ae', 'str': '#8fabb3'},
    'umbra-b': {'base03': '#2b282e', 'base02': '#353239',
                'base01': '#75766d', 'base00': '#898b80',
                'base0': '#a4a69b', 'base1': '#b1b3a8', 'str': '#8fa6a6'},
    'umbra-d': {'base03': '#292b2b', 'base02': '#333636',
                'base01': '#78746c', 'base00': '#8e887e',
                'base0': '#aaa499', 'base1': '#b7b1a6', 'str': '#8ba5ae'},
}

def theme_schemes(schemes):
    """Keep the original names and add the two selected Umbra candidates."""
    result = [s for s in schemes if s['name'] != 'solarized']
    umbra = next(s for s in result if s['name'] == 'umbra')
    return result + [{**umbra, 'name': f'umbra-{suffix.lower()}',
                      'label': f'Umbra {suffix}'} for suffix in ('B', 'D')]

def install_schemes(schemes):
    from solarized_reference import palette, green_palette
    return theme_schemes(schemes) + [
        dict(name='solarized', label='Solarized Dark Reading', colors=palette()),
        dict(name='solarized-green', label='Solarized Green', colors=green_palette())]


def workbench(c):
    bg, hl = c['base03'], c['base02']
    chrome = shade(bg, -min(4.0, hex2lab(bg)[0] * .45))
    over   = shade(bg, +3.2)          # popups and hovers sit above the page
    dim, txt, bright = c['base01'], c['base0'], c['base1']
    faint  = c['base00']
    accent = c['str']                 # the standout drives focus and badges
    return {
      "editor.background": bg, "editor.foreground": txt,
      "editorLineNumber.foreground": dim, "editorLineNumber.activeForeground": bright,
      "editor.lineHighlightBackground": hl,
      "editor.selectionBackground": shade(hl, +4), "editor.inactiveSelectionBackground": hl,
      "editor.selectionHighlightBackground": alpha(accent, .14),
      "editor.wordHighlightBackground": alpha(accent, .12),
      "editor.wordHighlightStrongBackground": alpha(accent, .18),
      "editor.findMatchBackground": alpha(accent, .34),
      "editor.findMatchHighlightBackground": alpha(accent, .18),
      "editorCursor.foreground": bright, "editorWhitespace.foreground": shade(hl, +6),
      "editorIndentGuide.background1": shade(hl, +3),
      "editorIndentGuide.activeIndentGuide1": dim,
      "editorRuler.foreground": hl, "editorBracketMatch.background": alpha(accent, .18),
      "editorBracketMatch.border": accent,
      "editorGutter.modifiedBackground": c['ty'], "editorGutter.addedBackground": c['kw'],
      "editorGutter.deletedBackground": c['err'],
      "editorError.foreground": c['err'], "editorWarning.foreground": c['ty'],
      "editorInfo.foreground": accent,
      "editorWidget.background": over, "editorWidget.border": shade(hl, +6),
      "editorSuggestWidget.selectedBackground": hl,
      "editorHoverWidget.background": over, "editorHoverWidget.border": shade(hl, +6),
      "peekViewEditor.background": shade(bg, -1),
      "peekViewResult.background": chrome,
      "diffEditor.insertedTextBackground": alpha(c['kw'], .12),
      "diffEditor.removedTextBackground": alpha(c['err'], .12),
      "sideBar.background": chrome, "sideBar.foreground": txt,
      "sideBar.border": shade(hl, +2),
      "sideBarSectionHeader.background": chrome, "sideBarSectionHeader.foreground": bright,
      "sideBarTitle.foreground": bright,
      "activityBar.background": chrome, "activityBar.foreground": bright,
      "activityBar.inactiveForeground": dim, "activityBar.border": shade(hl, +2),
      "activityBarBadge.background": accent, "activityBarBadge.foreground": bg,
      "statusBar.background": chrome, "statusBar.foreground": txt,
      "statusBar.border": shade(hl, +2),
      "statusBar.noFolderBackground": chrome,
      "statusBar.debuggingBackground": c['ty'], "statusBar.debuggingForeground": bg,
      "statusBarItem.remoteBackground": accent, "statusBarItem.remoteForeground": bg,
      "titleBar.activeBackground": chrome, "titleBar.activeForeground": txt,
      "titleBar.inactiveBackground": chrome, "titleBar.inactiveForeground": dim,
      "titleBar.border": shade(hl, +2),
      "tab.activeBackground": bg, "tab.activeForeground": bright,
      "tab.inactiveBackground": chrome, "tab.inactiveForeground": dim,
      "tab.border": shade(hl, +2), "tab.activeBorderTop": accent,
      "editorGroupHeader.tabsBackground": chrome,
      "editorGroupHeader.noTabsBackground": chrome,
      "editorGroup.border": shade(hl, +2),
      "panel.background": bg, "panel.border": shade(hl, +2),
      "panelTitle.activeForeground": bright, "panelTitle.inactiveForeground": dim,
      "terminal.background": bg, "terminal.foreground": txt,
      "terminalCursor.foreground": bright,
      "terminal.ansiBlack": hl, "terminal.ansiBrightBlack": dim,
      "terminal.ansiRed": c['err'], "terminal.ansiBrightRed": c['sp'],
      "terminal.ansiGreen": c['kw'], "terminal.ansiBrightGreen": faint,
      "terminal.ansiYellow": c['ty'], "terminal.ansiBrightYellow": txt,
      "terminal.ansiBlue": c['fn'], "terminal.ansiBrightBlue": bright,
      "terminal.ansiMagenta": c['meta'], "terminal.ansiBrightMagenta": c['num'],
      "terminal.ansiCyan": c['str'], "terminal.ansiBrightCyan": c['base2'],
      "terminal.ansiWhite": c['base2'], "terminal.ansiBrightWhite": c['base3'],
      "list.activeSelectionBackground": hl, "list.activeSelectionForeground": bright,
      "list.inactiveSelectionBackground": shade(chrome, +2),
      "list.hoverBackground": shade(chrome, +1.5),
      "list.highlightForeground": accent,
      "list.errorForeground": c['err'], "list.warningForeground": c['ty'],
      "input.background": shade(bg, -1), "input.foreground": txt,
      "input.border": shade(hl, +6), "input.placeholderForeground": dim,
      "inputOption.activeBorder": accent,
      "dropdown.background": over, "dropdown.border": shade(hl, +6),
      "badge.background": accent, "badge.foreground": bg,
      "button.background": accent, "button.foreground": bg,
      "button.hoverBackground": shade(accent, +5),
      "focusBorder": alpha(accent, .6),
      "scrollbarSlider.background": alpha(txt, .12),
      "scrollbarSlider.hoverBackground": alpha(txt, .2),
      "scrollbarSlider.activeBackground": alpha(txt, .3),
      "widget.shadow": "#00000060",
      "progressBar.background": accent,
      "breadcrumb.foreground": dim, "breadcrumb.focusForeground": bright,
      "menu.background": over, "menu.foreground": txt,
      "gitDecoration.modifiedResourceForeground": c['ty'],
      "gitDecoration.addedResourceForeground": c['kw'],
      "gitDecoration.deletedResourceForeground": c['err'],
      "gitDecoration.untrackedResourceForeground": c['meta'],
      "gitDecoration.ignoredResourceForeground": dim,
      "textLink.foreground": accent, "textLink.activeForeground": shade(accent, +6),
      "textBlockQuote.background": hl, "textBlockQuote.border": dim,
      "textCodeBlock.background": hl, "textSeparator.foreground": shade(hl, +6),
    }

def tokens(c, headings=None):
    h1, h2 = headings or (c['base1'], c['str'])
    def r(scope, fg=None, style=None):
        s = {"scope": scope, "settings": {}}
        if fg: s["settings"]["foreground"] = fg
        if style: s["settings"]["fontStyle"] = style
        return s
    return [
      r("comment, punctuation.definition.comment", c['base01'], "italic"),
      r("punctuation, meta.brace, punctuation.separator, punctuation.terminator", c['base00']),
      r("string, string.quoted, punctuation.definition.string", c['str']),
      r("string.regexp", c['str']),
      r("constant.numeric, constant.language, constant.character", c['num']),
      r("constant.other, support.constant", c['num']),
      r("keyword, keyword.control, keyword.operator.new, storage, storage.type, storage.modifier", c['kw']),
      r("keyword.operator", c['base0']),
      r("entity.name.function, support.function, meta.function-call.generic", c['fn']),
      r("entity.name.type, entity.name.class, support.type, support.class, entity.other.inherited-class", c['ty']),
      r("variable, variable.other, meta.definition.variable", c['base0']),
      r("variable.parameter", c['base0']),
      r("variable.language, variable.other.constant", c['num']),
      r("entity.name.tag, meta.tag", c['meta']),
      r("entity.other.attribute-name", c['ty']),
      r("meta.preprocessor, keyword.control.directive, meta.preprocessor.string", c['sp']),
      r("meta.decorator, punctuation.decorator, entity.name.function.decorator", c['meta']),
      r("invalid, invalid.illegal", c['err']),
      r("invalid.deprecated", c['err'], "italic"),
      # Neutral titles, quiet accent sections, and softer subheadings.
      r("markup.heading.1, markup.heading.1 entity.name", h1, "bold"),
      r("markup.heading, entity.name.section", c['base1'], "bold"),
      r("markup.heading.2, markup.heading.2 entity.name", h2, "bold"),
      r("markup.heading.3, markup.heading.3 entity.name, markup.heading.4, markup.heading.4 entity.name", c['fn'], "bold"),
      r("punctuation.definition.heading", c['base01']),
      r("markup.bold", c['base1'], "bold"),
      r("markup.italic", c['base1'], "italic"),
      r("markup.underline.link, string.other.link", c['fn']),
      r("markup.inline.raw, markup.raw.inline", c['base1']),
      r("punctuation.definition.raw", c['base01']),
      r("markup.fenced_code.block, markup.raw.block", c['base0']),
      r("markup.quote", c['base01'], "italic"),
      r("markup.list punctuation.definition.list, punctuation.definition.list.begin", c['base01']),
      r("markup.inserted", c['kw']),
      r("markup.deleted", c['err']),
      r("markup.changed", c['ty']),
      r("support.type.property-name, meta.object-literal.key", c['ty']),
      r("entity.name.namespace, entity.name.module", c['meta']),
    ]

def semantic(c):
    return {
      "function": c['fn'], "method": c['fn'],
      "class": c['ty'], "type": c['ty'], "interface": c['ty'], "enum": c['ty'],
      "string": c['str'], "number": c['num'], "keyword": c['kw'],
      "variable": c['base0'], "parameter": c['base0'],
      "property": c['ty'], "namespace": c['meta'],
      "*.declaration": {"fontStyle": ""},
    }

def build(s):
    colors = {**s['colors'], **READING_BASES.get(s['name'], {})}
    if s['name'] == 'verdigris':
        colors = verdigris_colors(colors)
    c = calm(colors)
    from markdown_design import prose
    r = prose(s['name'], c)
    ui = verdigris_workbench(c) if s['name'] == 'verdigris' else workbench(c)
    # Give links more separation from body text while retaining their hue.
    link_l, link_c, link_h = lab2lch(hex2lab(r['link']))
    link, _ = lch2hex((link_l + 3, link_c + 8, link_h))
    # The native rich Markdown editor reads these UI colors, not markup scopes.
    # It inherits body text for headings and emphasis and loads no preview CSS.
    ui.update({
        'textLink.foreground': link,
        'textLink.activeForeground': shade(link, +6),
        # Keep VS Code's warm yellow: the user prefers it for inline code.
        'textPreformat.foreground': '#d7ba7d',
        'textPreformat.background': c['base02'],
        'textBlockQuote.border': r['h2'],
        'textBlockQuote.background': alpha(r['h2'], .08),
        # The native editor further softens this shared heading/divider color.
        'textSeparator.foreground': alpha(link, .42),
        # Native Markdown uses this shared border around fenced code blocks.
        'widget.border': shade(c['base02'], +6),
    })
    markdown = [{"scope": scope, "settings": {"foreground": r[role]}}
                for scope, role in [(f"markup.heading.{n}, markup.heading.{n} entity.name", f'h{n}') for n in range(1,7)] + [
                    ('markup.bold', 'bold'), ('markup.italic', 'italic'),
                    ('markup.quote', 'quote'), ('markup.underline.link, string.other.link', 'link'),
                    ('markup.inline.raw, markup.raw.inline', 'inline'),
                    ('markup.list punctuation.definition.list, punctuation.definition.list.begin', 'marker')]]
    return {
      "$schema": "vscode://schemas/color-theme",
      "name": f"Solar Eclipse {s['label']}",
      "type": "dark",
      "semanticHighlighting": True,
      "colors": ui,
      "semanticTokenColors": semantic(c),
      "tokenColors": tokens(c, (c['heading1'], c['heading2']) if s['name'] == 'verdigris' else None) + markdown,
    }

if __name__ == '__main__':
    out = ROOT / 'vscode-colors-solar-eclipse'
    (out / 'themes').mkdir(parents=True, exist_ok=True)
    schemes = install_schemes(json.load(open(ROOT / 'schemes.json')))
    contributes = []
    for s in schemes:
        label = f"Solar Eclipse {s['label']}"
        path = f"themes/{label}-color-theme.json"
        json.dump(build(s), open(out / path, 'w', encoding='utf-8'),
                  indent=2, ensure_ascii=False)
        contributes.append({"label": label, "uiTheme": "vs-dark", "path": f"./{path}"})
        print(f"{path}: {len(build(s)['colors'])} workbench colours, "
              f"{len(build(s)['tokenColors'])} token rules")
    pkg = {
      "name": "solar-eclipse-themes",
      "displayName": "Solar Eclipse",
      "description": "Dark themes built from Solarized's measured structure.",
      "version": "1.0.0",
      "publisher": "local",
      "engines": {"vscode": "^1.70.0"},
      "categories": ["Themes"],
      "contributes": {"themes": contributes},
    }
    json.dump(pkg, open(out / 'package.json', 'w', encoding='utf-8'),
              indent=2, ensure_ascii=False)
    print("package.json:", ", ".join(t["label"] for t in contributes))
    # Keep embedded Markdown headings identical to the source-editor rules.
    css_path = out / 'markdown-editor.css'
    css = css_path.read_text()
    start = '/* Verdigris headings: generated by utils/make_vscode.py. */'
    end = '/* End Verdigris headings. */'
    before, rest = css.split(start, 1)
    _, after = rest.split(end, 1)
    from markdown_design import prose
    rules = []
    for scheme in schemes:
        c = {**scheme['colors'], **READING_BASES.get(scheme['name'], {})}
        if scheme['name'] == 'verdigris':
            c = verdigris_colors(c)
        r = prose(scheme['name'], c)
        selectors = {**{f'h{n}': f'h{n}' for n in range(1,7)},
                     'strong':'bold', 'em':'italic', 'a':'link',
                     'code':'inline', 'blockquote':'quote', 'li::marker':'marker'}
        for selector, role in selectors.items():
            rules.append(f'body[data-vscode-theme-name="Solar Eclipse {scheme["label"]}"] .vditor-reset {selector} {{ color: {r[role]} !important; }}')
    css_path.write_text(before + start + '\n' + '\n'.join(rules) + '\n' + end + after)
