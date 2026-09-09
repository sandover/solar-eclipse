# Solar Eclipse for VS Code

A real theme extension, unlike the MarkText port — one extension carrying all
three schemes, so they appear together in the theme picker.

## Install

No packaging or publishing needed. Copy this directory into the extensions
folder and reload:

```
cp -R vscode-colors-solar-eclipse \
      ~/.vscode/extensions/local.solar-eclipse-themes-1.0.0
```

Then **Cmd-Shift-P → Developer: Reload Window**, and pick the theme from
**Cmd-K Cmd-T**. Or set it directly in `settings.json`:

```json
"workbench.colorTheme": "Solar Eclipse Nocturne"
```

## What each scheme covers

127 workbench colours and 31 token rules, all derived from `schemes.json`:
editor, sidebar, activity bar, status bar, tabs, panel, terminal (all sixteen
ANSI slots), lists, inputs, git decorations and diffs. Semantic highlighting is
on, with semantic token colours matching the TextMate rules.

Two derived tones are computed rather than taken from the palette: the chrome
behind the sidebar and status bar sits 1.6 points darker than the editor
background, and popups sit 2.2 points lighter, so panels read as layered without
introducing a colour the scheme does not have.

## One difference from the MarkText port

The warm accent stays where it is here. In a markdown editor that colour lands
on every heading and reads as pallor, so the MarkText build moves it. In a code
editor it lands on numbers and constants, which are sparse, so it reads as
intended and is left alone.

## Rebuilding

```
python3 utils/make_vscode.py
```
