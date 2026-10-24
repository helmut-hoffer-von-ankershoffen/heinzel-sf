"""SF's theme: valid as Heinzelmännchen checks it, close to the console it copies, offered by the company module."""

import tomllib
from pathlib import Path

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
    assert theme.light.primary == theme.dark.primary == "#2365d1"
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


def test_light_is_white_with_light_grey_blue_borders_and_dark_text():
    light = load().light
    assert (light.background, light.border, light.foreground) == ("#ffffff", "#e2e6eb", "#1d232b")
    assert (light.accent_foreground, light.icon) == ("#2365d1", "#1d232b")


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
