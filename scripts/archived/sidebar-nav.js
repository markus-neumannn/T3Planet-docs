/**
 * T3Planet Docs — sidebar (deferred setup, no per-route JS work).
 * Mintlify handles active links and client navigation; we only add layout + prefetch.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "t3-sidebar-groups";
  var cachedState = null;
  var prefetched = Object.create(null);
  var setupDone = false;

  function getSidebarContent() {
    return document.getElementById("sidebar-content");
  }

  function isHomepage() {
    var path = (window.location.pathname || "/").split("?")[0].split("#")[0];
    if (path.length > 1 && path.endsWith("/")) path = path.slice(0, -1);
    return path === "/" || path === "/de" || path === "/de/index";
  }

  function syncNavbarOffset() {
    var navbar = document.getElementById("navbar");
    var sidebar =
      document.getElementById("sidebar") ||
      document.querySelector('[data-component-part="sidebar"]');
    var offset = 76;
    if (navbar) offset = Math.ceil(navbar.getBoundingClientRect().bottom) + 6;
    if (offset < 64) offset = 64;
    document.documentElement.style.setProperty("--t3-navbar-height", offset + "px");
    if (sidebar && window.innerWidth >= 1024) {
      sidebar.style.top = "var(--t3-navbar-height)";
      sidebar.style.bottom = "0";
      sidebar.style.display = "block";
      sidebar.style.visibility = "visible";
      sidebar.style.transform = "none";
    }
  }

  function loadExpandedState() {
    if (cachedState) return cachedState;
    try {
      cachedState = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (e) {
      cachedState = {};
    }
    return cachedState;
  }

  function saveExpandedState(state) {
    cachedState = state;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      /* ignore */
    }
  }

  function groupKey(header) {
    return (header.textContent || "").trim();
  }

  function setSectionExpanded(section, header, expanded) {
    section.classList.toggle("t3-sidebar-collapsed", !expanded);
    section.classList.toggle("t3-sidebar-expanded", expanded);
    if (header) header.setAttribute("aria-expanded", expanded ? "true" : "false");
  }

  function enhanceCollapsibleGroups() {
    var content = getSidebarContent();
    if (!content) return;

    var state = loadExpandedState();
    content
      .querySelectorAll(
        ".sidebar-group-header:not([data-t3-group-enhanced]), h5:not([data-t3-group-enhanced]), h4:not([data-t3-group-enhanced])"
      )
      .forEach(function (header) {
        var section =
          header.closest(".t3-sidebar-group") ||
          header.closest("[data-sidebar-group]") ||
          header.closest(".mt-6") ||
          header.parentElement;
        if (!section) return;

        section.classList.add("t3-sidebar-group");
        header.setAttribute("data-t3-group-enhanced", "1");
        header.setAttribute("role", "button");
        if (!header.hasAttribute("tabindex")) header.setAttribute("tabindex", "0");

        var key = groupKey(header);

        function toggle() {
          var collapsed = section.classList.toggle("t3-sidebar-collapsed");
          section.classList.toggle("t3-sidebar-expanded", !collapsed);
          header.setAttribute("aria-expanded", collapsed ? "false" : "true");
          state[key] = !collapsed;
          if (!isHomepage()) saveExpandedState(state);
        }

        header.addEventListener("click", function (e) {
          if (e.target.closest("a")) return;
          toggle();
        });

        header.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggle();
          }
        });

        if (state[key] === false) setSectionExpanded(section, header, false);
        else setSectionExpanded(section, header, true);
      });
  }

  function enhanceExpandableButtons() {
    var content = getSidebarContent();
    if (!content) return;
    content
      .querySelectorAll(
        "button[aria-controls]:not([data-t3-expand-enhanced]), button[aria-expanded]:not([data-t3-expand-enhanced])"
      )
      .forEach(function (btn) {
        if (!btn.querySelector("svg")) return;
        btn.setAttribute("data-t3-expand-enhanced", "1");
        btn.classList.add("t3-sidebar-expand-btn");
        var svg = btn.querySelector("svg");
        if (!svg) return;
        svg.classList.add("t3-sidebar-chevron");
        var wrap = svg.parentElement;
        if (wrap && wrap !== btn) wrap.classList.add("t3-sidebar-chevron-wrap");
      });
  }

  function removeTopSectionChevrons() {
    var content = getSidebarContent();
    if (!content || content.getAttribute("data-t3-chevrons-removed")) return;
    content.setAttribute("data-t3-chevrons-removed", "1");
    content.querySelectorAll(".sidebar-group-header").forEach(function (header) {
      header.classList.add("t3-sidebar-top-section");
      var chevron = header.querySelector(".t3-sidebar-chevron");
      if (chevron) chevron.remove();
    });
  }

  function setupSidebar() {
    if (setupDone) return;
    setupDone = true;
    enhanceCollapsibleGroups();
    removeTopSectionChevrons();
    enhanceExpandableButtons();
    document.documentElement.classList.add("t3-sidebar-ready");
  }

  function shouldPrefetch() {
    try {
      var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (conn && (conn.saveData || conn.effectiveType === "slow-2g" || conn.effectiveType === "2g")) {
        return false;
      }
    } catch (e) {
      /* ignore */
    }
    return true;
  }

  function prefetchLink(anchor) {
    if (!anchor || !shouldPrefetch()) return;
    var href = anchor.getAttribute("href") || "";
    if (!href || href.charAt(0) !== "/" || href.indexOf("#") === 0 || prefetched[href]) return;
    prefetched[href] = 1;

    var link = document.createElement("link");
    link.rel = "prefetch";
    link.href = href;
    link.as = "document";
    document.head.appendChild(link);

    try {
      if (window.next && window.next.router && window.next.router.prefetch) {
        window.next.router.prefetch(href);
      }
    } catch (e2) {
      /* ignore */
    }
  }

  function setupPrefetch() {
    var hoverTimer = null;
    document.addEventListener(
      "mouseover",
      function (e) {
        var anchor = e.target.closest('#sidebar-content a[href^="/"]');
        if (!anchor) return;
        if (hoverTimer) clearTimeout(hoverTimer);
        hoverTimer = setTimeout(function () {
          prefetchLink(anchor);
        }, 40);
      },
      { passive: true }
    );
  }

  function setupMobileSidebar() {
    var sidebar =
      document.getElementById("sidebar") ||
      document.querySelector('[data-component-part="sidebar"]');
    if (!sidebar || document.getElementById("t3-sidebar-backdrop")) return;

    var backdrop = document.createElement("div");
    backdrop.id = "t3-sidebar-backdrop";
    backdrop.className = "t3-sidebar-backdrop";
    backdrop.setAttribute("aria-hidden", "true");
    document.body.appendChild(backdrop);

    function closeMobile() {
      document.body.classList.remove("t3-sidebar-open");
      backdrop.classList.remove("t3-sidebar-backdrop-visible");
    }

    backdrop.addEventListener("click", closeMobile);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMobile();
    });
    document.addEventListener(
      "click",
      function (e) {
        if (e.target.closest('#sidebar-content a[href^="/"]') && window.innerWidth < 1024) {
          closeMobile();
        }
      },
      true
    );
  }

  function deferSidebarSetup() {
    var run = setupSidebar;
    if (typeof requestIdleCallback === "function") {
      requestIdleCallback(run, { timeout: 200 });
    } else {
      setTimeout(run, 0);
    }
  }

  function init() {
    if (!localStorage.getItem("t3-sidebar-v2")) {
      try {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.setItem("t3-sidebar-v2", "1");
      } catch (e) {
        /* ignore */
      }
    }

    document.documentElement.classList.add("t3-sidebar-ready");
    syncNavbarOffset();
    setupMobileSidebar();
    setupPrefetch();
    deferSidebarSetup();

    var navbar = document.getElementById("navbar");
    if (navbar && typeof ResizeObserver !== "undefined") {
      new ResizeObserver(syncNavbarOffset).observe(navbar);
    }
    window.addEventListener("resize", syncNavbarOffset, { passive: true });

    document.addEventListener(
      "mousedown",
      function (e) {
        var anchor = e.target.closest('#sidebar-content a[href^="/"], #pagination a[href^="/"]');
        if (anchor) prefetchLink(anchor);
      },
      { passive: true }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
