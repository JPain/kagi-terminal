"""Cascade check: Kagi's real theme stylesheet, then this theme, for every Kagi theme class."""
import asyncio, pathlib, re, sys, urllib.request
from playwright.async_api import async_playwright
here = pathlib.Path(__file__).parent

def fetch_kagi_css():
    """Download Kagi's current theme + framework stylesheets (not committed: they are Kagi's)."""
    ua = {'User-Agent': 'Mozilla/5.0 (kagi-terminal test)'}
    page = urllib.request.urlopen(urllib.request.Request('https://kagi.com/search?q=test', headers=ua)).read().decode()
    for name in ('kagi_themes.scss.css', 'main.scss.css'):
        path = re.search(r'href="(/asset/[^"]*/' + re.escape(name) + ')"', page).group(1)
        css = urllib.request.urlopen(urllib.request.Request('https://kagi.com' + path, headers=ua)).read()
        (here / name).write_bytes(css)
        print('fetched', path)

fetch_kagi_css()
css = (here.parent / 'kagi-terminal.css').read_text()
THEMES = ['theme_light', 'theme_dark', 'theme_moon_dark', 'theme_calm_blue', 'theme_dark_conditional', 'theme_moon_dark_conditional', '']
PAGE = """<!doctype html><html class="{cls}"><head>
<link rel=stylesheet href="kagi_themes.scss.css"><link rel=stylesheet href="main.scss.css">
<style>{css}</style>
<style>.t{{color:var(--search-result-title)}} .u{{color:var(--search-result-url-link)}} .s{{color:var(--search-result-content-text)}}
.bg{{background:var(--app-bg)}} .l{{color:var(--link)}} .p25{{background:var(--primary-25)}} .c1000{{background:var(--chrome-1000)}}</style>
</head><body class="{cls}"><div class="t">t</div><div class="u">u</div><div class="s">s</div><div class="bg">b</div>
<div class="l">l</div><div class="p25">p</div><div class="c1000">c</div></body></html>"""
WANT = {'.t': ('color', 'rgb(57, 255, 106)'), '.u': ('color', 'rgb(79, 160, 91)'), '.s': ('color', 'rgb(143, 227, 154)'),
        '.bg': ('backgroundColor', 'rgb(0, 0, 0)'), '.l': ('color', 'rgb(57, 255, 106)'),
        '.p25': ('backgroundColor', 'rgb(5, 13, 6)'), '.c1000': ('backgroundColor', 'rgb(0, 0, 0)'),
        'body': ('fontFamily', None)}
async def main():
    bad = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for scheme in ['light', 'dark']:
            p = await b.new_page(color_scheme=scheme)
            for cls in THEMES:
                f = here / 'page.html'; f.write_text(PAGE.format(cls=cls, css=css))
                await p.goto(f.as_uri())
                for sel, (prop, want) in WANT.items():
                    got = await p.eval_on_selector(sel, f'e => getComputedStyle(e).{prop}')
                    ok = ('monospace' in got) if want is None else got == want
                    bad += not ok
                    if not ok: print(f'FAIL {scheme:5} {cls or "(none)":28} {sel:6} {got} != {want}')
            await p.close()
        await b.close()
    print('all ok' if not bad else f'{bad} failures'); sys.exit(bool(bad))
asyncio.run(main())
