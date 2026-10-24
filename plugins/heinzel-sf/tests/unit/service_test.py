import pytest
from heinzel import Kernel, __version__
from heinzel_sf import SfService

pytestmark = pytest.mark.unit


def test_about_describes_the_plugin_without_modules_in_an_empty_kernel():
    about = SfService(Kernel()).about()
    assert about.plugin == "heinzel-sf"
    assert about.heinzel_version == __version__
    assert (about.modules, about.themes) == ([], [])
