/* ─────────────────────────────────────────────────────────────────
   .kf-input controllers — stepper, password eye, async validation
   ─────────────────────────────────────────────────────────────────
   One small script, three optional behaviors. Each binds to opt-in
   markup; if the markup isn't there, the script does nothing.

     <script src="/ds/primitives/input.js" defer></script>

   ── 1. Number stepper ──────────────────────────────────────────
   Wrap a number input in `.kf-input-wrap` and add stepper buttons:

     <div class="kf-input-wrap kf-md">
       <input type="number" class="kf-input kf-md" min="1" max="99" value="3" />
       <span class="kf-input-stepper">
         <button type="button" data-kf-step="-1" aria-label="Decrease">−</button>
         <button type="button" data-kf-step="+1" aria-label="Increase">+</button>
       </span>
     </div>

   The buttons clamp to min/max and dispatch input/change so any
   framework binding picks up the new value. Holding mouse down
   auto-repeats (accelerates after 600ms).

   ── 2. Password eye toggle ─────────────────────────────────────
   Wrap a password input and add a `.kf-input-eye` button:

     <div class="kf-input-wrap kf-md">
       <input type="password" class="kf-input kf-md" value="hunter2" />
       <button type="button" class="kf-input-eye" aria-label="Show password"></button>
     </div>

   The button toggles type between password/text and swaps the eye
   icon. The icons are inline SVG injected by the script — you don't
   need to put SVG in the HTML.

   ── 3. Async validation spinner ─────────────────────────────────
   Set data-kf-async on an input + provide an async validator function
   on `window.kfAsync[name]` (where name is data-kf-async value):

     <input type="email" class="kf-input kf-md" name="email"
            data-kf-async="email-available" />

     <script>
       window.kfAsync = window.kfAsync || {};
       window.kfAsync['email-available'] = async (value) => {
         if (!value) return null;
         const r = await fetch('/api/check?email=' + encodeURIComponent(value));
         const { ok, message } = await r.json();
         return ok ? null : { state: 'error', message };
       };
     </script>

   While checking, the field gets a spinner (right-side) and
   data-kf-checking on the wrapper. On result, the validator returns
   either null (valid, no message) or
     { state: 'error'|'warn'|'success', message?: string }
   The script applies data-state on the input + writes the message
   into the field's `.kf-field-message` if one exists.

   Debounced 400ms after typing stops.
   ─────────────────────────────────────────────────────────────── */

(() => {
  if (window.__kfInputInit) return;
  window.__kfInputInit = true;

  /* ─── Icons (data URIs for masks; inline SVG for eye buttons) ── */
  const EYE_OPEN = `<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8s-2.5 4.5-6.5 4.5S1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/></svg>`;
  const EYE_OFF  = `<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8s2.5-4.5 6-4.5c1.3 0 2.5.5 3.5 1.2M14 8s-2.5 4.5-6 4.5c-1.3 0-2.5-.5-3.5-1.2"/><path d="M2 2l12 12"/><path d="M9.4 9.4a2 2 0 0 1-2.8-2.8"/></svg>`;

  /* ─── 1. Number stepper ────────────────────────────────────── */
  function bindStepper(btn) {
    if (btn.__kfBound) return; btn.__kfBound = true;
    const wrap = btn.closest('.kf-input-wrap');
    const input = wrap?.querySelector('input[type="number"], input[type="text"]');
    if (!input) return;
    const step = parseFloat(btn.dataset.kfStep) || 1;

    const min = input.min !== '' ? parseFloat(input.min) : -Infinity;
    const max = input.max !== '' ? parseFloat(input.max) :  Infinity;
    const stepSize = parseFloat(input.step) || 1;

    function tick() {
      if (input.disabled || input.readOnly) return;
      const cur = parseFloat(input.value) || 0;
      const next = Math.min(max, Math.max(min, cur + step * stepSize));
      if (next === cur) return;
      input.value = String(next);
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    let timer = null, accel = null;
    function start() {
      tick();
      // Hold-to-repeat after a short pause, accelerating after 1s
      timer = setTimeout(() => {
        timer = setInterval(tick, 100);
        accel = setTimeout(() => {
          clearInterval(timer);
          timer = setInterval(tick, 50);
        }, 1000);
      }, 400);
    }
    function stop() {
      clearTimeout(timer); clearInterval(timer); clearTimeout(accel);
      timer = accel = null;
    }
    btn.addEventListener('mousedown', start);
    btn.addEventListener('touchstart', start, { passive: true });
    ['mouseup','mouseleave','touchend','touchcancel','blur'].forEach(ev => {
      btn.addEventListener(ev, stop);
    });
    // Keyboard activation = single tick
    btn.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tick(); }
    });
  }

  /* ─── 2. Password eye toggle ───────────────────────────────── */
  function bindEye(btn) {
    if (btn.__kfBound) return; btn.__kfBound = true;
    const wrap = btn.closest('.kf-input-wrap');
    const input = wrap?.querySelector('input');
    if (!input) return;
    btn.innerHTML = EYE_OPEN;
    btn.addEventListener('click', () => {
      if (input.type === 'password') {
        input.type = 'text';
        btn.innerHTML = EYE_OFF;
        btn.setAttribute('aria-label', 'Hide password');
      } else {
        input.type = 'password';
        btn.innerHTML = EYE_OPEN;
        btn.setAttribute('aria-label', 'Show password');
      }
    });
  }

  /* ─── 3. Async validation ──────────────────────────────────── */
  function bindAsync(input) {
    if (input.__kfBound) return; input.__kfBound = true;
    const name = input.dataset.kfAsync;
    if (!name) return;
    const wrap  = input.closest('.kf-input-wrap') || input;
    const field = input.closest('.kf-field');

    let timer = null, gen = 0;

    async function run() {
      const my = ++gen;
      const value = input.value;
      const validator = (window.kfAsync || {})[name];
      if (!validator) return;
      // Show spinner
      wrap.setAttribute('data-kf-checking', '');
      input.removeAttribute('data-state');
      try {
        const result = await validator(value, input);
        if (my !== gen) return;            // newer call superseded us
        wrap.removeAttribute('data-kf-checking');
        if (!result) {
          input.removeAttribute('data-state');
          if (field) field.removeAttribute('data-state');
          updateMessage(field, '');
        } else {
          input.setAttribute('data-state', result.state);
          if (field) field.setAttribute('data-state', result.state);
          updateMessage(field, result.message || '');
          if (result.state === 'error') triggerShake(input);
        }
      } catch (err) {
        if (my !== gen) return;
        wrap.removeAttribute('data-kf-checking');
        console.error('[kf async]', err);
      }
    }

    input.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(run, 400);
    });
    input.addEventListener('blur', () => {
      clearTimeout(timer);
      run();
    });
  }

  function updateMessage(field, text) {
    if (!field) return;
    const msg = field.querySelector('.kf-field-message');
    if (msg) msg.textContent = text;
  }

  function triggerShake(el) {
    const target = el.closest('.kf-field') || el;
    target.classList.remove('kf-shake');
    // force reflow so we can re-add the class and replay
    void target.offsetWidth;
    target.classList.add('kf-shake');
    target.addEventListener('animationend', function once() {
      target.classList.remove('kf-shake');
      target.removeEventListener('animationend', once);
    });
  }

  /* ─── Public helper ────────────────────────────────────────── */
  /* window.kfShake(elementOrSelector) — manually trigger shake on
     a field. Useful from form-submit handlers where you want every
     errored field to shake at once. */
  window.kfShake = function(target) {
    const el = typeof target === 'string' ? document.querySelector(target) : target;
    if (el) triggerShake(el);
  };

  /* ─── Bootstrap + observe ──────────────────────────────────── */
  function scan(root = document) {
    root.querySelectorAll('[data-kf-step]').forEach(bindStepper);
    root.querySelectorAll('.kf-input-eye').forEach(bindEye);
    root.querySelectorAll('input[data-kf-async]').forEach(bindAsync);
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
        if (n.matches?.('[data-kf-step]')) bindStepper(n);
        if (n.matches?.('.kf-input-eye'))   bindEye(n);
        if (n.matches?.('input[data-kf-async]')) bindAsync(n);
        n.querySelectorAll?.('[data-kf-step]').forEach(bindStepper);
        n.querySelectorAll?.('.kf-input-eye').forEach(bindEye);
        n.querySelectorAll?.('input[data-kf-async]').forEach(bindAsync);
      });
    }
  });
  mo.observe(document.body || document.documentElement, { childList: true, subtree: true });
})();
