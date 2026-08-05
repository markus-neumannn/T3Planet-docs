/**
 * T3Planet Docs UI — minimal: theme, search trigger, lazy image hints.
 */
(function () {
  "use strict";

  try {
    var scheme = localStorage.getItem("mintlify-color-scheme");
    if (scheme === "dark") {
      document.documentElement.classList.add("dark");
    } else if (scheme === "light") {
      document.documentElement.classList.remove("dark");
    }
  } catch (e) {
    /* ignore */
  }

  function openSearch() {
    var isMac = navigator.platform.toUpperCase().indexOf("MAC") >= 0;
    document.dispatchEvent(
      new KeyboardEvent("keydown", {
        key: "k",
        code: "KeyK",
        metaKey: isMac,
        ctrlKey: !isMac,
        bubbles: true,
        cancelable: true,
      })
    );
    var searchBtn = document.querySelector(
      'button[aria-label*="Search" i], [data-component-part="search"] button, .search-button'
    );
    if (searchBtn) searchBtn.click();
  }

  document.addEventListener(
    "click",
    function (e) {
      if (e.target.closest("[data-t3-search-trigger]")) {
        e.preventDefault();
        openSearch();
        return;
      }
      var anchor = e.target.closest('a[href^="/"]');
      if (!anchor) return;
      var area = document.getElementById("content-area");
      if (area) area.scrollTop = 0;
      if (window.scrollY) window.scrollTo(0, 0);
    },
    true
  );

  function optimizeImage(img, isFirst) {
    if (img.getAttribute("data-t3-optimized")) return;
    img.setAttribute("data-t3-optimized", "1");
    if (isFirst) {
      img.loading = "eager";
      img.setAttribute("fetchpriority", "high");
    } else if (!img.getAttribute("loading")) {
      img.loading = "lazy";
    }
    if (!img.getAttribute("decoding")) img.decoding = "async";
    if (!img.getAttribute("width") && img.naturalWidth) {
      img.setAttribute("width", String(img.naturalWidth));
      img.setAttribute("height", String(img.naturalHeight));
    }
  }

  function setupImageObserver() {
    var root =
      document.getElementById("content-area") ||
      document.getElementById("content-container") ||
      document.getElementById("content");
    if (!root) return;

    var first = root.querySelector("img");
    if (first) optimizeImage(first, true);

    if (!("IntersectionObserver" in window)) {
      root.querySelectorAll("img:not([data-t3-optimized])").forEach(function (img) {
        optimizeImage(img, false);
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            optimizeImage(entry.target, false);
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "200px 0px", threshold: 0.01 }
    );

    root.querySelectorAll("img:not([data-t3-optimized])").forEach(function (img) {
      observer.observe(img);
    });
  }

  function deferImages() {
    if (typeof requestIdleCallback === "function") {
      requestIdleCallback(setupImageObserver, { timeout: 600 });
    } else {
      setTimeout(setupImageObserver, 50);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", deferImages);
  } else {
    deferImages();
  }
})();
