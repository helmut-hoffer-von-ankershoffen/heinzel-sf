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

The repository is private, so git needs read access to it (`gh auth login`, or any git credential helper). The
plugin is independently versioned (first release 0.1.0) and needs hz 0.7.2 or newer for its avatar palette and winter decoration. Install that release first:

```sh
uv tool install --force "heinzel @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel@v0.7.2"
hz system plugin add "heinzel-sf @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf#subdirectory=plugins/heinzel-sf"
hz system theme use sf
```

Optional sound choices and **Follow my theme** commands are in the [plugin guide](plugins/heinzel-sf/README.md#soundscapes).

`hz system plugin add` keeps the installed core and every other plugin and adds this one to the `uv tool`
environment. The same in one `uv` command:

```sh
uv tool install --force "heinzel @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel@v0.7.2" \
  --with "heinzel-sf @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf#subdirectory=plugins/heinzel-sf"
```

Pin a revision with `heinzel-sf.git@<sha>` before `#subdirectory`. Remove it with `hz system plugin remove heinzel-sf`.

## Develop

```sh
make setup   # uv sync: the workspace, Heinzelmännchen (pinned in pyproject.toml) and the dev tools
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

For a fixed reproducible install, put `@v0.1.0` after `heinzel-sf` in the repository URL, before `#subdirectory`.
An explicit tag/commit remains pinned when updating hz; choose a newer reviewed tag explicitly to move it.

## Licence

Proprietary, all rights reserved: see [LICENSE](LICENSE).
