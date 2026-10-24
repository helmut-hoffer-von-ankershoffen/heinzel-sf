# AGENTS.md

Instructions for coding agents and humans working on heinzel-sf: SF's private Heinzelmännchen plugins, one per layer
in `plugins/<name>/`, in one `uv` workspace.

## Conventions are Heinzelmännchen's

Follow the public core's [AGENTS.md](https://github.com/helmut-hoffer-von-ankershoffen/heinzel/blob/main/AGENTS.md)
and [docs/CODING_STANDARDS.md](https://github.com/helmut-hoffer-von-ankershoffen/heinzel/blob/main/docs/CODING_STANDARDS.md),
and its ADRs on what a plugin is: layers (0040), playbooks (0037), themes (0044), names (0025). The public reference
company [heinzel-acme](https://github.com/helmut-hoffer-von-ankershoffen/heinzel-acme) is the worked example to copy.

1. **Public API only**: import `heinzel` and `heinzel.kernel`, never `heinzel.kernel._*`, `heinzel.modules.*` or
   `heinzel.heads.*`.
2. **Every change is tested** as `unit` or `integration` (offline), `e2e` only against real services; the suite
   refuses anything else.
3. **Conventional commits**, pull requests to `main`, squash merged after CI is green.
4. **Layers**: a layer's module name is its path from the root joined with `-` (`sf`, `sf-<org>`, `sf-<org>-<team>`);
   its distribution is `heinzel-<name>`; it declares `module.layer(parent=..., site=...)` and lists the parent's plugin
   as a dependency. Users always read "plugin", never "package".

## Confidentiality

This repository is private. Keep the company abbreviated as SF/sf in code, names and commits; the vendor's products
may be named in its docs. Nothing from here goes into the public core, its issues, pull requests or commits: not this
repository's name, nor its content.

## Commands

| Task | Command |
| --- | --- |
| Install everything | `make setup` |
| Everything CI checks | `make check` (`make lint`, `make typecheck`, `make test`) |
| Fix what tools can fix | `make fix` |
| Try it | see README.md, "Install" |

## Map

```
plugins/heinzel-sf/      the company layer (root): module `sf`
  src/heinzel_sf/        __init__.py (module, layer, theme, operations), _models.py, _service.py
  src/heinzel_sf/themes/ sf.toml, the web app theme
  tests/                 unit/, integration/ (Heinzelmännchen's CLI head with the real entry point)
pyproject.toml           the workspace: members, the pinned Heinzelmännchen, ruff, mypy, pytest
```
