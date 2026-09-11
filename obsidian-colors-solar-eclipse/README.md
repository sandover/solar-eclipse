# Solar Eclipse for Obsidian

Obsidian has a real theme system, unlike MarkText's Custom CSS override, but
unlike VS Code it has no single-extension model: every theme is its own
folder with its own manifest, and they show up together in **Settings ->
Appearance -> Themes** for you to switch between.

## Install

Copy whichever scheme folders you want into your vault's `.obsidian/themes/`
directory (create it if it doesn't exist), then pick one from **Settings ->
Appearance -> Themes**:

```
cp -R "Solar Eclipse Nocturne" /path/to/YourVault/.obsidian/themes/
```

Or all five at once:

```
cp -R "Solar Eclipse "* /path/to/YourVault/.obsidian/themes/
```

Themes are per-vault in Obsidian, so repeat this for each vault you want it
in. A theme's folder name must match its manifest exactly, which is already
true here -- don't rename the folder after copying it.

## What each theme covers

186 CSS custom properties per scheme, generated from `schemes.json`: the
twelve-step `--color-base-*` neutral ramp, the eight-colour extended palette,
backgrounds, text, interactive and accent colours, code/syntax highlighting,
headings, links, blockquotes, callouts, tags, lists, checkboxes, tables,
scrollbars, dividers, the titlebar, ribbon, status bar, tabs, and the file
explorer.

These are dark-only, like the VS Code and MarkText ports -- everything is
set under `.theme-dark` and nothing is defined for `.theme-light`. Leave
**Appearance -> Base color scheme** on Dark.

## Two decisions specific to this app

**The neutral ramp isn't neutral.** Obsidian's own `--color-base-00..100`
scale is genuinely grey. This one walks the six lightness steps already in
the palette -- background, highlight, comments, faint text, body text,
bright text -- which are already a ramp along the scheme's own hue, and fills
in the gaps between them in OKLab-adjacent CIELAB space. A plugin that reaches
for `--color-base-60` gets a tone that belongs to the scheme instead of a
generic grey.

**Only h1 carries colour.** A note is mostly headings, the densest,
most-scanned structure on the page -- more so than a MarkText document and
the opposite of a code file, where a coloured token type is rare. Colouring
every heading level the way VS Code colours syntax would put the most colour
exactly where "brightness carries the distinction, not hue" matters most, so
`h1` keeps the standout accent and `h2` through `h6` are pinned to the same
bright neutral tone, separated by size and weight instead. Obsidian and
MarkText agree on this now; VS Code already did the equivalent for markdown
inside a code file, colouring only `h1` and leaving the rest bold.

**Prose accents still get the MarkText correction.** Where an accent does
appear -- callouts, tags, links -- a warm mid-chroma hue that a code editor
would spend sparingly on numbers is moved to the coolest hue clear of the
rest, same algorithm as the MarkText port. Left alone, a drained warm hue
reads as skin rather than restraint once it's dense on a page instead of
sparse in code.

## Extended palette and callouts

Obsidian expects eight named colours (red, orange, yellow, green, cyan,
blue, purple, pink) but the schemes carry six accents for eight roles --
numbers share type names, and errors share the preprocessor marker -- so
`--color-red` equals `--color-orange`, and `--color-yellow` equals
`--color-pink`. That's the same restraint as the other ports, not a mistake
here specifically. Callout types (`note`, `warning`, `success`, ...) are
mapped onto the same six accents by their usual sense -- `tip`/`important`
land on the standout colour, `warning`/`caution` on the same tone as
`danger`/`error`, and so on.

## Rebuilding

```
python3 utils/make_obsidian.py
```

`_base-vars.css` isn't needed here the way it is for MarkText -- Obsidian's
variables are documented, not reverse-engineered from a bundled stylesheet,
so the generator writes directly against the names in
[Obsidian's CSS variable reference](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables).
