/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Skeleton load controller  ·  skeleton.js
   ────────────────────────────────────────────────────────────────
   Wires up the [data-loadable] content-swap pattern (see
   skeleton.css). Two responsibilities:

     1. On page mount: simulate a fetch for every [data-loadable]
        that starts with aria-busy="true". When the fetch resolves
        (delay configurable per element via data-load="<ms>"), flip
        aria-busy to "false" so the [data-real] content reveals.

     2. Refresh buttons: any [data-reload] element click re-runs
        the simulated fetch — flips every [data-loadable] back to
        aria-busy="true", then resolves them on staggered delays so
        the page looks lively rather than synchronous.

   This is intentionally a DEMO controller — it stands in for the
   production reality where your fetch/loading state would drive
   aria-busy directly. In React this looks like:

     <div data-loadable aria-busy={isLoading}>
       <div data-skel>…</div>
       <div data-real>{data}</div>
     </div>

   In Vue / Angular / Svelte the binding is just the same attribute.
   No framework lock-in.
   ════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  function loadOne(el) {
    const baseDelay = parseInt(el.dataset.load, 10);
    const delay = !isNaN(baseDelay) ? baseDelay : 600 + Math.random() * 900;
    setTimeout(() => {
      el.setAttribute('aria-busy', 'false');
      el.dispatchEvent(new CustomEvent('kskel:loaded', { bubbles: true }));
    }, delay);
  }

  function reloadAll(root) {
    const scope = root || document;
    scope.querySelectorAll('[data-loadable]').forEach((el) => {
      el.setAttribute('aria-busy', 'true');
      loadOne(el);
    });
  }

  // Initial mount: kick off the load for any [data-loadable] that
  // starts busy. Anything already aria-busy="false" is left alone.
  function init() {
    document.querySelectorAll('[data-loadable][aria-busy="true"]').forEach(loadOne);

    document.querySelectorAll('[data-reload]').forEach((btn) => {
      btn.addEventListener('click', () => reloadAll(document));
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Public — consumers can call window.kskel.reload() to refresh the page.
  window.kskel = { reload: reloadAll };
})();
