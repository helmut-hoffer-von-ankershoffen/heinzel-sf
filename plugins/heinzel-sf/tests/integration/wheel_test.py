"""The plugin's wheel, built offline with hatchling in-process, carries the theme and the fonts and logo it ships."""

import zipfile
from pathlib import Path

import pytest
from hatchling.builders.wheel import WheelBuilder

pytestmark = pytest.mark.integration

PLUGIN = Path(__file__).parents[2]
THEMES = "heinzel_sf/themes/"


def test_the_wheel_contains_the_theme_inter_its_licence_and_the_logo(tmp_path):
    (wheel,) = WheelBuilder(str(PLUGIN)).build(directory=str(tmp_path), versions=["standard"])
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        for font in ("InterVariable.woff2", "InterVariable-Italic.woff2"):
            name = f"{THEMES}fonts/{font}"
            assert name in names
            assert archive.read(name) == (PLUGIN / "src" / name).read_bytes()
    assert {f"{THEMES}sf.toml", f"{THEMES}fonts/LICENSE.txt"} <= names
    assert {f"{THEMES}logo/mark.svg", f"{THEMES}logo/wordmark-light.svg"} <= names
