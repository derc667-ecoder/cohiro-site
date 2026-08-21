# cohiro-site

The static site behind **cohiro.app**, served by GitHub Pages from `main`.

It exists because four separate things need a real HTTPS page on the app's own domain:

- the **privacy policy** URL that both app stores require
- a **public account-deletion** URL, which Google Play requires even though deletion also lives
  in the app
- the **email-confirmation landing page** Supabase redirects to (before this, Site URL was the
  custom scheme `cohiro://`, which a browser cannot render, so a successful confirmation showed a
  blank tab and read as a failure)
- later, **Universal Links / App Links** for invite deep links, which must be served from the
  domain the app claims - which is why these pages are here rather than on niugio.com

## Rules for anything added here

- **No external requests. None.** No web fonts, no analytics, no embeds, no third-party anything.
  Partly ethos, partly law: hotlinking Google Fonts was ruled a GDPR violation by the Munich
  Regional Court in 2022 (3 O 17493/20), and a German company's privacy page is the last place to
  carry a third-party request. The system font stack costs nothing and asks no one for anything.
- Colours come from the app's own tokens (`app/src/theme.ts` in the `listr` repo), so the site and
  the product agree. Dark mode is handled with `prefers-color-scheme`.
- Plain HTML, no build step. Anyone should be able to fix a typo from the GitHub web editor.
- **English lives at the root and German under `/de/`, and that cannot be renegotiated.** There
  is no `/en/` prefix because `/privacy/` and `/terms/` are hardcoded in shipped App Store
  binaries that can never be updated, in both store listings, and in the Google OAuth client
  config - and GitHub Pages cannot issue a server-side 301. A further locale takes the same
  shape: `/fr/`, `/es/`.
- **Every page carries the full `hreflang` set, including a self-reference, and every page
  carries the visible EN/DE switcher in its header.** The two must agree: the link a person
  clicks and the alternate a crawler reads are the same url. `.github/check-hreflang.py` proves
  it - reciprocity, self-reference, canonical agreement, every href resolving to a real file,
  and (with `--live`) every one of them answering 200 on cohiro.app. Run it before you push:
  ```bash
  python3 .github/check-hreflang.py --live
  ```
  The three invite pages are the deliberate exception and carry **no** `hreflang` at all; the
  reason is in their own `<head>`, and the script fails if one ever grows some.
- **`sitemap.xml` is hand-maintained, lists both languages, and lists nothing that is
  `noindex`.** Adding a page means adding an entry with the full `xhtml:link` trio, in both
  directions - a sitemap that lists only the English half quietly tells Google the German half
  is second-class. What belongs in it is decided by the page's own `<meta name="robots">`, never
  by taste, so the five `noindex` pages (`404.html`, the two invite pages, the two `confirmed/`
  pages) stay out. `lastmod` is read out of git, never typed:
  ```bash
  for f in $(python3 -c "import re;print(' '.join(re.findall(r'<loc>https://cohiro.app/(.*?)</loc>',open('sitemap.xml').read())))"); do
    printf '%-24s %s\n' "/$f" "$(git log -1 --format=%cs -- "${f}index.html")"
  done
  ```
  And check it parses before pushing, because a malformed sitemap is silent - Search Console
  rejects it and nothing on the site looks wrong:
  ```bash
  python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('sitemap.xml'); print('sitemap parses')"
  ```
- **No automatic redirect on `navigator.language`, anywhere except the invite page.** An
  auto-redirect overrides a language somebody deliberately chose and destroys the shareability
  of the link they were sent. `/join.js` guesses, and is the documented exception, because its
  reader is a non-user who was handed the link by somebody else - and it still never redirects.
- **`404.html` and `join/index.html` are twins and must stay identical apart from their
  comments.** GitHub Pages serves `404.html` for every real `/join/<CODE>` and
  `/de/join/<CODE>` URL, so a fix applied only to `join/index.html` reaches nobody - which
  is exactly what happened on 2026-08-20. `.github/workflows/invite-twins.yml` now fails
  the build on any drift; run the same check locally with:
  ```bash
  strip() { perl -0777 -pe 's/<!--.*?-->//gs' "$1" | sed '/^[[:space:]]*$/d'; }
  diff -u <(strip join/index.html) <(strip 404.html) && echo OK
  ```

## Related

- App source: the private `listr` repo (CoHiro is the product name, `listr` the internal codename)
- Company site: [niugio.com](https://niugio.com) / [`niugio-site`](https://github.com/derc667-ecoder/niugio-site)
