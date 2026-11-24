(function () {
    var nav = document.querySelector('.site-navbar');
    if (!nav) return;

    function update() {
        nav.classList.toggle('is-scrolled', window.scrollY > 10);
    }

    update();
    window.addEventListener('scroll', update, { passive: true });
})();