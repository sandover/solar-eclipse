# Solar Eclipse

Five dark colour schemes built to sit alongside Solarized Dark, so several
windows can be told apart at a glance without any of them being harder to look
at than the original.

**Nocturne** (violet) · **Verdigris** (weathered copper) · **Ashen** (near-grey) · **Umbra** (firelight) · **Totality** (near-black)
— with Solarized itself as a sixth.

<!-- palettes:start -->

| role | Nocturne | Verdigris | Ashen | Umbra | Totality |
| --- | --- | --- | --- | --- | --- |
| background | `#001a2d` | `#002324` | `#0f181e` | `#281713` | `#000d11` |
| highlight | `#05253a` | `#002e2f` | `#182228` | `#34211c` | `#001b21` |
| comments | `#5f6c7b` | `#527070` | `#656b70` | `#766764` | `#436069` |
| faint text | `#6b7988` | `#5e7d7d` | `#72787d` | `#837471` | `#4f6d76` |
| body text | `#85939b` | `#839590` | `#889397` | `#9b8e8e` | `#728586` |
| bright text | `#94a0a6` | `#94a19c` | `#97a0a2` | `#a79c9d` | `#829291` |
| pale | `#e3ebd9` | `#f8e5d7` | `#e7ead7` | `#dce9fb` | `#dfd6c4` |
| palest | `#f1f9e7` | `#fff5ed` | `#f6f8e5` | `#f1f7ff` | `#ede4d2` |
| function names | `#85969e` | `#84939d` | `#87838f` | `#8f8f81` | `#787b85` |
| strings | `#55b2ce` | `#53b3c5` | `#67a7a6` | `#4faabd` | `#6497a5` |
| special | `#7a5955` | `#546490` | `#785863` | `#4c6f51` | `#634d60` |
| keywords | `#a08e77` | `#9f9179` | `#849585` | `#8b8aa5` | `#818577` |
| numbers | `#5d8f85` | `#937668` | `#937469` | `#5d8e86` | `#896767` |
| type names | `#5d8f85` | `#937668` | `#937469` | `#5d8e86` | `#896767` |
| errors | `#725d60` | `#6d707e` | `#716e64` | `#6c737a` | `#675f58` |
| preprocessor | `#725d60` | `#6d707e` | `#716e64` | `#6c737a` | `#675f58` |

| | Nocturne | Verdigris | Ashen | Umbra | Totality |
| --- | --- | --- | --- | --- | --- |
| text contrast | 5.6:1 | 5.27:1 | 5.7:1 | 5.44:1 | 5.08:1 |

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

- Text contrast runs 4.75 to 5.70:1 across the six rather than being uniform.
  Darker grounds raise it; that spread is what separates the backgrounds.
- The closest pair of backgrounds is Nocturne and Ashen, 0.033 apart in
  OKLab where 0.05 reads as clearly different. Only their lightness and
  saturation gap separates them; their hues are 14 degrees apart.
- The ground-hue plane is full. Five schemes at L*8 to 15 tile it, and any new
  position inside the accepted hues lands within 0.03 of an existing ground —
  below the 0.05 where two read as clearly different. Totality separates on
  **level** instead: the ground drops to L*3 and the whole text ladder drops
  with it, so the gentle contrast survives rather than a black ground turning
  into glare. Depth also survives peripheral vision better than hue does.
- **A ground recedes in proportion to how close its hue sits to the daylight
  axis** — roughly hue 45 to 225 in CIELAB, warm at one end and cool at the
  other. Colour constancy discounts variation along that axis, so a ground near
  it reads as illumination and disappears; one far from it reads as paint and
  keeps announcing itself. Ranked against real verdicts this was monotonic:
  everything kept sits under 27 degrees off the axis, everything rejected over
  60. It is also why purple is hard — purple is off-axis by definition, so a
  ground that reads as violet cannot fully recede.
- Warm hues fail at both ends in a palette this drained: saturated they read as
  too red, drained they read as skin. Accents avoid the band. Drained *greens*
  are fine — they read as sage.
- That warning is about **accents, not grounds**. Umbra's ground is warm and it
  recedes, because at L*10 nothing reads as skin and hue 40 is 5 degrees off the
  daylight axis — as on-axis as Solarized's blue. The earlier warm schemes that
  failed sat 75 to 87 degrees off it. Warm was never the problem; off-axis was.
  Umbra bans the corpse band for accents, since a warm ground otherwise lays
  them straight through it.
- The choices past the measured rules are one person's taste, tuned by hand.
  They are not claimed to generalise.
