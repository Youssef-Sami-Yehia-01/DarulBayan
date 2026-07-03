/**
 * Popup modal controller (components/modal.html).
 *
 * Any element with data-modal-url opens the modal and loads that URL's
 * HTML fragment into it. Forms inside the modal POST via fetch:
 *   204 -> success: close and reload the page
 *   4xx -> validation errors: fragment is re-rendered inside the modal
 */
(function () {
    "use strict";

    const modal = document.getElementById("modal");
    if (!modal) return;
    const body = document.getElementById("modal-body");
    const FETCH_HEADERS = { "X-Requested-With": "XMLHttpRequest" };

    function open(url) {
        fetch(url, { headers: FETCH_HEADERS })
            .then(function (response) { return response.text(); })
            .then(function (html) {
                body.innerHTML = html;
                modal.hidden = false;
                document.body.classList.add("no-scroll");
            });
    }

    function close() {
        modal.hidden = true;
        body.innerHTML = "";
        document.body.classList.remove("no-scroll");
    }

    document.addEventListener("click", function (event) {
        const opener = event.target.closest("[data-modal-url]");
        if (opener) {
            open(opener.dataset.modalUrl);
            return;
        }
        if (event.target.closest("[data-modal-close]")) close();
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !modal.hidden) close();
    });

    modal.addEventListener("submit", function (event) {
        const form = event.target.closest("form");
        if (!form) return;
        event.preventDefault();
        fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: FETCH_HEADERS,
        }).then(function (response) {
            if (response.status === 204) {
                window.location.reload();
                return null;
            }
            return response.text();
        }).then(function (html) {
            if (html) body.innerHTML = html;
        });
    });
})();
