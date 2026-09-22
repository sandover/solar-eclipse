"""Solarized palette and VS Code bundled-theme reading assignments."""
import json
from pathlib import Path

REFERENCE = json.loads((Path(__file__).resolve().parent.parent /
                        'references/solarized-dark.json').read_text())


def palette():
    """Keep historical repository slot names without treating them as syntax rules."""
    colors = REFERENCE['palette']
    return {**{k: v for k, v in colors.items() if k.startswith('base')},
            **{slot: colors[name] for slot, name in REFERENCE['repository_slots'].items()}}


def reading_colors(colors):
    """Apply VS Code Markdown token colors, plus explicit workshop extras."""
    return {**colors, **REFERENCE['markdown'], **REFERENCE['workshop_extensions']}


def green_palette():
    """Only the six dark/reading neutrals depart from the original palette."""
    return {**palette(), 'base03': '#002c2d', 'base02': '#073737',
            'base01': '#576f6e', 'base00': '#647c7c',
            'base0': '#859490', 'base1': '#95a19c'}
