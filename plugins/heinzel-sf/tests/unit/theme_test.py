"""SF's theme: valid as Heinzelmännchen checks it, close to the console it copies, offered by the company module."""

import re
import tomllib
from pathlib import Path
from xml.etree import ElementTree as ET

import heinzel_sf
import pytest
from heinzel import LayerLet, Theme, ThemeLet
from heinzel.kernel import font_stack_problem

pytestmark = pytest.mark.unit

THEME = Path(heinzel_sf.__file__).parent / "themes" / "sf.toml"


def load() -> Theme:
    return Theme.model_validate(tomllib.loads(THEME.read_text(encoding="utf-8")))


def test_the_sf_theme_is_valid_with_the_console_blue_and_an_8px_radius():
    theme = load()
    assert (theme.name, theme.title, theme.radius, theme.border_width) == ("sf", "SF", "0.5rem", "1px")
    assert theme.radius_control == "0.375rem"
    assert (theme.light.primary, theme.dark.primary) == ("#276ee1", "#2365d1")
    assert theme.light.primary_foreground == theme.dark.primary_foreground == "#ffffff"


def test_dark_uses_the_measured_console_colours():
    dark = load().dark
    measured = {
        "background": "#16181d",
        "sidebar": "#191e24",
        "foreground": "#d7dbe1",
        "muted_foreground": "#979fab",
        "border": "#23272c",
        "accent": "#233554",
        "card": "#16181d",
        "ring": "#2365d1",
        "accent_foreground": "#71aaff",
        "icon": "#d7dbe1",
    }
    assert {key: getattr(dark, key) for key in measured} == measured


def test_light_uses_the_measured_console_colours():
    light = load().light
    measured = {
        "background": "#ffffff",
        "sidebar": "#ffffff",
        "foreground": "#23272c",
        "muted_foreground": "#626c7e",
        "border": "#d7dbe1",
        "card": "#ffffff",
        "muted": "#eeeff1",
        "accent": "#e3efff",
        "accent_foreground": "#2365d1",
        "primary": "#276ee1",
        "primary_foreground": "#ffffff",
        "ring": "#276ee1",
        "icon": "#23272c",
        "input": "#ffffff",
        "popover": "#ffffff",
    }
    assert {key: getattr(light, key) for key in measured} == measured


def _luminance(colour: str) -> float:
    channels = [int(colour[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def test_light_text_is_readable_on_white_and_on_its_panels():
    light = load().light
    for token in ("foreground", "muted_foreground", "ok", "warn", "bad", "accent_foreground"):
        assert contrast(getattr(light, token), light.background) >= 4.5, token
    assert contrast(light.muted_foreground, light.muted) >= 4.5
    assert contrast(light.accent_foreground, light.accent) >= 4.5
    assert contrast(light.primary_foreground, light.primary) >= 4.5


def test_type_scale_and_density_match_the_console():
    theme = load()
    measured = {
        "font_size": "14px",
        "font_size_small": "12px",
        "heading_weight": 550,
        "heading_tracking": "-0.5px",
        "icon_size": "16px",
        "row_height": "30px",
        "spacing": "0.25rem",
    }
    assert {key: getattr(theme, key) for key in measured} == measured


def test_it_ships_inter_as_variable_woff2_files_inside_the_theme_directory():
    fonts = load().fonts
    assert [(font.family, font.file, font.weight, font.style) for font in fonts] == [
        ("Inter", "fonts/InterVariable.woff2", "100 900", "normal"),
        ("Inter", "fonts/InterVariable-Italic.woff2", "100 900", "italic"),
    ]
    root = THEME.parent.resolve()
    for font in fonts:
        path = (THEME.parent / font.file).resolve(strict=True)
        assert path.is_relative_to(root)
        assert path.read_bytes()[:4] == b"wOF2"
        assert path.stat().st_size < 2 * 1024 * 1024
    licence = (THEME.parent / "fonts" / "LICENSE.txt").read_text(encoding="utf-8")
    assert "SIL Open Font License, Version 1.1" in licence


def test_font_stacks_start_with_inter_and_pass_the_validator():
    theme = load()
    assert theme.font_sans.startswith("Inter, ")
    assert theme.font_sans.endswith("sans-serif")
    assert theme.font_mono.endswith("monospace")
    assert font_stack_problem(theme.font_sans) is None
    assert {font.family for font in theme.fonts} == {theme.font_sans.split(",")[0]}
    assert font_stack_problem(theme.font_mono) is None


def test_the_company_module_offers_it_and_is_the_root_layer():
    offered = [let.theme for let in heinzel_sf.module.lets if isinstance(let, ThemeLet)]
    assert [theme.name for theme in offered] == ["sf"]
    assert offered[0].dark.background == "#16181d"
    (let,) = [let for let in heinzel_sf.module.lets if isinstance(let, ThemeLet)]
    assert let.directory == THEME.parent
    assert [let.font(index)[:4] for index in range(len(let.theme.fonts))] == [b"wOF2", b"wOF2"]
    (layer,) = [let for let in heinzel_sf.module.lets if isinstance(let, LayerLet)]
    assert (layer.name, layer.parent, layer.site) == ("sf", None, None)


LOGO_FILES = ("logo/mark.svg", "logo/wordmark-light.svg")
MAX_LOGO_BYTES = 200 * 1024


@pytest.mark.parametrize("file", LOGO_FILES)
def test_logo_files_are_small_clean_svgs_inside_the_theme_directory(file):
    root = THEME.parent.resolve()
    path = (THEME.parent / file).resolve(strict=True)
    assert path.is_relative_to(root)
    assert path.stat().st_size <= MAX_LOGO_BYTES
    svg = ET.fromstring(path.read_bytes())  # noqa: S314 - our own file, checked for what it may not hold
    assert svg.tag == "{http://www.w3.org/2000/svg}svg"
    for element in svg.iter():
        assert element.tag.rsplit("}", 1)[-1] not in {"script", "foreignObject", "image", "use", "a", "style"}
        for attribute in element.attrib:
            name = attribute.rsplit("}", 1)[-1].lower()
            assert not name.startswith("on"), (file, attribute)
            assert name != "href", (file, attribute)
    assert b"url(" not in path.read_bytes()


def test_the_logo_is_the_vendor_blue_on_both_modes():
    for file in LOGO_FILES:
        fills = set(re.findall(r'fill="([^"]+)"', (THEME.parent / file).read_text(encoding="utf-8")))
        assert fills == {"#2cb6e8"}, file


def test_the_theme_declares_the_logo_and_a_light_main_tint():
    theme = load()
    assert theme.logo is not None
    assert (theme.logo.light, theme.logo.dark, theme.logo.mark) == ("logo/wordmark-light.svg", None, "logo/mark.svg")
    assert (theme.logo.alt, theme.logo.height) == ("Snowflake", "24px")
    assert set(theme.logo.files()) == set(LOGO_FILES)
    assert (theme.light.main_tint, theme.dark.main_tint) == ("#eef5fd", None)


def test_heinzel_accepts_and_serves_the_logo_files():
    (let,) = [let for let in heinzel_sf.module.lets if isinstance(let, ThemeLet)]
    logos = let.logos()
    assert logos is not None
    for name in ("light", "dark", "mark"):
        assert logos.content(name).startswith(b"<svg")
        assert logos.url(name).startswith(f"/theme-assets/sf/{name}.svg?v=")
    assert logos.content("dark") == logos.content("light")
