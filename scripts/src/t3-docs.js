(function () {
  "use strict";
  // Mintlify can evaluate this bundle more than once (inline + _static).
  // A second init duplicates observers/listeners and clears the close cooldown.
  if (window.__t3DocsNavBound) return;
  window.__t3DocsNavBound = 1;

  var prefetched = Object.create(null);
  var prefetchPending = 0;
  var prefetchSessionCount = 0;
  var prefetchGateOpen = false;
  // Keep early gate (t3-stats-inline.js) in sync with intentional prefetches
  try {
    Object.defineProperty(window, "__t3PrefetchGateOpen", {
      configurable: true,
      get: function () {
        return prefetchGateOpen;
      },
      set: function (v) {
        prefetchGateOpen = !!v;
      },
    });
  } catch (eGate) {
    window.__t3PrefetchGateOpen = false;
  }
  var PREFETCH_MAX = 4;
  var PREFETCH_SESSION_MAX = 12;
  var staticLinksDone = false;
  var statsLoaded = false;
  var imgIo = null;
  var iframeIo = null;
  var routePath = "";
  var HUB_ROUTES = [
    "/",
    "/ExtNsT3AF/Index",
    "/AllExtensions/Index",
    "/AllTemplates/Index",
    "/AIFoundationExtensions/Index",
    "/License/Index",
    "/ExtThemes/Index",
    "/EXTKarma/Index",
    "/ExtNsT3AI/Index",
    "/ExtNsT3AA/Index",
    "/ExtNsT3AC/Index",
    "/ExtNsT3AS/Index",
    "/ExtNsT3AL/Index",
    "/ExtNsT3AB/Index",
    "/ExtRTECKEditorPack/Index",
    "/ExtNsRevolutionSlider/Index",
    "/EXTAvatar/Index",
    "/EXTBootstrap/Index"
  ];

  try {
    var s = localStorage.getItem("mintlify-color-scheme");
    if (s === "dark") document.documentElement.classList.add("dark");
    else if (s === "light") document.documentElement.classList.remove("dark");
  } catch (eTheme) {}

  var path = (window.location.pathname || "").replace(/\/$/, "") || "";
  function redirectLegacyPath(p) {
    if (!p) return "";
    if (p === "/AIUniverseExtensions" || p === "/AIUniverseExtensions/Index") return "/AIFoundationExtensions/Index";
    if (p.indexOf("/AIUniverseExtensions/") === 0) return "/AIFoundationExtensions/" + p.slice("/AIUniverseExtensions/".length);
    // Canonical product slug is ExtNsT3AF (matches live RTD). Legacy T3AF/AIFoundation/AIUniverse → ExtNsT3AF.
    // Do not redirect /ExtNsT3AF (canonical); keep AIFoundationExtensions hub as-is.
    if (p === "/T3AF" || p === "/T3AF/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/T3AF/") === 0) return "/ExtNsT3AF/" + p.slice("/T3AF/".length);
    if (p === "/de/T3AF" || p === "/de/T3AF/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/de/T3AF/") === 0) return "/ExtNsT3AF/" + p.slice("/de/T3AF/".length);
    if (p === "/AIFoundation" || p === "/AIFoundation/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/AIFoundation/") === 0) return "/ExtNsT3AF/" + p.slice("/AIFoundation/".length);
    if (p === "/de/AIFoundation" || p === "/de/AIFoundation/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/de/AIFoundation/") === 0) return "/ExtNsT3AF/" + p.slice("/de/AIFoundation/".length);
    if (p === "/AIUniverse" || p === "/AIUniverse/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/AIUniverse/") === 0) return "/ExtNsT3AF/" + p.slice("/AIUniverse/".length);
    if (p === "/de/AIUniverse" || p === "/de/AIUniverse/Index") return "/ExtNsT3AF/Index";
    if (p.indexOf("/de/AIUniverse/") === 0) return "/ExtNsT3AF/" + p.slice("/de/AIUniverse/".length);
    if (p === "/de/AIUniverseExtensions" || p === "/de/AIUniverseExtensions/Index") return "/AIFoundationExtensions/Index";
    if (p.indexOf("/de/AIUniverseExtensions/") === 0) return "/AIFoundationExtensions/" + p.slice("/de/AIUniverseExtensions/".length);
    return "";
  }
  var legacyRedirect = redirectLegacyPath(path);
  if (legacyRedirect) {
    location.replace(legacyRedirect + location.search + location.hash);
    return;
  }
  if (path === "/de" || path === "/de/index") {
    location.replace("/" + location.search + location.hash);
    return;
  }
  if (path.indexOf("/de/") === 0) {
    var en = path.slice(3) || "/";
    if (en === "/index") en = "/";
    location.replace(en + location.search + location.hash);
    return;
  }

  routePath = path || "/";

  var progressEl = null; // legacy alias → nav loader overlay
  var progressBar = null;
  var progressTimer = null;
  var progressDelay = null;
  var progressValue = 0;
  var loaderEl = null;
  var loaderHideTimer = null;
  var loaderSafetyTimer = null;
  var veilEl = null;
  var veilTimer = null;
  var holdEl = null;
  var holdInner = null;
  var holdReleaseTimer = null;
  var lockedScrollY = 0;
  var scrollLocked = false;
  var navStartedAt = 0;
  var navToken = 0;
  var progressVisible = false;
  var PROGRESS_SHOW_MS = 120;
  var LOADER_MAX_MS = 12000;
  var userNavPriority = false;
  var docPrefetchControllers = [];
  var pendingNavHref = "";
  var reducedMotion = false;
  try {
    reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (eRm) {}


  function idle(fn, timeout) {
    if (typeof requestIdleCallback === "function") requestIdleCallback(fn, { timeout: timeout || 400 });
    else setTimeout(fn, timeout || 0);
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments;
      var self = this;
      t = setTimeout(function () {
        fn.apply(self, args);
      }, ms);
    };
  }

  function contentRoot() {
    return (
      document.getElementById("content-area") ||
      document.getElementById("content") ||
      document.querySelector("main .mdx-content") ||
      document.querySelector("main") ||
      document.querySelector("[data-page-content]") ||
      document.querySelector("article")
    );
  }

  function currentPath() {
    return (location.pathname || "").replace(/\/$/, "") || "/";
  }

  function isAiDocsRoute(p) {
    return /^\/(?:T3AF|ExtNsT3AF|ExtNsT3(?:AA|AB|AC|AI|AL|AS))(?:\/|$)/.test(p || "");
  }

  function applyRouteClasses() {
    var p = currentPath();
    document.documentElement.classList.toggle("t3-ai-docs", isAiDocsRoute(p));
  }

  function applyContentClasses() {
    var root = contentRoot() || document;
    var isLanding =
      !!root.querySelector(".t3-home-landing, .t3-hub-landing, .t3-template-landing") ||
      !!document.querySelector(".t3-home-landing, .t3-hub-landing, .t3-template-landing");
    document.documentElement.classList.toggle("t3-landing-doc", isLanding);
  }

  function contentBounds() {
    var top = 64;
    var nav = document.getElementById("navbar");
    if (nav) top = Math.max(56, Math.ceil(nav.getBoundingClientRect().bottom));
    var left = 0;
    if (window.innerWidth >= 1024) {
      var sb = document.getElementById("sidebar") || document.querySelector('aside[id*="sidebar" i]');
      if (sb) {
        var r = sb.getBoundingClientRect();
        if (r.width > 48 && r.right > 0) left = Math.round(r.right);
      }
      if (!left) {
        var cssW = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--t3-sidebar-width"));
        if (cssW) left = Math.round(cssW);
      }
    }
    return { top: top, left: left };
  }

  function applyOverlayBounds(el) {
    if (!el) return;
    var b = contentBounds();
    el.style.top = b.top + "px";
    el.style.left = b.left + "px";
    el.style.right = "0";
    // Keep footer visible — inset hold above on-screen footer
    var footer =
      document.querySelector("footer#footer") ||
      document.querySelector("#footer") ||
      document.querySelector("footer");
    var bottom = 0;
    if (footer) {
      var fr = footer.getBoundingClientRect();
      var h = Math.max(fr.height, footer.offsetHeight || 0);
      if (h > 20 && fr.top < window.innerHeight && fr.bottom > 0) {
        bottom = Math.max(0, Math.round(window.innerHeight - fr.top));
      }
    }
    el.style.bottom = bottom + "px";
  }

  var closeBtnTrackRaf = 0;

  function positionMobileNavCloseButton(nav) {
    var btn = document.querySelector("[data-t3-drawer-close]");
    if (!btn || !nav) return;
    var r = nav.getBoundingClientRect();
    // Skip while drawer is still mostly off-screen (opening from the right)
    if (r.left > window.innerWidth - 20) return;

    var size = 40;
    var gap = 12;
    // Dock to the LEFT EDGE of the right-side drawer (not viewport-left).
    // Viewport-left made the X look stranded far from the menu on tablets.
    var left = Math.round(r.left - size - gap);
    if (left < 8) {
      // Narrow gutter: shrink control but keep it hugging the drawer
      size = Math.max(28, Math.min(40, r.left - 16));
      left = Math.max(8, Math.round(r.left - size - 8));
      if (left < 8) left = 8;
      if (left + size > r.left - 4) {
        size = Math.max(24, r.left - left - 6);
      }
    }
    var top = Math.round(r.top + 12);
    if (top < 8) top = 8;

    btn.style.setProperty("width", size + "px", "important");
    btn.style.setProperty("height", size + "px", "important");
    btn.style.setProperty("min-width", "0", "important");
    btn.style.setProperty("min-height", "0", "important");
    btn.style.setProperty("left", left + "px", "important");
    btn.style.setProperty("right", "auto", "important");
    btn.style.setProperty("top", top + "px", "important");
  }

  function trackMobileNavCloseButton(nav) {
    if (closeBtnTrackRaf) cancelAnimationFrame(closeBtnTrackRaf);
    var start = performance.now();
    function tick(now) {
      if (!document.getElementById("mobile-nav")) {
        closeBtnTrackRaf = 0;
        return;
      }
      positionMobileNavCloseButton(nav);
      // Follow the slide-in (~400ms) plus a short settle
      if (now - start < 520) {
        closeBtnTrackRaf = requestAnimationFrame(tick);
      } else {
        closeBtnTrackRaf = 0;
        positionMobileNavCloseButton(nav);
      }
    }
    closeBtnTrackRaf = requestAnimationFrame(tick);
  }

  function ensureMobileNavCloseButton(nav) {
    var existing = document.querySelector("[data-t3-drawer-close]");
    if (!nav) {
      if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
      return;
    }
    var btn = existing;
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("data-t3-drawer-close", "1");
      btn.setAttribute("aria-label", "Close navigation");
      btn.className = "t3-drawer-close";
      btn.innerHTML =
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>';
      document.body.appendChild(btn);
    }
    // Always (re)bind so a stale listener from a prior bundle eval cannot stick
    if (btn.dataset.t3CloseBound !== "1") {
      btn.dataset.t3CloseBound = "1";
      btn.addEventListener(
        "click",
        function (e) {
          e.preventDefault();
          e.stopPropagation();
          closeMobileNav();
        },
        true
      );
    }
    trackMobileNavCloseButton(nav);
  }

  var mobileNavCloseCooldownUntil = 0;
  var mobileNavSwallowBound = false;
  var mobileNavDismissLock = false;

  function isMobileNavTrigger(el) {
    if (!el || !el.closest) return false;
    var btn = el.closest("button");
    if (!btn) return false;
    // Never treat close controls as the open hamburger (label is "Close navigation")
    if (btn.hasAttribute("data-t3-drawer-close")) return false;
    var label = (btn.getAttribute("aria-label") || "").toLowerCase();
    if (label.indexOf("close") !== -1) return false;
    var cls = String(btn.className || "");
    var text = (btn.textContent || "").toLowerCase();
    // Open control is the lg:hidden Navigation strip (not Close *)
    if (cls.indexOf("lg:hidden") !== -1) return true;
    if (label.indexOf("open menu") !== -1 || label.indexOf("open sidebar") !== -1) return true;
    if (label.indexOf("open navigation") !== -1) return true;
    if (text.indexOf("navigation") !== -1 && cls.indexOf("lg:hidden") !== -1) return true;
    return false;
  }

  function findMintlifyMobileNavDismiss(nav) {
    // Prefer backdrop: Mintlify's native "Close navigation" sits at left-full,
    // which is off-screen when the drawer opens from the right.
    var backdrop = document.querySelector('[class*="[--backdrop-opacity"]');
    if (backdrop) return backdrop;
    var root = nav || document.getElementById("mobile-nav");
    return (
      (root &&
        root.querySelector(
          'button[aria-label*="Close navigation" i]:not([data-t3-drawer-close])'
        )) ||
      document.querySelector(
        'button[aria-label*="Close navigation" i]:not([data-t3-drawer-close])'
      ) ||
      (root && root.querySelector('button[aria-label*="Close" i]')) ||
      null
    );
  }

  function dismissMintlifyMobileNav() {
    if (!document.getElementById("mobile-nav")) return;
    // Escape is the reliable Headless UI / Base UI dismiss (native X is off-screen
    // on a right drawer; sync .click() on it is flaky inside our click handler).
    try {
      document.dispatchEvent(
        new KeyboardEvent("keydown", {
          key: "Escape",
          code: "Escape",
          keyCode: 27,
          which: 27,
          bubbles: true,
          cancelable: true,
        })
      );
    } catch (err) {}
    if (!document.getElementById("mobile-nav")) return;
    var dismiss = findMintlifyMobileNavDismiss(document.getElementById("mobile-nav"));
    if (!dismiss || mobileNavDismissLock) return;
    mobileNavDismissLock = true;
    try {
      dismiss.click();
    } catch (err2) {}
    setTimeout(function () {
      mobileNavDismissLock = false;
    }, 200);
  }

  function clickMintlifyMobileNavDismiss(nav) {
    if (mobileNavDismissLock) return false;
    var dismiss = findMintlifyMobileNavDismiss(nav);
    if (!dismiss) return false;
    mobileNavDismissLock = true;
    try {
      dismiss.click();
    } catch (err) {}
    setTimeout(function () {
      mobileNavDismissLock = false;
    }, 200);
    return true;
  }

  function swallowGhostClicks(ms) {
    ms = ms || 450;
    var until = Date.now() + ms;
    var blockTrigger = function (e) {
      if (Date.now() > until) {
        document.removeEventListener("click", blockTrigger, true);
        document.removeEventListener("pointerup", blockTrigger, true);
        document.removeEventListener("pointerdown", blockTrigger, true);
        document.removeEventListener("touchend", blockTrigger, true);
        return;
      }
      if (!isMobileNavTrigger(e.target)) return;
      e.preventDefault();
      e.stopPropagation();
      if (e.stopImmediatePropagation) e.stopImmediatePropagation();
    };
    document.addEventListener("click", blockTrigger, true);
    document.addEventListener("pointerup", blockTrigger, true);
    document.addEventListener("pointerdown", blockTrigger, true);
    document.addEventListener("touchend", blockTrigger, true);
  }

  function armMobileNavCloseCooldown(ms) {
    ms = ms || 700;
    mobileNavCloseCooldownUntil = Date.now() + ms;
    document.documentElement.classList.add("t3-mobile-nav-closing");
    // Inline pointer-events beat React listeners (capture order can't)
    var disabled = [];
    var buttons = document.querySelectorAll("button");
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      if (!isMobileNavTrigger(btn)) continue;
      disabled.push(btn);
      btn.style.setProperty("pointer-events", "none", "important");
      btn.setAttribute("data-t3-nav-trigger-locked", "1");
    }
    swallowGhostClicks(ms);
    // Fresh React remounts of the hamburger lose inline locks — CSS class covers
    // them, and this poll dismisses a ghost reopen after a successful close.
    var sawClosed = false;
    var poll = setInterval(function () {
      if (Date.now() >= mobileNavCloseCooldownUntil) {
        clearInterval(poll);
        return;
      }
      var openNow = !!document.getElementById("mobile-nav");
      if (!openNow) {
        sawClosed = true;
      } else if (sawClosed) {
        setMobileNavOpen(false);
        dismissMintlifyMobileNav();
      }
      // Re-lock any new trigger nodes Mintlify just mounted
      var more = document.querySelectorAll("button");
      for (var k = 0; k < more.length; k++) {
        var b2 = more[k];
        if (!isMobileNavTrigger(b2)) continue;
        if (b2.getAttribute("data-t3-nav-trigger-locked") === "1") continue;
        disabled.push(b2);
        b2.style.setProperty("pointer-events", "none", "important");
        b2.setAttribute("data-t3-nav-trigger-locked", "1");
      }
    }, 32);
    setTimeout(function () {
      clearInterval(poll);
      if (Date.now() >= mobileNavCloseCooldownUntil - 10) {
        document.documentElement.classList.remove("t3-mobile-nav-closing");
      }
      for (var j = 0; j < disabled.length; j++) {
        disabled[j].style.removeProperty("pointer-events");
        disabled[j].removeAttribute("data-t3-nav-trigger-locked");
      }
    }, ms + 30);
  }

  function setMobileNavOpen(open) {
    // Ignore reopen while closing cooldown is active (click-through / ghost click)
    if (open && Date.now() < mobileNavCloseCooldownUntil) {
      return;
    }
    document.documentElement.classList.toggle("t3-mobile-nav-open", !!open);
    if (open) {
      // Never clear the close-guard class here — only the cooldown timer may
      document.documentElement.setAttribute("data-t3-mobile-nav", "open");
    } else {
      document.documentElement.removeAttribute("data-t3-mobile-nav");
      var btn = document.querySelector("[data-t3-drawer-close]");
      if (btn && btn.parentNode) btn.parentNode.removeChild(btn);
    }
  }

  function closeMobileNav() {
    var nav = document.getElementById("mobile-nav");
    armMobileNavCloseCooldown(700);
    if (!nav) {
      setMobileNavOpen(false);
      return;
    }
    if (!reducedMotion && nav.classList.contains("t3-drawer-from-right")) {
      nav.classList.add("t3-drawer-exiting");
      nav.classList.remove("t3-drawer-entered", "t3-drawer-preenter");
    }
    // Clear our open flag first so our Escape listener does not re-enter
    setMobileNavOpen(false);
    setTimeout(function () {
      dismissMintlifyMobileNav();
      setTimeout(function () {
        if (document.getElementById("mobile-nav")) dismissMintlifyMobileNav();
      }, 100);
    }, 0);
  }

  function dockMobileNavRight(nav) {
    if (!nav) return;
    nav.setAttribute("data-swipe-direction", "right");
    nav.classList.add("t3-drawer-from-right");
    var wrap = nav.closest(".fixed.inset-0.flex") || nav.parentElement;
    if (wrap) {
      wrap.classList.add("t3-drawer-right-wrap");
      wrap.style.justifyContent = "flex-end";
    }
  }

  function animateMobileNavFromRight(nav) {
    if (!nav) return;
    // Never re-enter / undo an in-progress close
    if (Date.now() < mobileNavCloseCooldownUntil) return;
    if (nav.classList.contains("t3-drawer-exiting")) return;
    var rect = nav.getBoundingClientRect();
    var stuckOffscreen =
      rect.left >= window.innerWidth - 8 ||
      nav.classList.contains("t3-drawer-preenter");
    if (
      nav.dataset.t3RightAnim === "1" &&
      !stuckOffscreen &&
      nav.classList.contains("t3-drawer-entered")
    ) {
      return;
    }
    if (reducedMotion) {
      nav.classList.add("t3-drawer-entered");
      nav.classList.remove("t3-drawer-preenter", "t3-drawer-exiting");
      nav.style.transform = "translate3d(0, 0, 0)";
      nav.style.opacity = "1";
      nav.dataset.t3RightAnim = "1";
      return;
    }
    nav.dataset.t3RightAnim = "1";
    nav.classList.add("t3-drawer-from-right");
    nav.classList.remove("t3-drawer-entered", "t3-drawer-exiting");
    // Inline start state beats Mintlify's left-entry matrix during open
    nav.style.transition = "none";
    nav.style.transform = "translate3d(104%, 0, 0)";
    nav.style.opacity = "0.94";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (!document.getElementById("mobile-nav")) return;
        nav.style.transition =
          "transform 0.4s cubic-bezier(0.32, 0.72, 0, 1), opacity 0.28s ease";
        nav.style.transform = "translate3d(0, 0, 0)";
        nav.style.opacity = "1";
        nav.classList.add("t3-drawer-entered");
        nav.classList.remove("t3-drawer-preenter");
        setTimeout(function () {
          if (!document.getElementById("mobile-nav")) return;
          nav.style.transition = "";
        }, 420);
      });
    });
  }

  function bindMobileNavSwipe(nav) {
    if (!nav || nav.dataset.t3SwipeBound === "1" || reducedMotion) return;
    nav.dataset.t3SwipeBound = "1";
    var startX = 0;
    var startY = 0;
    var tracking = false;
    nav.addEventListener(
      "touchstart",
      function (e) {
        if (!e.touches || !e.touches[0]) return;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        tracking = true;
      },
      { passive: true }
    );
    nav.addEventListener(
      "touchend",
      function (e) {
        if (!tracking) return;
        tracking = false;
        var t = e.changedTouches && e.changedTouches[0];
        if (!t) return;
        var dx = t.clientX - startX;
        var dy = Math.abs(t.clientY - startY);
        // Swipe right to close (drawer opens from the right)
        if (dx > 64 && dy < 72) closeMobileNav();
      },
      { passive: true }
    );
  }

  function enhanceMobileNav(nav) {
    if (!nav) return;
    if (Date.now() < mobileNavCloseCooldownUntil) return;
    dockMobileNavRight(nav);
    animateMobileNavFromRight(nav);
    if (nav.dataset.t3SwipeBound !== "1") bindMobileNavSwipe(nav);
    ensureMobileNavCloseButton(nav);
    if (nav.dataset.t3SwipeDirGuard !== "1") {
      nav.dataset.t3SwipeDirGuard = "1";
      var attrObs = new MutationObserver(function () {
        if (nav.getAttribute("data-swipe-direction") !== "right") {
          nav.setAttribute("data-swipe-direction", "right");
        }
      });
      attrObs.observe(nav, { attributes: true, attributeFilter: ["data-swipe-direction"] });
    }
  }

  function bindMobileNavEnhancements() {
    if (window.__t3MobileNavEnhancementsBound) return;
    window.__t3MobileNavEnhancementsBound = 1;
    // Right-side drawer: dock, animate, swipe, ESC, close control
    var obs = new MutationObserver(function () {
      var nav = document.getElementById("mobile-nav");
      var open = !!nav;
      // During close cooldown: never re-enhance/animate. One throttled dismiss if
      // Mintlify remounted the drawer from a ghost hamburger tap.
      if (Date.now() < mobileNavCloseCooldownUntil) {
        setMobileNavOpen(false);
        if (open) dismissMintlifyMobileNav();
        return;
      }
      setMobileNavOpen(open);
      if (open) enhanceMobileNav(nav);
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });

    window.addEventListener(
      "resize",
      function () {
        var nav = document.getElementById("mobile-nav");
        if (nav) positionMobileNavCloseButton(nav);
      },
      { passive: true }
    );

    // Backdrop / outside tap: arm cooldown so the same click cannot reopen via hamburger
    document.addEventListener(
      "pointerdown",
      function (e) {
        if (!document.documentElement.classList.contains("t3-mobile-nav-open")) return;
        if (e.target && e.target.closest && e.target.closest("#mobile-nav")) return;
        if (e.target && e.target.closest && e.target.closest("[data-t3-drawer-close]")) return;
        var wrap = document.querySelector(".t3-drawer-right-wrap, .fixed.inset-0.flex.z-40");
        if (!wrap) return;
        // Click on overlay area (not the drawer panel)
        if (wrap.contains(e.target) || (e.target.className && String(e.target.className).indexOf("backdrop") !== -1)) {
          armMobileNavCloseCooldown(700);
        }
      },
      true
    );

    document.addEventListener(
      "keydown",
      function (e) {
        if (e.key === "Escape" && document.documentElement.classList.contains("t3-mobile-nav-open")) {
          closeMobileNav();
        }
      },
      true
    );

    // Close drawer after in-drawer link navigation (SPA feel)
    document.addEventListener(
      "click",
      function (e) {
        if (!document.documentElement.classList.contains("t3-mobile-nav-open")) return;
        var a = e.target.closest && e.target.closest("#mobile-nav a[href]");
        if (!a) return;
        var href = a.getAttribute("href") || "";
        if (!href || href.charAt(0) === "#") return;
        // Allow Mintlify to navigate, then dismiss
        setTimeout(function () {
          closeMobileNav();
        }, 40);
      },
      true
    );

    var existing = document.getElementById("mobile-nav");
    setMobileNavOpen(!!existing);
    if (existing) enhanceMobileNav(existing);
  }


  function dotsMarkup() {
    return (
      '<div class="t3-dots-container" aria-hidden="true">' +
      '<span class="t3-dot"></span>' +
      '<span class="t3-dot"></span>' +
      '<span class="t3-dot"></span>' +
      "</div>" +
      '<span class="t3-nav-loader-sr sr-only">Loading documentation</span>'
    );
  }

  function ensureNavLoader() {
    if (loaderEl) return loaderEl;
    loaderEl = document.createElement("div");
    loaderEl.id = "t3-nav-loader";
    loaderEl.setAttribute("aria-hidden", "true");
    loaderEl.innerHTML =
      '<div class="t3-nav-loader-panel" role="status" aria-live="polite" aria-atomic="true">' +
      dotsMarkup() +
      "</div>";
    document.documentElement.appendChild(loaderEl);
    progressEl = loaderEl; // keep legacy callers / cleanup paths safe
    return loaderEl;
  }

  function ensureProgress() {
    return ensureNavLoader();
  }

  function showNavLoader() {
    ensureNavLoader();
    if (loaderHideTimer) {
      clearTimeout(loaderHideTimer);
      loaderHideTimer = null;
    }
    loaderEl.classList.remove("t3-nav-loader-exit");
    loaderEl.classList.add("t3-nav-loader-active");
    loaderEl.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("t3-loader-on");
    lockPageScroll();
    bindHoldScrollBlock(true);
  }

  function hideNavLoader(immediate) {
    if (!loaderEl) {
      document.documentElement.classList.remove("t3-loader-on", "t3-holding");
      bindHoldScrollBlock(false);
      unlockPageScroll();
      return;
    }
    function clearUi() {
      loaderHideTimer = null;
      loaderEl.classList.remove("t3-nav-loader-active", "t3-nav-loader-exit");
      loaderEl.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("t3-loader-on", "t3-holding");
      bindHoldScrollBlock(false);
      unlockPageScroll();
    }
    if (loaderHideTimer) {
      clearTimeout(loaderHideTimer);
      loaderHideTimer = null;
    }
    if (immediate || reducedMotion || !loaderEl.classList.contains("t3-nav-loader-active")) {
      clearUi();
      return;
    }
    loaderEl.classList.add("t3-nav-loader-exit");
    loaderHideTimer = setTimeout(clearUi, 220);
    // Hard clear — never leave blur overlay / scroll lock stuck
    setTimeout(function () {
      if (document.documentElement.classList.contains("t3-loader-on")) clearUi();
    }, 400);
  }

  function holdStatusMarkup() {
    return dotsMarkup();
  }

  function veilMarkup() {
    return (
      '<div class="t3-page-veil-inner">' +
      '<div class="t3-page-veil-status">' +
      '<span class="t3-page-veil-spinner" aria-hidden="true"></span>' +
      '<span class="t3-page-veil-status-text">Loading page…</span>' +
      "</div>" +
      '<div class="t3-skel t3-skel-eyebrow"></div>' +
      '<div class="t3-skel t3-skel-title"></div>' +
      '<div class="t3-skel t3-skel-line"></div>' +
      '<div class="t3-skel t3-skel-line"></div>' +
      '<div class="t3-skel t3-skel-line t3-skel-short"></div>' +
      '<div class="t3-skel t3-skel-hero"></div>' +
      '<div class="t3-skel-grid">' +
      '<div class="t3-skel t3-skel-card"></div>' +
      '<div class="t3-skel t3-skel-card"></div>' +
      '<div class="t3-skel t3-skel-card"></div>' +
      "</div>" +
      '<div class="t3-skel t3-skel-line"></div>' +
      '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
      '<div class="t3-skel t3-skel-line t3-skel-short"></div>' +
      "</div>"
    );
  }

  function ensureVeil() {
    if (!veilEl) {
      veilEl = document.createElement("div");
      veilEl.id = "t3-page-veil";
      veilEl.setAttribute("aria-hidden", "true");
      document.documentElement.appendChild(veilEl);
    }
    if (!veilEl.querySelector(".t3-page-veil-status")) {
      veilEl.innerHTML = veilMarkup();
    }
    applyOverlayBounds(veilEl);
    return veilEl;
  }

  function ensureHold() {
    if (!holdEl) {
      holdEl = document.createElement("div");
      holdEl.id = "t3-page-hold";
      holdEl.setAttribute("aria-hidden", "true");
      holdInner = document.createElement("div");
      holdInner.className = "t3-page-hold-inner";
      holdEl.appendChild(holdInner);
      document.documentElement.appendChild(holdEl);
    }
    applyOverlayBounds(holdEl);
    return holdEl;
  }

  function contentLooksReady(root) {
    root = root || contentRoot();
    if (!root) return false;
    if (root.querySelector(".t3-page-veil, #t3-page-hold")) return false;
    var text = (root.innerText || "").replace(/\s+/g, " ").trim();
    if (text.length >= 48) return true;
    if (root.querySelector("h1, h2, img, pre, table, .mdx-content, article")) {
      return text.length >= 12;
    }
    return false;
  }

  function docsSkeletonMarkup(kind) {
    // kind: "docs" | "install" | "hub"
    var main =
      '<div class="t3-skel-main">' +
      '<div class="t3-skel t3-skel-crumb"></div>' +
      '<div class="t3-skel t3-skel-title"></div>' +
      '<div class="t3-skel t3-skel-line"></div>' +
      '<div class="t3-skel t3-skel-line"></div>' +
      '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
      '<div class="t3-skel t3-skel-line t3-skel-short"></div>';

    if (kind === "hub") {
      main +=
        '<div class="t3-skel-card-row">' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        "</div>" +
        '<div class="t3-skel-card-row">' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        '<div class="t3-skel t3-skel-hub-card"></div>' +
        "</div>";
    } else if (kind === "install") {
      main +=
        '<div class="t3-skel t3-skel-step"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-code">' +
        '<div class="t3-skel t3-skel-code-bar"></div>' +
        '<div class="t3-skel t3-skel-code-line"></div>' +
        '<div class="t3-skel t3-skel-code-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-code-line t3-skel-short"></div>' +
        "</div>" +
        '<div class="t3-skel t3-skel-step"></div>' +
        '<div class="t3-skel t3-skel-line"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-panel"></div>' +
        '<div class="t3-skel t3-skel-step"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-code">' +
        '<div class="t3-skel t3-skel-code-bar"></div>' +
        '<div class="t3-skel t3-skel-code-line"></div>' +
        '<div class="t3-skel t3-skel-code-line t3-skel-short"></div>' +
        "</div>";
    } else {
      main +=
        '<div class="t3-skel t3-skel-panel"></div>' +
        '<div class="t3-skel t3-skel-line"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-code">' +
        '<div class="t3-skel t3-skel-code-bar"></div>' +
        '<div class="t3-skel t3-skel-code-line"></div>' +
        '<div class="t3-skel t3-skel-code-line"></div>' +
        '<div class="t3-skel t3-skel-code-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-code-line t3-skel-short"></div>' +
        "</div>" +
        '<div class="t3-skel t3-skel-line"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-short"></div>' +
        '<div class="t3-skel t3-skel-note"></div>' +
        '<div class="t3-skel t3-skel-line"></div>' +
        '<div class="t3-skel t3-skel-line t3-skel-mid"></div>';
    }
    main += "</div>";

    var toc =
      '<div class="t3-skel-toc" aria-hidden="true">' +
      '<div class="t3-skel t3-skel-toc-label"></div>' +
      '<div class="t3-skel t3-skel-toc-item"></div>' +
      '<div class="t3-skel t3-skel-toc-item t3-skel-mid"></div>' +
      '<div class="t3-skel t3-skel-toc-item"></div>' +
      '<div class="t3-skel t3-skel-toc-item t3-skel-short"></div>' +
      '<div class="t3-skel t3-skel-toc-item t3-skel-mid"></div>' +
      '<div class="t3-skel t3-skel-toc-item"></div>' +
      "</div>";

    return (
      '<div class="t3-page-hold-light t3-page-hold-light--' +
      kind +
      '" role="status" aria-live="polite" aria-label="Loading page">' +
      '<div class="t3-skel-layout">' +
      main +
      toc +
      "</div></div>"
    );
  }

  function skeletonKindForHref(href) {
    href = (href || "").split("?")[0].split("#")[0];
    var path = href || currentPath();
    if (/Installation|ReInstall|UpdateVersion|UpdateGuide|UpgradeGuide|QuickInstallation/i.test(path)) return "install";
    if (/\/(AllExtensions|AllTemplates|AIFoundationExtensions|T3AF|License|ExtNsT3[A-Z]{2}|EXT[A-Za-z]+)\/Index\/?$/i.test(path)) {
      return "hub";
    }
    return "docs";
  }

  function lockPageScroll() {
    if (scrollLocked) return;
    scrollLocked = true;
    lockedScrollY = window.scrollY || window.pageYOffset || 0;
    var gutter = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    document.documentElement.style.setProperty("--t3-scrollbar-gutter", gutter + "px");
    document.documentElement.style.setProperty("--t3-scroll-lock-top", "-" + lockedScrollY + "px");
    document.documentElement.classList.add("t3-scroll-locked");
  }

  function unlockPageScroll() {
    if (!scrollLocked) return;
    scrollLocked = false;
    document.documentElement.classList.remove("t3-scroll-locked");
    document.documentElement.style.removeProperty("--t3-scroll-lock-top");
    document.documentElement.style.removeProperty("--t3-scrollbar-gutter");
    window.scrollTo(0, lockedScrollY || 0);
    lockedScrollY = 0;
  }

  var holdScrollOpts = { passive: false, capture: true };

  function onHoldScrollBlock(e) {
    if (!document.documentElement.classList.contains("t3-holding") &&
        !document.documentElement.classList.contains("t3-nav-busy")) {
      return;
    }
    // Allow scrolling inside the mobile drawer if it is open
    if (document.documentElement.classList.contains("t3-mobile-nav-open")) return;
    var key = e.type === "keydown" ? e.key : "";
    if (e.type === "keydown") {
      if (
        key !== "ArrowUp" &&
        key !== "ArrowDown" &&
        key !== "PageUp" &&
        key !== "PageDown" &&
        key !== "Home" &&
        key !== "End" &&
        key !== " " &&
        key !== "Spacebar"
      ) {
        return;
      }
      // Don't trap typing in inputs
      var t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    }
    e.preventDefault();
  }

  function bindHoldScrollBlock(on) {
    if (on) {
      window.addEventListener("wheel", onHoldScrollBlock, holdScrollOpts);
      window.addEventListener("touchmove", onHoldScrollBlock, holdScrollOpts);
      window.addEventListener("keydown", onHoldScrollBlock, holdScrollOpts);
    } else {
      window.removeEventListener("wheel", onHoldScrollBlock, holdScrollOpts);
      window.removeEventListener("touchmove", onHoldScrollBlock, holdScrollOpts);
      window.removeEventListener("keydown", onHoldScrollBlock, holdScrollOpts);
    }
  }

  function captureHold(href) {
    // Legacy path: full-screen blur loader replaces opaque skeleton hold.
    showNavLoader();
    document.documentElement.classList.add("t3-holding");
    return true;
  }

  function setProgressWidth(v) {
    progressValue = Math.max(0, Math.min(99.5, v));
  }

  function clearProgressTimers() {
    if (progressTimer) {
      clearInterval(progressTimer);
      progressTimer = null;
    }
    if (progressDelay) {
      clearTimeout(progressDelay);
      progressDelay = null;
    }
    if (veilTimer) {
      clearTimeout(veilTimer);
      veilTimer = null;
    }
    if (holdReleaseTimer) {
      clearTimeout(holdReleaseTimer);
      holdReleaseTimer = null;
    }
    if (loaderSafetyTimer) {
      clearTimeout(loaderSafetyTimer);
      loaderSafetyTimer = null;
    }
    // Intentionally do NOT clear loaderHideTimer here — progress(false) settle
    // relies on the fade-out completing. progress(true) clears via hideNavLoader(true).
  }

  function showVeil() {
    ensureVeil().classList.add("t3-page-veil-active");
    document.documentElement.classList.add("t3-route-loading");
    // Soften frozen page under skeleton for slow hops
    if (holdEl) holdEl.classList.add("t3-page-hold-dim");
  }

  function hideVeil() {
    if (!veilEl) return;
    veilEl.classList.remove("t3-page-veil-active");
    document.documentElement.classList.remove("t3-route-loading");
  }

  function releaseHold(immediate) {
    document.documentElement.classList.remove("t3-holding");
    if (holdEl) {
      holdEl.classList.remove("t3-page-hold-active", "t3-page-hold-exit", "t3-page-hold-dim", "t3-page-hold-rich", "t3-page-hold-plain");
      if (holdInner) {
        holdInner.innerHTML = "";
        holdInner.style.transform = "";
      }
    }
    hideNavLoader(immediate);
  }

  function announceNav(msg) {
    var live = document.getElementById("t3-nav-live");
    if (!live) {
      live = document.createElement("div");
      live.id = "t3-nav-live";
      live.className = "sr-only";
      live.setAttribute("aria-live", "polite");
      live.setAttribute("aria-atomic", "true");
      document.body.appendChild(live);
    }
    live.textContent = msg;
  }

  function progress(active) {
    ensureNavLoader();
    if (active) {
      clearProgressTimers();
      navToken += 1;
      navStartedAt = Date.now();
      progressVisible = false;
      hideNavLoader(true);
      document.documentElement.classList.add("t3-nav-busy");
      document.documentElement.setAttribute("aria-busy", "true");

      // Flicker guard: show full-screen blur loader only when nav is still busy.
      var showMs = reducedMotion ? 0 : PROGRESS_SHOW_MS;
      progressDelay = setTimeout(function () {
        if (!document.documentElement.classList.contains("t3-nav-busy")) return;
        progressVisible = true;
        showNavLoader();
        announceNav("Loading page");
      }, showMs);

      // Hard safety: never leave blur overlay stuck.
      var tokenSafety = navToken;
      loaderSafetyTimer = setTimeout(function () {
        if (tokenSafety !== navToken) return;
        if (!document.documentElement.classList.contains("t3-nav-busy")) return;
        progress(false);
      }, LOADER_MAX_MS);
      return;
    }

    // Complete — wait until destination content is present, then settle UI.
    clearProgressTimers();
    var token = navToken;
    var elapsed = Date.now() - (navStartedAt || Date.now());
    var tries = 0;
    var wasVisible = progressVisible;

    function finish() {
      if (token !== navToken) return;
      document.documentElement.classList.remove("t3-nav-busy");
      document.documentElement.removeAttribute("aria-busy");
      pendingNavHref = "";
      userNavPriority = false;
      prefetchGateOpen = false;
      try {
        window.__t3PrefetchGateOpen = false;
      } catch (eGate2) {}
      hideVeil();

      if (elapsed >= 280 && !reducedMotion) {
        document.documentElement.classList.add("t3-route-enter");
        setTimeout(function () {
          document.documentElement.classList.remove("t3-route-enter");
        }, 180);
      }

      if (!wasVisible) {
        progressVisible = false;
        releaseHold(true);
        return;
      }

      announceNav("Page loaded");
      progressVisible = false;
      releaseHold(false);
    }

    function waitReady() {
      if (token !== navToken) return;
      if (contentLooksReady() || tries > 8) {
        if (typeof requestAnimationFrame === "function") requestAnimationFrame(finish);
        else setTimeout(finish, 0);
        return;
      }
      tries += 1;
      if (typeof requestAnimationFrame === "function") requestAnimationFrame(waitReady);
      else setTimeout(waitReady, 8);
    }

    waitReady();
  }

  function injectPerfHints() {
    if (document.getElementById("t3-perf-hints")) return;
    var frag = document.createDocumentFragment();
    var mark = document.createElement("meta");
    mark.id = "t3-perf-hints";
    mark.setAttribute("data-t3", "1");
    frag.appendChild(mark);
    // Mintlify loads Lucide/FontAwesome SVGs + KaTeX from CloudFront — warm the
    // connection early so ~30 icon requests don't each pay full TLS/DNS.
    [
      ["preconnect", "https://d3gk2c5xim1je2.cloudfront.net", "anonymous"],
      ["dns-prefetch", "https://d3gk2c5xim1je2.cloudfront.net"],
      ["preconnect", "https://d4tuoctqmanu0.cloudfront.net", "anonymous"],
      ["dns-prefetch", "https://d4tuoctqmanu0.cloudfront.net"],
      ["dns-prefetch", "https://app.supademo.com"],
    ].forEach(function (row) {
      var l = document.createElement("link");
      l.rel = row[0];
      l.href = row[1];
      if (row[2]) l.crossOrigin = row[2];
      frag.appendChild(l);
    });
    // Preload only the most common first-paint sidebar icons (avoid connection thrash).
    ["house", "sparkles", "puzzle"].forEach(function (name) {
      var l = document.createElement("link");
      l.rel = "preload";
      l.as = "image";
      l.href = "https://d3gk2c5xim1je2.cloudfront.net/lucide/v1.16.0/" + name + ".svg";
      frag.appendChild(l);
    });
    document.head.appendChild(frag);
  }

  function cleanRoute(href) {
    if (!href || href[0] !== "/") return href;
    var hash = href.indexOf("#");
    var query = href.indexOf("?");
    var cut = href.length;
    if (hash !== -1) cut = Math.min(cut, hash);
    if (query !== -1) cut = Math.min(cut, query);
    var base = href.slice(0, cut);
    var tail = href.slice(cut);
    if (base.length > 5 && base.slice(-5) === ".html") {
      base = base.slice(0, -5);
      if (base === "/index" || base === "/Index") base = "/";
    }
    // Mintlify file routes use capital Index; lowercase /index 404s or loops.
    if (base === "/index" || base === "/Index") {
      base = "/";
    } else if (base.length > 6 && /\/index\/?$/i.test(base)) {
      base = base.replace(/\/index\/?$/i, "/Index");
    }
    // Strip trailing slash except root
    if (base.length > 1 && base.charAt(base.length - 1) === "/") {
      base = base.slice(0, -1);
    }
    return base + tail;
  }

  function shouldPrefetch() {
    try {
      var c = navigator.connection;
      if (c && (c.saveData || c.effectiveType === "2g" || c.effectiveType === "slow-2g")) return false;
    } catch (e) {}
    // Local mint compiles every RSC prefetch — never idle-flood the queue.
    if (isLocalMintDev() && !prefetchGateOpen) return false;
    if (prefetchSessionCount >= PREFETCH_SESSION_MAX) return false;
    return prefetchPending < PREFETCH_MAX;
  }

  function gateLocalRscFetch() {
    if (gateLocalRscFetch.done || !isLocalMintDev()) return;
    gateLocalRscFetch.done = true;
    try {
      if (typeof window.fetch !== "function" || window.fetch.__t3RscGated) return;
      var origFetch = window.fetch.bind(window);
      window.fetch = function (input, init) {
        var url = "";
        try {
          if (typeof input === "string") url = input;
          else if (input && typeof input.url === "string") url = input.url;
        } catch (eUrl) {}
        // Block Mintlify/Next automatic RSC prefetches that flood local compile.
        // Allow RSC while a user navigation is in flight (t3-nav-busy / pending href),
        // otherwise a 4s gate timeout 204s mid-compile and SPA stalls for 6–9s.
        if (
          url &&
          (url.indexOf("?_rsc=") !== -1 || url.indexOf("&_rsc=") !== -1) &&
          !prefetchGateOpen &&
          !window.__t3PrefetchGateOpen &&
          !document.documentElement.classList.contains("t3-nav-busy") &&
          !(pendingNavHref && url.indexOf(pendingNavHref.split("#")[0].split("?")[0]) !== -1)
        ) {
          return Promise.resolve(
            new Response("", {
              status: 204,
              statusText: "No Content",
              headers: { "Cache-Control": "no-store" },
            })
          );
        }
        return origFetch(input, init);
      };
      window.fetch.__t3RscGated = 1;
    } catch (eGate) {}
  }

  function gateNextRouterPrefetch() {
    if (gateNextRouterPrefetch.done) return;
    function tryPatch() {
      try {
        if (!window.next || !window.next.router || !window.next.router.prefetch) return false;
        if (window.next.router.__t3PrefetchGated) {
          gateNextRouterPrefetch.done = true;
          return true;
        }
        var orig = window.next.router.prefetch.bind(window.next.router);
        window.next.router.prefetch = function () {
          // Block Mintlify/Next viewport prefetches on local (hundreds of ?_rsc compiles).
          // Production CDN serves prebuilt RSC — leave native prefetch alone.
          if (isLocalMintDev() && !prefetchGateOpen && !document.documentElement.classList.contains("t3-nav-busy")) {
            return typeof Promise !== "undefined" ? Promise.resolve() : undefined;
          }
          return orig.apply(null, arguments);
        };
        window.next.router.__t3PrefetchGated = 1;
        gateNextRouterPrefetch.done = true;
        return true;
      } catch (err) {
        return false;
      }
    }
    if (tryPatch()) return;
    var n = 0;
    var t = setInterval(function () {
      if (tryPatch() || ++n > 60) clearInterval(t);
    }, 50);
  }

  function nextPrefetch(href) {
    try {
      if (window.next && window.next.router && window.next.router.prefetch) {
        window.next.router.prefetch(href);
        return true;
      }
    } catch (e2) {}
    return false;
  }

  function prefetch(href) {
    href = cleanRoute(href);
    if (!href || href[0] !== "/" || href[1] === "/" || prefetched[href]) return;
    // Intent-only on local mint; tiny idle budget on production CDN
    if (isLocalMintDev() && !prefetchGateOpen) return;
    if (!shouldPrefetch() && !prefetchGateOpen) return;
    prefetched[href] = 1;
    prefetchPending++;
    prefetchSessionCount++;
    var prevGate = prefetchGateOpen;
    prefetchGateOpen = true;
    try {
      if (!nextPrefetch(href)) {
        var l = document.createElement("link");
        l.rel = "prefetch";
        l.href = href;
        l.as = "document";
        document.head.appendChild(l);
      }
    } finally {
      prefetchGateOpen = prevGate;
    }
    setTimeout(function () {
      prefetchPending = Math.max(0, prefetchPending - 1);
    }, 1200);
  }

  function abortBackgroundPrefetch() {
    // Free browser connections so a real click→location.assign is never queued.
    try {
      for (var i = 0; i < docPrefetchControllers.length; i++) {
        try {
          docPrefetchControllers[i].abort();
        } catch (eAb) {}
      }
    } catch (eList) {}
    docPrefetchControllers = [];
    // Drop link[rel=prefetch] tags we added — they also occupy HTTP/2 slots.
    try {
      var nodes = document.querySelectorAll('link[data-t3-doc-prefetch="1"]');
      for (var n = 0; n < nodes.length; n++) {
        try {
          nodes[n].parentNode.removeChild(nodes[n]);
        } catch (eRm) {}
      }
    } catch (eNodes) {}
  }

  function pauseBackgroundWarmForUserNav() {
    userNavPriority = true;
    abortBackgroundPrefetch();
  }

  function hardNavigate(go) {
    // Free HTTP/1.1 sockets (mint BYPASS can HOL-block the document ~10s),
    // but NEVER assign in the same synchronous turn as stop() — Chromium
    // can cancel that assign (first click stays on home). Defer one task.
    try {
      if (typeof window.stop === "function") window.stop();
    } catch (eStop) {}
    var target = go;
    setTimeout(function () {
      try {
        window.location.assign(target);
      } catch (eAssign) {
        window.location.href = target;
      }
    }, 0);
  }

  function warmPathViaProxy(href) {
    // Proxy-side warm returns 202 quickly and does not download HTML in the browser.
    href = cleanRoute(href || "");
    if (!href || href[0] !== "/") return;
    if (!isBehindCacheProxy()) return;
    if (userNavPriority) return;
    try {
      if (typeof fetch !== "function") return;
      var ctrl = null;
      var init = { credentials: "same-origin", cache: "no-store" };
      if (typeof AbortController === "function") {
        ctrl = new AbortController();
        init.signal = ctrl.signal;
        docPrefetchControllers.push(ctrl);
      }
      fetch("/__t3_cache_warm?path=" + encodeURIComponent(href), init)
        .catch(function () {})
        .finally(function () {
          if (!ctrl) return;
          var ix = docPrefetchControllers.indexOf(ctrl);
          if (ix >= 0) docPrefetchControllers.splice(ix, 1);
        });
    } catch (eWarm) {}
  }

  function prefetchDocument(href, opts) {
    href = cleanRoute(href || "");
    if (!href || href[0] !== "/") return;
    opts = opts || {};
    // Background warm must never compete with an in-flight user navigation.
    if (userNavPriority && !opts.priority) return;
    if (prefetched["doc:" + href] && !opts.force) return;
    prefetched["doc:" + href] = 1;

    // Behind :3000: warm server-side only. Full-document fetch/prefetch in the
    // browser saturated the connection pool and delayed location.assign by 10–30s.
    if (isBehindCacheProxy() && !opts.browserFetch) {
      warmPathViaProxy(href);
      return;
    }

    try {
      var l = document.createElement("link");
      l.rel = "prefetch";
      l.as = "document";
      l.href = href;
      l.setAttribute("data-t3-doc-prefetch", "1");
      document.head.appendChild(l);
    } catch (ePref) {}
    // Raw mint / explicit browserFetch: warm compile via a cancellable fetch.
    try {
      if (typeof fetch === "function") {
        var ctrl = null;
        var init = { credentials: "same-origin", cache: "force-cache" };
        if (typeof AbortController === "function") {
          ctrl = new AbortController();
          init.signal = ctrl.signal;
          docPrefetchControllers.push(ctrl);
        }
        fetch(href, init)
          .catch(function () {})
          .finally(function () {
            if (!ctrl) return;
            var ix = docPrefetchControllers.indexOf(ctrl);
            if (ix >= 0) docPrefetchControllers.splice(ix, 1);
          });
      }
    } catch (eFetch) {}
  }

  function isBehindCacheProxy() {
    // Local stack: mint :3001, cache proxy :3000 (LAN demo URL).
    try {
      var port = String(location.port || "");
      return port === "3000";
    } catch (e) {
      return false;
    }
  }

  function warmHomeOnLocal() {
    if (!isLocalMintDev()) return;
    if (currentPath() === "/") return;
    // Compile + cache home in the background so logo click is not a cold 6–9s load.
    idle(function () {
      prefetchDocument("/");
    }, 500);
  }

  function warmHubsBehindProxy() {
    // Behind :3000 the HTML cache proxy absorbs cold mint compiles.
    // Warm more hubs, but still sequential + spaced so we never saturate
    // the browser connection pool (that made location.assign hang).
    if (!isBehindCacheProxy()) return;
    var hubs = HUB_ROUTES.slice(0, 6);
    var i = 0;
    function next() {
      if (i >= hubs.length) return;
      // Yield immediately when the user is navigating (hard assign needs free sockets).
      if (
        userNavPriority ||
        document.documentElement.classList.contains("t3-nav-busy") ||
        document.documentElement.classList.contains("t3-holding")
      ) {
        idle(next, 2500);
        return;
      }
      var href = hubs[i++];
      if (href === currentPath()) {
        idle(next, 40);
        return;
      }
      // Proxy-side warm only (no browser HTML download).
      warmPathViaProxy(href);
      idle(next, 1600);
    }
    idle(next, 1500);
  }

  function prefetchAdjacentBehindProxy() {
    // After a warm page settles, quietly warm likely next hops into the proxy.
    if (!isBehindCacheProxy()) return;
    try {
      var pag = document.getElementById("pagination");
      if (pag) {
        pag.querySelectorAll('a[href^="/"]').forEach(function (a) {
          prefetchDocument(a.getAttribute("href") || "");
        });
      }
      var sb = document.getElementById("sidebar-content");
      if (!sb) return;
      var links = sb.querySelectorAll('a[href^="/"]');
      var cur = currentPath();
      var idx = -1;
      var hrefs = [];
      for (var i = 0; i < links.length; i++) {
        var h = cleanRoute(links[i].getAttribute("href") || "");
        if (!h) continue;
        hrefs.push(h);
        if (h === cur) idx = hrefs.length - 1;
      }
      var picks = [];
      if (idx >= 0) {
        if (hrefs[idx - 1]) picks.push(hrefs[idx - 1]);
        if (hrefs[idx + 1]) picks.push(hrefs[idx + 1]);
        if (hrefs[idx + 2]) picks.push(hrefs[idx + 2]);
      }
      // Also first few siblings under the same product prefix
      var prefix = cur.split("/").slice(0, 2).join("/") + "/";
      for (var j = 0; j < hrefs.length && picks.length < 6; j++) {
        if (hrefs[j].indexOf(prefix) === 0 && hrefs[j] !== cur && picks.indexOf(hrefs[j]) === -1) {
          picks.push(hrefs[j]);
        }
      }
      picks.slice(0, 4).forEach(function (href, n) {
        setTimeout(function () {
          try {
            fetch("/__t3_cache_warm?path=" + encodeURIComponent(href), {
              credentials: "same-origin",
              cache: "no-store",
            }).catch(function () {});
          } catch (e1) {}
          prefetchDocument(href);
        }, 800 + n * 900);
      });
    } catch (eAdj) {}
  }

  function bindLogoHomePrefetch() {
    function isLogoHome(a) {
      if (!a) return false;
      var href = cleanRoute(a.getAttribute("href") || "");
      if (href !== "/" && href !== "/Index") return false;
      return !!(
        a.querySelector("img.nav-logo, img[src*='t3planet'], img[alt*='logo'], img[alt*='Logo']") ||
        a.querySelector("span.sr-only")
      );
    }
    document.addEventListener(
      "pointerenter",
      function (e) {
        var a = e.target.closest && e.target.closest('a[href="/"], a[href="/Index"], a[href="/Index/"]');
        if (!isLogoHome(a)) return;
        prefetchDocument("/");
        prefetchOnIntent("/");
      },
      true
    );
    document.addEventListener(
      "pointerdown",
      function (e) {
        var a = e.target.closest && e.target.closest('a[href="/"], a[href="/Index"], a[href="/Index/"]');
        if (!isLogoHome(a)) return;
        prefetchDocument("/");
      },
      { capture: true, passive: true }
    );
  }

  function prefetchHubs() {
    if (isLocalMintDev()) return;
    HUB_ROUTES.forEach(prefetch);
  }

  function isLocalMintDev() {
    try {
      var h = location.hostname || "";
      return h === "localhost" || h === "127.0.0.1" || /^192\.168\./.test(h) || /^10\./.test(h);
    } catch (e) {
      return false;
    }
  }

  function prefetchRouteManifest() {
    // Never flood mint compile queue. Production: warm a handful of hubs only.
    if (isLocalMintDev()) return;
    if (!shouldPrefetch()) return;
    HUB_ROUTES.forEach(prefetch);
  }

  function prefetchNeighbors() {
    if (isLocalMintDev()) return;
    var pag = document.getElementById("pagination");
    if (!pag) return;
    pag.querySelectorAll('a[href^="/"]').forEach(function (a) {
      prefetch(a.getAttribute("href") || "");
    });
  }

  function prefetchVisibleSidebar() {
    // Sidebar can contain 100+ links — idle prefetch of these is what created
    // 200+ ?_rsc requests and multi-minute loads on mint dev.
    if (isLocalMintDev()) return;
    var sb = document.getElementById("sidebar-content");
    if (!sb) return;
    var links = sb.querySelectorAll('a[href^="/"]');
    var n = Math.min(links.length, 8);
    for (var i = 0; i < n; i++) prefetch(links[i].getAttribute("href") || "");
  }

  var prefetchOnIntent = function (href) {
    // Allow a single intentional hover/focus prefetch even on local mint.
    // Idle/viewport floods stay gated; this warms only the link the user aims at.
    if (isBehindCacheProxy()) {
      prefetchDocument(href);
    }
    prefetchGateOpen = true;
    try {
      prefetch(href);
    } finally {
      // Keep gate open long enough for local mint to finish compiling this one route.
      setTimeout(function () {
        if (!document.documentElement.classList.contains("t3-nav-busy")) {
          prefetchGateOpen = false;
        }
      }, isLocalMintDev() ? 15000 : 400);
    }
  };

  function ensureImgObserver() {
    if (imgIo || !("IntersectionObserver" in window)) return imgIo;
    imgIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var img = entry.target;
          applyLazyImage(img, Number(img.getAttribute("data-t3-idx") || "0"));
          imgIo.unobserve(img);
        });
      },
      { rootMargin: "100px 0px" }
    );
    return imgIo;
  }

  function applyLazyImage(img, idx) {
    if (!img || img.getAttribute("data-t3")) return;
    // Skip chrome logos / decorative nav marks
    var src = img.getAttribute("src") || img.getAttribute("data-src") || "";
    if (/\/_static\/(t3planet|logo|favicon)/i.test(src)) {
      img.setAttribute("data-t3", "1");
      if (!img.getAttribute("decoding")) img.decoding = "async";
      return;
    }
    img.setAttribute("data-t3", "1");
    // Reserve space when dimensions are known (reduces CLS on long docs).
    try {
      if (!img.getAttribute("width") && img.naturalWidth > 0) {
        img.setAttribute("width", String(img.naturalWidth));
      }
      if (!img.getAttribute("height") && img.naturalHeight > 0) {
        img.setAttribute("height", String(img.naturalHeight));
      }
    } catch (eDim) {}
    // First in-content image stays eager for LCP; everything else lazy.
    // Also lazy any image whose top is below the first viewport.
    var belowFold = false;
    try {
      var top = img.getBoundingClientRect().top;
      belowFold = top > (window.innerHeight || 800) * 0.9;
    } catch (eRect) {}
    if (idx > 0 || belowFold) {
      img.loading = "lazy";
      if (!img.getAttribute("fetchpriority")) img.setAttribute("fetchpriority", "low");
    } else if (!img.getAttribute("fetchpriority")) {
      img.setAttribute("fetchpriority", "high");
    }
    if (!img.getAttribute("decoding")) img.decoding = "async";
  }

  function collectContentRoots() {
    var roots = [];
    var primary = contentRoot();
    if (primary) roots.push(primary);
    var main = document.querySelector("main");
    if (main && roots.indexOf(main) === -1) roots.push(main);
    var article = document.querySelector("article");
    if (article && roots.indexOf(article) === -1) roots.push(article);
    return roots;
  }

  function lazyImages() {
    var roots = collectContentRoots();
    if (!roots.length) return;
    var seen = [];
    for (var r = 0; r < roots.length; r++) {
      var imgs = roots[r].querySelectorAll("img:not([data-t3])");
      for (var i = 0; i < imgs.length; i++) {
        if (seen.indexOf(imgs[i]) !== -1) continue;
        seen.push(imgs[i]);
      }
    }
    for (var j = 0; j < seen.length; j++) {
      applyLazyImage(seen[j], j);
    }
  }

  function observeLateMedia() {
    if (observeLateMedia.done || !("MutationObserver" in window)) return;
    observeLateMedia.done = true;
    var sched = null;
    var mo = new MutationObserver(function () {
      if (sched) return;
      sched = setTimeout(function () {
        sched = null;
        lazyImages();
        lazyIframes();
      }, 40);
    });
    try {
      mo.observe(document.documentElement, { childList: true, subtree: true });
    } catch (eMo) {}
  }

  function ensureIframeObserver() {
    if (iframeIo || !("IntersectionObserver" in window)) return iframeIo;
    iframeIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          activateIframe(entry.target);
          iframeIo.unobserve(entry.target);
        });
      },
      { rootMargin: "120px 0px" }
    );
    return iframeIo;
  }

  function activateIframe(iframe) {
    var src = iframe.getAttribute("data-t3-src");
    if (!src || iframe.getAttribute("src")) return;
    iframe.setAttribute("src", src);
    iframe.removeAttribute("data-t3-src");
    iframe.removeAttribute("data-t3-iframe");
  }

  function lazyIframes() {
    var root = contentRoot();
    if (!root) return;
    var frames = root.querySelectorAll("iframe[src]:not([data-t3-iframe])");
    if (!frames.length) return;
    for (var i = 0; i < frames.length; i++) {
      var iframe = frames[i];
      var src = iframe.getAttribute("src");
      if (!src) continue;
      iframe.setAttribute("data-t3-iframe", "1");
      iframe.setAttribute("data-t3-src", src);
      iframe.removeAttribute("src");
    }
    var pending = root.querySelectorAll("iframe[data-t3-src]");
    if (!pending.length) return;
    var io = ensureIframeObserver();
    if (!io) {
      pending.forEach(activateIframe);
      return;
    }
    pending.forEach(function (f) {
      if (!f.getAttribute("src")) io.observe(f);
    });
  }

  function canonicalCleanUrl() {
    var p = currentPath();
    if (!p.endsWith(".html")) return;
    var clean = p.slice(0, -5);
    if (clean === "/index") clean = "/";
    history.replaceState(null, "", clean + location.search + location.hash);
    routePath = clean;
  }

  function rewriteLinksIn(root) {
    if (!root) return;
    var links = root.querySelectorAll('a[href*=".html"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute("href");
      if (!href || href[0] !== "/" || href[0] === "#") continue;
      var next = cleanRoute(href);
      if (next !== href) a.setAttribute("href", next);
    }
  }

  function rewriteStaticLinks() {
    if (staticLinksDone) return;
    staticLinksDone = true;
    rewriteLinksIn(document.getElementById("navbar"));
    rewriteLinksIn(document.getElementById("sidebar-content"));
    rewriteLinksIn(document.getElementById("pagination"));
    rewriteLinksIn(document.querySelector("footer"));
    document.querySelectorAll(".t3-category-nav a[href^='/']").forEach(function (a) {
      var href = cleanRoute(a.getAttribute("href") || "");
      if (href !== a.getAttribute("href")) a.setAttribute("href", href);
    });
  }

  function rewriteContentLinks() {
    rewriteLinksIn(contentRoot());
  }

  function syncNavbarHeight() {
    var nav = document.getElementById("navbar");
    if (!nav) return;
    var h = Math.max(64, Math.ceil(nav.getBoundingClientRect().bottom) + 6);
    document.documentElement.style.setProperty("--t3-navbar-height", h + "px");
  }

  function formatStat(value, lang) {
    return lang === "de" ? String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ".") : value.toLocaleString("en-US");
  }

  function applyDocStats(stats) {
    if (!stats) return;
    var lang = document.documentElement.lang === "de" ? "de" : "en";
    var bucket = stats[lang] || stats.en || {};
    document.querySelectorAll("[data-t3-stat]").forEach(function (el) {
      var key = el.getAttribute("data-t3-stat");
      if (!key || key === "locale") return;
      var value = bucket[key];
      if (typeof value !== "number") return;
      el.textContent = formatStat(value, lang);
    });
    statsLoaded = true;
  }

  function hydrateDocStats() {
    if (statsLoaded) return;
    if (window.__T3_DOC_STATS__) {
      applyDocStats(window.__T3_DOC_STATS__);
      return;
    }
    fetch("/_static/t3-stats.json", { priority: "low" })
      .then(function (res) {
        if (!res.ok) throw new Error("stats");
        return res.json();
      })
      .then(applyDocStats)
      .catch(function () {});
  }

  function enhanceContentCritical() {
    applyContentClasses();
    rewriteContentLinks();
    // Defer heavy iframes BEFORE the browser starts dozens of embed navigations.
    lazyIframes();
    lazyImages();
  }

  function enhanceContentDeferred() {
    lazyIframes();
    lazyImages();
    // Production CDN: RSC neighbor prefetch.
    // Cache proxy: document warm into :3000 memory (no RSC flood).
    if (!isLocalMintDev()) prefetchNeighbors();
    else if (isBehindCacheProxy()) prefetchAdjacentBehindProxy();
  }

  var onRouteChange = debounce(function () {
    var next = currentPath();
    if (next === routePath) {
      applyRouteClasses();
      progress(false);
      return;
    }
    routePath = next;
    canonicalCleanUrl();
    applyRouteClasses();
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(function () {
        enhanceContentCritical();
        idle(enhanceContentDeferred, 300);
      });
    } else {
      enhanceContentCritical();
      idle(enhanceContentDeferred, 300);
    }
    progress(false);
  }, 8);

  function patchHistory() {
    if (patchHistory.done) return;
    patchHistory.done = true;
    var origPush = history.pushState;
    if (origPush) {
      history.pushState = function () {
        var result = origPush.apply(this, arguments);
        onRouteChange();
        return result;
      };
    }
    try {
      if (window.next && window.next.router && window.next.router.events) {
        window.next.router.events.on("routeChangeStart", function () {
          // Ignore framework/boot starts — only show hold for user-initiated nav
          if (!pendingNavHref && !document.documentElement.classList.contains("t3-nav-busy")) return;
          progress(true);
        });
        window.next.router.events.on("routeChangeComplete", onRouteChange);
        window.next.router.events.on("routeChangeError", function () {
          progress(false);
        });
      }
    } catch (e3) {}
  }

  
  function isInternalNavAnchor(a) {
    if (!a || a.target === "_blank") return null;
    var href = cleanRoute(a.getAttribute("href") || "");
    if (!href || href[0] !== "/" || href[1] === "/") return null;
    var pathOnly = (href.split("#")[0].split("?")[0] || "/").replace(/\/$/, "") || "/";
    if (pathOnly === currentPath()) return null;
    // Skip static/asset downloads (not SPA doc routes)
    if (/\.(txt|json|xml|css|js|map|png|jpe?g|gif|webp|svg|pdf|zip)$/i.test(pathOnly)) return null;
    return href;
  }

  function beginNavFromLink(href, opts) {
    if (!href) return;
    opts = opts || {};
    pendingNavHref = href;
    prefetchGateOpen = true;
    // Keep the early-inline RSC gate in sync (it only checks __t3PrefetchGateOpen).
    try {
      window.__t3PrefetchGateOpen = true;
    } catch (eGate) {}
    try {
      prefetch(href);
    } catch (ePrefetch) {}
    // Do NOT auto-close the gate on a timer. Mint local RSC often takes >4s;
    // closing early 204s the in-flight navigation. Gate closes in progress(false).
    // Production CDN: progress bar only (matches live Sphinx — no opaque hold).
    // Local mint: opaque hold only when navigation is committed (click), never on
    // pointerdown — a hold with pointer-events between pointerdown and click
    // steals the click, so location.assign never runs and the skeleton sticks.
    if (opts.deferHold) return;
    if (isLocalMintDev()) {
      if (!document.documentElement.classList.contains("t3-nav-busy")) {
        progress(true);
      } else if (!document.documentElement.classList.contains("t3-holding")) {
        captureHold(href);
      }
    } else if (!document.documentElement.classList.contains("t3-nav-busy")) {
      progress(true);
    }
  }

  function bindPrefetchPointerDown() {
    document.addEventListener(
      "pointerdown",
      function (e) {
        if (e.button !== 0 && e.pointerType !== "touch") return;
        var a = e.target.closest && e.target.closest('a[href^="/"]');
        var href = isInternalNavAnchor(a);
        if (!href) return;
        // Warm prefetch only — do not paint hold/busy until click commits nav.
        beginNavFromLink(href, { deferHold: true });
        if (isLocalMintDev()) {
          try {
            prefetchDocument(href, { priority: true });
          } catch (eDoc) {}
        }
      },
      { capture: true, passive: true }
    );
  }

  function bindPrefetchIntent() {
    var root = document;
    root.addEventListener(
      "pointerenter",
      function (e) {
        var a = e.target.closest && e.target.closest('a[href^="/"]');
        if (!a || a.target === "_blank") return;
        var href = cleanRoute(a.getAttribute("href") || "");
        if (!href || href[0] === "#" || href === currentPath()) return;
        prefetchOnIntent(href);
      },
      true
    );
    root.addEventListener(
      "focusin",
      function (e) {
        var a = e.target.closest && e.target.closest('a[href^="/"]');
        if (!a) return;
        prefetchOnIntent(cleanRoute(a.getAttribute("href") || ""));
      },
      true
    );
  }

  function openSearch() {
    var desktop = document.getElementById("search-bar-entry");
    var mobile = document.getElementById("search-bar-entry-mobile");
    var trigger = desktop || mobile;
    if (trigger && typeof trigger.click === "function") {
      trigger.click();
      return true;
    }
    try {
      var ev = new KeyboardEvent("keydown", {
        key: "k",
        code: "KeyK",
        metaKey: true,
        ctrlKey: true,
        bubbles: true,
      });
      document.dispatchEvent(ev);
      return true;
    } catch (e4) {}
    return false;
  }

  function bindSearchTriggers() {
    document.addEventListener(
      "click",
      function (e) {
        var btn = e.target.closest && e.target.closest("[data-t3-search-trigger]");
        if (!btn) return;
        e.preventDefault();
        openSearch();
      },
      false
    );
  }


  function recoverEmptyDocOnce() {
    if (window.__t3EmptyRecovered) return;
    // Only on local preview behind proxy
    if (!isBehindCacheProxy()) return;
    // Never fight an in-flight hard navigation (would yank user back with ?_t3r=).
    if (
      pendingNavHref ||
      document.documentElement.classList.contains("t3-nav-busy") ||
      document.documentElement.classList.contains("t3-holding")
    ) {
      return;
    }
    var root = contentRoot();
    if (!root) return;
    var text = (root.innerText || "").replace(/\s+/g, " ").trim();
    // Real docs pages have substantial text; empty/skeleton shells do not.
    if (text.length > 80) return;
    // Ignore true hubs that are card-only but still have labels
    if (root.querySelector("h1, h2, .t3-home-landing, .t3-hub-landing, article p")) {
      var t2 = (root.innerText || "").replace(/\s+/g, " ").trim();
      if (t2.length > 40) return;
    }
    // Hub / landing routes with a real title are never "empty cache" — skip.
    if (/\/Index\/?$/i.test(currentPath()) && root.querySelector("h1")) return;
    window.__t3EmptyRecovered = 1;
    try {
      var pathAtRecover = currentPath();
      var u = new URL(location.href);
      if (u.searchParams.get("_t3r")) return;
      u.searchParams.set("_t3r", String(Date.now()));
      // Drop ONLY this path from the proxy cache — never purge everything
      // (full purge made the next hop cold and felt like a bounce to home).
      try {
        fetch(
          "/__t3_cache_purge?path=" + encodeURIComponent(pathAtRecover),
          { cache: "no-store" }
        ).catch(function () {});
      } catch (ePurge) {}
      setTimeout(function () {
        // Abort if the user already navigated away or a nav started.
        if (currentPath() !== pathAtRecover) return;
        if (
          pendingNavHref ||
          document.documentElement.classList.contains("t3-nav-busy") ||
          document.documentElement.classList.contains("t3-holding")
        ) {
          return;
        }
        location.replace(u.pathname + u.search + u.hash);
      }, 150);
    } catch (eRec) {}
  }

  var hardNavBound = false;
  function bindHardNavClicks() {
    if (hardNavBound) return;
    hardNavBound = true;
    try { window.__t3HardNav = 1; } catch (eMark) {}
    // Capture as early as possible so first click after home load is not
    // swallowed by Mintlify SPA (that path hangs / bounces to home).
    document.addEventListener(
      "click",
      function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        var a = e.target.closest && e.target.closest('a[href^="/"]');
        var href = isInternalNavAnchor(a);
        if (!href) return;
        if (href !== a.getAttribute("href")) a.setAttribute("href", href);
        if (isLocalMintDev()) {
          var go = cleanRoute(href);
          if (go === "/Index") go = "/";
          pendingNavHref = go;
          pauseBackgroundWarmForUserNav();
          e.preventDefault();
          e.stopPropagation();
          try {
            e.stopImmediatePropagation();
          } catch (eStop) {}
          try {
            progress(true);
          } catch (eUi) {}
          hardNavigate(go);
          return;
        }
        beginNavFromLink(href);
      },
      true
    );
  }

  function canonicalizeIndexPath() {
    // Mintlify routes are /…/Index; lowercase /index works but breaks cache keys
    // and can feel like a first-click bounce when mixed with capital Index links.
    try {
      var p = location.pathname || "/";
      if (p === "/index" || p === "/Index/") {
        history.replaceState(null, "", "/" + location.search + location.hash);
        return;
      }
      if (/\/index\/?$/i.test(p) && !/\/Index\/?$/.test(p)) {
        var fixed = p.replace(/\/index\/?$/i, "/Index");
        history.replaceState(null, "", fixed + location.search + location.hash);
      }
    } catch (eCanon) {}
  }

  function init() {
    if (document.documentElement.dataset.t3DocsInit === "1") return;
    document.documentElement.dataset.t3DocsInit = "1";
    canonicalizeIndexPath();

  // Safety: never leave skeleton/hold painted forever (bad cache / hung RSC).
  setInterval(function () {
    try {
      if (!document.documentElement.classList.contains("t3-holding") &&
          !document.documentElement.classList.contains("t3-nav-busy")) return;
      if (!navStartedAt) return;
      if (Date.now() - navStartedAt < 12000) return;
      progress(false);
    } catch (eSafe) {}
  }, 2000);

    injectPerfHints();
    gateNextRouterPrefetch();
    ensureProgress();
    canonicalCleanUrl();
    routePath = currentPath();
    document.documentElement.classList.add("t3-sidebar-ready");
    applyRouteClasses();
    syncNavbarHeight();
    patchHistory();
    // Intent-only hover prefetch (single link). Idle/viewport floods stay gated.
    bindPrefetchIntent();
    bindPrefetchPointerDown();
    bindSearchTriggers();

    window.addEventListener(
      "resize",
      debounce(function () {
        syncNavbarHeight();
        applyOverlayBounds(holdEl);
        applyOverlayBounds(veilEl);
      }, 150),
      { passive: true }
    );

    bindHardNavClicks();

    window.addEventListener("popstate", function () {
      // History nav may already be mid-swap — freeze if possible, else skeleton ASAP
      progress(true);
      if (!document.documentElement.classList.contains("t3-holding")) {
        showVeil();
      }
      onRouteChange();
    });

    rewriteStaticLinks();
    enhanceContentCritical();
    observeLateMedia();
    setTimeout(recoverEmptyDocOnce, 1200);
    bindMobileNavEnhancements();
    bindLogoHomePrefetch();
    // Re-apply after Mintlify hydrates MDX images / embeds
    setTimeout(function () {
      lazyIframes();
      lazyImages();
    }, 120);
    setTimeout(function () {
      lazyIframes();
      lazyImages();
    }, 600);
    idle(enhanceContentDeferred, 200);
    idle(hydrateDocStats, 50);
    warmHomeOnLocal();
    // Behind cache proxy: warm hub HTML into proxy memory (no RSC flood).
    // Production CDN: native idle prefetch of hubs + a few sidebar links.
    if (isBehindCacheProxy()) {
      idle(warmHubsBehindProxy, 400);
    } else if (!isLocalMintDev()) {
      idle(prefetchHubs, 400);
      idle(prefetchVisibleSidebar, 800);
    }
  }

  gateLocalRscFetch();
  gateNextRouterPrefetch();
  // Bind nav interceptor immediately — do not wait for DOMContentLoaded/init.
  // First click from home often happens before init() and was falling through
  // to Mintlify SPA (stay on home / require second click).
  bindHardNavClicks();
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
