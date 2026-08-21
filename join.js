// Shared by BOTH invite twins: join/index.html and 404.html. GitHub Pages serves 404.html for
// every /join/<CODE> URL, because that path is not a file; the newer /join/?c=<CODE> form is
// join/index.html itself, a real file. So this one script is what runs on the page visitors
// actually open, whichever of the two shapes the link they were sent happens to be. It used to be
// an inline <script> copied into both files, which is how a fix once landed on only one of them.
//
// Lift the code out of the URL - /join/?c=AB12CD, or the older /join/AB12CD - and show it, so the
// visitor can type it even though the app is not installed. One same-origin static file and
// dependency-free: this site makes no third-party requests, and a page whose whole job is to be
// readable must not need a bundle to work.
//
// The code is displayed only. It is never sent anywhere from this page, and GitHub Pages is
// static, so there is nothing here that could log it.

// THE GERMAN INVITE PAGE CANNOT BE A GERMAN HTML FILE ALONE, so it is this object as well.
// GitHub Pages has exactly one 404.html, at the site root. /de/join/<CODE> is not a file, so the
// OLD path form serves that same English root file, and only a runtime swap can make it German.
// The newer /de/join/?c=<CODE> form does land on de/join/index.html - but that file deliberately
// ships the twins' English markup under a German head (see its own header comment), so the German
// still arrives from here. One catalog, one place, on whichever file got served.
//
// Wording is the app's own German catalog (app/src/locales/de in the listr repo), so the site and
// the product cannot disagree about what things are called: Haushalt, Einkaufsliste, Vorrat
// (never Inventar), Konto, Einladungscode, and the locked verb "beitreten". Register is du.
//
// *Asterisks* mark a <strong>. Two of the steps need one, and the alternative was cutting those
// sentences into five hooks apiece - which the app catalog refuses to do, on the grounds that a
// translator has to be able to reorder a whole sentence. \u00a0 is written as an escape rather
// than typed, because an invisible character in a source file is one nobody can review.
//
// THERE IS NO ESCAPE FOR A LITERAL ASTERISK. A string containing one would split on it and come
// out with the wrong halves bolded, silently. No German string needs one today; a string that
// ever does has to be reworded, or this syntax has to grow an escape first.
var de = {
  skip: 'Zum Inhalt springen',
  crumbNav: 'Brotkrumennavigation',
  langNav: 'Sprache',
  home: 'Startseite',
  crumb: 'Haushalt beitreten',
  h1: 'Du wurdest eingeladen',
  lede: 'Jemand, mit dem du zusammenwohnst, möchte bei CoHiro eine Einkaufsliste und einen Vorrat mit dir teilen.',
  codeLabel: 'Dein Einladungscode',
  noCode: 'sieh in deiner Nachricht nach',
  hint: 'Wenn du CoHiro schon hast, öffnet dieser Link die App direkt zum Beitreten.',
  howTo: 'So trittst du bei',
  step1: 'Installiere CoHiro. Die App gibt es *im App\u00a0Store*, bald auch bei *Google\u00a0Play*.',
  step2: 'Erstelle ein Konto oder melde dich an, wenn du schon eines hast.',
  step3: 'Öffne den Tab *Haushalt*, wähle *Haushalt beitreten* und gib den Code oben ein.',
  whatIs: 'Was ist CoHiro?',
  about: 'Eine Einkaufsliste, die der ganze Haushalt gemeinsam pflegt, und ein Vorrat, der zeigt, was wirklich da ist. Was knapp wird, landet von selbst auf der Liste, damit nie alles an einer Person hängen bleibt.',
  aboutLink: 'Mehr über CoHiro',
  fine: 'Mit einem Einladungscode trittst du genau einem Haushalt bei. Er läuft ab, und wer ihn geschickt hat, kann ihn jederzeit ungültig machen. Er enthält nichts über dich und nichts über die andere Person: siehe',
  fineLink: 'Datenschutzerklärung',
  madeBy: 'CoHiro kommt von der Niugio UG (haftungsbeschränkt), Urbanstraße 71, 10967 Berlin, Deutschland.',
  privacy: 'Datenschutz',
  terms: 'Nutzungsbedingungen',
  support: 'Hilfe',
  del: 'Konto löschen',
  title: 'Du wurdest zu einem Haushalt bei CoHiro eingeladen',
  titleCode: 'Haushalt bei CoHiro beitreten, Code ',
};

// WHICH LANGUAGE, in this order: an explicit /de/ URL always wins, then the reader's browser.
//
// THE BROWSER STEP IS A DELIBERATE EXCEPTION TO THIS SITE'S STANDING RULE, which is that
// navigator.language never picks the language. That rule exists to stop an auto-REDIRECT
// throwing away a URL somebody deliberately chose and shared, and nothing here redirects: the
// address a sender pasted into a message is the address that stays in the bar, byte for byte.
// And the reader of THIS page is a non-user who was handed the link by someone else, so the
// sender's locale is only a guess about the recipient - the browser's own preference is the one
// piece of evidence on the page about which language this person actually reads. Do not "fix"
// this into a redirect, and do not delete it because the rest of the site does not do it.
//
// ONLY navigator.languages[0] IS READ, AND THAT IS DELIBERATE. Testing the whole list instead -
// languages.some(/^de/i) - would flip a German speaker who has deliberately set an English UI
// with German further down into German, against the preference they actually stated first. The
// top entry is the answer to "which language does this person want"; the rest of the list is the
// answer to "which can they read", and that is a different question.
//
// AND ONE THING NOW BEATS THE BROWSER GUESS: ?lang=en. The moment this page grew a visible
// switcher, the guess acquired a way to be WRONG IN PUBLIC. A German-browser reader opening
// /join/?c=<CODE> is shown German by the rule above, so the switcher offers them English - and
// without a marker that English link would point at the url they are already on, reload, guess
// German again, and read to them as a broken control. The marker is written by the switcher
// itself, never by a sender, so it never appears in a link anybody shares; it is matched
// literally against the raw query, never decoded, and it is used as a boolean that decides
// between two hard-coded branches, so it cannot reach the DOM. A /de/ path still wins over it
// outright - the German half of the switcher therefore needs no marker at all.
(function () {
  var pref = (navigator.languages && navigator.languages[0]) || navigator.language || '';
  var forcedEn = /(^|&)lang=en(&|$)/.test(location.search.slice(1));
  var german = location.pathname.indexOf('/de/') === 0 || (!forcedEn && /^de/i.test(pref));

  if (german) {
    document.documentElement.lang = 'de';
    // de/join/index.html ships <body lang="en"> so that with JavaScript off its English markup is
    // honestly labelled English under a German <head>. Once the German is in, the body is German.
    document.body.lang = 'de';
    document.title = de.title;
    document.querySelectorAll('[data-i18n],[data-de-href],[data-de-label]').forEach(function (n) {
      var s = de[n.dataset.i18n];
      // Built as text nodes, never as markup: the only thing this page ever renders as HTML is
      // the HTML file itself. Odd pieces of the split are the *emphasised* ones.
      if (s) {
        n.textContent = '';
        s.split('*').forEach(function (part, i) {
          var node = document.createTextNode(part);
          if (i % 2) { var b = document.createElement('strong'); b.appendChild(node); node = b; }
          n.appendChild(node);
        });
      }
      if (n.dataset.deHref) n.setAttribute('href', n.dataset.deHref);
      if (n.dataset.deLabel) n.setAttribute('aria-label', de[n.dataset.deLabel]);
    });
  }

  // THE EN/DE SWITCHER, AND THE ONE THING IT MUST NEVER DO: DROP THE INVITE CODE.
  //
  // Every other page on this site can hard-code its counterpart's url in the markup, because
  // every other page's url is the same for everybody. THIS page's url carries a one-off code
  // that belongs to the reader - /join/?c=<CODE>, or the older /join/<CODE> - and a switcher
  // that navigated to a bare /de/join/ would throw it away, leaving a person holding an invite
  // on a page that tells them to check their message. That is the worst outcome available here,
  // and it is one click away in the naive version, so the hrefs are built from the url in the
  // bar rather than written down: swap the /de prefix, keep the path, keep the query.
  //
  // WHICH SIDE IS THE CURRENT-LANGUAGE MARKER FOLLOWS WHAT IS ON THE SCREEN, not what the url
  // looks like. On /join/?c=X with a German browser the page above has just rendered German, so
  // "Deutsch" is the marker and "English" is the link, even though the path is the English one.
  // A switcher that claimed English was current while the reader looked at German would be
  // describing a different page than the one they are on.
  //
  // The order stays English-first in both languages, so the control does not move under the
  // finger of somebody switching back and forth to compare.
  //
  // Built with createElement and text nodes, like everything else here: this page renders no
  // markup it did not ship with.
  var nav = document.getElementById('langs');
  if (nav) {
    // Our own marker is stripped before either href is built, so it cannot accumulate on
    // repeated switches and cannot travel to the German side, where the path decides anyway.
    var q = location.search.replace(/^\?/, '').split('&').filter(function (part) {
      return part && part !== 'lang=en';
    }).join('&');
    q = q ? '?' + q : '';

    var enPath = location.pathname.indexOf('/de/') === 0
      ? location.pathname.slice(3)   // /de/join/AB12 -> /join/AB12, and /de/ -> /
      : location.pathname;
    var deLink = nav.querySelector('a[hreflang="de"]');
    if (deLink) deLink.setAttribute('href', '/de' + enPath + q);

    if (german) {
      var enLink = document.createElement('a');
      enLink.setAttribute('href', enPath + (q ? q + '&' : '?') + 'lang=en');
      enLink.setAttribute('hreflang', 'en');
      enLink.setAttribute('lang', 'en');
      enLink.appendChild(document.createTextNode('English'));
      var deNow = document.createElement('span');
      deNow.setAttribute('aria-current', 'true');
      deNow.appendChild(document.createTextNode('Deutsch'));
      var wasCurrent = nav.querySelector('[aria-current]');
      if (wasCurrent) nav.replaceChild(enLink, wasCurrent);
      if (deLink) nav.replaceChild(deNow, deLink);
    }
  }

  // WHERE THE CODE COMES FROM, AND WHY THERE ARE NOW TWO PLACES.
  //
  // The original form is the path, /join/<CODE>. That path is not a file, so GitHub Pages answers
  // HTTP 404 and serves 404.html. It works for a person and is invisible to every link previewer
  // there is: facebookexternalhit (WhatsApp, Messenger), iMessage, Slack and Twitterbot all refuse
  // to render a card for a non-200 response. So every invite CoHiro has ever sent went out as a
  // bare, unadorned link, however correct the nine og: tags on the page are. Confirmed by the
  // owner on 2026-08-21, pasting a real invite into WhatsApp: no card at all.
  //
  // The new form puts the code in the query instead - /join/?c=<CODE> - which IS join/index.html:
  // a real file, a real 200, and therefore a real preview card. /de/join/?c=<CODE> likewise, and
  // that one is the bigger win, because it serves de/join/index.html's German og: tags rather
  // than the English ones on the root 404.
  //
  // BOTH ARE READ, AND THE PATH FORM HAS TO KEEP WORKING FOREVER. Links already sent live in other
  // people's message history indefinitely, and nothing changed here can reach them.
  //
  // WHEN BOTH ARE PRESENT, THE PATH WINS. Neither one can inject anything, because both go through
  // the same gate below - so this is not a safety choice, it is a truthfulness one. A query string
  // is the easy thing to append unnoticed to the tail of somebody else's link; if ?c= could
  // override /join/<CODE>, then a forwarded invite could be made to DISPLAY a code its own URL
  // does not contain. The more structural half of the URL wins. In practice the two never
  // collide - the new form's path carries no code at all - so this rule only ever decides a URL
  // somebody hand-built.

  // ONE GATE, BOTH SOURCES, AND IT REJECTS RATHER THAN REPAIRS.
  //
  // The code is displayed and never sent anywhere, so the failure mode is showing something that
  // is not a code - and the query string is now the most attacker-controllable input this site
  // has. URLSearchParams DECODES, it does not sanitise: ?c=%3Cimg%20src=x%20onerror=alert(1)%3E
  // hands back a live-looking <img src=x onerror=alert(1)> string with a straight face. So:
  //   - the character class is the one the path form has always used, [A-Za-z0-9], and nothing
  //     else is ever allowed through;
  //   - it is anchored at BOTH ends, because an unanchored test passes any string that merely
  //     CONTAINS something code-shaped - which is what the query half needs and, see below, is
  //     exactly what the path half must NOT be given;
  //   - the length is bounded, and THE NUMBER IS THE APP'S, not one invented here. The app's own
  //     parser (lib/parseJoinUrl.ts in the listr repo) caps a code at 64 characters, four times
  //     the 16 a real one has. Two halves of one feature, in two repos, each defining "a code"
  //     slightly differently is how a link starts working on one side and not the other, so this
  //     side quotes that side instead of picking its own bound;
  //   - and a value that fails is refused WHOLE. Nothing is trimmed, truncated or escaped into
  //     shape, because a half-salvaged code is a wrong code displayed with confidence.
  // What comes out then reaches the page through textContent and nothing else: never innerHTML,
  // never an attribute, never an href. document.title is a plain string property, not markup.
  function clean(v) {
    return typeof v === 'string' && /^[A-Za-z0-9]{1,64}$/.test(v) ? v.toUpperCase() : '';
  }

  // THE TWO HALVES REACH THAT GATE DIFFERENTLY, AND THE ASYMMETRY IS THE POINT. The query half is
  // new, so it can be exact: what URLSearchParams hands back is put through the gate whole, and a
  // near-miss is refused rather than trimmed into shape. The path half is GRANDFATHERED and must
  // not narrow, so the pattern below is byte-identical to the one that shipped - an alnum run
  // after a `join/` segment, tolerating whatever follows it.
  //
  // THAT TOLERANCE IS NOT SLOPPINESS, IT IS THE CASE THAT ACTUALLY HAPPENS. A sender ends the
  // sentence containing their link, or a chat app linkifies one character too many, and what gets
  // opened is /join/<CODE>. or /join/<CODE>) - which has always worked and has to keep working.
  // Taking the segment whole and demanding it be exactly a code looks stricter and is simply
  // wrong here: it retires every punctuated link in every message history at once, and worse, the
  // app would still JOIN on that URL (lib/parseJoinUrl.ts keeps the same tolerance, deliberately
  // and for this reason) while this page told the reader there was no code. Not a hypothetical and
  // not caught by reasoning: the four punctuation shapes were driven through this file and all
  // four regressed, and the broken version was live on the site for some minutes before this.
  //
  // Not decoded, on purpose: location.pathname is still percent-encoded, so an encoded payload
  // keeps its % signs, fails the class, and no decoder ever runs. The captured run is alnum by
  // construction, so the gate is only enforcing the length cap on this half.
  var seg = location.pathname.match(/\/join\/([A-Za-z0-9]+)/);
  var code = seg ? clean(seg[1]) : '';

  // Guarded for its own sake: a browser without URLSearchParams still gets the path form, and the
  // query form falls back to the page's own "check your message" rather than throwing.
  if (!code && typeof URLSearchParams === 'function') {
    // EXACTLY ONE c=, OR NONE OF THEM - deliberately not .get(), which would silently hand back
    // the first of several. ?c=abc&c=def is a URL nobody can reason about, and quietly picking one
    // half of it is how a reader is shown a code their sender never wrote. The app refuses that
    // URL outright (same file as above), and a page that confidently displayed "ABC" for a link
    // the app then declines to open would be worse than one that says "check your message".
    var all = new URLSearchParams(location.search).getAll('c');
    code = all.length === 1 ? clean(all[0]) : '';
  }

  // No code, or a value that failed the gate: leave the page exactly as it was served. That is
  // already the right answer in both languages - "check your message", or the German catalog's
  // "sieh in deiner Nachricht nach", which the block above has put there by now.
  if (!code) return;

  var el = document.getElementById('code');
  // Guarded because this stopped being an inline script welded to its own markup: any page that
  // loads /join.js without a #code element would otherwise throw here and take the rest down.
  if (el) el.textContent = code;
  document.title = (german ? de.titleCode : 'Join a household on CoHiro with code ') + code;
})();
