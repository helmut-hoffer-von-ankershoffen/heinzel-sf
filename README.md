# heinzel-sf

**SF's private plugins for [Heinzelmännchen](https://github.com/helmut-hoffer-von-ankershoffen/heinzel) (`hz`), the
open-source crew of AI helpers that drafts a team's busywork and asks before anything leaves the machine.** Today
they give `hz ui` SF's winter look and two quiet sound streams, and they are the company layer that SF's org, site and
team layers will stack on. One plugin per layer, in one `uv` workspace, laid out like the public reference company
[heinzel-acme](https://github.com/helmut-hoffer-von-ankershoffen/heinzel-acme). This repository is private; its
plugins are never published to a public index.

| Plugin | Layer | What it brings |
| --- | --- | --- |
| [`heinzel-sf`](plugins/heinzel-sf/) | company (root, no parent) | `hz sf info`; the winter web app theme `sf`; Snow (`sf-snow`) and Fireplace (`sf-fireplace`) streams |

Org, site and team layers (`sf-<org>`, `sf-<site>`, `sf-<org>-<team>`) come later, as further plugins in
`plugins/` that name their parent with `module.layer(parent=...)` and list it as a dependency. The theme, its tokens
and the soundscapes are described in the [plugin guide](plugins/heinzel-sf/README.md).

## Install

You need Heinzelmännchen first. For macOS and Linux, one command installs the app with its default plugins and opens it:

```sh
uvx heinzel@latest
```

No uv yet? The guided installer sets it up first:

```sh
curl -LsSf https://helmut.hoffer-von-ankershoffen.me/heinzel/install.sh | sh
```

Windows may work, but is not supported. Details: the
[standard app installation guide](https://helmut.hoffer-von-ankershoffen.me/heinzel/guides/install/).

This plugin lives in a private repository, so it also needs [Git](https://git-scm.com/install/) and the
[GitHub CLI](https://cli.github.com/), signed in with an account that may read it. In a second terminal:

```sh
gh auth login
gh auth setup-git
hz system plugin add https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf --confirm
hz system theme use sf
```

The installer resolves the plugin's metadata and source itself, checks that it fits your Heinzelmännchen, and keeps the
app and its other plugins. Restart the workspace afterwards so the running process loads the module. Sound choices
and **Follow my theme** are in the [plugin guide](plugins/heinzel-sf/README.md#soundscapes); sound never starts until
you press Play. Remove the plugin with `hz system plugin remove heinzel-sf`.

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
