# Solar Eclipse for VS Code

## WYSIWYG Markdown Editor

The optional `zaaack.markdown-editor` extension embeds Vditor, so its document
typography does not fully follow ordinary editor settings. Set
`markdown-editor.customCss` to the contents of `markdown-editor.css` for an
Inconsolata reading surface whose text and accents follow the active VS Code
theme. The stylesheet intentionally leaves Vditor's alternating table rows,
cell backgrounds, and borders unchanged.

A real theme extension, unlike the MarkText port — one extension carrying all
seven schemes, so they appear together in the theme picker.

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

The extension includes Nocturne, Verdigris, Ashen, Umbra, Totality, and the
Umbra B and Umbra D candidates. All cover the editor, navigation, terminal,
code tokens, Markdown, and controls.

## Reading and color

VS Code-specific adjustments live in `utils/make_vscode.py`. They do not
change the Obsidian or MarkText ports. Verdigris retains its established
background and relates its text and accents to that ground in CIELAB D65. Nocturne has a less saturated background; Ashen
has softer body text; Totality uses a slightly lifted dark surface.

Umbra B pairs plum `#2b282e` with green silver `#a4a69b`. Umbra D pairs
slate `#292b2b` with warm silver `#aaa499`. These are the selected reading
candidates, available as separate themes for comparison.

Code accents stay within the body text's lightness and a restrained chroma
limit. Markdown titles use the bright neutral; second-level headings use
the link accent. Embedded Markdown styling also softens heading rules and
forces links to follow the active theme instead of a default bright blue.
Verdigris uses related green-silver titles and quieter teal section headings. Inline code
uses a quiet text color instead of the embedded editor's yellow default.
The user's Inconsolata choice and existing table surfaces are preserved.

Verdigris defines one coordinated green, olive, and muted-gold family across
syntax, brackets, terminal colors, navigation, controls, notifications, and
diagnostics. A restrained copper tone distinguishes errors. Bright terminal
colors rise only slightly above their normal counterparts. The default vivid
yellow and orchid bracket colors are explicitly replaced. These relationships
are a visual candidate; numerical checks do not establish reading comfort.

## Rebuilding

```
python3 utils/make_vscode.py
```


The local set includes nine themes: Nocturne, Verdigris, Ashen, Umbra,
Totality, Umbra B, Umbra D, Solarized Dark Reading, and Solarized Green.
The Solarized reading themes are adaptations, separate from the bundled
VS Code Solarized reference.
