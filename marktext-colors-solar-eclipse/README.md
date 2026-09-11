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

The `theme` setting underneath stays on a built-in name, and Preferences will
keep reporting it. That is not laziness on our part: `addThemeStyle` in the
renderer bundle is a `switch` over hardcoded theme names with **no `default`
branch**, and the "Import custom themes" / "Open themes folder" buttons in the
Theme pane are rendered with `v-show=false` and carry no click handler — the
feature is a stub. An unrecognised name is worse than a wrong one, because it
also drops `dark` from `document.body` and flips CodeMirror to its light theme.

So a real built-in has to stay selected. **Keep it on `solarized-dark`**: the
switch only decides which base CSS loads, and every rule that base sets is now
either a variable we own or one of the six named above. Any theme in the
bundle's `railscastsThemes` list would work equally well; a light one would
not.

To set it without the GUI, write the file into the `customCss` field of
`~/Library/Application Support/marktext/preferences.json` **with MarkText
closed**, or the running app may overwrite it from memory on quit.

## Two things that needed hand-mapping

**Headings.** MarkText runs h1 red through h6 blue. Matched by role, h1 lands on
our dimmest colour, so headings are re-pointed by prominence instead: brightest
at h1, quietest at h6.

**Code blocks, twice.** Rendered code is Prism, which hardcodes its token
colours as literal hexes rather than variables. Code you are *editing* is
CodeMirror, and MarkText hands it the Railscasts theme for every dark scheme —
a `#2b2b2b` box with red keywords and amber strings, none of it a variable. A
fence therefore changes palette the moment the cursor enters it unless both are
set. Both are set.

**What the built-in theme leaks.** Most of its rules write a literal hex and
then the variable, so ours wins. Six do not: the title-bar glyph fill and its
hover, the sidebar's right edge, the two tab-bar underlines, and Prism's
default text colour. Those keep whatever base theme is selected showing through
until they are named explicitly, which they now are.

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
