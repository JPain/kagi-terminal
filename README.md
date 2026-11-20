# Kagi Terminal

A phosphor-green terminal theme for [Kagi Search](https://kagi.com): black screen, monospace
type, `>` prompts on result titles, inverse-video hover, and faint scanlines. Inspired by
DuckDuckGo's Terminal theme; Kagi has no built-in equivalent, but it does let you add your
own CSS.

<!-- screenshots: home and results page, green and amber -->

## Install

1. Copy everything in [`kagi-terminal.css`](kagi-terminal.css).
2. On Kagi, open **Settings → Appearance → [Custom CSS](https://kagi.com/settings/custom_css)**.
3. Turn on **Enable Custom CSS**, paste, and click **Apply Custom CSS**.

It works with any of Kagi's own themes selected (Light, Dark, Moon Dark, Calm Blue).
If something ever looks broken, add `&no_css` to a search URL to see Kagi without it.

## Options

All the settings are variables at the top of the file.

- **Palette.** Green phosphor by default. Amber and white-on-black palettes are included
  as commented blocks: uncomment one to use it.
- **Font.** Your system's monospace font. For a chunkier, bitmap-style look, uncomment the
  `@import` line for [VT323](https://fonts.google.com/specimen/VT323) and add `"VT323"` to the
  front of `--t-font`.
- **Effects.** `--t-glow` (text glow on titles), `--t-scanlines` (scanline strength) and
  `--t-images` (a filter on photos; a full green-monochrome filter is in the comment). Each
  notes the value that turns it off.

Glow and scanlines turn off by themselves if your system asks for more contrast, and
animations stop if it asks for reduced motion.

## How it works

Kagi draws almost everything from its own CSS variables (`--app-bg`, `--search-result-title`,
`--primary-*` and so on), which its themes set on classes such as `.theme_dark`. This theme
sets the same variables on the same classes with a phosphor palette, so widgets, menus and
dialogs follow along without the theme having to know their markup. A short list of
structural rules adds the terminal touches: monospace everywhere, square corners, no shadows,
the `>` prompt, inverse-video hover and selection, dashed rules between results.

## Testing

`test/check.py` downloads Kagi's current theme stylesheet, loads it with this theme under
each of Kagi's theme classes in light and dark mode, and checks the colours that come out. It
needs Python with [Playwright](https://playwright.dev/python/):

```sh
python test/check.py      # cascade check against Kagi's live stylesheet
python test/shot.py       # renders test/mock.html, a hand-made page using Kagi's class names
```

The mock is only a quick look; real Kagi pages need a signed-in account to check.

## Licence

MIT. Not affiliated with Kagi or DuckDuckGo.
