// Sub tabs for the audits page (Audits Feed / Audited Establishments)
(function () {
    var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;

    function activate(tab, moveFocus) {
        tabs.forEach(function (t) {
            var selected = t === tab;
            t.setAttribute('aria-selected', selected ? 'true' : 'false');
            t.tabIndex = selected ? 0 : -1;
            t.classList.toggle('is-active', selected);
            document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
        });
        if (moveFocus) tab.focus();
        try {
            history.replaceState(null, '', '#' + tab.dataset.tab);
        } catch (e) { /* ignore */ }
    }

    tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { activate(tab, false); });

        // Arrow keys / Home / End move between tabs
        tab.addEventListener('keydown', function (e) {
            var next = null;
            if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
            if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
            if (e.key === 'Home') next = tabs[0];
            if (e.key === 'End') next = tabs[tabs.length - 1];
            if (next) {
                e.preventDefault();
                activate(next, true);
            }
        });
    });

    // Open the tab named in the URL hash (e.g. /audits/#places)
    var wanted = window.location.hash.replace('#', '');
    var match = tabs.filter(function (t) { return t.dataset.tab === wanted; })[0];
    if (match) activate(match, false);
})();