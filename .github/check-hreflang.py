#!/usr/bin/env python3
"""Prove the two language versions of this site actually point at each other.

WHY A SCRIPT AND NOT A READING. A wrong hreflang is invisible: no user sees it, no page looks
broken, nothing 404s. It is read only by crawlers, and the way you find out it was wrong is
that the German pages quietly never rank. That is the exact shape of defect a human review
cannot catch and a machine catches every time, so this is the check and the reading is not.

WHAT IT ASSERTS, all of it on EVERY html file in the repo:

  1. EVERY PAGE IS CLASSIFIED. A file either carries a full alternate set or it loads /join.js
     and must carry none - there is no third state, and no file may fall out of both lists.
     This is what stops the whole check passing vacuously: deleting every alternate on the
     site does not empty the work, it moves twelve files into the wrong bucket and reddens.
  2. THE SELF-REFERENCE EXISTS AND MATCHES THE CANONICAL BYTE FOR BYTE. An annotation set that
     does not name its own page is discarded whole, and a canonical that disagrees with the
     self-reference is two contradictory claims about the same document.
  3. THE CANONICAL IS THE PAGE'S OWN URL, derived from where the file sits, so a copy-pasted
     head cannot leave one page claiming to be another.
  4. RECIPROCITY. If A names B as its de alternate, B must name A as its en alternate. The
     strongest form of that is the one used here: every page in a cluster must carry the
     IDENTICAL set. A one-way alternate is the classic silent error and it is what this line
     exists for.
  5. x-default IS THE ENGLISH URL. English is the root of this site and cannot move: /privacy/
     and /terms/ are hardcoded in shipped store binaries and in the Google OAuth client, and
     GitHub Pages cannot issue a 301.
  6. NO ALTERNATE THAT DOES NOT EXIST. Every href must resolve to a real file in this repo...
  7. ...AND, with --live, must answer 200 on cohiro.app with no redirect. That is the far side
     of the repo/production boundary; the file existing here proves only that it was written.
  8. THE VISIBLE SWITCHER AGREES WITH THE INVISIBLE ONE. The header's language link must point
     at exactly the alternate the head declares, so the thing a person clicks and the thing a
     crawler reads can never diverge.

ADDING A LOCALE. Add the pages, add one line to ENDONYMS below, and add the third href to
every alternate set. Everything else here is derived from the files, deliberately: a check
that keeps a hand-written list of what to check goes stale, and its staleness reports as
success.

    python3 .github/check-hreflang.py           # structure only, no network
    python3 .github/check-hreflang.py --live    # ...and every url fetched from cohiro.app
"""

import os
import re
import sys
import time
import urllib.error
import urllib.request

ORIGIN = "https://cohiro.app"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The name of each language IN THAT LANGUAGE, which is what the switcher shows. Adding a
# locale means adding a line here; a locale that appears in an hreflang without appearing
# here is named as an error rather than skipped.
ENDONYMS = {"en": "English", "de": "Deutsch"}

RE_HTML_LANG = re.compile(r'<html\s+lang="([^"]+)"')
RE_CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>')
RE_ALTERNATE = re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"\s*/?>')
RE_JOIN_JS = re.compile(r'<script\s+src="/join\.js"')
RE_LANGS_NAV = re.compile(r'<nav class="langs"[^>]*>(.*?)</nav>', re.S)
RE_NAV_LABEL = re.compile(r'<nav class="langs"[^>]*\saria-label="([^"]*)"')
RE_NAV_LINK = re.compile(r'<a\s+href="([^"]+)"\s+hreflang="([^"]+)"\s+lang="([^"]+)">([^<]+)</a>')
RE_NAV_CURRENT = re.compile(r'<span\s+aria-current="true">([^<]+)</span>')

problems = []


def fail(where, msg):
    problems.append("%s: %s" % (where, msg))


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # og-src/ holds the OG-CARD SOURCE TEMPLATES (rendered to og*.png by hand, never
        # served as pages - they have no url, no alternates and no switcher BY DESIGN), so
        # they are not pages this check can hold to page rules. Excluding the directory,
        # not the filenames: the next card source added there must not redden the build
        # either. Added 2026-09-04, when the 2026-09-01 og-card round first put .html files
        # in the repo that are not pages and this job went red on main for three days
        # without anyone noticing - Pages deploys regardless of checks.
        dirnames[:] = [d for d in dirnames if d not in (".git", ".github", "og-src")]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def url_for(relpath):
    """The url a file is served at. 404.html has none, and that is the point of returning None."""
    if relpath == "404.html":
        return None
    if relpath == "index.html":
        return ORIGIN + "/"
    if relpath.endswith("/index.html"):
        return ORIGIN + "/" + relpath[: -len("index.html")]
    return None


def file_for(url):
    """The file a url is served from, or None if this repo has nothing at that url."""
    if not url.startswith(ORIGIN + "/"):
        return None
    path = url[len(ORIGIN) + 1:]
    if path and not path.endswith("/"):
        return None
    rel = (path + "index.html") if path else "index.html"
    return rel if os.path.isfile(os.path.join(ROOT, rel)) else None


def fetch(url, attempts=1, pause=15):
    """200 and no redirect, or a sentence saying what happened instead."""
    last = ""
    for i in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": "cohiro-site-hreflang-check"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status != 200:
                    last = "HTTP %s" % r.status
                elif r.geturl() != url:
                    last = "redirected to %s" % r.geturl()
                else:
                    return None
        except urllib.error.HTTPError as e:
            last = "HTTP %s" % e.code
        except Exception as e:                                  # noqa: BLE001
            last = "%s: %s" % (type(e).__name__, e)
        if i + 1 < attempts:
            time.sleep(pause)
    return last


def main():
    live = "--live" in sys.argv
    attempts = 8 if "--wait-for-deploy" in sys.argv else 1

    files = html_files()
    if not files:
        sys.exit("check-hreflang: found no html files at all. Wrong ROOT?")

    pages = {}       # relpath -> {"lang", "canonical", "alts"}
    exempt = []      # relpath, deliberately unannotated

    for rel in files:
        raw = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        body = strip_comments(raw)
        alts = RE_ALTERNATE.findall(body)
        loads_join_js = bool(RE_JOIN_JS.search(body))

        # ---- 1. every page is classified, and the two states are mutually exclusive
        if loads_join_js:
            exempt.append(rel)
            if alts:
                fail(rel, "loads /join.js and still declares %d rel=alternate link(s). The "
                          "invite pages carry no hreflang on purpose: 404.html is served at "
                          "every non-file path, so it has no url of its own to self-reference, "
                          "and a set that cannot include it cannot be made reciprocal for its "
                          "twins. Delete these, or read the head comment first." % len(alts))
            continue
        if not alts:
            fail(rel, "has no rel=alternate links and does not load /join.js. Every page on "
                      "this site is one or the other. If this is a new page, give it the "
                      "three-line alternate set; if it is a new invite-family page, it should "
                      "be loading /join.js.")
            continue

        lang_m = RE_HTML_LANG.search(body)
        canon_m = RE_CANONICAL.search(body)
        if not lang_m:
            fail(rel, 'no <html lang="..."> attribute')
            continue
        if not canon_m:
            fail(rel, "no canonical link")
            continue

        alt_map = {}
        for lang, href in alts:
            if lang in alt_map:
                fail(rel, 'declares hreflang="%s" twice' % lang)
            alt_map[lang] = href
        pages[rel] = {"lang": lang_m.group(1), "canonical": canon_m.group(1), "alts": alt_map,
                      "raw": raw}

    # ---- per page
    for rel, page in sorted(pages.items()):
        lang, canonical, alts = page["lang"], page["canonical"], page["alts"]
        own = url_for(rel)

        # 3. the canonical is this page's own url
        if own is None:
            fail(rel, "is annotated but is not served at a url this script can derive "
                      "(only index.html files and the root have one)")
        elif canonical != own:
            fail(rel, "canonical is %s but this file is served at %s" % (canonical, own))

        # 2. self-reference present, and identical to the canonical byte for byte
        if lang not in alts:
            fail(rel, 'is lang="%s" but declares no hreflang="%s" self-reference. A set that '
                      "omits its own page is discarded whole." % (lang, lang))
        elif alts[lang] != canonical:
            fail(rel, 'hreflang="%s" self-reference is %s but the canonical is %s. They must '
                      "be the same string, trailing slash included."
                      % (lang, alts[lang], canonical))

        # 5. x-default is the English url
        if "x-default" not in alts:
            fail(rel, "declares no x-default")
        elif "en" not in alts:
            fail(rel, 'declares no hreflang="en"')
        elif alts["x-default"] != alts["en"]:
            fail(rel, "x-default is %s but the English url is %s. English is this site's root "
                      "and is the only correct default." % (alts["x-default"], alts["en"]))

        for alt_lang, href in sorted(alts.items()):
            if alt_lang != "x-default" and alt_lang not in ENDONYMS:
                fail(rel, 'declares hreflang="%s", which is not in ENDONYMS in this script. '
                          "Add it there (the language's name in its own language) so the "
                          "switcher check can see it too." % alt_lang)
            if not href.startswith(ORIGIN + "/"):
                fail(rel, "%s alternate %s is not an absolute cohiro.app url" % (alt_lang, href))
            elif not href.endswith("/"):
                fail(rel, "%s alternate %s has no trailing slash; the rest of the site uses "
                          "slashed urls and the canonical must match this string exactly"
                          % (alt_lang, href))
            # 6. no alternate that does not exist
            elif file_for(href) is None:
                fail(rel, "%s alternate %s does not exist in this repo" % (alt_lang, href))

        # 4. reciprocity, in its strongest form: one cluster, one identical set
        for alt_lang, href in sorted(alts.items()):
            if alt_lang == "x-default" or href == canonical:
                continue
            other_rel = file_for(href)
            if other_rel is None:
                continue                                   # already reported above
            other = pages.get(other_rel)
            if other is None:
                fail(rel, "names %s as its %s alternate, but that page declares no alternates "
                          "at all. hreflang must be reciprocal: a one-way alternate is ignored."
                          % (href, alt_lang))
            elif other["alts"] != alts:
                fail(rel, "names %s as its %s alternate, but that page's alternate set differs.\n"
                          "      here : %s\n      there: %s\n      Every page in a cluster must "
                          "carry the identical set." % (href, alt_lang,
                                                        dict(sorted(alts.items())),
                                                        dict(sorted(other["alts"].items()))))

    # ---- 8. the visible switcher agrees with the head, on every page including the exempt ones
    for rel in files:
        raw = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        body = strip_comments(raw)
        navs = RE_LANGS_NAV.findall(body)
        if len(navs) != 1:
            fail(rel, "has %d <nav class=\"langs\"> switchers; every page gets exactly one"
                      % len(navs))
            continue
        inner = navs[0]
        label = RE_NAV_LABEL.search(body)
        if not label or not label.group(1).strip():
            fail(rel, "the switcher has no aria-label. It is navigation, so it needs a name "
                      "that says what it is.")
        links = RE_NAV_LINK.findall(inner)
        currents = RE_NAV_CURRENT.findall(inner)
        if len(links) != 1 or len(currents) != 1:
            fail(rel, "the switcher has %d link(s) and %d current marker(s); it must have "
                      "exactly one of each, and the current language must not be a link"
                      % (len(links), len(currents)))
            continue
        href, hreflang, anchor_lang, text = links[0]
        if hreflang != anchor_lang:
            fail(rel, 'switcher link has hreflang="%s" but lang="%s"' % (hreflang, anchor_lang))
        if ENDONYMS.get(hreflang) != text:
            fail(rel, 'switcher link to "%s" is labelled %r; it must be %r, the language\'s own '
                      "name" % (hreflang, text, ENDONYMS.get(hreflang)))
        if file_for(ORIGIN + href) is None:
            fail(rel, "switcher link points at %s, which does not exist in this repo" % href)

        page = pages.get(rel)
        if page is None:
            continue                       # invite family: the href is rewritten by /join.js
        if ENDONYMS.get(page["lang"]) != currents[0]:
            fail(rel, 'is lang="%s" but the switcher marks %r as current; it must mark %r'
                      % (page["lang"], currents[0], ENDONYMS.get(page["lang"])))
        declared = page["alts"].get(hreflang)
        if declared != ORIGIN + href:
            fail(rel, "the switcher sends a reader to %s but the head declares the %s "
                      "alternate as %s. The visible control and the invisible one must agree."
                      % (ORIGIN + href, hreflang, declared))

    # ---- 7. the far side
    urls = sorted({href for p in pages.values() for href in p["alts"].values()})
    checked_live = 0
    if live:
        for url in urls:
            why = fetch(url, attempts=attempts)
            checked_live += 1
            print("  %-42s %s" % (url, "200" if why is None else "FAIL - " + why))
            if why:
                fail("live", "%s is declared as an alternate but %s" % (url, why))
    else:
        print("  (structure only: --live not given, so nothing was fetched from cohiro.app)")

    print("")
    print("  html files            %d" % len(files))
    print("  annotated pages       %d" % len(pages))
    print("  invite pages (exempt) %d  %s" % (len(exempt), ", ".join(sorted(exempt))))
    print("  distinct alternate urls %d" % len(urls))
    print("  live urls fetched     %d" % checked_live)

    # Non-vacuity, stated rather than assumed: this file has been wrong before by measuring
    # nothing and saying so cheerfully.
    if len(pages) < 2:
        sys.exit("\ncheck-hreflang: fewer than two annotated pages. Something is not being "
                 "seen; a green run here would mean nothing.")
    if not exempt:
        sys.exit("\ncheck-hreflang: no page loads /join.js. The invite family should be "
                 "exempt-and-present, not absent.")

    if problems:
        print("\nFAIL: %d problem(s).\n" % len(problems))
        for p in problems:
            print("  - %s" % p)
        print("\nA wrong hreflang is invisible to every human who visits the site, which is "
              "why this runs.\n")
        return 1
    print("\nOK: %d pages, every alternate set reciprocal, self-referencing, matching its "
          "canonical%s.\n" % (len(pages), " and live" if live else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
