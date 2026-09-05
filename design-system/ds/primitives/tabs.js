/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Tabs primitive  ·  .ktab  ·  interactive controller
   ────────────────────────────────────────────────────────────────
   What it does:
     1. Auto-wires every .ktab on the page (DOMContentLoaded).
     2. Click on a .ktab-item → swaps aria-selected; if the item
        has aria-controls, toggles the referenced [role="tabpanel"].
     3. For underline + vertical variants, measures the active
        item's bounding rect and writes CSS variables
          --ktab-active-x / --ktab-active-w   (underline)
          --ktab-active-y / --ktab-active-h   (vertical)
        which the CSS picks up to render the sliding crimson bar.
     4. ResizeObserver re-snaps the indicator on layout changes
        (font load, container resize, density toggle, etc).
     5. Idempotent — calling window.__supercatTabsInit() again is
        safe; already-initialized wrappers are skipped.

   No dependencies. Pure vanilla. Works inside any framework that
   renders .ktab markup (React, Vue, Svelte, plain HTML).

   Re-init for SPA routers:
     window.__supercatTabsInit()        — re-scan + wire new tabs

   Disable a single tab:
     <button class="ktab-item" disabled>            — native
     <button class="ktab-item" aria-disabled="true">— ARIA-only
   The controller ignores clicks on disabled items.
   ══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  function getItems(ktab) {
    return Array.prototype.slice.call(
      ktab.querySelectorAll('.ktab-item[role="tab"], .ktab-item')
    ).filter(function (n) { return n.parentElement === ktab; });
  }

  function isDisabled(item) {
    return item.disabled || item.getAttribute('aria-disabled') === 'true';
  }

  function variantOf(ktab) {
    if (ktab.classList.contains('ktab-pills')) return 'pills';
    if (ktab.classList.contains('ktab-seg')) return 'seg';
    if (ktab.classList.contains('ktab-vertical')) return 'vertical';
    return 'underline';
  }

  function ensureBar(ktab) {
    var bar = ktab.querySelector(':scope > .ktab-bar');
    if (!bar) {
      bar = document.createElement('span');
      bar.className = 'ktab-bar';
      bar.setAttribute('aria-hidden', 'true');
      ktab.appendChild(bar);
    }
    return bar;
  }

  // Animation timing — matches the CSS --duration-medium / --ease-emph
  // tokens. Kept in sync here so the JS-driven Web Animations API uses
  // the same motion vocabulary as the rest of the system.
  var ANIM_MS = 320;
  var ANIM_EASE = 'cubic-bezier(0.2, 0.8, 0.2, 1)';

  function targetStyleFor(v, active) {
    if (v === 'vertical') {
      return { top: active.offsetTop + 'px', height: active.offsetHeight + 'px' };
    }
    if (v === 'seg') {
      // Use transform for the X-axis — compositor-friendly and immune
      // to the layout-shift contention that breaks `left` transitions
      // when aria-selected toggles font-weight on the items.
      return { transform: 'translateX(' + active.offsetLeft + 'px)', width: active.offsetWidth + 'px' };
    }
    return { left: active.offsetLeft + 'px', width: active.offsetWidth + 'px' };
  }

  function readCurrentStyle(v, bar) {
    var cs = window.getComputedStyle(bar);
    if (v === 'vertical') {
      return { top: cs.top, height: cs.height };
    }
    if (v === 'seg') {
      // Read computed transform — Chrome returns matrix(...) form;
      // it's fine for WAAPI as a starting frame.
      return { transform: cs.transform === 'none' ? 'translateX(0px)' : cs.transform, width: cs.width };
    }
    return { left: cs.left, width: cs.width };
  }

  function applyStyles(bar, styles) {
    for (var k in styles) {
      if (Object.prototype.hasOwnProperty.call(styles, k)) {
        bar.style[k] = styles[k];
      }
    }
  }

  function positionIndicator(ktab, immediate) {
    var v = variantOf(ktab);
    // Pills use per-item background fills (no shared sliding element).
    // Underline + segmented + vertical use a shared .ktab-bar element.
    if (v === 'pills') return;

    var items = getItems(ktab);
    if (!items.length) return;
    var active = null;
    for (var i = 0; i < items.length; i++) {
      if (items[i].getAttribute('aria-selected') === 'true') { active = items[i]; break; }
    }
    if (!active) active = items[0];

    var bar = ensureBar(ktab);
    var target = targetStyleFor(v, active);

    if (immediate) {
      // Snap with no animation — initial layout, resize, font load.
      if (bar.__ktabAnim) { bar.__ktabAnim.cancel(); bar.__ktabAnim = null; }
      applyStyles(bar, target);
      return;
    }

    // Cancel any in-flight animation so we restart cleanly.
    if (bar.__ktabAnim) { bar.__ktabAnim.cancel(); bar.__ktabAnim = null; }

    var from = readCurrentStyle(v, bar);

    // Commit the final state immediately to inline style so the bar
    // settles there once the animation finishes (and so a subsequent
    // resize re-measurement is correct).
    applyStyles(bar, target);

    // Animate via Web Animations API — bulletproof, runs on the
    // compositor where applicable, doesn't depend on CSS transition
    // semantics that silently fail under simultaneous layout shifts.
    try {
      var anim = bar.animate([from, target], {
        duration: ANIM_MS,
        easing: ANIM_EASE,
        fill: 'none',
      });
      bar.__ktabAnim = anim;
      anim.onfinish = anim.oncancel = function () {
        if (bar.__ktabAnim === anim) bar.__ktabAnim = null;
      };
    } catch (e) {
      // WAAPI not available (very old browser) — bar already snapped via
      // applyStyles above, so the change is at least visually correct.
    }
  }

  function togglePanels(ktab, activeItem) {
    var items = getItems(ktab);
    items.forEach(function (item) {
      var panelId = item.getAttribute('aria-controls');
      if (!panelId) return;
      var panel = document.getElementById(panelId);
      if (!panel) return;
      if (item === activeItem) panel.removeAttribute('hidden');
      else panel.setAttribute('hidden', '');
    });
  }

  function setActive(ktab, item, opts) {
    if (!item || isDisabled(item)) return;
    var items = getItems(ktab);
    items.forEach(function (i) {
      i.setAttribute('aria-selected', i === item ? 'true' : 'false');
    });
    togglePanels(ktab, item);
    positionIndicator(ktab, !!(opts && opts.immediate));
  }

  function initKtab(ktab) {
    if (ktab.__ktabInit) return;
    ktab.__ktabInit = true;

    var items = getItems(ktab);
    if (!items.length) return;

    items.forEach(function (item) {
      item.addEventListener('click', function (e) {
        if (isDisabled(item)) { e.preventDefault(); return; }
        setActive(ktab, item, { immediate: false });
      });
    });

    // Initial position — snap, no animation
    positionIndicator(ktab, true);

    // Re-snap on size changes (font load, container resize, density toggle).
    // BUT skip while a click-triggered animation is in flight — otherwise
    // the layout-shift caused by aria-selected toggling font-weight on
    // items fires ResizeObserver, which cancels the active animation.
    if (typeof ResizeObserver !== 'undefined') {
      var ro = new ResizeObserver(function () {
        var bar = ktab.querySelector(':scope > .ktab-bar');
        if (bar && bar.__ktabAnim) return;  // don't disturb the running slide
        positionIndicator(ktab, true);
      });
      ro.observe(ktab);
    }

    // Re-snap after web fonts load (text width changes ≈ active item width).
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        var bar = ktab.querySelector(':scope > .ktab-bar');
        if (bar && bar.__ktabAnim) return;
        positionIndicator(ktab, true);
      }).catch(function () { /* noop */ });
    }
  }

  function initAll(root) {
    var scope = root || document;
    scope.querySelectorAll('.ktab').forEach(initKtab);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initAll(); });
  } else {
    initAll();
  }

  // Expose for SPA routers / dynamically-mounted markup
  if (typeof window !== 'undefined') {
    window.__supercatTabsInit = initAll;
  }
})();
