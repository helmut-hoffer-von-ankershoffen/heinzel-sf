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
  src/heinzel_sf/soundscapes/  sf-snow.toml, sf-fireplace.toml: the sound streams
  src/heinzel_sf/themes/ sf.toml, the web app theme
  src/heinzel_sf/themes/fonts/  Inter woff2 files and their licence
  src/heinzel_sf/themes/logo/   the theme's SVG logos
  tests/                 unit/, integration/ (Heinzelmännchen's CLI head with the real entry point)
.github/workflows/       ci.yml (the checks), release.yml (the private GitHub release)
pyproject.toml           the workspace: members, a compatible Heinzelmännchen range, ruff, mypy, pytest
```

## Releasing

Releases go through a pull request. Nothing is tagged or published until you tag.

1. Update the plugin version, `uv.lock` and [CHANGELOG.md](CHANGELOG.md); run `make check`.
2. Review the whole diff. Merge only when CI is green.
3. Tag the merged main commit `vX.Y.Z`.

The Release workflow then checks the tag against the version, that the repository is private and that the commit is on
main. It runs the full checks, builds the wheel and source archive, and attaches them to this repository's GitHub
release. It never overwrites a tag or release and never uploads to a public index. If publishing fails, diagnose it,
then dispatch the workflow again for the same tag.
