// Shared by BOTH invite twins: join/index.html and 404.html. GitHub Pages serves 404.html for
// every real /join/<CODE> URL, because that path is not a file - so this one script is what runs
// on the page visitors actually open. It used to be an inline <script> copied into both files,
// which is how a fix once landed on only one of them.
//
// Lift the code out of the path (/join/AB12CD) and show it, so the visitor can type it even
// though the app is not installed. One same-origin static file and dependency-free: this site
// makes no third-party requests, and a page whose whole job is to be readable must not need a
// bundle to work.
//
// The code is displayed only. It is never sent anywhere from this page, and GitHub Pages is
// static, so there is nothing here that could log it.

// THE GERMAN INVITE PAGE CANNOT BE A GERMAN HTML FILE, so it is this object instead.
// GitHub Pages has exactly one 404.html, at the site root. /join/<CODE> is not a file, and
// neither is /de/join/<CODE>, so BOTH of them serve that same English file. A de/join/index.html
// can only ever answer the bare /de/join/ path, which is the one path nobody is ever sent. The
// only place a German invite page can exist is here, at runtime, on whichever file got served.
//
// Wording is the app's own German catalog (app/src/locales/de in the listr repo), so the site and
// the product cannot disagree about what things are called: Haushalt, Einkaufsliste, Vorrat
// (never Inventar), Konto, Einladungscode, and the locked verb "beitreten". Register is du.
//
// *Asterisks* mark a <strong>. Two of the steps need one, and the alternative was cutting those
// sentences into five hooks apiece - which the app catalog refuses to do, on the grounds that a
// translator has to be able to reorder a whole sentence. \u00a0 is written as an escape rather
// than typed, because an invisible character in a source file is one nobody can review.
var de = {
  skip: 'Zum Inhalt springen',
  crumbNav: 'Brotkrumennavigation',
  home: 'Startseite',
  crumb: 'Haushalt beitreten',
  h1: 'Du wurdest eingeladen',
  lede: 'Jemand aus deinem Haushalt möchte bei CoHiro eine Einkaufsliste und einen Vorrat mit dir teilen.',
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
  madeBy: 'CoHiro kommt von der Niugio UG (haftungsbeschränkt), Urbanstraße 71, 10967 Berlin, Germany.',
  privacy: 'Datenschutz',
  terms: 'Nutzungsbedingungen',
  del: 'Konto löschen',
  title: 'Du wurdest zu einem Haushalt bei CoHiro eingeladen',
  titleCode: 'Haushalt bei CoHiro beitreten mit Code ',
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
(function () {
  var pref = (navigator.languages && navigator.languages[0]) || navigator.language || '';
  var german = location.pathname.indexOf('/de/') === 0 || /^de/i.test(pref);

  if (german) {
    document.documentElement.lang = 'de';
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

  var m = location.pathname.match(/\/join\/([A-Za-z0-9]+)/);
  if (!m) return;
  var code = m[1].toUpperCase();
  var el = document.getElementById('code');
  // Guarded because this stopped being an inline script welded to its own markup: any page that
  // loads /join.js without a #code element would otherwise throw here and take the rest down.
  if (el) el.textContent = code;
  document.title = (german ? de.titleCode : 'Join a household on CoHiro with code ') + code;
})();
