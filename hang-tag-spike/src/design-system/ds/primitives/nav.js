/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Side-nav behavior  ·  .knav
   ────────────────────────────────────────────────────────────────
   ▸ Wires up the collapse-to-rail toggle (.knav-toggle) and
     persists the chosen state in localStorage so it survives
     reloads and page navigations across the app.
   ▸ The state is per-document; mark the sidebar that should react
     to the toggle with `data-knav-collapsible` (or just include a
     `.knav-toggle` button — the script auto-discovers it).
   ▸ Adds .knav-rail on activation, removes it on full mode.
   ════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var STORAGE_KEY = 'supercat:knav:rail';

  function readState() {
    try { return localStorage.getItem(STORAGE_KEY) === '1'; }
    catch (e) { return false; }
  }
  function writeState(on) {
    try { localStorage.setItem(STORAGE_KEY, on ? '1' : '0'); }
    catch (e) { /* private mode — silent */ }
  }

  function apply(nav, rail) {
    if (rail) nav.classList.add('knav-rail');
    else nav.classList.remove('knav-rail');
    var btn = nav.querySelector('.knav-toggle');
    if (btn) {
      btn.setAttribute('aria-pressed', rail ? 'true' : 'false');
      btn.setAttribute('aria-label', rail ? 'Expand sidebar' : 'Collapse sidebar');
      btn.setAttribute('title',      rail ? 'Expand sidebar' : 'Collapse sidebar');
    }
  }

  function init() {
    var navs = document.querySelectorAll('.knav');
    if (!navs.length) return;
    var rail = readState();

    navs.forEach(function (nav) {
      // Skip drawer variants — rail only applies to the desktop sidebar.
      if (nav.classList.contains('knav-drawer')) return;
      apply(nav, rail);

      var btn = nav.querySelector('.knav-toggle');
      if (!btn || btn.dataset.knavBound === '1') return;
      btn.dataset.knavBound = '1';
      btn.addEventListener('click', function () {
        rail = !nav.classList.contains('knav-rail');
        writeState(rail);
        document.querySelectorAll('.knav').forEach(function (n) {
          if (!n.classList.contains('knav-drawer')) apply(n, rail);
        });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
