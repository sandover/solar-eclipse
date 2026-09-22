# Solarized Dark reference

Our application reference is **VS Code 1.138.0's bundled Solarized (dark)**.
`vscode-solarized-dark.json` is a complete, unmodified-content snapshot of the
installed theme, reformatted for reading. Upstream source:
<https://github.com/microsoft/vscode/blob/main/extensions/theme-solarized-dark/themes/solarized-dark-color-theme.json>.

The published sixteen-color palette remains in `solarized-dark.json`. Its
Markdown assignments now follow the bundled theme, rather than the unaccented
CSS foundation from the Solarized website:

| Element | VS Code scope | Color |
| --- | --- | --- |
| All ATX headings | markup.heading | Blue |
| Bold and italic | markup.bold / markup.italic | Magenta |
| Inline code | markup.inline.raw | Cyan |
| Quotation | markup.quote | Green |
| Whole list item | markup.list | Yellow |
| Link label | string.other.link.title.markdown, inheriting string | Cyan |

The link-label scope comes from VS Code's bundled Markdown grammar. A raw link
URL has a different scope and normally inherits the body foreground; a rendered
link displays its label. Do not mistake repository palette slot names for a
complete syntax-highlighting grammar.

The workshop transfers these token colors to rendered Markdown. Its typography,
spacing, tables, highlights, and callouts are explicit design adaptations, not
VS Code's built-in rendered Markdown preview. Code examples are illustrative
and do not reproduce VS Code's full grammar or semantic highlighting engine.
Editor background, body foreground, sidebar background, and selection backing
come directly from the bundled theme. The other widget backings remain quiet
workshop adaptations.

Solarized Green keeps the original code accents and its six greener neutrals.
Its Markdown composition now uses our prose design in `utils/markdown_design.py`;
it is deliberately separate from the unchanged VS Code reference.

Tests compare Markdown role assignments with the bundled theme snapshot. The
page builder checks the original sixteen-color palette against the reference.
A visual review in the browser is also required: tests do not establish harmony.
