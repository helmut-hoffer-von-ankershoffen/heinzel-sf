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
    }
    assert {key: getattr(dark, key) for key in measured} == measured


def test_light_is_white_with_light_grey_blue_borders_and_dark_text():
    light = load().light
    assert (light.background, light.border, light.foreground) == ("#ffffff", "#e2e6eb", "#1d232b")


def test_font_stacks_start_with_inter_and_pass_the_validator():
    theme = load()
    assert theme.font_sans.startswith("Inter, ")
    assert theme.font_sans.endswith("sans-serif")
    assert theme.font_mono.endswith("monospace")
    assert font_stack_problem(theme.font_sans) is None
    assert font_stack_problem(theme.font_mono) is None


def test_the_company_module_offers_it_and_is_the_root_layer():
    offered = [let.theme for let in heinzel_sf.module.lets if isinstance(let, ThemeLet)]
    assert [theme.name for theme in offered] == ["sf"]
    assert offered[0].dark.background == "#16181d"
    (layer,) = [let for let in heinzel_sf.module.lets if isinstance(let, LayerLet)]
    assert (layer.name, layer.parent, layer.site) == ("sf", None, None)
