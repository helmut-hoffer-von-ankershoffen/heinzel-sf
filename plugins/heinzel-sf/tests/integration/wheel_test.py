"""The plugin's wheel, built offline with hatchling in-process, carries the theme and the fonts and logo it ships."""

import zipfile
from email.parser import BytesParser
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


def test_the_wheel_carries_both_requested_stream_manifests_without_media(tmp_path):
    (wheel,) = WheelBuilder(str(PLUGIN)).build(directory=str(tmp_path), versions=["standard"])
    with zipfile.ZipFile(wheel) as archive:
        metadata_name = next(name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
        assert metadata["Version"] == "0.1.0"
        assert "heinzel<1,>=0.7.2" in metadata.get_all("Requires-Dist")
        for name in ("sf-snow", "sf-fireplace"):
            member = f"heinzel_sf/soundscapes/{name}.toml"
            assert archive.read(member) == (PLUGIN / "src" / member).read_bytes()
        assert not any(name.endswith(("/soundscapes/sf.toml", "/soundscapes/sf-2.toml")) for name in archive.namelist())
        assert not any(name.endswith((".mp3", ".ogg", ".opus", ".mp4")) for name in archive.namelist())
