from importlib.metadata import PackageNotFoundError

import pytest
from heinzel import Kernel, __version__
from heinzel_sf import SfService, _service

pytestmark = pytest.mark.unit


def test_about_describes_the_plugin_without_modules_in_an_empty_kernel():
    about = SfService(Kernel()).about()
    assert about.plugin == "heinzel-sf"
    assert about.heinzel_version == __version__
    assert (about.modules, about.themes) == ([], [])


def test_uninstalled_source_does_not_invent_a_release_version(monkeypatch):
    def absent(name):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(_service, "version", absent)
    assert SfService(Kernel()).about().version == "unknown"
