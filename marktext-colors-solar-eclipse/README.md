# Solar Eclipse for MarkText

MarkText cannot install themes — the docs say custom theme support is "planned
for a future release". What it has is **Preferences → Theme → Custom CSS**,
which overrides whichever built-in theme is selected.

That turns out to be enough. MarkText's built-in themes set 79 CSS variables on
`:root`, covering the sidebar, tab bar, buttons and notifications as well as the
editor, so overriding them re-colours the whole application.

## Install

1. Open **Preferences → Theme → Custom CSS**.
2. Paste the contents of the `.css` file for the scheme you want.

The `theme` setting underneath stays on a built-in name — MarkText has no way to
register a new one — so Preferences will still report whatever it was. Only the
colours change.

To set it without the GUI, write the file into the `customCss` field of
`~/Library/Application Support/marktext/preferences.json` **with MarkText
closed**, or the running app may overwrite it from memory on quit.

## Two things that needed hand-mapping

**Headings.** MarkText runs h1 red through h6 blue. Matched by role, h1 lands on
our dimmest colour, so headings are re-pointed by prominence instead: brightest
at h1, quietest at h6.

**Code blocks.** Prism hardcodes its token colours as literal hexes rather than
variables, so fenced code would keep Solarized's palette regardless of
everything else. Those get explicit rules appended.

## A correction specific to this app

A markdown document is mostly headings and prose, so a warm mid-chroma accent
that a code editor would spend on numbers ends up on every h2 and h3 here — and
drained warm hues read as skin rather than as restraint. In these builds any
such colour keeps its brightness and vividness and moves to the coolest hue
clear of the rest. Merged roles move together. The palettes themselves are
unchanged, so the code-editor ports keep the warm colour where it is used
sparingly.

## Rebuilding

```
python3 utils/make_marktext.py ashen
```

`_base-vars.css` is MarkText's own variable block, lifted from the application
bundle. It is the input the generator re-colours.
