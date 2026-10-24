"""Models returned by the plugin's operations."""

from pydantic import BaseModel, Field


class SfAbout(BaseModel):
    """What this plugin is, where it runs and what it brings."""

    plugin: str = Field(description="Distribution name of the plugin.")
    version: str = Field(description="Installed version of the plugin.")
    heinzel_version: str = Field(description="Version of the Heinzelmännchen it runs in.")
    modules: list[str] = Field(description="Qualified names of the modules the plugin provides.")
    themes: list[str] = Field(description="Names of the web app themes the plugin offers.")
