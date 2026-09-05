/* ════════════════════════════════════════════════════════════════
   SuperCat DS — App Sidebar  ·  <sc-app-sidebar>
   ────────────────────────────────────────────────────────────────
   The universal app left-sidebar (.knav) as a custom element. One
   source of truth — change here once, every app page updates.

   Usage:
     <sc-app-sidebar
       active="dashboard"          (which top-level item is current)
       orders-count="1,287"        (badge count on Orders)
       org-name="Opame Collective"
       org-badge="OP"
       user-name="Alex Malyshev"
       user-avatar="AM"
       user-role="Account"
     ></sc-app-sidebar>

   Behavior wired up:
     • Brand mark (gold double-wave) + full wordmark
     • Collapse-to-rail toggle on the right edge — hover-revealed,
       vertically centered. State persists in localStorage
       (`supercat:knav:rail`) so it survives navigation.
     • Smooth width animation on collapse.
     • Expandable groups — items with sublists toggle open on click.
   ════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Design-system root resolver ──────────────────────────────────
     Lets the sidebar work from file:// (unzip + double-click), any
     localhost subpath, or a production root. Detects the design-
     system root from this script's own src and rewrites absolute
     hrefs through it at render time. */
  const _scriptEl =
    document.currentScript ||
    document.querySelector('script[src*="app-sidebar.js"]');
  const _scriptSrc = _scriptEl ? _scriptEl.src : '';
  const DS_ROOT = _scriptSrc
    ? _scriptSrc.replace(/nav\/app-sidebar\.js(?:\?.*)?$/, '')
    : '/';
  function resolveHref(href) {
    if (!href) return href;
    if (/^([a-z][a-z0-9+.-]*:)?\/\//i.test(href)) return href;
    if (href.charAt(0) === '#' || href.charAt(0) === '?') return href;
    if (href.charAt(0) === '/') return DS_ROOT + href.slice(1);
    return href;
  }

  /* ── SVG icon set — single source of truth ───────────────────── */

  const ICONS = {
    'mark': '<svg viewBox="0 0 41 28" aria-hidden="true">' +
      '<path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="currentColor"/>' +
      '<path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="currentColor"/>' +
    '</svg>',
    'home':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-8 9 8M5 9v12h14V9"/></svg>',
    'dash':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3h7v9H3zM14 3h7v5h-7zM14 12h7v9h-7zM3 16h7v5H3z"/></svg>',
    'sparkle':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 4.9L18 9.5l-4.2 1.6L12 16l-1.8-4.9L6 9.5l4.2-1.6L12 3z"/></svg>',
    'users':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="4"/><path d="M2 21v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1"/><circle cx="17" cy="6" r="3"/><path d="M22 19v-1a4 4 0 0 0-4-4h-1"/></svg>',
    'orders':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h2l2 11h11l2-8H6"/><circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/></svg>',
    'products':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7l9-4 9 4-9 4-9-4zM3 12l9 4 9-4M3 17l9 4 9-4"/></svg>',
    'customers': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21v-1a5 5 0 0 1 5-5h6a5 5 0 0 1 5 5v1"/><circle cx="12" cy="8" r="4"/></svg>',
    'lists':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6h12M9 12h12M9 18h12"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
    'library':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 11l5-3 4 2 6-4 3 2"/></svg>',
    'formats':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h10l4 4v12H5z"/><path d="M15 4v4h4"/></svg>',
    'notice':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l13-7v16L3 13z"/><path d="M16 10h4M16 14h4"/></svg>',
    'gear':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
    'mobile':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></svg>',
    'file':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h10l4 4v12H5z"/><path d="M15 4v4h4"/><path d="M9 14h6M9 18h4"/></svg>',
    'upload':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5M12 3v12"/></svg>',
    'chev-r':    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6,3 11,8 6,13"/></svg>',
    'chev-d':    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="3,6 8,11 13,6"/></svg>',
    'chev-l':    '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="7.5,2 3.5,6 7.5,10"/></svg>',
  };

  function icon(name) { return ICONS[name] || ''; }


  /* ── Logo wordmark — pulls from window.SC_LOGO populated by
        marketing-nav.js (single shared source). Fallback inline if
        marketing-nav.js hasn't loaded yet. */

  const LOGO_WORD_FALLBACK =
    '<svg class="knav-brand-logo" viewBox="0 0 237 28" aria-label="Supercat Solutions">' +
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

  function getWordmark() {
    if (window.SC_LOGO && window.SC_LOGO.wordSvg) {
      // marketing-nav.js exposes the wordmark SVG but without the .knav-brand-logo class
      // Patch class onto the outer <svg> for sidebar styling.
      return window.SC_LOGO.wordSvg.replace('class="vn-brand-logo"', 'class="knav-brand-logo"');
    }
    return LOGO_WORD_FALLBACK;
  }


  /* ── Item structure ─────────────────────────────────────────── */

  // Each entry: { key, label, icon, href, count, expandable, children }
  // expandable items toggle a sublist; non-expandable navigate.
  const MAIN_ITEMS = [
    { key: 'home',      label: 'Home',       icon: 'home',      href: '/app/dashboard.html' },
    { key: 'dashboard', label: 'Dashboard',  icon: 'dash',      href: '/app/dashboard.html' },
    { key: 'intelligence', label: 'Intelligence', icon: 'sparkle', href: '/app/sales-portal-cycle03-chrome.html' },
    { key: 'users',     label: 'Users',      icon: 'users',     expandable: true, children: [
      { label: 'All users',     href: '#' },
      { label: 'Roles',         href: '#' },
      { label: 'Invitations',   href: '#' },
    ]},
    { key: 'orders',    label: 'Orders',     icon: 'orders',    href: '/app/orders.html' },
    { key: 'products',  label: 'Products',   icon: 'products',  expandable: true, children: [
      { label: 'All products',  href: '/app/products.html' },
      { label: 'Add product',   href: '#' },
      { label: 'Categories',    href: '#' },
    ]},
    { key: 'customers', label: 'Customers',  icon: 'customers', expandable: true, children: [
      { label: 'All customers', href: '#' },
      { label: 'Segments',      href: '#' },
    ]},
    { key: 'lists',     label: 'SmartLists', icon: 'lists',     href: '#' },
    { key: 'library',   label: 'Library',    icon: 'library',   href: '#' },
    { key: 'formats',   label: 'Formats',    icon: 'formats',   expandable: true, children: [
      { label: 'Catalog PDF',   href: '#' },
      { label: 'Price sheet',   href: '#' },
      { label: 'Custom',        href: '#' },
    ]},
    { key: 'notice',    label: 'Notices',    icon: 'notice',    href: '#' },
  ];

  const TOOLS_ITEMS = [
    { key: 'settings', label: 'Company Settings', icon: 'gear',   href: '/app/settings.html' },
    { key: 'mobile',   label: 'Mobile Sites',     icon: 'mobile', href: '#' },
    { key: 'import',   label: 'File Import Status', icon: 'file', href: '#' },
    { key: 'data',     label: 'Import Data',      icon: 'upload', expandable: true, children: [
      { label: 'New import',   href: '#' },
      { label: 'History',      href: '#' },
    ]},
  ];


  /* ── Render ─────────────────────────────────────────────────── */

  function renderItem(item, activeKey, orderCount) {
    const active = item.key === activeKey;
    if (item.expandable) {
      const sub = item.children.map(function (c) {
        return '<a class="knav-item knav-sub" href="' + resolveHref(c.href) + '"><span class="knav-text">' + c.label + '</span></a>';
      }).join('');
      return (
        '<button class="knav-item knav-expand" type="button" aria-expanded="false" data-knav-expand="' + item.key + '">' +
          '<span class="knav-icon">' + icon(item.icon) + '</span>' +
          '<span class="knav-text">' + item.label + '</span>' +
          '<span class="knav-trail knav-expand-chev" aria-hidden="true">' + icon('chev-d') + '</span>' +
        '</button>' +
        '<div class="knav-sublist" data-knav-sublist="' + item.key + '" hidden>' + sub + '</div>'
      );
    }
    let trail = '';
    if (item.key === 'orders' && orderCount) {
      trail = '<span class="knav-trail"><span class="knav-count">' + orderCount + '</span></span>';
    }
    return (
      '<a class="knav-item" href="' + resolveHref(item.href || '#') + '"' + (active ? ' aria-current="page"' : '') + '>' +
        '<span class="knav-icon">' + icon(item.icon) + '</span>' +
        '<span class="knav-text">' + item.label + '</span>' +
        trail +
      '</a>'
    );
  }

  function renderAside(opts) {
    const active     = opts.active     || 'dashboard';
    const orderCount = opts.orderCount || '';
    const orgName    = opts.orgName    || 'Opame Collective';
    const orgBadge   = opts.orgBadge   || 'OP';
    const userName   = opts.userName   || 'Alex Malyshev';
    const userAvatar = opts.userAvatar || 'AM';
    const userRole   = opts.userRole   || 'Account';

    const mainHtml  = MAIN_ITEMS.map(function (i) { return renderItem(i, active, orderCount); }).join('');
    const toolsHtml = TOOLS_ITEMS.map(function (i) { return renderItem(i, active, orderCount); }).join('');

    return (
      '<aside class="knav knav-floating" aria-label="Primary navigation">' +
        '<button class="knav-toggle" type="button" aria-label="Collapse sidebar" title="Collapse sidebar" aria-pressed="false">' +
          icon('chev-l') +
        '</button>' +
        '<header class="knav-brand">' +
          '<a class="knav-brand-link" href="' + resolveHref('/app/dashboard.html') + '">' +
            '<span class="knav-brand-mark" aria-hidden="true">' + icon('mark') + '</span>' +
            getWordmark() +
          '</a>' +
        '</header>' +
        '<div class="knav-body">' +
          '<nav class="knav-list" aria-label="Main">' + mainHtml + '</nav>' +
          '<div class="knav-section">' +
            '<h3 class="knav-eyebrow">Settings &amp; Tools</h3>' +
            '<nav class="knav-list">' + toolsHtml + '</nav>' +
          '</div>' +
          '<div class="knav-spacer"></div>' +
        '</div>' +
        '<footer class="knav-account">' +
          '<div class="knav-org">' +
            '<span class="knav-org-badge" aria-hidden="true">' + orgBadge + '</span>' +
            '<span class="knav-org-name">' + orgName + '</span>' +
          '</div>' +
          '<button class="knav-user">' +
            '<span class="knav-user-avatar">' + userAvatar + '</span>' +
            '<span class="knav-user-info">' +
              '<span class="knav-user-name">' + userName + '</span>' +
              '<span class="knav-user-role">' + userRole + '</span>' +
            '</span>' +
            '<span class="knav-user-trail">' + icon('chev-r') + '</span>' +
          '</button>' +
        '</footer>' +
      '</aside>'
    );
  }


  /* ── Behaviour: rail toggle + expandable groups ─────────────── */

  const RAIL_KEY = 'supercat:knav:rail';

  function readRail() {
    try { return localStorage.getItem(RAIL_KEY) === '1'; }
    catch (e) { return false; }
  }
  function writeRail(on) {
    try { localStorage.setItem(RAIL_KEY, on ? '1' : '0'); }
    catch (e) {}
  }

  function applyRail(nav, rail) {
    nav.classList.toggle('knav-rail', rail);
    const btn = nav.querySelector('.knav-toggle');
    if (btn) {
      btn.setAttribute('aria-pressed', rail ? 'true' : 'false');
      const label = rail ? 'Expand sidebar' : 'Collapse sidebar';
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
    }
    // In rail mode, close all expandable groups (no room for sublists)
    if (rail) {
      nav.querySelectorAll('[data-knav-expand]').forEach(function (b) {
        b.setAttribute('aria-expanded', 'false');
        const list = nav.querySelector('[data-knav-sublist="' + b.dataset.knavExpand + '"]');
        if (list) list.hidden = true;
      });
    }
  }

  function bindToggle(nav) {
    const btn = nav.querySelector('.knav-toggle');
    if (!btn || btn.dataset.scBound === '1') return;
    btn.dataset.scBound = '1';
    btn.addEventListener('click', function () {
      const rail = !nav.classList.contains('knav-rail');
      writeRail(rail);
      // Apply to every .knav on the page (and sync state across all instances).
      document.querySelectorAll('.knav').forEach(function (n) {
        if (!n.classList.contains('knav-drawer')) applyRail(n, rail);
      });
    });
  }

  function bindExpandable(nav) {
    nav.querySelectorAll('[data-knav-expand]').forEach(function (btn) {
      if (btn.dataset.scBound === '1') return;
      btn.dataset.scBound = '1';
      btn.addEventListener('click', function () {
        // No expand in rail mode — toggle the sidebar open first.
        if (nav.classList.contains('knav-rail')) return;
        const expanded = btn.getAttribute('aria-expanded') === 'true';
        const next = !expanded;
        btn.setAttribute('aria-expanded', next ? 'true' : 'false');
        const list = nav.querySelector('[data-knav-sublist="' + btn.dataset.knavExpand + '"]');
        if (list) list.hidden = !next;
      });
    });
  }


  /* ── Custom element ─────────────────────────────────────────── */

  class ScAppSidebar extends HTMLElement {
    connectedCallback() {
      if (this._rendered) return;
      this._rendered = true;
      this.innerHTML = renderAside({
        active:     this.getAttribute('active'),
        orderCount: this.getAttribute('orders-count'),
        orgName:    this.getAttribute('org-name'),
        orgBadge:   this.getAttribute('org-badge'),
        userName:   this.getAttribute('user-name'),
        userAvatar: this.getAttribute('user-avatar'),
        userRole:   this.getAttribute('user-role'),
      });
      const nav = this.querySelector('.knav');
      if (nav) {
        applyRail(nav, readRail());
        bindToggle(nav);
        bindExpandable(nav);
      }
    }
  }

  if (!customElements.get('sc-app-sidebar')) {
    customElements.define('sc-app-sidebar', ScAppSidebar);
  }

  // Also handle any static .knav already in the DOM (legacy markup).
  function bindStaticNavs() {
    document.querySelectorAll('.knav').forEach(function (nav) {
      if (nav.dataset.scBound === '1') return;
      nav.dataset.scBound = '1';
      applyRail(nav, readRail());
      bindToggle(nav);
      bindExpandable(nav);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindStaticNavs, { once: true });
  } else {
    bindStaticNavs();
  }
})();
