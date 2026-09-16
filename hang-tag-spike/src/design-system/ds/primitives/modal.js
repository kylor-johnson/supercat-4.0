/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Modal behavior  ·  .kmd
   ────────────────────────────────────────────────────────────────
   Two helpers:

   1) Close handlers — any element with `[data-kmd-close]` inside a
      <dialog class="kmd"> closes the parent dialog on click. Also
      closes if the user clicks the backdrop (outside the modal box).

   2) Three-dots menu — any button with `[data-kmd-menu-trigger]`
      opens the menu (next sibling .kmd-menu, or referenced via
      `aria-controls`) positioned below the trigger. ESC + click-
      outside close it.

   Framework-agnostic vanilla. Drop in via <script src="…" defer>.

   Mount-timing-robust: a document-level delegation handler catches
   backdrop clicks + [data-kmd-close] clicks for dialogs that appear
   AFTER init() runs (React routes that mount canonical HTML via
   dangerouslySetInnerHTML after DOMContentLoaded). Direct binding
   stays for static dialogs; delegation is the safety net.
   ════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── Document-level delegation — works regardless of mount timing.
     Bound exactly once on script load. Catches dialogs mounted later
     via dangerouslySetInnerHTML / React portals / dynamic insertion. */
  if (!document.documentElement.dataset.scKmdDelegated) {
    document.documentElement.dataset.scKmdDelegated = '1';
    document.addEventListener('click', function (e) {
      /* Backdrop click — target IS the dialog element itself.
         Native <dialog> dispatches click on the dialog when the user
         clicks the ::backdrop area. */
      var t = e.target;
      if (t && t.tagName === 'DIALOG' && t.classList && t.classList.contains('kmd') && t.hasAttribute('open')) {
        t.close();
        return;
      }
      /* [data-kmd-close] anywhere inside an open .kmd dialog. */
      var closeBtn = t && t.closest && t.closest('[data-kmd-close]');
      if (closeBtn) {
        var dlg = closeBtn.closest('dialog.kmd');
        if (dlg && typeof dlg.close === 'function') dlg.close();
      }
    });
    /* Escape key — native <dialog>.showModal() already handles Escape,
       but if a consumer uses .show() (non-modal), wire Escape here. */
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      var openDlg = document.querySelector('dialog.kmd[open]');
      if (openDlg && typeof openDlg.close === 'function') openDlg.close();
    });
  }

  /* ── Dialog close handlers (direct binding for static dialogs) ── */

  function bindDialogClose(root) {
    (root || document).querySelectorAll('[data-kmd-close]').forEach(function (btn) {
      if (btn.dataset.scBound === '1') return;
      btn.dataset.scBound = '1';
      btn.addEventListener('click', function () {
        var dlg = btn.closest('dialog.kmd');
        if (dlg && typeof dlg.close === 'function') dlg.close();
      });
    });

    /* Click outside the dialog box (on ::backdrop) → close. */
    document.querySelectorAll('dialog.kmd').forEach(function (dlg) {
      if (dlg.dataset.scBound === '1') return;
      dlg.dataset.scBound = '1';
      dlg.addEventListener('click', function (e) {
        if (e.target === dlg) dlg.close();
      });
    });
  }


  /* ── Menu popover ───────────────────────────────────────────── */

  function positionMenu(trigger, menu) {
    var r = trigger.getBoundingClientRect();
    var prefer = trigger.dataset.kmdMenuAlign || 'end'; // start | end
    menu.style.position = 'fixed';
    menu.style.top  = (r.bottom + 6) + 'px';
    if (prefer === 'start') {
      menu.style.left  = r.left + 'px';
      menu.style.right = 'auto';
    } else {
      menu.style.right = (window.innerWidth - r.right) + 'px';
      menu.style.left  = 'auto';
    }
    /* Flip up if it would overflow the viewport bottom. */
    var mr = menu.getBoundingClientRect();
    if (mr.bottom > window.innerHeight - 8) {
      menu.style.top = (r.top - mr.height - 6) + 'px';
    }
  }

  function closeMenu(menu, trigger) {
    menu.hidden = true;
    if (trigger) trigger.setAttribute('aria-expanded', 'false');
  }

  function bindMenu() {
    document.querySelectorAll('[data-kmd-menu-trigger]').forEach(function (trigger) {
      if (trigger.dataset.scBound === '1') return;
      trigger.dataset.scBound = '1';

      var menu = null;
      var menuId = trigger.getAttribute('aria-controls');
      if (menuId) menu = document.getElementById(menuId);
      if (!menu) {
        // fallback — next sibling
        menu = trigger.nextElementSibling;
        if (menu && !menu.classList.contains('kmd-menu')) menu = null;
      }
      if (!menu) return;

      menu.hidden = true;
      trigger.setAttribute('aria-haspopup', 'true');
      trigger.setAttribute('aria-expanded', 'false');

      trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = !menu.hidden;
        if (open) {
          closeMenu(menu, trigger);
        } else {
          menu.hidden = false;
          trigger.setAttribute('aria-expanded', 'true');
          positionMenu(trigger, menu);
        }
      });

      /* Click any menu item → close. */
      menu.querySelectorAll('.kmd-menu-item').forEach(function (item) {
        item.addEventListener('click', function () { closeMenu(menu, trigger); });
      });

      /* Click outside → close. */
      document.addEventListener('click', function (e) {
        if (menu.hidden) return;
        if (menu.contains(e.target) || trigger.contains(e.target)) return;
        closeMenu(menu, trigger);
      });

      /* ESC → close. */
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !menu.hidden) closeMenu(menu, trigger);
      });
    });
  }


  /* ── Mount ──────────────────────────────────────────────────── */

  function init() {
    bindDialogClose();
    bindMenu();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
