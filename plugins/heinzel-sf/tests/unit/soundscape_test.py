"""The requested streams are registered data, with one winter-theme default and no bundled media."""

import heinzel_sf
import pytest
from heinzel import SoundscapeLet

pytestmark = pytest.mark.unit


def test_requested_snow_and_fireplace_streams_are_registered_with_one_theme_pair():
    offered = {let.name: let.soundscape for let in heinzel_sf.module.lets if isinstance(let, SoundscapeLet)}
    snow, fireplace = offered["sf-snow"], offered["sf-fireplace"]
    assert (snow.title, snow.kind, snow.stream.provider, snow.stream.video) == (
        "Snow",
        "stream",
        "youtube",
        "Owg5DxmM4uE",
    )
    assert (fireplace.title, fireplace.kind, fireplace.stream.provider, fireplace.stream.video) == (
        "Fireplace",
        "stream",
        "youtube",
        "2wYtJwDkKIk",
    )
    assert [name for name, sound in offered.items() if "sf" in sound.pairs_with] == ["sf-snow"]
    assert snow.assets() == fireplace.assets() == {}
    assert {"sf", "sf-2"} <= offered.keys()  # existing choices retain their stable identity
