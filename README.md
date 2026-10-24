# heinzel-sf

Private [Heinzelmännchen](https://github.com/helmut-hoffer-von-ankershoffen/heinzel) (`hz`) plugins for SF: the
company's layers (heinzel ADR 0040), one plugin per layer in [`plugins/`](plugins/), in one `uv` workspace, laid out
like the public reference company [heinzel-acme](https://github.com/helmut-hoffer-von-ankershoffen/heinzel-acme).

| Plugin | Layer | What it brings |
| --- | --- | --- |
| [`heinzel-sf`](plugins/heinzel-sf/) | company (root, no parent) | `hz sf info`; the web app theme `sf`, after the vendor's web console |

Org, site and team layers (`sf-<org>`, `sf-<site>`, `sf-<org>-<team>`) come later, as further plugins in
`plugins/` that name their parent with `module.layer(parent=...)` and list it as a dependency.

## Install

The repository is private, so git needs read access to it (`gh auth login`, or any git credential helper). The
plugin needs a Heinzelmännchen whose themes have type scale, density and font files (heinzel #73, after 0.3.0);
until that is merged and released, install the core from its branch (`@main` once it is merged):

```sh
uv tool install --force "heinzel @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel@feat/theme-type-density-fonts"
hz system plugin add "heinzel-sf @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf#subdirectory=plugins/heinzel-sf"
hz system theme use sf
```

`hz system plugin add` keeps the installed core and every other plugin and adds this one to the `uv tool`
environment. The same in one `uv` command:

```sh
uv tool install --force "heinzel @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel@feat/theme-type-density-fonts" \
  --with "heinzel-sf @ git+https://github.com/helmut-hoffer-von-ankershoffen/heinzel-sf#subdirectory=plugins/heinzel-sf"
```

Pin a revision with `heinzel-sf.git@<sha>` before `#subdirectory`. Remove it with `hz system plugin remove heinzel-sf`.

## Develop

```sh
make setup   # uv sync: the workspace, Heinzelmännchen (pinned in pyproject.toml) and the dev tools
make check   # ruff, mypy, pytest: what CI runs
```

Conventions are Heinzelmännchen's: see [AGENTS.md](AGENTS.md).

## Licence

Proprietary, all rights reserved: see [LICENSE](LICENSE).
