"""SF, the company layer: the root of SF's layers for Heinzelmännchen (heinzel ADR 0040).

A Heinzelmännchen plugin, discovered through the `heinzel.modules` entry point in pyproject.toml. It is the root
layer (no parent): SF's org, site and team layers are separate plugins in this repository's `plugins/` that name
`sf` as their parent. For now it brings SF's look for the web app, data in `themes/` (`hz system theme use sf`),
and two soundscapes in `soundscapes/`: Snow and Fireplace.
"""

from pathlib import Path

from heinzel import Module

from heinzel_sf._models import SfAbout
from heinzel_sf._service import SfService

module = Module("sf", "SF, the company layer: its look for the web app, later its adapters and playbooks.")
module.layer()  # the root of SF's tree: no parent, no site
module.service(SfService)
module.theme(Path(__file__).parent / "themes")  # read and checked now; `hz system theme list` shows it
module.soundscape(Path(__file__).parent / "soundscapes")  # `hz system sound list` shows it


@module.operation
def info(service: SfService) -> SfAbout:
    """Show this plugin's version, the Heinzelmännchen it runs on and what it brings."""
    return service.about()


@module.info
def system_info(service: SfService) -> SfAbout:
    """Contribute this plugin's details to `hz system info`."""
    return service.about()


__all__ = ["SfAbout", "SfService", "module"]
