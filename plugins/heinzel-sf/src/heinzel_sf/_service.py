"""The plugin's logic, independent of any head."""

from importlib.metadata import PackageNotFoundError, version

from heinzel import Kernel, ThemeLet, __version__

from heinzel_sf._models import SfAbout

DISTRIBUTION = "heinzel-sf"


class SfService:
    """Everything the sf module does; operations stay thin and call into it."""

    def __init__(self, kernel: Kernel) -> None:
        """Create the service; the kernel is injected."""
        self._kernel = kernel

    def about(self) -> SfAbout:
        """Describe the plugin, the Heinzelmännchen installation it runs in and the themes it offers."""
        try:
            installed = version(DISTRIBUTION)
        except PackageNotFoundError:  # pragma: no cover - only when running from an uninstalled source tree
            installed = "0.0.0"
        records = [r for r in self._kernel.modules if r.origin.distribution == DISTRIBUTION]
        return SfAbout(
            plugin=DISTRIBUTION,
            version=installed,
            heinzel_version=__version__,
            modules=[r.qualname for r in records],
            themes=[let.name for r in records for let in r.module.lets if isinstance(let, ThemeLet)],
        )
