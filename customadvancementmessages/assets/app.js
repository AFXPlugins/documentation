// CustomPlayerNametags docs — shared behavior

document.addEventListener('DOMContentLoaded', () => {
  // Mobile sidebar toggle
  const menuBtn = document.querySelector('.menu-btn');
  const sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') &&
          !sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
    sidebar.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => sidebar.classList.remove('open')));
  }

  // Copy-to-clipboard on code blocks
  document.querySelectorAll('.code-block').forEach(block => {
    const btn = block.querySelector('.copy-btn');
    const code = block.querySelector('code');
    if (!btn || !code) return;
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.innerText);
        btn.textContent = 'copied';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'copy'; btn.classList.remove('copied'); }, 1500);
      } catch (err) {
        btn.textContent = 'select + ⌘/ctrl-C';
      }
    });
  });

  initThemeSwitcher();
});

// ---- Theme toggle (light/dark slider) ----
// Storage key MUST match the inline no-flash script in every page's <head>.
const THEME_STORAGE_KEY = 'afxplugins-theme';

function getStoredTheme() {
  try {
    const t = localStorage.getItem(THEME_STORAGE_KEY);
    return (t === 'light' || t === 'dark') ? t : null;
  } catch (err) {
    return null; // storage unavailable
  }
}

function systemPrefersLight() {
  return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches);
}

// The theme actually being rendered right now: an explicit stored choice,
// or — on a first visit, before any choice has been made — the visitor's
// OS/browser preference (handled purely by CSS, with no data-theme
// attribute set, so there's nothing for JS to flash-fix).
function effectiveTheme(stored) {
  return stored || (systemPrefersLight() ? 'light' : 'dark');
}

function applyExplicitTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  document.documentElement.setAttribute('data-toggle-state', theme);
  try { localStorage.setItem(THEME_STORAGE_KEY, theme); } catch (err) { /* storage unavailable */ }
}

function initThemeSwitcher() {
  const toggle = document.querySelector('[data-theme-toggle]');
  if (!toggle) return;

  let stored = getStoredTheme();

  const syncUI = () => {
    toggle.setAttribute('aria-checked', effectiveTheme(stored) === 'dark' ? 'true' : 'false');
  };
  syncUI();

  toggle.addEventListener('click', () => {
    const next = effectiveTheme(stored) === 'dark' ? 'light' : 'dark';
    applyExplicitTheme(next);
    stored = next;
    syncUI();
  });

  // Until the visitor makes an explicit choice, keep the slider's knob in
  // sync if their OS/browser color-scheme preference changes mid-session.
  if (window.matchMedia) {
    const mq = window.matchMedia('(prefers-color-scheme: light)');
    const onSystemChange = () => { if (!stored) syncUI(); };
    if (mq.addEventListener) mq.addEventListener('change', onSystemChange);
    else if (mq.addListener) mq.addListener(onSystemChange);
  }
}
