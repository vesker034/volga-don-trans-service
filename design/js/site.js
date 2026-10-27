(function () {
  'use strict';

  var html = document.documentElement;

  var savedTheme = localStorage.getItem('vdts_theme');
  if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
  }

  var themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('vdts_theme', next);
    });
  }

  var banner = document.getElementById('cookieBanner');
  var acceptBtn = document.getElementById('cookieAccept');
  if (banner && !localStorage.getItem('cookies_accepted')) {
    banner.hidden = false;
    document.body.classList.add('has-cookie-banner');
  }
  if (acceptBtn && banner) {
    acceptBtn.addEventListener('click', function () {
      localStorage.setItem('cookies_accepted', '1');
      banner.hidden = true;
      document.body.classList.remove('has-cookie-banner');
    });
  }

  document.querySelectorAll('.faq-accordion__trigger').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-accordion__item');
      var isOpen = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });
})();
