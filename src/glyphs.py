"""Load custom glyphs and make keymap-drawer output broadly renderable."""

import re
from pathlib import Path
from xml.dom import minidom


def load_glyphs(directory: Path) -> dict[str, str]:
    """Load SVG glyphs, using each file's stem as its keymap-drawer name."""
    return {
        glyph.stem: glyph.read_text(encoding="utf-8").strip()
        for glyph in sorted(directory.glob("*.svg"))
    }


def inline_glyphs(svg: str, glyphs: dict[str, str]) -> str:
    """Inline custom glyphs for SVG viewers that do not resolve nested <use> tags."""
    glyph_contents = {}
    for name, source in glyphs.items():
        root = minidom.parseString(source).documentElement
        view_box = root.getAttribute("viewBox")
        contents = "".join(child.toxml() for child in root.childNodes)
        glyph_contents[name] = (view_box, contents)

    use_pattern = re.compile(
        r'<use href="#(?P<name>[^"]+)"[^>]*'
        r' x="(?P<x>[^"]+)" y="(?P<y>[^"]+)"'
        r' height="(?P<height>[^"]+)" width="(?P<width>[^"]+)"'
        r' class="(?P<class>[^"]+)"/>'
    )

    def replace_use(match: re.Match[str]) -> str:
        name = match.group("name")
        if name not in glyph_contents:
            return match.group(0)
        view_box, contents = glyph_contents[name]
        return (
            f'<svg x="{match.group("x")}" y="{match.group("y")}" '
            f'height="{match.group("height")}" width="{match.group("width")}" '
            f'viewBox="{view_box}" class="{match.group("class")}">{contents}</svg>'
        )

    return use_pattern.sub(replace_use, svg)
