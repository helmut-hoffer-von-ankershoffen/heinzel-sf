"""Heinzelmännchen's CLI head with this plugin discovered through its real entry point. Offline."""

import tomllib

import pytest
from heinzel.kernel import user_config_dir

pytestmark = pytest.mark.integration


def test_info_names_the_module_and_the_theme(hz):
    about = hz("sf", "info").json
    assert about["plugin"] == "heinzel-sf"
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
    assert hz("system", "theme", "use", "sf").json["selected"] == "sf"
    config = tomllib.loads((user_config_dir() / "config.toml").read_text(encoding="utf-8"))
    assert config["system"]["theme"]["name"] == "sf"
