/**
 * Admin panel behavior: collapsible sidebar on small screens.
 */
(function () {
    "use strict";

    const toggle = document.querySelector("[data-sidebar-toggle]");
    const sidebar = document.getElementById("panel-sidebar");
    if (!toggle || !sidebar) return;

    toggle.addEventListener("click", function () {
        const open = sidebar.classList.toggle("panel-sidebar--open");
        toggle.setAttribute("aria-expanded", String(open));
    });

    // Close the sidebar when clicking outside it (mobile only)
    document.addEventListener("click", function (event) {
        if (!sidebar.classList.contains("panel-sidebar--open")) return;
        if (event.target.closest("#panel-sidebar") || event.target.closest("[data-sidebar-toggle]")) return;
        sidebar.classList.remove("panel-sidebar--open");
        toggle.setAttribute("aria-expanded", "false");
    });
})();
