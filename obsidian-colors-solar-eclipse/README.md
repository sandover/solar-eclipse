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

The themes cover reading surfaces, headings, links, lists, quotes, callouts,
tags, checkboxes, tables, navigation, tabs, and controls. They are dark-only;
set **Appearance -> Base color scheme** to Dark.

## Reading design

All five themes use dedicated prose roles from `utils/obsidian_reading.py`.

- Titles, major sections, and smaller headings have distinct, coordinated
  hues. H3/H4 share a color family; H5/H6 return to a quiet neutral.
  Size, weight, and spacing support the hierarchy at every level.
- Body text uses the shared palette with a small brightness reduction for
  Ashen and a cooler silver tone for Umbra. The theme preserves the fonts
  selected in appearance settings.
- A 1.6 line height and wider list-item spacing give dense notes more air.
  Reading view adds a little more space between top-level list items.
- Links share one accent, with a thin, subdued underline in the document.
- The selected file has a tinted background and a narrow location marker.
- Quotes and tags use a secondary accent. Highlights use a muted warm tint.
  Success, warning, and error callouts have distinct semantic colors.
- Readable line length is 740px when Obsidian's readable-line-length option
  is enabled. Existing font-size and line-length preferences remain available.

Umbra pairs silver titles, mineral-blue sections, and lilac subheadings
with a smoky plum-gray reading surface and a cooler slate sidebar and tab bar.
Nocturne uses silver, mist blue, and lavender on deep
blue. Ashen pairs warm stone titles with blue and sage on graphite.
Totality uses dim silver, faded blue, and dusky violet on deep ink.
Verdigris pairs its deep green background with warm silver titles, blue
sections and links, olive-gold subheadings, and occasional brass highlights.
Ashen and Nocturne use quieter blue accents to reduce their visual intensity.
Nocturne's background has less blue saturation. Totality lifts its near-black
surface slightly and dims its accents so links sit closer to body text.

`schemes.json` still supplies the shared base palette. Obsidian-specific
changes do not change the VS Code or MarkText ports. The generated CSS uses
Obsidian's built-in variables for most styling and a few scoped rules for
links, list grouping, and the selected file.

## Rebuilding

```
python3 utils/make_obsidian.py
```

`_base-vars.css` isn't needed here the way it is for MarkText -- Obsidian's
variables are documented, not reverse-engineered from a bundled stylesheet,
so the generator writes directly against the names in
[Obsidian's CSS variable reference](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables).


The local set includes nine themes: Nocturne, Verdigris, Ashen, Umbra,
Totality, Umbra B, Umbra D, Solarized Dark Reading, and Solarized Green.
The Solarized reading themes are adaptations, separate from the bundled
VS Code Solarized reference.
