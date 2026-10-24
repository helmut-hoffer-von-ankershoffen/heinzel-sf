# heinzel-sf

SF's company layer for [Heinzelmännchen](https://github.com/helmut-hoffer-von-ankershoffen/heinzel) (`hz`): the root
of SF's layers (heinzel ADR 0040, no parent). SF's org, site and team layers come later as sibling plugins in this
repository that name `sf` as their parent. Private; never published to an index.

## What it brings

- `hz sf info`: this plugin, its version, its modules and its themes; also a section in `hz system info`.
- The web app theme **`sf`** (heinzel ADR 0044), in [`src/heinzel_sf/themes/sf.toml`](src/heinzel_sf/themes/sf.toml),
  offered with `module.theme(...)`. It makes `hz ui` look like the vendor's web console, Snowsight:

  ```sh
  hz system theme list        # sf is listed, from heinzel-sf
  hz system theme use sf      # writes [system.theme] name = "sf" to your user config
  hz ui
  ```

## The theme

Dark is measured from Snowsight; light is derived to match it.

| Token | Dark | Light | Where it comes from |
| --- | --- | --- | --- |
| background, card | `#16181d` | `#ffffff` | measured: page and cards |
| sidebar | `#191e24` | `#f6f8fa` | measured: the navigation |
| foreground | `#d7dbe1` | `#1d232b` | measured: body text |
| muted_foreground | `#979fab` | `#5e6876` | measured: secondary text |
| border | `#23272c` | `#e2e6eb` | measured: card and panel hairlines |
| primary / primary_foreground | `#2365d1` / `#ffffff` | same | measured: primary buttons |
| accent | `#233554` | `#e4edfb` | measured: the active navigation item |
| ring | `#2365d1` | `#2365d1` | the primary blue |
| muted, popover, input | `#1c2027`, `#1c2027`, `#2d333b` | `#f2f4f7`, `#ffffff`, `#d3d9e0` | derived |
| ok, warn, bad | `#4cb782`, `#e3a53c`, `#ef6461` | `#16794a`, `#9a5b00`, `#c4302b` | derived, tuned to the palette |

Fonts: `Inter, -apple-system, system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` (the console's stack;
fonts are the machine's own, so without Inter installed the system font is used) and a system monospace stack.
Radius `0.5rem` (8px, the console's cards), border `1px`.

### Not themeable yet

A theme is colours, fonts, a radius and a border width; the rest of the console's look is layout, which hz's themes
don't reach (yet):

- the collapsed **64px icon rail** for navigation (logo, expand toggle, grouped icons, bell and avatar at the bottom);
- the **floating chat launcher**: the assistant panel on the right collapses to a blue button at the right edge;
- the **top gradient** of the main area (fading into `#181e26` over a faint diagonal pattern), and no header bar;
- the console's **6px control radius** next to the 8px card radius (hz has one radius), translucent secondary
  buttons, the 14px base font size, and the lighter blue (`#71aaff`) of active tabs and the active item's text (hz has
  no accent-foreground token).

## Install

See the [repository README](../../README.md#install).

## Develop

From the repository root: `make check` (lint, types, tests). The tests are `unit` (the theme as Heinzelmännchen
validates it) and `integration` (Heinzelmännchen's CLI head with the real entry point: `hz system theme list` and
`use`).
