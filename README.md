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

## Related

- App source: the private `listr` repo (CoHiro is the product name, `listr` the internal codename)
- Company site: [niugio.com](https://niugio.com) / [`niugio-site`](https://github.com/derc667-ecoder/niugio-site)
