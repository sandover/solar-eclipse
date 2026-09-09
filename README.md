# Solar Eclipse

Three dark colour schemes built to sit alongside Solarized Dark, so four
windows can be told apart at a glance without any of them being harder to
look at than the original.

**Nocturne** (violet) · **Verdigris** (weathered copper) · **Ashen** (near-grey)
— plus Solarized itself as the fourth.

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

The schemes here then depart from the original deliberately, in two ways that
came out of use rather than measurement:

- **Far less colour.** Roughly 70% less than Solarized on average. Brightness
  carries the distinctions instead of hue.
- **Six accents, not eight.** Numbers share a colour with type names, errors
  with preprocessor markers, which buys back the spacing between the rest.

## Files

| | |
| --- | --- |
| `pal.py` | sRGB / CIELAB / OKLab conversion, gamut mapping, contrast |
| `generate.py` | builds the palettes; `SPECS` at the bottom is the dial |
| `schemes.json` | generated output |
| `build.py` | inlines `schemes.json` into the pages |
| `tmpl.html` → `index.html` | the tuning tool: previews and per-colour sliders |
| `howtmpl.html` → `how.html` | a measured account of how Solarized works |
| `PALETTES.md` | every colour as plain text |
| `analysis/` | one-off measurements, kept because they are the evidence |

To rebuild:

```
python3 generate.py && python3 build.py
```

## Caveats

- Text contrast runs 4.75 to 5.70:1 across the four rather than being uniform.
  Darker grounds raise it; the spread is what separates the backgrounds.
- The closest pair of backgrounds is Solarized and Verdigris, 0.040 apart in
  OKLab where 0.05 reads as clearly different. Only their lightness gap
  separates them.
- The colour choices past the measured rules are one person's taste, tuned by
  hand and read back out of the tool. They are not claimed to generalise.
