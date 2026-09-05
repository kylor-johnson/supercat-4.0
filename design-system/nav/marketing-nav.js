/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Marketing Nav controller  ·  .vn
   ────────────────────────────────────────────────────────────────
   Two things in one file:

   1) Defines <sc-marketing-nav> custom element — the universal
      shared snippet. Every marketing page just writes:
        <sc-marketing-nav current="reference"></sc-marketing-nav>
      and gets the full two-pill nav, mega menus, mobile burger,
      theme toggle, and CTA. Change the markup here once → every
      page updates.

      Supported attributes:
        current   — sets aria-current on the matching mega link
                    ("portal" · "reference" · "tokens" · "dashboard" · "orders" · …)
        cta-href  — override the primary CTA destination
                    (default: /app/dashboard.html)
        cta-label — override the primary CTA label (default: "Open App")

   2) Init logic — binds:
      • Hover/focus mega-menu open/close on .vn-link[data-mega]
      • Theme toggle on [data-vn-theme] — flips <html data-theme>,
        persists to localStorage under 'supercat-theme'
      • Mobile chrome — burger + accordion + duplicate CTA
      • Restructures the left pill into a glass wrapper + mega
        siblings (so the mega panels can have their own backdrop)

   Framework-agnostic vanilla. Drop in via <script src="…" defer>.
   ════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Design-system root resolver ──────────────────────────────────
     Computes the URL prefix to the design-system root from this
     script's own location. Makes the nav work in three contexts
     without any per-page config:
       • file://   (unzip + double-click index.html)
       • localhost (any subpath — e.g. dev preview rooted elsewhere)
       • production (served from /)
     Every absolute href in the data ('/app/...', '/ds/...') is
     rewritten through resolveHref() at render time. */
  const _scriptEl =
    document.currentScript ||
    document.querySelector('script[src*="marketing-nav.js"]');
  const _scriptSrc = _scriptEl ? _scriptEl.src : '';
  const DS_ROOT = _scriptSrc
    ? _scriptSrc.replace(/nav\/marketing-nav\.js(?:\?.*)?$/, '')
    : '/';
  function resolveHref(href) {
    if (!href) return href;
    if (/^([a-z][a-z0-9+.-]*:)?\/\//i.test(href)) return href; // http://, //
    if (href.charAt(0) === '#' || href.charAt(0) === '?') return href;
    if (href.charAt(0) === '/') return DS_ROOT + href.slice(1);
    return href;
  }

  /* ── Logo SVG — single source of truth for the wordmark ───────── */

  const LOGO_WORD_SVG =
    '<svg class="vn-brand-logo" viewBox="0 0 237 28" aria-hidden="true">' +
      '<path class="logo-word" d="M49.001 18.931V15.1316C49.0258 14.9292 48.9804 14.7268 48.8646 14.5575C48.6952 14.4543 48.4968 14.4088 48.3025 14.4336H46.7732C45.5911 14.4336 45 13.8431 45 12.6619V8.77581C45 7.59469 45.5911 7 46.7732 7H48.753C49.9351 7 50.5262 7.59469 50.5262 8.77581V10.9316H48.9762V9.01947C49.0796 8.73864 48.9349 8.42891 48.6538 8.32566C48.5298 8.28024 48.3976 8.28024 48.2777 8.32566H47.2444C46.9633 8.22242 46.6533 8.36696 46.55 8.64779C46.5045 8.76755 46.5045 8.89971 46.55 9.01947V12.41C46.5252 12.6041 46.5706 12.8024 46.674 12.9717C46.8434 13.0832 47.046 13.1327 47.2444 13.1038H48.7737C49.9558 13.1038 50.551 13.6985 50.551 14.8796V19.1953C50.551 20.3764 49.9558 20.967 48.7737 20.967H46.8186C45.6365 20.967 45.0455 20.3764 45.0455 19.1953V17.0395H46.5955V18.931C46.4921 19.2118 46.6368 19.5215 46.9178 19.6248C47.0377 19.6702 47.17 19.6702 47.2898 19.6248H48.3025C48.4968 19.6496 48.6952 19.6041 48.8646 19.5009C48.9804 19.3357 49.03 19.1333 49.001 18.931Z"/>' +
      '<path class="logo-word" d="M60.5261 7H62.0513V19.1953C62.0513 20.3764 61.4602 20.967 60.2781 20.967H57.9841C56.802 20.967 56.2109 20.3764 56.2109 19.1953V7H57.7361V18.931C57.7072 19.1333 57.7568 19.3357 57.8725 19.5009C58.042 19.6041 58.2404 19.6496 58.4346 19.6248H59.8482C60.0425 19.6496 60.2409 19.6041 60.4104 19.5009C60.5261 19.3357 60.5757 19.1333 60.5468 18.931L60.5261 7Z"/>' +
      '<path class="logo-word" d="M68.0586 7H72.1258C73.3079 7 73.9031 7.59469 73.9031 8.77581V13.5622C73.9031 14.7475 73.3079 15.3381 72.1258 15.3381H69.5879V20.9504H68.0586V7ZM72.3737 13.3351V9.01947C72.4812 8.73864 72.3407 8.42891 72.0596 8.32153C71.9356 8.27611 71.7992 8.27611 71.6752 8.32153H69.6086V14.0289H71.6752C71.9563 14.1322 72.2663 13.9917 72.3737 13.7109C72.4192 13.5912 72.4192 13.4549 72.3737 13.3351Z"/>' +
      '<path class="logo-word" d="M80.9553 19.6413H84.7952V20.967H79.4219V7H84.6505V8.32566H80.9677V13.0419H83.9768V14.3882H80.9677L80.9553 19.6413Z"/>' +
      '<path class="logo-word" d="M91.6074 15.1316V20.967H90.0781V7H94.1577C95.3398 7 95.935 7.59469 95.935 8.77581V13.3558C95.935 14.4171 95.4679 15.0077 94.5421 15.1068L96.6377 20.967H94.9843L92.9177 15.1316H91.6074ZM91.6074 8.32566V13.8059H93.6741C93.9552 13.9133 94.2652 13.7729 94.3726 13.492C94.4181 13.3681 94.4181 13.2319 94.3726 13.108V9.01947C94.4801 8.73864 94.3395 8.42891 94.0585 8.32153C93.9345 8.27611 93.7981 8.27611 93.6741 8.32153H91.6074V8.32566Z"/>' +
      '<path class="logo-word" d="M107.467 11.1339H105.917V9.01947C105.942 8.81711 105.896 8.61475 105.78 8.44543C105.615 8.34218 105.417 8.29676 105.222 8.32153H103.982C103.701 8.21829 103.391 8.36283 103.288 8.64366C103.243 8.76755 103.243 8.89971 103.288 9.01947V18.9681C103.263 19.1622 103.309 19.3605 103.412 19.5298C103.581 19.6454 103.784 19.6909 103.987 19.6661H105.227C105.421 19.6867 105.619 19.6413 105.785 19.5298C105.896 19.3646 105.946 19.1664 105.921 18.9681V16.8661H107.471V19.2242C107.471 20.4053 106.88 21 105.698 21H103.515C102.333 21 101.742 20.4053 101.742 19.2242V8.77581C101.742 7.59469 102.333 7 103.515 7H105.698C106.88 7 107.471 7.59469 107.471 8.77581V11.1339H107.467Z"/>' +
      '<path class="logo-word" d="M117.786 20.967L117.199 17.4195H114.367L113.851 20.967H112.301L114.479 7H116.93L119.336 20.967H117.786ZM114.549 16.0938H116.996L115.694 8.07788L114.549 16.0938Z"/>' +
      '<path class="logo-word" d="M129.405 7V8.32566H127.157V20.967H125.627V8.32566H123.379V7H129.405Z"/>' +
      '<path class="logo-word" d="M144.532 18.931V15.1316C144.557 14.9292 144.512 14.7268 144.396 14.5575C144.226 14.4543 144.028 14.4088 143.834 14.4336H142.304C141.122 14.4336 140.531 13.8431 140.531 12.6619V8.77581C140.531 7.59469 141.122 7 142.304 7H144.284C145.466 7 146.057 7.59469 146.057 8.77581V10.9316H144.507V9.01947C144.611 8.73864 144.47 8.42891 144.189 8.32153C144.069 8.27611 143.933 8.27611 143.813 8.32153H142.776C142.495 8.21829 142.185 8.36283 142.081 8.63953C142.036 8.76342 142.036 8.89558 142.081 9.01947V12.41C142.056 12.6041 142.102 12.8024 142.205 12.9717C142.375 13.0832 142.577 13.1327 142.776 13.1038H144.305C145.487 13.1038 146.082 13.6985 146.082 14.8796V19.1953C146.082 20.3764 145.487 20.967 144.305 20.967H142.35C141.168 20.967 140.577 20.3764 140.577 19.1953V17.0395H142.127V18.931C142.023 19.2118 142.168 19.5215 142.449 19.6248C142.569 19.6702 142.701 19.6702 142.821 19.6248H143.834C144.028 19.6496 144.226 19.6041 144.396 19.5009C144.512 19.3357 144.561 19.1333 144.532 18.931Z"/>' +
      '<path class="logo-word" d="M153.468 7H155.762C156.945 7 157.536 7.59469 157.536 8.77581V19.1953C157.536 20.3764 156.945 20.967 155.762 20.967H153.468C152.286 20.967 151.695 20.3764 151.695 19.1953V8.77581C151.695 7.59469 152.286 7 153.468 7ZM156.01 18.931V9.01947C156.035 8.81711 155.99 8.61475 155.874 8.44543C155.705 8.34218 155.506 8.29676 155.312 8.32153H153.919C153.725 8.29676 153.526 8.34218 153.357 8.44543C153.266 8.52802 153.225 8.71799 153.225 9.01947V18.931C153.225 19.2283 153.266 19.4224 153.357 19.5009C153.526 19.6041 153.725 19.6496 153.919 19.6248H155.328C155.523 19.6496 155.721 19.6041 155.891 19.5009C156.002 19.3316 156.044 19.1292 156.01 18.931Z"/>' +
      '<path class="logo-word" d="M165.025 19.6413H168.237V20.967H163.496V7H165.025V19.6413Z"/>' +
      '<path class="logo-word" d="M177.428 7H178.958V19.1953C178.958 20.3764 178.367 20.967 177.18 20.967H174.891C173.704 20.967 173.109 20.3764 173.113 19.1953V7H174.643V18.931C174.614 19.1292 174.663 19.3316 174.775 19.5009C174.944 19.6041 175.143 19.6496 175.337 19.6248H176.734C176.928 19.6496 177.127 19.6041 177.292 19.5009C177.408 19.3357 177.457 19.1333 177.428 18.931V7Z"/>' +
      '<path class="logo-word" d="M189.857 7V8.32566H187.609V20.967H186.079V8.32566H183.852V7H189.857Z"/>' +
      '<path class="logo-word" d="M195.008 7H196.537V20.967H195.008V7Z"/>' +
      '<path class="logo-word" d="M204.516 7H206.81C207.992 7 208.587 7.59469 208.587 8.77581V19.1953C208.587 20.3764 207.992 20.967 206.81 20.967H204.516C203.333 20.967 202.742 20.3764 202.742 19.1953V8.77581C202.73 7.59469 203.321 7 204.516 7ZM207.045 18.931V9.01947C207.07 8.81711 207.024 8.61475 206.909 8.44543C206.739 8.34218 206.541 8.29676 206.347 8.32153H204.954C204.759 8.29676 204.561 8.34218 204.392 8.44543C204.28 8.61475 204.23 8.81711 204.259 9.01947V18.931C204.23 19.1292 204.28 19.3316 204.392 19.5009C204.561 19.6041 204.759 19.6496 204.954 19.6248H206.347C206.541 19.6496 206.739 19.6041 206.909 19.5009C207.024 19.3357 207.074 19.1333 207.045 18.931Z"/>' +
      '<path class="logo-word" d="M219.111 7H220.529V20.967H218.842L215.949 10.1469V20.967H214.531V7H216.329L219.115 17.4442V7H219.111Z"/>' +
      '<path class="logo-word" d="M230.255 18.931V15.1316C230.284 14.9292 230.234 14.7268 230.123 14.5575C229.953 14.4543 229.755 14.413 229.561 14.4336H228.031C226.849 14.4336 226.254 13.8431 226.254 12.6619V8.77581C226.254 7.59469 226.849 7 228.031 7H230.007C231.193 7 231.784 7.59469 231.784 8.77581V10.9316H230.234V9.01947C230.342 8.73864 230.201 8.42891 229.92 8.32153C229.796 8.27611 229.66 8.27611 229.536 8.32153H228.486C228.201 8.22655 227.895 8.37935 227.8 8.66018C227.758 8.77581 227.763 8.90384 227.804 9.01947V12.41C227.779 12.6041 227.825 12.8024 227.928 12.9717C228.097 13.0832 228.3 13.1327 228.502 13.1038H230.032C231.214 13.1038 231.805 13.6985 231.805 14.8796V19.1953C231.805 20.3764 231.214 20.967 230.032 20.967H228.073C226.886 20.967 226.291 20.3764 226.295 19.1953V17.0395H227.845V18.931C227.82 19.1292 227.862 19.3316 227.969 19.5009C228.139 19.6083 228.345 19.6496 228.544 19.6248H229.556C229.751 19.6454 229.949 19.6041 230.119 19.5009C230.23 19.3357 230.28 19.1292 230.255 18.931Z"/>' +
      '<path class="logo-word" d="M234.88 7V7.1941H234.306V8.69735H234.078V7.1941H233.504V7H234.88ZM236.72 8.69735L236.641 7.54513C236.641 7.44602 236.641 7.31799 236.62 7.18171C236.583 7.28083 236.525 7.45841 236.484 7.59469L236.091 8.68083H235.835L235.422 7.56578C235.389 7.45841 235.335 7.29735 235.298 7.18997V7.55339L235.215 8.70561H234.992L235.128 7.00826H235.459L235.872 8.0944C235.922 8.21829 235.951 8.33805 235.988 8.44956C236.025 8.33392 236.071 8.19351 236.104 8.10678L236.517 7.00826H236.848L237.001 8.70561L236.72 8.69735Z"/>' +
      '<path class="logo-mark" d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z"/>' +
      '<path class="logo-mark" d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z"/>' +
    '</svg>';

  const BRAND_MARK_SVG =
    '<svg viewBox="0 0 41 28" aria-hidden="true">' +
      '<path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="currentColor"/>' +
      '<path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="currentColor"/>' +
    '</svg>';

  // Exposed globally for other primitives (footer, app sidebar) that
  // need the same wordmark + mark — never duplicate the paths in HTML.
  window.SC_LOGO = { wordSvg: LOGO_WORD_SVG, markSvg: BRAND_MARK_SVG };

  /* Inject hidden <symbol id="sc-wordmark"> + <symbol id="i-mark"> so
     any page can drop `<svg><use href="#sc-wordmark"/></svg>` or
     `<svg><use href="#i-mark"/></svg>` without inlining the paths. */
  function ensureLogoSymbols() {
    if (document.getElementById('sc-wordmark')) return;
    // Extract paths from LOGO_WORD_SVG (everything between outer <svg> tags).
    const wordInner = LOGO_WORD_SVG.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    const markInner = BRAND_MARK_SVG.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    const wrap = document.createElement('div');
    wrap.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden';
    wrap.setAttribute('aria-hidden', 'true');
    wrap.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0">' +
        '<defs>' +
          '<symbol id="sc-wordmark" viewBox="0 0 237 28">' + wordInner + '</symbol>' +
          (document.getElementById('i-mark') ? '' :
            '<symbol id="i-mark" viewBox="0 0 41 28">' + markInner + '</symbol>') +
        '</defs>' +
      '</svg>';
    document.body.insertBefore(wrap, document.body.firstChild);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureLogoSymbols, { once: true });
  } else {
    ensureLogoSymbols();
  }


  /* ── Nav structure — what goes in the mega menus ──────────────── */

  /* Mega-panel structure — mirrors the portal (index.html) sections.
     The Reference lives under "Foundation" since it documents the
     system that powers both product families, not a single product.
     Each top-level link maps 1-to-1 to a portal section. */

  const MEGA_FOUNDATION = {
    title: 'Foundation',
    cards: [
      { ix: '01 · Foundation', nm: 'Reference',              ds: 'The complete design system on one page — tokens, primitives, patterns. Source of truth for both products.', href: '/ds/reference.html',           key: 'reference' },
      { ix: '02 · Foundation', nm: 'Tokens · W3C JSON',      ds: 'Machine-readable mirror for Figma + Style Dictionary.',                                                    href: '/ds/tokens/design-tokens.json', key: 'tokens', external: true },
      { ix: '03 · Foundation', nm: 'Primitives index',       ds: 'Twelve framework-agnostic CSS components — .kb · .kf-* · .kc · .knav · .kmd · .kfoot.',                     href: '/ds/primitives/',              key: 'primitives', external: true },
    ],
  };
  const MEGA_MARKETING = {
    title: 'Web Marketing',
    cards: [
      { ix: '01 · Web Marketing', nm: 'MaxROI · 90-Day payback',  ds: 'Live calculator + lead-magnet landing page. Editorial hero, real customer math, scenario toggle, cost-of-waiting moment, intent-aware lead modal.', href: '/marketing/maxroi.html', key: 'maxroi' },
    ],
  };
  const MEGA_APP = {
    title: 'Web / iPad App',
    cards: [
      { ix: '01 · App', nm: 'Dashboard',        ds: 'Metric tiles · chart · best-sellers · activity. Skeleton-loaded.', href: '/app/dashboard.html',  key: 'dashboard' },
      { ix: '02 · App', nm: 'Orders',           ds: 'Data table · filters · pagination.',                               href: '/app/orders.html',     key: 'orders' },
      { ix: '03 · App', nm: 'Products',         ds: 'Card-view grid · status flags.',                                   href: '/app/products.html',   key: 'products' },
      { ix: '04 · App', nm: 'Company Settings', ds: 'Horizontal tabs · panel swap · sticky save bar.',                  href: '/app/settings.html',   key: 'settings' },
      { ix: '05 · App', nm: 'Sign in',          ds: 'Two-panel auth flow — editorial brand left, form right.',          href: '/app/signin.html',     key: 'signin' },
    ],
  };
  const MEGA_DOCS = {
    title: 'Docs',
    cards: [
      { ix: '01 · Docs', nm: 'SURFACES.md',        ds: 'Web Marketing vs Web / iPad App — file-by-file map.',         href: '/docs/SURFACES.md',        key: 'surfaces' },
      { ix: '02 · Docs', nm: 'FRAMEWORK-GUIDE.md', ds: 'React · Vue · Angular · Svelte · Tailwind · LLM contract.',   href: '/docs/FRAMEWORK-GUIDE.md', key: 'framework' },
      { ix: '03 · Docs', nm: 'README.md',          ds: 'System overview · structure · token contract.',               href: '/README.md',               key: 'readme' },
    ],
  };
  /* Each panel gets a stable `key` slug used in data-mega attributes.
     This is decoupled from the display title so we can keep panel
     titles human-readable ("Web Marketing", "Web / iPad App") while
     the markup stays tidy. */
  MEGA_FOUNDATION.key = 'foundation';
  MEGA_MARKETING.key  = 'marketing';
  MEGA_APP.key        = 'app';
  MEGA_DOCS.key       = 'docs';
  const MEGAS = [MEGA_FOUNDATION, MEGA_MARKETING, MEGA_APP, MEGA_DOCS];

  function megaKey(m) { return m.key; }

  function renderMegaPanel(group, currentKey) {
    const cards = group.cards.map(function (c) {
      const attrs = c.external ? ' target="_blank" rel="noopener"' : '';
      const cur   = c.key === currentKey ? ' aria-current="page"' : '';
      return (
        '<a class="vn-mega-card" href="' + resolveHref(c.href) + '"' + attrs + cur + '>' +
          '<span class="ix">' + c.ix + '</span>' +
          '<span class="nm">' + c.nm + '</span>' +
          '<span class="ds">' + c.ds + '</span>' +
        '</a>'
      );
    }).join('');
    return (
      '<div class="vn-mega" data-mega="' + megaKey(group) + '" aria-hidden="true">' +
        '<div class="vn-mega-grid">' + cards + '</div>' +
      '</div>'
    );
  }

  function renderLinkButton(group) {
    return (
      '<button class="vn-link" data-mega="' + megaKey(group) + '" ' +
        'aria-expanded="false" aria-haspopup="true">' +
        group.title +
      '</button>'
    );
  }

  /* Render section anchor links — used when `sections` is provided.
     Same .vn-link visual chrome as the mega-menu buttons, just with
     <a href="#anchor"> instead of <button data-mega="…">. Lets pages
     keep the dark glass pill design while listing on-page sections
     instead of cross-site mega menus. */
  function renderSectionLink(section) {
    return (
      '<a class="vn-link vn-link-section" href="' + resolveHref(section.href) + '"' +
        (section.current ? ' aria-current="page"' : '') + '>' +
        section.label +
      '</a>'
    );
  }

  function renderNavHtml(opts) {
    opts = opts || {};
    const ctaHref  = resolveHref(opts.ctaHref  || '/app/dashboard.html');
    const ctaLabel = opts.ctaLabel || 'Open App';
    const current  = opts.current  || '';
    /* Brand logo destination — pages can override where the SuperCat
       wordmark links to via brand-href="https://supercatsolutions.com".
       Defaults to /index.html (the design-system portal). On a real
       marketing/lead-magnet page, set this to the product home so the
       logo click takes visitors to the main site (with UTMs applied by
       the page-local outbound-link decorator). */
    const brandHref = opts.brandHref ? opts.brandHref : resolveHref('/index.html');
    const sections = Array.isArray(opts.sections) ? opts.sections : null;
    const showMega = !sections;

    const arrow =
      '<svg class="arr-svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M3 8h10M9 4l4 4-4 4"/>' +
      '</svg>';

    const themeSvg =
      '<svg class="vn-theme-light" viewBox="0 0 16 16" aria-hidden="true">' +
        '<path d="M13 9.5a5.5 5.5 0 0 1-7-7 6 6 0 1 0 7 7z"/>' +
      '</svg>' +
      '<svg class="vn-theme-dark" viewBox="0 0 16 16" aria-hidden="true">' +
        '<circle cx="8" cy="8" r="3"/>' +
        '<path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.5 1.5M11.5 11.5L13 13M3 13l1.5-1.5M11.5 4.5L13 3"/>' +
      '</svg>';

    const linksHtml = showMega
      ? MEGAS.map(renderLinkButton).join('')
      : sections.map(renderSectionLink).join('');
    const megasHtml = showMega
      ? MEGAS.map(function (g) { return renderMegaPanel(g, current); }).join('')
      : '';

    return (
      '<header class="vn vn-floating' + (showMega ? '' : ' vn-sections') + '">' +
        '<div class="vn-shell">' +
          '<a class="vn-brand" href="' + brandHref + '" aria-label="SuperCat Solutions — home"' +
            (current === 'portal' ? ' aria-current="page"' : '') + '>' +
            LOGO_WORD_SVG +
          '</a>' +
          '<div class="vn-cluster">' +
            '<nav class="vn-links" aria-label="' + (showMega ? 'Main' : 'On this page') + '">' +
              linksHtml +
            '</nav>' +
            '<span class="vn-divider" aria-hidden="true"></span>' +
            '<button class="vn-theme" data-vn-theme aria-label="Toggle theme">' + themeSvg + '</button>' +
            '<a class="kb kb-md kb-primary" href="' + ctaHref + '">' + ctaLabel + arrow + '</a>' +
          '</div>' +
        '</div>' +
        megasHtml +
      '</header>'
    );
  }


  /* ── Custom element ──────────────────────────────────────────── */

  class ScMarketingNav extends HTMLElement {
    connectedCallback() {
      if (this._rendered) return;
      this._rendered = true;
      let sections = null;
      const sectionsAttr = this.getAttribute('sections');
      if (sectionsAttr) {
        try { sections = JSON.parse(sectionsAttr); }
        catch (e) { console.warn('<sc-marketing-nav> sections attribute: invalid JSON', e); }
      }
      this.innerHTML = renderNavHtml({
        current:   this.getAttribute('current')    || '',
        ctaHref:   this.getAttribute('cta-href')   || '',
        ctaLabel:  this.getAttribute('cta-label')  || '',
        brandHref: this.getAttribute('brand-href') || '',
        sections: sections,
      });
      // If init() already ran, bind this instance now.
      if (window.__scNavReady) initOne(this.querySelector('.vn'));
    }
  }
  if (!customElements.get('sc-marketing-nav')) {
    customElements.define('sc-marketing-nav', ScMarketingNav);
  }


  /* ── Theme ─────────────────────────────────────────────────── */

  const root = document.documentElement;
  const STORAGE_KEY = 'supercat-theme';

  function applyTheme(theme) {
    if (theme === 'dark') root.setAttribute('data-theme', 'dark');
    else root.removeAttribute('data-theme');
  }

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'dark') applyTheme('dark');
  } catch (e) { /* localStorage may be blocked */ }

  function bindThemeToggle(scope) {
    (scope || document).querySelectorAll('[data-vn-theme]').forEach(function (btn) {
      if (btn.dataset.scBound === '1') return;
      btn.dataset.scBound = '1';
      btn.addEventListener('click', function () {
        const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        try { localStorage.setItem(STORAGE_KEY, next); } catch (e) {}
      });
    });
  }


  /* ── Mega menus ────────────────────────────────────────────── */

  function bindMega(nav) {
    const links = nav.querySelectorAll('.vn-link[data-mega]');
    const megas = nav.querySelectorAll('.vn-mega[data-mega]');
    let closeTimer = null;

    function open(key) {
      clearTimeout(closeTimer);
      links.forEach(function (l) { l.setAttribute('aria-expanded', l.dataset.mega === key ? 'true' : 'false'); });
      megas.forEach(function (m) {
        const match = m.dataset.mega === key;
        m.classList.toggle('is-open', match);
        m.setAttribute('aria-hidden', match ? 'false' : 'true');
      });
    }
    function close() {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () {
        links.forEach(function (l) { l.setAttribute('aria-expanded', 'false'); });
        megas.forEach(function (m) {
          m.classList.remove('is-open');
          m.setAttribute('aria-hidden', 'true');
        });
      }, 160);
    }

    links.forEach(function (link) {
      link.addEventListener('mouseenter', function () { open(link.dataset.mega); });
      link.addEventListener('focus',      function () { open(link.dataset.mega); });
      link.addEventListener('mouseleave', close);
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const isOpen = link.getAttribute('aria-expanded') === 'true';
        if (isOpen) close();
        else open(link.dataset.mega);
      });
    });

    megas.forEach(function (mega) {
      mega.addEventListener('mouseenter', function () { open(mega.dataset.mega); });
      mega.addEventListener('mouseleave', close);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) close();
    });
  }


  /* ── Mobile chrome ───────────────────────────────────────────
     Build the burger + mobile menu accordion the first time a nav
     is processed. Idempotent — repeat calls skip if nodes exist. */

  function buildMobileChrome(nav) {
    const cluster = nav.querySelector('.vn-cluster');
    if (!cluster) return;
    const existingCta = cluster.querySelector('.kb.kb-primary:not(.vn-cta-mobile)');
    const ctaHref = existingCta ? existingCta.getAttribute('href') : resolveHref('/app/dashboard.html');
    /* Read CTA label from the desktop pill (it was rendered from opts.ctaLabel /
       cta-label="…" in renderNavHtml). Keeps mobile pill + drawer in sync with
       desktop instead of hardcoding "Open" / "Open App". */
    const ctaLabel = (existingCta && (existingCta.textContent || '').trim()) || 'Open App';

    const ARROW_SVG =
      '<svg class="arr-svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M3 8h10M9 4l4 4-4 4"/>' +
      '</svg>';
    const THEME_SVG =
      '<svg class="vn-theme-light" viewBox="0 0 16 16" aria-hidden="true">' +
        '<path d="M13 9.5a5.5 5.5 0 0 1-7-7 6 6 0 1 0 7 7z"/>' +
      '</svg>' +
      '<svg class="vn-theme-dark" viewBox="0 0 16 16" aria-hidden="true">' +
        '<circle cx="8" cy="8" r="3"/>' +
        '<path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.5 1.5M11.5 11.5L13 13M3 13l1.5-1.5M11.5 4.5L13 3"/>' +
      '</svg>';

    if (!cluster.querySelector('.vn-burger')) {
      const burger = document.createElement('button');
      burger.className = 'vn-burger';
      burger.setAttribute('aria-label', 'Open menu');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-controls', 'vn-mobile-menu');
      burger.innerHTML =
        '<span class="vn-burger-icon" aria-hidden="true">' +
          '<svg class="vn-burger-open" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">' +
            '<path d="M2 5.5h12M2 10.5h12"/>' +
          '</svg>' +
          '<svg class="vn-burger-close" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">' +
            '<path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/>' +
          '</svg>' +
        '</span>';
      cluster.appendChild(burger);
    }

    if (!cluster.querySelector('.vn-cta-mobile')) {
      const ctaMobile = document.createElement('a');
      ctaMobile.className = 'kb kb-md kb-primary vn-cta-mobile';
      ctaMobile.setAttribute('href', ctaHref);
      ctaMobile.innerHTML = ctaLabel + ARROW_SVG;
      cluster.appendChild(ctaMobile);
    }

    if (!nav.querySelector('.vn-mobile-menu')) {
      const menu = document.createElement('div');
      menu.className = 'vn-mobile-menu';
      menu.id = 'vn-mobile-menu';
      menu.setAttribute('aria-hidden', 'true');

      const PLUS_SVG =
        '<svg class="vn-section-plus" viewBox="0 0 16 16" aria-hidden="true">' +
          '<path d="M8 3v10M3 8h10"/>' +
        '</svg>';

      /* Sections mode mirrors what the desktop pill renders: one flat
         list of in-page anchors, no accordion. Cross-site mode keeps the
         expandable MEGAS accordion. The distinguishing marker is the
         `vn-sections` class added in renderNavHtml when opts.sections is
         provided — we read that here so mobile + desktop stay in sync. */
      const isSectionsMode = nav.classList.contains('vn-sections');
      let sectionsHtml;
      if (isSectionsMode) {
        const sectionLinks = nav.querySelectorAll('.vn-links .vn-link-section');
        sectionsHtml =
          '<nav class="vn-mobile-sections-list" aria-label="On this page">' +
            Array.from(sectionLinks).map(function (a) {
              const isCurrent = a.hasAttribute('aria-current');
              return '<a class="vn-mobile-section-link" href="' + a.getAttribute('href') + '"' +
                (isCurrent ? ' aria-current="page"' : '') +
                '>' + a.textContent + '</a>';
            }).join('') +
          '</nav>';
      } else {
        sectionsHtml = MEGAS.map(function (g, i) {
          const linksHtml = g.cards.map(function (c) {
            return '<a href="' + resolveHref(c.href) + '">' + c.nm + '</a>';
          }).join('');
          return (
            '<section class="vn-mobile-section">' +
              '<button class="vn-mobile-section-header" aria-expanded="false" aria-controls="vn-mobile-body-' + i + '">' +
                '<span class="vn-mobile-section-title">' + g.title + '</span>' +
                PLUS_SVG +
              '</button>' +
              '<div class="vn-mobile-section-body" id="vn-mobile-body-' + i + '">' +
                linksHtml +
              '</div>' +
            '</section>'
          );
        }).join('');
      }

      menu.innerHTML =
        sectionsHtml +
        '<div class="vn-mobile-actions">' +
          '<button class="vn-theme" data-vn-theme aria-label="Toggle theme">' + THEME_SVG + '</button>' +
          '<a class="kb kb-md kb-primary" href="' + ctaHref + '">' + ctaLabel + ARROW_SVG + '</a>' +
        '</div>';
      nav.appendChild(menu);
    }
  }


  /* ── Accordion + burger ────────────────────────────────────── */

  function bindAccordion(nav) {
    nav.querySelectorAll('.vn-mobile-section-header').forEach(function (header) {
      if (header.dataset.scBound === '1') return;
      header.dataset.scBound = '1';
      header.addEventListener('click', function (e) {
        e.stopPropagation();
        const expanded = header.getAttribute('aria-expanded') === 'true';
        header.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      });
    });
  }

  function bindBurger(nav) {
    const burger = nav.querySelector('.vn-burger');
    const menu = nav.querySelector('.vn-mobile-menu');
    if (!burger || !menu || burger.dataset.scBound === '1') return;
    burger.dataset.scBound = '1';

    function close() {
      menu.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
    }
    function open() {
      menu.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      menu.setAttribute('aria-hidden', 'false');
    }
    burger.addEventListener('click', function (e) {
      e.stopPropagation();
      if (menu.classList.contains('is-open')) close();
      else open();
    });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }


  /* ── Restructure (left-pill glass wrapper for mega panels) ─── */

  function restructureNav(nav) {
    const shell = nav.querySelector('.vn-shell');
    if (!shell) return;
    let pillLeft = shell.querySelector(':scope > .vn-pill-left');
    const brand = shell.querySelector(':scope > .vn-brand');
    const cluster = shell.querySelector(':scope > .vn-cluster');
    const linksInCluster = cluster ? cluster.querySelector(':scope > .vn-links') : null;

    if (!pillLeft && brand) {
      pillLeft = document.createElement('div');
      pillLeft.className = 'vn-pill-left';
      brand.parentNode.insertBefore(pillLeft, brand);

      const glass = document.createElement('div');
      glass.className = 'vn-pill-left-glass';
      pillLeft.appendChild(glass);
      glass.appendChild(brand);

      if (linksInCluster) {
        const divider = document.createElement('span');
        divider.className = 'vn-divider';
        divider.setAttribute('aria-hidden', 'true');
        glass.appendChild(divider);
        glass.appendChild(linksInCluster);
      }
      if (cluster) {
        cluster.querySelectorAll(':scope > .vn-divider').forEach(function (d) { d.remove(); });
      }
    }
    if (pillLeft) {
      nav.querySelectorAll(':scope > .vn-mega').forEach(function (mega) { pillLeft.appendChild(mega); });
    }
  }


  /* ── Bind one nav (used by upgrade path) ───────────────────── */

  function initOne(nav) {
    if (!nav || nav.dataset.scInitDone === '1') return;
    nav.dataset.scInitDone = '1';
    restructureNav(nav);
    buildMobileChrome(nav);
    bindMega(nav);
    bindBurger(nav);
    bindAccordion(nav);
    bindThemeToggle(nav);
  }


  /* ── Mount ─────────────────────────────────────────────────── */

  function init() {
    document.querySelectorAll('.vn').forEach(initOne);
    bindThemeToggle(document); // catch any [data-vn-theme] outside a nav
    window.__scNavReady = true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
