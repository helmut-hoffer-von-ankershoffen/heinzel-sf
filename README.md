# SF for Heinzelmännchen

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/helmut-hoffer-von-ankershoffen/heinzel/main/docs/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/helmut-hoffer-von-ankershoffen/heinzel/main/docs/assets/hero-light.svg" alt="A small crowd of Heinzelmännchen helpers walking together" width="860">
  </picture>
</p>

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
curl -LsSf https://heinzel.team/install.sh | sh
```

Windows may work, but is not supported. Details: the
[standard app installation guide](https://heinzel.team/guides/install/).

This plugin lives in a private repository, so it also needs [Git](https://git-scm.com/install/) and the
[GitHub CLI](https://cli.github.com/), signed in with an account that may read it. In a second terminal:

```sh
gh auth login
gh auth setup-git
hz system plugin add git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf --confirm
hz system theme use sf
```

The installer resolves the plugin's metadata and source itself, checks that it fits your Heinzelmännchen, and keeps the
app and its other plugins. Restart the web app afterwards so the running process loads the module. Sound choices
and **Follow my theme** are in the [plugin guide](plugins/heinzel-sf/README.md#soundscapes); sound never starts until
you press Play. Remove the plugin with `hz system plugin remove heinzel-sf`.

## Develop

```sh
make setup   # uv sync: the workspace, the compatible SDK resolved in uv.lock, and the dev tools
make check   # ruff, mypy, pytest: what CI runs
```

Conventions are Heinzelmännchen's: see [AGENTS.md](AGENTS.md).

## Releases

Needs Heinzelmännchen 0.7.2 or newer, below 1. Plugin versions follow their own SemVer and need not match hz.
[CHANGELOG.md](CHANGELOG.md) lists each release. Maintainers: see "Releasing" in [AGENTS.md](AGENTS.md#releasing).

## Licence

Proprietary, all rights reserved: see [LICENSE](LICENSE).
