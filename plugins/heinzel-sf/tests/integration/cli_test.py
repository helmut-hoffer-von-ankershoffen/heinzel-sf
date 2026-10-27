"""Heinzelmännchen's CLI head with this plugin discovered through its real entry point. Offline."""

import tomllib

import pytest
from heinzel.kernel import user_config_dir

pytestmark = pytest.mark.integration


def test_info_names_the_module_and_the_theme(hz):
    about = hz("sf", "info").json
    assert about["plugin"] == "heinzel-sf"
    assert about["version"] == "0.1.0"
    assert (about["modules"], about["themes"]) == (["sf"], ["sf"])


def test_contributes_to_system_info(hz):
    assert hz("system", "info").json["sections"]["sf"]["plugin"] == "heinzel-sf"


def test_the_sf_theme_is_listed_with_valid_tokens_and_can_be_used(hz):
    listed = hz("system", "theme", "list").json
    (sf,) = [theme for theme in listed["themes"] if theme["name"] == "sf"]
    assert (sf["plugin"], sf["module"], sf["title"]) == ("heinzel-sf", "sf", "SF")
    assert (sf["dark"]["background"], sf["light"]["primary"], sf["radius"]) == ("#16181d", "#276ee1", "0.5rem")
    assert (sf["dark"]["accent_foreground"], sf["font_size"], sf["row_height"]) == ("#71aaff", "14px", "30px")
    assert [(font["family"], font["weight"], font["style"]) for font in sf["fonts"]] == [
        ("Inter", "100 900", "normal"),
        ("Inter", "100 900", "italic"),
    ]
    urls = [font["url"].split("?v=")[0] for font in sf["fonts"]]
    assert urls == ["/theme-fonts/sf/0.woff2", "/theme-fonts/sf/1.woff2"]
    logo = sf["logo"]
    assert (logo["alt"], logo["height"]) == ("Snowflake", "24px")
    assert logo["light"].startswith("/theme-assets/sf/light.svg?v=")
    assert logo["mark"].startswith("/theme-assets/sf/mark.svg?v=")
    assert hz("system", "theme", "use", "sf").json["selected"] == "sf"
    config = tomllib.loads((user_config_dir() / "config.toml").read_text(encoding="utf-8"))
    assert config["system"]["theme"]["name"] == "sf"


def test_sound_list_exposes_the_packaged_requested_streams_without_enabling_sound(hz):
    listed = hz("system", "sound", "list").json
    assert (listed["selected"], listed["effective"], listed["follow_theme"]) == ("off", "off", False)
    offered = {sound["name"]: sound for sound in listed["soundscapes"]}
    assert {"sf", "sf-2"}.isdisjoint(offered)
    for name, title, video in (
        ("sf-snow", "Snow", "Owg5DxmM4uE"),
        ("sf-fireplace", "Fireplace", "2wYtJwDkKIk"),
    ):
        sound = offered[name]
        assert (sound["title"], sound["kind"], sound["plugin"]) == (title, "stream", "heinzel-sf")
        assert sound["stream"]["video"] == video
        assert sound["stream"]["embed_url"] == f"https://www.youtube-nocookie.com/embed/{video}"
        assert sound["stream"]["watch_url"] == f"https://www.youtube.com/watch?v={video}"
    assert hz("system", "sound", "use", "sf-fireplace").json["effective"] == "sf-fireplace"
    assert hz("system", "sound", "use", "sf-snow").json["effective"] == "sf-snow"


def test_follow_theme_chooses_only_snow_and_explicit_fireplace_remains_available(hz):
    hz("system", "theme", "use", "sf")
    hz("system", "config", "set", "system.sound.follow_theme", "true")
    listed = hz("system", "sound", "list").json
    assert (listed["selected"], listed["effective"], listed["follow_theme"]) == ("off", "sf-snow", True)
    assert [sound["name"] for sound in listed["soundscapes"] if "sf" in sound["pairs_with"]] == ["sf-snow"]
    hz("system", "config", "set", "system.sound.follow_theme", "false")
    assert hz("system", "sound", "use", "sf-fireplace").json["effective"] == "sf-fireplace"
    assert hz("system", "sound", "use", "off").json["effective"] == "off"
