#!/usr/bin/env python3
"""Prove no page on this site claims that the members of a household live together.

THE RULE. A CoHiro household does not require anybody to cohabit. It can be a couple in two
flats, family in different cities, or friends who share one list. Copy that says "the people
you live with" / "alle, die zusammenwohnen" is therefore not a tone problem: it asserts a
living arrangement the product does not know about and does not require, it narrows the
audience of the marketing pages to a fraction of the people the app is for, and on the privacy
policy it names a SMALLER set of readers than the one that can actually read your notes.

WHY A SCRIPT AND NOT A READING. This exact claim has now been written three times by three
different people who all agreed with the rule, because "the people you live with" is simply
what English reaches for when it means "household". It came back once already after being
fixed (the invite page, 45f2d85: the first fix replaced a wrong phrase with a differently
wrong one). A rule that lives in a review comment is re-litigated every time somebody
"improves" a sentence; this one fails a build instead.

WHAT IT READS, and the counts are printed on every run because a scanner that quietly sees
fewer files than you think reports less work, and less work is indistinguishable from progress:

  * every .html and .js file in the repo, .git and .github excluded.
  * INCLUDING THE HTML COMMENTS. This is the deliberate difference from check-hreflang.py,
    which strips them. index.html's og comment stated the belief in prose ("CoHiro spreads by
    one person telling the people they live with") while the copy beneath it was being fixed,
    and a comment that teaches a mistake re-teaches it to the next person. The cost of that
    choice is that this file's own rules cannot be quoted in an html comment - which is why
    the rule is written out in README.md, a file this script does not read.

WHAT IT DOES NOT READ, stated so the gap is a decision: .md (see above), and everything with
no prose in it - the css, the sitemap, robots.txt, the two .well-known files. The app's own
strings are not here at all; they live in the private listr repo's i18n catalog, and the same
rule applies to them by hand.

TWO SCOPES, because the same words are not wrong in the same places:

  1. EVERY FILE: the cohabiting claim itself, in English and German.
  2. THE INVITE FAMILY ONLY: "from your household" / "aus deinem Haushalt". Those pages are
     read by somebody who is NOT a member yet - being invited in is the entire reason they
     are there - so addressing them as a member is false in the other direction. Which files
     those are is DERIVED, never listed: a page is invite-family if it loads /join.js, plus
     join.js itself, which holds the German catalog. A hand-written list would go stale and
     its staleness would report as success.

THERE IS DELIBERATELY NO ALLOWLIST. If you are trying to say the app does NOT require people
to live together, say it positively - "wherever they live", "egal wo sie wohnen" - which is
shorter than the negation and does not plant the idea in the reader's head on the way past.

    python3 .github/check-copy-claims.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANNED_SUFFIXES = (".html", ".js")

RE_JOIN_JS = re.compile(r'<script\s+src="/join\.js"')

WHY_COHABITING = (
    "A CoHiro household does not require anybody to live together: a couple in two flats, "
    "family in different cities and friends sharing one list are all households in this app. "
    "This sentence asserts a living arrangement the product does not know about."
)
FIX_COHABITING = (
    'Name who shares the list, not where they sleep: "the other members of your household" / '
    '"die anderen Mitglieder deines Haushalts", or "wherever they live" / "egal wo sie wohnen" '
    "when the point is that it does not matter. Addressing somebody who is not a member yet, "
    "say what is being shared and make no claim about the sender at all."
)

WHY_NOT_A_MEMBER = (
    "The invite pages are read by somebody who is NOT in the household yet - being invited "
    "into it is the entire reason they are on that page - so any phrasing that treats the "
    "reader as an existing member is false."
)
FIX_NOT_A_MEMBER = (
    'Make no claim about the sender: "Someone wants to share a shopping list and household '
    'inventory with you on CoHiro." / "Jemand möchte bei CoHiro eine Einkaufsliste und einen '
    'Vorrat mit dir teilen." The <h1> above already establishes that this is an invite.'
)

# Each pattern carries the strings it MUST catch and the strings it MUST NOT, and self_test()
# runs them on every invocation. A regex that has quietly stopped matching anything is the
# failure mode this whole file exists to avoid, and it cannot be seen in a green run.
RULES = [
    {
        "id": "cohabiting",
        "rule": "CoHiro copy must not claim that household members live together.",
        "why": WHY_COHABITING,
        "fix": FIX_COHABITING,
        "scope": "all",
        "patterns": [
            {
                "name": "live/lives/living/lived with",
                "re": re.compile(r"\bliv(?:e|es|ed|ing)\s+with\b", re.I),
                "catches": [
                    "A shared shopping list and household inventory for the people you live with.",
                    "Invite the people you live with, and everyone has the same rights",
                    "the people you\n  live with put into your shared list",
                    "a note that you would not want the people you live with to read",
                    "one person telling the people they live with",
                ],
                "permits": [
                    "Your account and everything in it must live within the European Union.",
                    "Invite people into your household, wherever they live, and every member",
                    "The other members of your household cannot see it.",
                ],
            },
            {
                "name": "live/living together",
                "re": re.compile(r"\bliv(?:e|es|ed|ing)\s+together\b", re.I),
                "catches": ["for people who live together", "Living Together"],
                "permits": ["Everything you add lives in one shared list."],
            },
            {
                "name": "under the same/one roof",
                "re": re.compile(r"\bunder\s+(?:the\s+same|one)\s+roof\b", re.I),
                "catches": ["a shopping list for everyone under one roof"],
                "permits": ["Everything the household adds sits under the same heading."],
            },
            {
                "name": "zusammenwohnen / zusammenleben (one word)",
                "re": re.compile(r"zusammen(?:wohn|leb)\w*", re.I),
                "catches": [
                    "ein gemeinsamer Vorrat für alle, die zusammenwohnen.",
                    "Lade die Menschen ein, mit denen du zusammenwohnst.",
                    "die Menschen, mit denen\ndu zusammenlebst, nicht lesen sollen",
                    "Jemand, mit dem du zusammenwohnst",
                    "das Zusammenleben im Haushalt",
                ],
                "permits": [
                    "Lade Menschen in deinen Haushalt ein, egal wo sie wohnen.",
                    "Alle Mitglieder tragen zusammen ein, was fehlt.",
                    "Kurz zusammengefasst: es gibt keine Werbung.",
                ],
            },
            {
                "name": "zusammen wohnen / zusammen leben (spaced)",
                "re": re.compile(r"\bzusammen\s+(?:wohn|leb)(?:en|st|t|e)\b", re.I),
                "catches": [
                    "für alle, die zusammen wohnen",
                    "Menschen, die zusammen leben",
                ],
                "permits": ["Wir haben das zusammen lebendig gemacht."],
            },
            {
                "name": "leben/wohnen zusammen",
                "re": re.compile(r"\b(?:leb|wohn)(?:e|st|t|en)\s+zusammen\b", re.I),
                "catches": [
                    "Menschen, die hier leben zusammen mit dir",
                    "ihr wohnt zusammen",
                ],
                "permits": [
                    "Ihr tragt zusammen ein, was fehlt.",
                    "Wir fassen das zusammen.",
                ],
            },
            {
                "name": "unter einem Dach",
                "re": re.compile(r"\bunter\s+einem\s+Dach\b", re.I),
                "catches": ["eine Liste für alle unter einem Dach"],
                "permits": ["Alles unter einem Namen."],
            },
        ],
    },
    {
        "id": "not-a-member-yet",
        "rule": "The invite pages must not address their reader as a member of the household.",
        "why": WHY_NOT_A_MEMBER,
        "fix": FIX_NOT_A_MEMBER,
        "scope": "invite",
        "patterns": [
            {
                "name": "from your household",
                "re": re.compile(r"\bfrom\s+(?:your|the)\s+household\b", re.I),
                "catches": ["Someone from your household has invited you"],
                "permits": ["Whoever runs a household can remove members from it."],
            },
            {
                "name": "aus deinem/eurem/Ihrem Haushalt",
                "re": re.compile(r"\baus\s+(?:deinem|eurem|Ihrem)\s+Haushalt\b", re.I),
                "catches": ["Jemand aus deinem Haushalt hat dich eingeladen"],
                "permits": [
                    "Ein Einladungscode lässt jeden, der ihn hat, deinem Haushalt beitreten.",
                    "niemand in deinem Haushalt kann sie sehen",
                ],
            },
        ],
    },
]


def self_test():
    """The measurer, measured. Runs before anything is scanned, every single time.

    Every "permits" string is tested against EVERY pattern, not just its own: a new pattern
    that would redden a sentence some other rule already declared good is the way a check of
    this shape turns into one people switch off.
    """
    bad = []
    innocent = [(r["id"], p["name"], s)
                for r in RULES for p in r["patterns"] for s in p["permits"]]
    for rule in RULES:
        for pat in rule["patterns"]:
            for s in pat["catches"]:
                if not pat["re"].search(s):
                    bad.append("%s / %s: fails to catch %r" % (rule["id"], pat["name"], s))
            for owner_rule, owner_pat, s in innocent:
                m = pat["re"].search(s)
                if m:
                    bad.append("%s / %s: fires on innocent text %r (matched %r; that fixture "
                               "is listed under %s / %s)"
                               % (rule["id"], pat["name"], s, m.group(0), owner_rule, owner_pat))
    if bad:
        print("check-copy-claims: THE PATTERNS THEMSELVES ARE WRONG. Nothing was scanned.\n")
        for b in bad:
            print("  - %s" % b)
        print("\nEvery pattern above carries the strings it must catch and the strings it must")
        print("leave alone. Fix the pattern, or fix the fixture if the copy has legitimately")
        print("changed - but never delete a fixture to make this pass.\n")
        sys.exit(2)
    return sum(len(r["patterns"]) for r in RULES)


def scanned_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".github")]
        for name in filenames:
            if name.endswith(SCANNED_SUFFIXES):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def excerpt(text, start, end):
    """The offending phrase in enough of its line to be recognisable, wrapping collapsed."""
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    line_end = len(text) if line_end == -1 else line_end
    before = re.sub(r"\s+", " ", text[line_start:start])[-45:]
    hit = re.sub(r"\s+", " ", text[start:end])
    after = re.sub(r"\s+", " ", text[end:line_end])[:45]
    return "%s>>> %s <<<%s" % (before, hit, after)


def main():
    n_patterns = self_test()

    files = scanned_files()
    html = [f for f in files if f.endswith(".html")]
    js = [f for f in files if f.endswith(".js")]
    if not files:
        sys.exit("check-copy-claims: found no files to scan at all. Wrong ROOT?")

    texts = {f: open(os.path.join(ROOT, f), encoding="utf-8").read() for f in files}
    invite = sorted([f for f in html if RE_JOIN_JS.search(texts[f])]
                    + [f for f in js if os.path.basename(f) == "join.js"])

    findings = []
    for rule in RULES:
        targets = invite if rule["scope"] == "invite" else files
        for rel in targets:
            text = texts[rel]
            for pat in rule["patterns"]:
                for m in pat["re"].finditer(text):
                    findings.append({
                        "file": rel,
                        "line": text.count("\n", 0, m.start()) + 1,
                        "phrase": re.sub(r"\s+", " ", m.group(0)),
                        "excerpt": excerpt(text, m.start(), m.end()),
                        "rule": rule,
                        "pattern": pat["name"],
                    })
    findings.sort(key=lambda f: (f["file"], f["line"]))

    print("  files scanned         %d  (%d html, %d js)" % (len(files), len(html), len(js)))
    for rel in files:
        print("      %-26s %6d bytes" % (rel, len(texts[rel].encode("utf-8"))))
    print("  invite family         %d  %s" % (len(invite), ", ".join(invite)))
    print("  patterns              %d, across %d rule(s)" % (n_patterns, len(RULES)))

    # Non-vacuity, stated rather than assumed. A check of this shape can only fail by seeing
    # too little, and seeing too little looks exactly like having nothing to report.
    if len(html) < 5:
        sys.exit("\ncheck-copy-claims: only %d html files were found. This site has more than "
                 "that; something is not being seen and a green run here would mean nothing."
                 % len(html))
    if not invite:
        sys.exit("\ncheck-copy-claims: no file loads /join.js and there is no join.js, so the "
                 "invite-scope rule scanned nothing. Either the invite pages moved or the way "
                 "this script finds them has gone stale.")

    if findings:
        print("\nFAIL: %d occurrence(s) of copy this site does not allow.\n" % len(findings))
        for f in findings:
            print('  %s:%d  "%s"   [%s / %s]'
                  % (f["file"], f["line"], f["phrase"], f["rule"]["id"], f["pattern"]))
            print("      %s" % f["excerpt"])
        seen = []
        for f in findings:
            if f["rule"]["id"] not in seen:
                seen.append(f["rule"]["id"])
                print("\n  RULE  %s" % f["rule"]["rule"])
                print("  WHY   %s" % f["rule"]["why"])
                print("  FIX   %s" % f["rule"]["fix"])
        print("\n  There is no allowlist and adding one is not the fix. If the sentence is "
              "trying to say\n  the app does NOT require living together, say it positively "
              '("wherever they live",\n  "egal wo sie wohnen"): it is shorter than the negation '
              "and does not plant the idea.\n  The rule is also written down in README.md.\n")
        return 1

    print("\nOK: %d files, %d patterns, no page claims that household members live together.\n"
          % (len(files), n_patterns))
    return 0


if __name__ == "__main__":
    sys.exit(main())
