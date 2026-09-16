/* ─────────────────────────────────────────────────────────────────
   .kf-date — Custom date picker controller
   ─────────────────────────────────────────────────────────────────
   Wires up popover open/close, month nav, and date selection on any
   .kf-date container. The underlying <input type="date"> stays the
   source of truth — we just write to it and dispatch 'input' + 'change'
   so any framework's bindings update automatically.

   Usage:
     <script src="/ds/primitives/date.js" defer></script>

   Required DOM (the controller queries inside each .kf-date):
     - input[type="date"]    the real input (value source of truth)
     - .kf-date-trigger      button to open popover
     - .kf-date-pop          empty container — controller fills it

   No setup call needed; the script auto-attaches to every .kf-date
   on the page and watches for new ones via MutationObserver.

   The script is idempotent — safe to load twice, and re-runs are no-ops.
   ─────────────────────────────────────────────────────────────── */

(() => {
  if (window.__kfDateInit) return;
  window.__kfDateInit = true;

  const MONTHS = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
  ];
  const DOW = ['M','T','W','T','F','S','S']; // Mon-first

  /* ─── Helpers ──────────────────────────────────────────────── */
  function toISO(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }
  function fromISO(s) {
    if (!s) return null;
    const [y, m, d] = s.split('-').map(Number);
    if (!y || !m || !d) return null;
    return new Date(y, m - 1, d);
  }
  function sameDay(a, b) {
    return a && b &&
      a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate();
  }
  function startOfMonth(d) { return new Date(d.getFullYear(), d.getMonth(), 1); }
  function addMonths(d, n) { return new Date(d.getFullYear(), d.getMonth() + n, 1); }

  /* ─── Render ───────────────────────────────────────────────── */
  function renderDays(state) {
    const { view: cursor, selected, min, max } = state;
    const today = new Date();

    const first = startOfMonth(cursor);
    // Mon-first offset: 0 if Mon, … 6 if Sun
    const offset = (first.getDay() + 6) % 7;
    const startDate = new Date(first); startDate.setDate(1 - offset);

    const cells = [];
    // Header — weekday labels
    for (let i = 0; i < 7; i++) {
      cells.push(`<span class="kf-date-dow">${DOW[i]}</span>`);
    }
    // 6 weeks × 7 days = 42 cells
    for (let i = 0; i < 42; i++) {
      const d = new Date(startDate);
      d.setDate(startDate.getDate() + i);

      const inMonth = d.getMonth() === cursor.getMonth();
      const isToday = sameDay(d, today);
      const isSel   = sameDay(d, selected);
      const isDisabled = (min && d < min) || (max && d > max);

      const attrs = [
        `type="button"`,
        `class="kf-date-day"`,
        `data-iso="${toISO(d)}"`,
        !inMonth   ? 'data-out' : '',
        isToday    ? 'data-today' : '',
        isSel      ? 'data-selected' : '',
        isDisabled ? 'disabled' : ''
      ].filter(Boolean).join(' ');

      cells.push(`<button ${attrs}>${d.getDate()}</button>`);
    }
    return `<div class="kf-date-grid">${cells.join('')}</div>`;
  }

  function renderMonths(state) {
    const sel = state.selected ? state.selected.getMonth() : -1;
    const inViewYear = state.view.getFullYear();
    const cells = MONTHS.map((m, i) => {
      const isSel = sel === i && state.selected && state.selected.getFullYear() === inViewYear;
      return `<button type="button" class="kf-date-mo" data-mo="${i}" ${isSel ? 'data-selected' : ''}>${m.slice(0,3)}</button>`;
    }).join('');
    return `<div class="kf-date-grid-months">${cells}</div>`;
  }

  function renderYears(state) {
    const yr = state.view.getFullYear();
    const start = yr - (yr % 12);
    const sel = state.selected ? state.selected.getFullYear() : -1;
    const cells = [];
    for (let i = -1; i <= 12; i++) {
      const y = start + i;
      const out = i < 0 || i >= 12;
      cells.push(`<button type="button" class="kf-date-yr" data-yr="${y}" ${out ? 'data-out' : ''} ${sel === y ? 'data-selected' : ''}>${y}</button>`);
    }
    return `<div class="kf-date-grid-years">${cells}</div>`;
  }

  function renderHead(state) {
    let title = '';
    if (state.viewMode === 'days') {
      title = `${MONTHS[state.view.getMonth()]} ${state.view.getFullYear()}`;
    } else if (state.viewMode === 'months') {
      title = `${state.view.getFullYear()}`;
    } else {
      const yr = state.view.getFullYear();
      const start = yr - (yr % 12);
      title = `${start} – ${start + 11}`;
    }
    return `
      <div class="kf-date-head">
        <button type="button" class="kf-date-title" data-act="cycle">
          ${title}
          <svg class="kf-date-title-chev" viewBox="0 0 9 9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <path d="m2 3.5 2.5 2.5L7 3.5"/>
          </svg>
        </button>
        <span class="kf-date-nav">
          <button type="button" class="kf-date-nav-btn" data-act="prev" aria-label="Previous">
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7.5 2.5 4 6l3.5 3.5"/></svg>
          </button>
          <button type="button" class="kf-date-nav-btn" data-act="next" aria-label="Next">
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 2.5 8 6l-3.5 3.5"/></svg>
          </button>
        </span>
      </div>
    `;
  }

  function renderFoot() {
    return `
      <div class="kf-date-foot">
        <button type="button" class="kf-date-shortcut" data-act="today">Today</button>
        <button type="button" class="kf-date-shortcut" data-act="clear">Clear</button>
      </div>
    `;
  }

  function render(pop, state) {
    pop.dataset.view = state.viewMode;
    let body = '';
    if (state.viewMode === 'days')        body = renderDays(state);
    else if (state.viewMode === 'months') body = renderMonths(state);
    else                                  body = renderYears(state);
    pop.innerHTML = renderHead(state) + body + renderFoot();
  }

  /* ─── Wire up one .kf-date ─────────────────────────────────── */
  function init(root) {
    if (root.__kfd) return;
    const input   = root.querySelector('input[type="date"]');
    const trigger = root.querySelector('.kf-date-trigger');
    const pop     = root.querySelector('.kf-date-pop');
    if (!input || !trigger || !pop) return;

    const state = {
      open: false,
      viewMode: 'days',                // 'days' | 'months' | 'years'
      selected: fromISO(input.value),
      view: fromISO(input.value) || new Date(),
      min: input.min ? fromISO(input.min) : null,
      max: input.max ? fromISO(input.max) : null
    };

    function open() {
      // Re-sync selected from input in case the user typed something
      state.selected = fromISO(input.value);
      state.view = state.selected || new Date();
      state.viewMode = 'days';
      pop.hidden = false;
      state.open = true;
      render(pop, state);
      // Close on outside click
      setTimeout(() => document.addEventListener('mousedown', onOutside), 0);
      // Close on escape
      document.addEventListener('keydown', onEsc);
    }
    function close() {
      pop.hidden = true;
      state.open = false;
      document.removeEventListener('mousedown', onOutside);
      document.removeEventListener('keydown', onEsc);
    }
    function onOutside(e) {
      if (!root.contains(e.target)) close();
    }
    function onEsc(e) {
      if (e.key === 'Escape') close();
    }

    trigger.addEventListener('click', () => {
      state.open ? close() : open();
    });

    pop.addEventListener('click', e => {
      const btn = e.target.closest('button');
      if (!btn) return;

      if (btn.dataset.iso) {
        // Day pick
        state.selected = fromISO(btn.dataset.iso);
        input.value = btn.dataset.iso;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        close();
        return;
      }
      if (btn.dataset.act === 'prev') {
        if (state.viewMode === 'days')   state.view = addMonths(state.view, -1);
        else if (state.viewMode === 'months') state.view = new Date(state.view.getFullYear() - 1, state.view.getMonth(), 1);
        else                              state.view = new Date(state.view.getFullYear() - 12, state.view.getMonth(), 1);
        render(pop, state);
        return;
      }
      if (btn.dataset.act === 'next') {
        if (state.viewMode === 'days')   state.view = addMonths(state.view, 1);
        else if (state.viewMode === 'months') state.view = new Date(state.view.getFullYear() + 1, state.view.getMonth(), 1);
        else                              state.view = new Date(state.view.getFullYear() + 12, state.view.getMonth(), 1);
        render(pop, state);
        return;
      }
      if (btn.dataset.act === 'cycle') {
        // days → months → years → days
        state.viewMode = state.viewMode === 'days'   ? 'months'
                       : state.viewMode === 'months' ? 'years'
                       : 'days';
        render(pop, state);
        return;
      }
      if (btn.dataset.act === 'today') {
        const t = new Date();
        state.selected = t;
        state.view = t;
        state.viewMode = 'days';
        input.value = toISO(t);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        close();
        return;
      }
      if (btn.dataset.act === 'clear') {
        state.selected = null;
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        close();
        return;
      }
      if (btn.dataset.mo !== undefined) {
        state.view = new Date(state.view.getFullYear(), Number(btn.dataset.mo), 1);
        state.viewMode = 'days';
        render(pop, state);
        return;
      }
      if (btn.dataset.yr !== undefined) {
        state.view = new Date(Number(btn.dataset.yr), state.view.getMonth(), 1);
        state.viewMode = 'months';
        render(pop, state);
        return;
      }
    });

    // External value changes (framework writes) → keep popover in sync
    input.addEventListener('input', () => {
      state.selected = fromISO(input.value);
      if (state.open) render(pop, state);
    });

    root.__kfd = { open, close, refresh: () => render(pop, state) };
  }

  /* ─── Bootstrap + observe ──────────────────────────────────── */
  function scan(root = document) {
    root.querySelectorAll('.kf-date').forEach(init);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => scan());
  } else {
    scan();
  }

  const mo = new MutationObserver(muts => {
    for (const m of muts) {
      m.addedNodes.forEach(n => {
        if (n.nodeType !== 1) return;
        if (n.matches?.('.kf-date')) init(n);
        n.querySelectorAll?.('.kf-date').forEach(init);
      });
    }
  });
  mo.observe(document.body || document.documentElement, { childList: true, subtree: true });
})();
