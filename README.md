# Solar Eclipse

Three dark colour schemes built to sit alongside Solarized Dark, so several
windows can be told apart at a glance without any of them being harder to look
at than the original.

**Nocturne** (violet) · **Verdigris** (weathered copper) · **Ashen** (near-grey)
— with Solarized itself as a fourth.

<!-- palettes:start -->

| role | Nocturne | Verdigris | Ashen |
| --- | --- | --- | --- |
| background | `#181d33` | `#002324` | `#0f181e` |
| highlight | `#222840` | `#002e2f` | `#182228` |
| comments | `#676a7a` | `#527070` | `#656b70` |
| faint text | `#747688` | `#5e7d7d` | `#72787d` |
| body text | `#8a929c` | `#839590` | `#889397` |
| bright text | `#979fa8` | `#94a19c` | `#97a0a2` |
| pale | `#daeddf` | `#f8e5d7` | `#e7ead7` |
| palest | `#e8fbed` | `#fff5ed` | `#f6f8e5` |
| function names | `#85969e` | `#84939d` | `#87838f` |
| strings | `#55b2ce` | `#53b3c5` | `#67a7a6` |
| special | `#7a5955` | `#546490` | `#785863` |
| keywords | `#a08e77` | `#9f9179` | `#849585` |
| numbers | `#5d8f85` | `#937668` | `#937469` |
| type names | `#5d8f85` | `#937668` | `#937469` |
| errors | `#725d60` | `#6d707e` | `#716e64` |
| preprocessor | `#725d60` | `#6d707e` | `#716e64` |

| | Nocturne | Verdigris | Ashen |
| --- | --- | --- | --- |
| text contrast | 5.29:1 | 5.27:1 | 5.7:1 |

<!-- palettes:end -->

Merged roles share a colour: numbers with type names, errors with preprocessor
markers. Six accents rather than eight, which buys back the spacing between the
rest.

## How they were made

Solarized's restfulness was measured out of its sixteen hex values rather than
taken from its documentation. Three rules did most of the work:

- **No coloured token is brighter than the prose around it.** Every accent sits
  between the comment tone and the body-text tone.
- **Every accent is the same perceptual distance from the background**, achieved
  by trading brightness against saturation. Solarized's red is its most
  saturated colour and one of its dimmest.
- **Nothing sits at the edge of what a screen can display.** It uses about 87%
  of the colour available at each hue.

Feeding those rules Solarized's own background reconstructs Solarized to within
a just-noticeable difference, which is the check that they are the real
structure and not a story about it.

These then depart from the original deliberately, in two ways that came out of
use rather than measurement: roughly **70% less colour**, with brightness
carrying the distinctions instead of hue; and **six accents rather than eight**.

## Layout

Ports are one directory per application, as Solarized does it, each holding a
README and one file per scheme.

| | |
| --- | --- |
| `schemes.json` | canonical palettes — the source every port is built from |
| `marktext-colors-solar-eclipse/` | Custom CSS for MarkText |
| `vscode-colors-solar-eclipse/` | theme extension for VS Code |
| `utils/` | generator, build scripts, and the analysis behind each finding |
| `index.html` | tuning tool: previews and per-colour sliders |
| `how.html` | a measured account of how Solarized works |

Unlike Solarized, the canonical values here are generated rather than kept in
prose, and the table above is rebuilt from `schemes.json` — ports are built from
the same file, so they cannot drift from it.

```
python3 utils/generate.py        # palettes -> schemes.json
python3 utils/build.py           # pages, and the table above
python3 utils/make_marktext.py ashen
python3 utils/make_vscode.py
```

## Caveats

- Text contrast runs 4.75 to 5.70:1 across the four rather than being uniform.
  Darker grounds raise it; that spread is what separates the backgrounds.
- The closest pair of backgrounds is Solarized and Verdigris, 0.040 apart in
  OKLab where 0.05 reads as clearly different. Only their lightness gap
  separates them.
- Warm hues fail at both ends in a palette this drained: saturated they read as
  too red, drained they read as skin. Accents avoid the band. Drained *greens*
  are fine — they read as sage.
- The choices past the measured rules are one person's taste, tuned by hand.
  They are not claimed to generalise.
