#!/usr/bin/env python3
"""Build a VS Code colour-theme extension from schemes.json.

Unlike MarkText, VS Code installs real themes: a folder under ~/.vscode/extensions
with a package.json declaring them. One extension carries all three schemes, so
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

def workbench(c):
    bg, hl = c['base03'], c['base02']
    chrome = shade(bg, -1.6)          # sidebar, status bar, inactive tabs
    over   = shade(bg, +2.2)          # popups and hovers sit above the page
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
    }

def tokens(c):
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
      r("markup.heading, entity.name.section", c['str'], "bold"),
      r("markup.bold", c['base1'], "bold"),
      r("markup.italic", c['base1'], "italic"),
      r("markup.underline.link, string.other.link", c['fn']),
      r("markup.inline.raw, markup.raw", c['str']),
      r("markup.quote", c['base01'], "italic"),
      r("markup.list punctuation.definition.list", c['num']),
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
    c = s['colors']
    return {
      "$schema": "vscode://schemas/color-theme",
      "name": f"Solar Eclipse {s['label']}",
      "type": "dark",
      "semanticHighlighting": True,
      "colors": workbench(c),
      "semanticTokenColors": semantic(c),
      "tokenColors": tokens(c),
    }

if __name__ == '__main__':
    out = ROOT / 'vscode-colors-solar-eclipse'
    (out / 'themes').mkdir(parents=True, exist_ok=True)
    schemes = [s for s in json.load(open(ROOT / 'schemes.json'))
               if s['name'] != 'solarized']
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
