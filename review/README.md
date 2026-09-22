# Color workshop

Open the repository's `index.html`, or serve the repository locally:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765`. Keep using the same browser and address to
retain access to its local saves. No server receives your palette choices.

## Explore

Choose a starting point: shared palettes, current VS Code generator palettes,
Obsidian reading palettes, or the Verdigris E candidate. Candidates are labeled;
they do not represent an installed theme. The original gallery remains available.

Select a swatch or click a preview element. Adjust perceptual lightness, chroma,
and hue in CIELAB with the same D65 reference as the Python palette tools.
You can also enter a hex value or use the color picker. Transparent roles have
an opacity control. When a requested color falls outside sRGB, the page reports
the reduced chroma used for display. It preserves requested lightness and hue.

Some roles inherit another color. Editing one detaches it; the inheritance menu
can reconnect it. This lets you explore a shared color relationship or separate
a Markdown role from a code token. Reset restores the role's starting value.

The Markdown sample includes six heading levels, sustained prose, emphasis,
links, nested lists, tasks, quotations, inline code, a highlight, a callout, and
a table. Other views show Markdown source and representative TypeScript, HTML,
and CSS. You can add your own plain-text paragraph and vary typeface, text size,
line spacing, and line width. Inconsolata, IBM Plex Sans, and Atkinson
Hyperlegible are bundled locally, including their licenses, and work offline.
The selected typeface applies to all three preview modes. These are browser approximations, not exact
renderings of VS Code or Obsidian. They cover the named palette and reading
roles, not every application-specific workbench setting.

Use Compare to keep the starting point, another theme, or a saved snapshot beside
your draft. Judge the entire composition; contrast numbers do not prove comfort.

## Save and discuss

Drafts autosave in localStorage, separately for each starting point. Save snapshot
creates a named copy with your notes and reading conditions. Load restores one.
Reset this draft leaves snapshots intact. The page reports storage errors rather
than claiming the data was saved.

Export JSON downloads the complete current palette, inherited roles, resolved
hex values, original baseline, notes, and reading conditions. Keep that file as
a backup: browser storage can be cleared. Import JSON validates a file and adds
it as a snapshot without replacing the active draft. Click Load to use it.

Attach the exported JSON in our conversation, or use Copy discussion notes to
paste a concise list of edits and your observations. The assistant cannot see
localStorage automatically. Nothing here modifies or installs repository themes.

## Maintain

- `tmpl.html`: page structure; `index.html` is generated.
- `review/workshop.js`: editing, comparison, and local persistence.
- `review/color.js`: color conversion, gamut mapping, and contrast.
- `review/examples.js`: preview content.
- `review/workshop.css`: layout and preview styles.
- `utils/review_data.py`: starting points derived from existing theme generators.

Run `python3 utils/build.py` to regenerate pages after changing the template or
starting palettes. This existing command also refreshes the README palette table
and SVG. Run `node --test tests/color.test.cjs` to check color conversion against
the Python tools, gamut behavior, alpha compositing, and complete palette links.

The older gallery's browser saves remain under their old storage key. They are
not migrated into the workshop: they describe different palettes and controls.

## Solarized Green candidate

This is a close variation of Solarized Dark, available in the workshop's
Candidate group. Its six dark and reading neutrals move about 32 degrees toward
green in D65 Lab hue. Their lightness and chroma stay close to the reference;
sRGB limits slightly reduce the background chroma. Body text moves with the
surfaces, rather than becoming an unrelated neutral.

The eight original accents and two pale neutrals stay unchanged. Keeping these
anchors lets us judge whether the greener foundation retains the original
palette's balance. Markdown role assignments use our restrained prose composition, separate from the VS Code reference
in the workshop, so the comparison isolates the palette change. This is a
starting hypothesis for visual review, not a claim of equivalent comfort.

Source: [Solarized's design notes](https://ethanschoonover.com/solarized/).
The candidate lives in `utils/review_data.py`; it has not been installed in an editor.

The reference and its exact scope are documented in [references](../references/README.md).


## Prose design review, September 2026

`utils/markdown_design.py` owns the shared reading assignments for the local
families. It preserves each starting point's text and ground while coordinating
headings, links, emphasis, quotations, markers, and overlays. The original
Solarized reference remains unchanged. Revised drafts preserve earlier browser
work as snapshots before loading the new starting colors.

Visual review covered the workshop compositions for all shared, VS Code, and
Obsidian families, plus Solarized Green, using prose, nested lists, quotes,
inline code, highlights, and tables. Cool titles and warm section headings
provide structure; pale subheadings remain distinct without a third accent.
This signs off the workshop compositions, not native app rendering or
long-session comfort. Generated editor files require no workshop export.
They have been updated in the repo, not installed into running applications.

Solarized Dark · Reading now uses the same prose design process as every other
local Markdown profile. Solarized Dark · VS Code reference is a separate,
explicitly labeled comparison. The original background and body text remain
identical in both; headings, emphasis, lists, and detail colors differ.
