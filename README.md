# heinzel-sf

Private [Heinzelmännchen](https://github.com/helmut-hoffer-von-ankershoffen/heinzel) (`hz`) plugins for SF: the
company's layers (heinzel ADR 0040), one plugin per layer in [`plugins/`](plugins/), in one `uv` workspace, laid out
like the public reference company [heinzel-acme](https://github.com/helmut-hoffer-von-ankershoffen/heinzel-acme).

| Plugin | Layer | What it brings |
| --- | --- | --- |
| [`heinzel-sf`](plugins/heinzel-sf/) | company (root, no parent) | `hz sf info`; the winter web app theme `sf`; Snow (`sf-snow`) and Fireplace (`sf-fireplace`) streams |

Org, site and team layers (`sf-<org>`, `sf-<site>`, `sf-<org>-<team>`) come later, as further plugins in
`plugins/` that name their parent with `module.layer(parent=...)` and list it as a dependency.

## Install

Start the standard app with one command:

```sh
uvx heinzel@latest
```

The first run installs the app and its default plugins automatically and opens the workspace.
For this private plugin, authenticate GitHub with `gh auth login` if needed. In a second terminal:

```sh
hz system plugin add https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf --confirm
hz system theme use sf
```

The installer resolves the plugin's project metadata and compatible source automatically. It keeps the installed
app and its other plugins. No Core reinstall, force flag, version number or manual subdirectory is needed.
Restart the workspace after adding a plugin so its running process loads the new module.

Optional sound choices and **Follow my theme** commands are in the [plugin guide](plugins/heinzel-sf/README.md#soundscapes).
Remove the plugin with `hz system plugin remove heinzel-sf`.

## Develop

```sh
make setup   # uv sync: the workspace, the compatible SDK resolved in uv.lock, and the dev tools
make check   # ruff, mypy, pytest: what CI runs
```

Conventions are Heinzelmännchen's: see [AGENTS.md](AGENTS.md).

## Releases

Plugin versions follow independent SemVer. The plugin declares its compatible hz range in its `pyproject.toml`;
its version does not need to match hz. [CHANGELOG.md](CHANGELOG.md) records each reviewed release.

Prepare a release through a pull request: update the plugin version, `uv.lock` and changelog, run `make check`,
review the complete diff, and merge only after CI is green. Tag the reviewed main commit `vX.Y.Z`; the Release
workflow checks the tag/version, repository privacy and main ancestry, runs the full checks, builds the plugin
wheel/source archive and publishes them to this private repository's GitHub release. It never overwrites tags or
releases and never uploads to a public package index. A failed publication can be dispatched again for that existing
tag after diagnosing its failure. No version tag is created by the source change alone.

Reproducible source revisions and compatibility requirements are recorded in installation history and plugin metadata.

## Licence

Proprietary, all rights reserved: see [LICENSE](LICENSE).
