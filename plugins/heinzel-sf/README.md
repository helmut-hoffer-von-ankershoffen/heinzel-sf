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

Both modes are measured from Snowsight.

| Token | Dark | Light | Where it comes from |
| --- | --- | --- | --- |
| background, card | `#16181d` | `#ffffff` | measured: page and cards |
| sidebar | `#191e24` | `#ffffff` | measured: the navigation (light: white with a hairline right border, `#d7dae0`) |
| foreground | `#d7dbe1` | `#23272c` | measured: body text |
| muted_foreground | `#979fab` | `#626c7e` | measured: secondary text |
| border | `#23272c` | `#d7dbe1` | measured: card and panel hairlines |
| muted | `#1c2027` | `#eeeff1` | light measured: hover and quiet panels (the trial card); dark derived |
| primary / primary_foreground | `#2365d1` / `#ffffff` | `#276ee1` / `#ffffff` | measured: primary buttons |
| accent | `#233554` | `#e3efff` | measured: the active navigation item |
| accent_foreground | `#71aaff` | `#2365d1` | measured: the active item's text and icon, links |
| icon | `#d7dbe1` | `#23272c` | measured: navigation icons are in the text colour |
| ring | `#2365d1` | `#276ee1` | the primary blue |
| popover, input | `#1c2027`, `#2d333b` | `#ffffff`, `#ffffff` | dark derived; light measured |
| main_tint | none | `#eef5fd` | light measured: the tint at the top of the main area, fading to white |
| ok, warn, bad | `#4cb782`, `#e3a53c`, `#ef6461` | `#16794a`, `#9a5b00`, `#c4302b` | derived; light at least 4.5:1 on white |

Type and density, measured from the console: text `14px` (`font_size`), secondary text `12px` (`font_size_small`),
headings weight `550` with `-0.5px` tracking, navigation rows `30px` (`row_height`), icons `16px` (`icon_size`),
spacing step `0.25rem`; radius `0.375rem` (6px) for controls and navigation items (`radius_control`) and `0.5rem`
(8px) for cards and dialogs (`radius`); border `1px`.

Fonts: `Inter, -apple-system, system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` (the console's stack) and a
system monospace stack. Inter ships with the theme, so `hz ui` looks the same without it installed.

### Inter

[`src/heinzel_sf/themes/fonts/`](src/heinzel_sf/themes/fonts/) holds Inter 4.1's variable fonts as woff2,
`InterVariable.woff2` and `InterVariable-Italic.woff2` (weights 100 to 900), unchanged from the official release
[`Inter-4.1.zip`](https://github.com/rsms/inter/releases/tag/v4.1) (its `web/` folder). The release publishes no
checksum; the upright file matches the copy on the Inter site byte for byte. SHA-256:

| File | SHA-256 |
| --- | --- |
| `Inter-4.1.zip` | `9883fdd4a49d4fb66bd8177ba6625ef9a64aa45899767dde3d36aa425756b11e` |
| `InterVariable.woff2` | `693b77d4f32ee9b8bfc995589b5fad5e99adf2832738661f5402f9978429a8e3` |
| `InterVariable-Italic.woff2` | `e564f652916db6c139570fefb9524a77c4d48f30c92928de9db19b6b5c7a262a` |

Inter is © The Inter Project Authors, licensed under the SIL Open Font License 1.1:
[`fonts/LICENSE.txt`](src/heinzel_sf/themes/fonts/LICENSE.txt), shipped in the wheel next to the fonts. The theme
declares them as `[[fonts]]`; the web app serves them from its own origin at `/theme-fonts/sf/<n>.woff2`.

### Logo

`[logo]` in the theme names [`logo/wordmark-light.svg`](src/heinzel_sf/themes/logo/wordmark-light.svg) (mark and word)
and [`logo/mark.svg`](src/heinzel_sf/themes/logo/mark.svg) (the square mark, for the collapsed rail), `alt`
"Snowflake", `24px` high: cleaned single-colour SVGs in the vendor's `#2cb6e8`, which reads on both sidebars, so dark
uses the light file. The web app serves them from its own origin at `/theme-assets/sf/<light|dark|mark>.svg`.

### Not themeable yet

A theme is colours, fonts, type scale, density, radii and a border width; the rest of the console's look is layout,
which hz's themes don't reach (yet):

- the collapsed **64px icon rail** for navigation (logo, expand toggle, grouped icons, bell and avatar at the bottom);
- the **floating chat launcher**: the assistant panel on the right collapses to a blue button at the right edge;
- the **top gradient** of the main area (fading into `#181e26` over a faint diagonal pattern), and no header bar;
- translucent secondary buttons.

## Install

See the [repository README](../../README.md#install).

## Develop

From the repository root: `make check` (lint, types, tests). The tests are `unit` (the theme as Heinzelmännchen
validates it, its font files) and `integration` (Heinzelmännchen's CLI head with the real entry point:
`hz system theme list` and `use`; the wheel, built in-process, carries the fonts and their licence).

The theme dresses the core Heinzelmännchen for winter, with a snowy cap and frosty scarf. Personal hat and shirt
colours keep precedence; age, beard, build, state and accessories continue to work. This needs the core's optional
`[heinzel]` theme table (ADR 0064), included from hz 0.7.2.
