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
(function () {
  var m = location.pathname.match(/\/join\/([A-Za-z0-9]+)/);
  if (!m) return;
  var code = m[1].toUpperCase();
  var el = document.getElementById('code');
  el.textContent = code;
  document.title = 'Join a household on CoHiro with code ' + code;
})();
