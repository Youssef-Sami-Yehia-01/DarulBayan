/**
 * Mobile navigation toggle for the site header.
 * Opens/closes the nav panel and keeps aria-expanded in sync.
 */
(function () {
    "use strict";

    const toggle = document.querySelector(".site-header__toggle");
    const nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", function () {
        const open = nav.classList.toggle("site-nav--open");
        toggle.setAttribute("aria-expanded", String(open));
    });

    // Close the menu after navigating (single-page anchor links)
    nav.addEventListener("click", function (event) {
        if (event.target.closest("a")) {
            nav.classList.remove("site-nav--open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });
})();
