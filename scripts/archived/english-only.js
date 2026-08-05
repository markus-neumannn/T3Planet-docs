/**
 * English-only mode: redirect legacy /de URLs to English.
 * Language UI is hidden via custom.css (no MutationObserver).
 */
(function () {
  "use strict";

  var path = window.location.pathname.replace(/\/$/, "") || "";
  if (path === "/de" || path === "/de/index") {
    window.location.replace("/" + window.location.search + window.location.hash);
    return;
  }
  if (path.indexOf("/de/") === 0) {
    var enPath = path.slice(3) || "/index";
    if (enPath === "/index") enPath = "/";
    window.location.replace(enPath + window.location.search + window.location.hash);
  }
})();
