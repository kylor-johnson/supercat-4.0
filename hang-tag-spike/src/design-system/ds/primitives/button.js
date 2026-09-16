/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Button loader / success injector
   ────────────────────────────────────────────────────────────────
   Framework-agnostic. Works with React, Vue, Svelte, vanilla, or
   server-rendered HTML. Authors only toggle attributes:

     btn.setAttribute('data-loading', '')   // start orbit
     btn.removeAttribute('data-loading');
     btn.setAttribute('data-success', '')   // collapse → check
     btn.removeAttribute('data-success');   // back to idle

   The script:
     • observes .kb nodes (mutation + child list)
     • injects/sizes an SVG ring on data-loading
     • on data-loading→removed-with-data-success, animates
       the orbit closed into a full ring, then reveals the check
     • cleans up on detach / state reset

   Idempotent: safe to load multiple times (guarded by symbol).
   No globals leaked.
   ════════════════════════════════════════════════════════════════ */
(() => {
  if (window.__kbButtonInit) return;
  window.__kbButtonInit = true;

  const NS = "http://www.w3.org/2000/svg";
  const HALO_OUTSET_X = 8;
  const HALO_OUTSET_Y = 6;
  const BTN_RADIUS = 8;
  const HALO_RADIUS_X = BTN_RADIUS + HALO_OUTSET_X;
  const HALO_RADIUS_Y = BTN_RADIUS + HALO_OUTSET_Y;
  const STROKE = 1.5;
  const COMET_LEN = 22;
  const LAP_MS = 2400;

  const orbits = new WeakMap();

  function ensureLoader(btn) {
    let svg = btn.querySelector(":scope > .kb-loader");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "kb-loader");
      svg.setAttribute("aria-hidden", "true");
      const rect = document.createElementNS(NS, "rect");
      rect.setAttribute("pathLength", "100");
      rect.setAttribute("stroke-dasharray", `${COMET_LEN} ${100 - COMET_LEN}`);
      rect.setAttribute("stroke-dashoffset", "0");
      svg.appendChild(rect);
      btn.appendChild(svg);
    }
    return svg;
  }

  function ensureCheck(btn) {
    let svg = btn.querySelector(":scope > .kb-check");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "kb-check");
      svg.setAttribute("viewBox", "0 0 24 24");
      svg.setAttribute("aria-hidden", "true");
      const path = document.createElementNS(NS, "path");
      path.setAttribute("d", "M5 12 L10 17 L19 8");
      svg.appendChild(path);
      btn.appendChild(svg);
    }
    return svg;
  }

  function sizeLoader(btn) {
    const svg = ensureLoader(btn);
    const r = btn.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return null;
    const w = r.width + HALO_OUTSET_X * 2;
    const h = r.height + HALO_OUTSET_Y * 2;
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    svg.setAttribute("width", w);
    svg.setAttribute("height", h);
    const rect = svg.querySelector("rect");
    const inset = STROKE / 2;
    rect.setAttribute("x", inset);
    rect.setAttribute("y", inset);
    rect.setAttribute("width", Math.max(0, w - STROKE));
    rect.setAttribute("height", Math.max(0, h - STROKE));
    rect.setAttribute("rx", HALO_RADIUS_X);
    rect.setAttribute("ry", HALO_RADIUS_Y);
    return rect;
  }

  function bezY(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
  function bezDerivative(t) {
    return t < 0.5 ? 12 * t * t : 3 * Math.pow(-2 * t + 2, 2);
  }

  function startOrbit(btn) {
    if (orbits.get(btn)?.alive) return;
    const rect = sizeLoader(btn);
    if (!rect) return;
    rect.style.opacity = "1";
    rect.setAttribute("stroke-dasharray", `0 100`);
    rect.setAttribute("stroke-dashoffset", "0");
    btn.setAttribute("aria-busy", "true");
    btn.classList.add("kb-orbit");
    const state = {
      rect,
      raf: null,
      alive: true,
      offset: 0,
      currentDash: 0,
      lapStart: performance.now(),
      lapDuration: LAP_MS,
      lapBase: 0,
      lap: 0,
      introT0: performance.now(),
      introMs: 540,
    };
    orbits.set(btn, state);

    const tick = (now) => {
      if (!state.alive) return;
      let lapT = (now - state.lapStart) / state.lapDuration;
      if (lapT >= 1) {
        state.lapBase -= 100;
        state.lap += 1;
        state.lapStart += state.lapDuration;
        state.lapDuration = LAP_MS * (0.85 + Math.random() * 0.30);
        lapT = (now - state.lapStart) / state.lapDuration;
        if (lapT > 1) lapT = 1;
        if (lapT < 0) lapT = 0;
      }
      const eased = bezY(lapT);
      state.offset = state.lapBase - 100 * eased;

      const introT = Math.min(1, (now - state.introT0) / state.introMs);
      const introEase = 1 - Math.pow(1 - introT, 3);
      let targetDash;
      if (introT < 1) {
        targetDash = COMET_LEN * introEase;
      } else {
        const vel = bezDerivative(lapT);
        const velNorm = Math.min(1, vel / 3);
        const phaseSeed = (state.lap * 0.61803) % 1;
        const wobble = Math.sin((lapT + phaseSeed) * Math.PI * 2) * 4 * velNorm;
        targetDash = COMET_LEN + wobble;
      }
      state.currentDash += (targetDash - state.currentDash) * 0.18;
      const d = Math.max(0.5, state.currentDash);

      const offRounded = Math.round(state.offset * 100) / 100;
      const dRounded = Math.round(d * 100) / 100;
      if (offRounded !== state.lastOff) {
        rect.style.strokeDashoffset = offRounded;
        state.lastOff = offRounded;
      }
      if (dRounded !== state.lastDash) {
        rect.style.strokeDasharray = `${dRounded} ${(100 - dRounded).toFixed(2)}`;
        state.lastDash = dRounded;
      }

      state.raf = requestAnimationFrame(tick);
    };
    state.raf = requestAnimationFrame(tick);
  }

  function stopOrbit(btn, opts = {}) {
    const state = orbits.get(btn);
    if (!state) return;
    state.alive = false;
    if (state.raf) cancelAnimationFrame(state.raf);
    orbits.delete(btn);
    btn.removeAttribute("aria-busy");
    btn.classList.remove("kb-orbit");

    const svg = btn.querySelector(":scope > .kb-loader");
    const rect = svg?.querySelector("rect");
    if (opts.success && rect) {
      const currentDash = state.currentDash || COMET_LEN;
      const currentOffset = state.offset ?? 0;
      const closeOffset = currentOffset - 50;

      btn.classList.add("kb-ring-forming");

      const FORM_MS = 560;
      const COLLAPSE_MS = 420;

      const grow = rect.animate([
        { strokeDasharray: `${currentDash} ${100 - currentDash}`, strokeDashoffset: currentOffset },
        { strokeDasharray: "100 0", strokeDashoffset: closeOffset }
      ], { duration: FORM_MS, fill: "forwards", easing: "cubic-bezier(0.4, 0, 0.2, 1)" });

      grow.onfinish = () => {
        btn.classList.remove("kb-ring-forming");
        const collapse = rect.animate([
          { opacity: 1 },
          { opacity: 0 }
        ], { duration: COLLAPSE_MS, fill: "forwards", easing: "cubic-bezier(0.4, 0, 0.2, 1)" });
        collapse.onfinish = () => svg?.remove();
      };
    } else {
      svg?.remove();
    }
  }

  function syncBtn(btn) {
    const wasLoading = orbits.has(btn);
    const isLoading = btn.hasAttribute("data-loading");
    const isSuccess = btn.hasAttribute("data-success");
    if (isSuccess) ensureCheck(btn);
    if (!isSuccess) {
      btn.querySelector(":scope > .kb-check")?.remove();
      btn.classList.remove("kb-ring-forming");
    }
    if (isLoading) {
      startOrbit(btn);
    } else if (wasLoading) {
      stopOrbit(btn, { success: isSuccess });
    } else if (!isSuccess) {
      btn.querySelector(":scope > .kb-loader")?.remove();
    }
  }

  function syncAll(root = document) {
    root.querySelectorAll?.(".kb").forEach(syncBtn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => syncAll());
  } else {
    syncAll();
  }

  new MutationObserver((muts) => {
    for (const m of muts) {
      if (m.type === "attributes" && (m.attributeName === "data-loading" || m.attributeName === "data-success")) {
        syncBtn(m.target);
      } else if (m.type === "childList") {
        m.addedNodes.forEach((n) => {
          if (n.nodeType !== 1) return;
          if (n.matches?.(".kb")) syncBtn(n);
          n.querySelectorAll?.(".kb").forEach(syncBtn);
        });
        m.removedNodes.forEach((n) => {
          if (n.nodeType !== 1) return;
          if (orbits.has(n)) {
            const state = orbits.get(n);
            state.alive = false;
            if (state.raf) cancelAnimationFrame(state.raf);
            orbits.delete(n);
          }
        });
      }
    }
  }).observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["data-loading", "data-success"],
  });

  const ro = new ResizeObserver((entries) => {
    for (const e of entries) {
      if (e.target.hasAttribute("data-loading")) sizeLoader(e.target);
    }
  });
  document.querySelectorAll(".kb").forEach((b) => ro.observe(b));
  new MutationObserver((muts) => {
    for (const m of muts) {
      m.addedNodes.forEach((n) => {
        if (n.nodeType !== 1) return;
        if (n.matches?.(".kb")) ro.observe(n);
        n.querySelectorAll?.(".kb").forEach((b) => ro.observe(b));
      });
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
