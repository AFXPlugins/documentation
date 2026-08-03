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

// ---- Theme switcher ----
// 'browser' is the default theme: it has no data-theme attribute, so the
// stylesheet's prefers-color-scheme media query decides light vs dark.
const DEFAULT_THEME = 'browser';

function applyTheme(theme, persist) {
  if (theme === DEFAULT_THEME) {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', theme);
  }
  if (persist) {
    try { localStorage.setItem('cpn-theme', theme); } catch (err) { /* storage unavailable */ }
  }
  document.querySelectorAll('.theme-option').forEach(opt => {
    opt.setAttribute('aria-checked', opt.getAttribute('data-theme-value') === theme ? 'true' : 'false');
  });
}

function initThemeSwitcher() {
  const wrap = document.querySelector('[data-theme-switcher]');
  if (!wrap) return;
  const btn = wrap.querySelector('.theme-btn');
  const menu = wrap.querySelector('.theme-menu');
  if (!btn || !menu) return;

  let current = DEFAULT_THEME;
  try { current = localStorage.getItem('cpn-theme') || DEFAULT_THEME; } catch (err) { /* storage unavailable */ }
  applyTheme(current, false);

  const closeMenu = () => {
    wrap.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  };

  btn.addEventListener('click', () => {
    const willOpen = !wrap.classList.contains('open');
    wrap.classList.toggle('open', willOpen);
    btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
  });

  document.addEventListener('click', (e) => {
    if (wrap.classList.contains('open') && !wrap.contains(e.target)) closeMenu();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && wrap.classList.contains('open')) {
      closeMenu();
      btn.focus();
    }
  });

  menu.querySelectorAll('.theme-option').forEach(option => {
    option.addEventListener('click', () => {
      applyTheme(option.getAttribute('data-theme-value'), true);
      closeMenu();
    });
  });
}
