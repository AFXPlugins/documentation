import os
import shutil
import html

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,1..1000&family=Merriweather+Sans:ital,wght@0,300..800;1,300..800&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap" rel="stylesheet">'''

THEME_TOGGLE = '''<button class="theme-toggle" type="button" role="switch" aria-label="Switch between light and dark mode" data-theme-toggle>
    <span class="theme-toggle-track">
      <svg class="theme-toggle-icon theme-toggle-icon-sun" width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="3" stroke="currentColor" stroke-width="1.2"/><path d="M6.5 0.6v1.6M6.5 10.8v1.6M12.4 6.5h-1.6M2.2 6.5H0.6M10.6 2.4l-1.1 1.1M3.5 9.5l-1.1 1.1M10.6 10.6l-1.1-1.1M3.5 3.5L2.4 2.4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
      <svg class="theme-toggle-icon theme-toggle-icon-moon" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M11 7.6A5 5 0 114.4 1a4 4 0 006.6 6.6z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
      <span class="theme-toggle-thumb"></span>
    </span>
  </button>'''


def callout(title, body):
    """A boxed note. Pass an empty title to omit the heading span."""
    title_html = f'<span class="callout-title">{title}</span>' if title else ""
    return f'<div class="callout">{title_html}<p>{body}</p></div>'


def code(lang, text):
    return (
        f'<div class="code-block"><pre><code class="lang-{lang}">{html.escape(text)}'
        f'</code></pre><button class="copy-btn">copy</button></div>'
    )

def doc_image(src, alt, caption=None):
    """A framed screenshot/preview image, with an optional caption line."""
    caption_html = f'<div class="doc-image-caption">{caption}</div>' if caption else ""
    return f'''
<div class="doc-image-frame">
  <img class="doc-image" src="{src}" alt="{alt}" loading="lazy">
  {caption_html}
</div>
'''


class Site:
    def __init__(self, out_dir, site_slug, site_name, storage_key,
                 repo_url, modrinth_url, version, nav_groups,
                 logo_path, logo_alt):
        self.out_dir = out_dir
        self.site_slug = site_slug
        self.site_name = site_name
        self.storage_key = storage_key
        self.repo_url = repo_url
        self.modrinth_url = modrinth_url
        self.version = version
        self.nav_groups = nav_groups
        self.logo_path = logo_path
        self.logo_alt = logo_alt

        os.makedirs(self.out_dir, exist_ok=True)
        self._copy_assets()

    def _copy_assets(self):
        # BASE_DIR/assets -> out_dir/assets (style.css, app.js, img/*)
        base_dir = os.path.dirname(os.path.abspath(self.out_dir))
        src = os.path.join(base_dir, "assets")
        dst = os.path.join(self.out_dir, "assets")
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            self._strip_homepage_only_css(os.path.join(dst, "style.css"))

    @staticmethod
    def _strip_homepage_only_css(css_path):
        # The root stylesheet also carries homepage-grid rules (.home-main,
        # .home-content, etc.) that don't apply inside a plugin subsite.
        if not os.path.isfile(css_path):
            return
        with open(css_path, "rb") as f:
            data = f.read()
        marker = b"/* ---------- homepage-only layout (no sidebar) ---------- */"
        idx = data.find(marker)
        if idx == -1:
            return
        # Trim from the marker (and the blank line right before it) to EOF,
        # preserving the file's existing line-ending convention (this
        # stylesheet uses CRLF throughout, unlike the generated HTML).
        head = data[:idx].rstrip(b"\r\n")
        with open(css_path, "wb") as f:
            f.write(head + b"\n")

    def _nav_href(self, prefix, target_slug):
        path = "" if target_slug == "index" else f"{target_slug}/"
        href = prefix + path
        return href if href else "./"

    def _render_nav(self, prefix, current_slug):
        groups_html = []
        for label, entries in self.nav_groups:
            links = []
            for slug, title in entries:
                href = self._nav_href(prefix, slug)
                active = 'class="active"' if slug == current_slug else ""
                links.append(f'<a href="{href}" {active}><span class="dot"></span>{title}</a>')
            groups_html.append(
                f'<div class="sidebar-group"><div class="sidebar-label">{label}</div>'
                f'<nav>\n' + "\n".join(links) + "\n</nav></div>"
            )
        return "\n".join(groups_html)

    def _render_prev_next(self, prefix, prev, nxt):
        if prev:
            slug, title = prev
            prev_html = (f'<a class="pn-link pn-prev" href="{self._nav_href(prefix, slug)}">'
                         f'<div class="pn-dir">&larr; Previous</div>'
                         f'<div class="pn-title">{title}</div></a>')
        else:
            prev_html = "<div></div>"

        if nxt:
            slug, title = nxt
            next_html = (f'<a class="pn-link pn-next" href="{self._nav_href(prefix, slug)}">'
                        f'<div class="pn-dir">Next &rarr;</div>'
                        f'<div class="pn-title">{title}</div></a>')
        else:
            next_html = "<div></div>"

        return f'<div class="prev-next">{prev_html}{next_html}</div>'

    def page(self, slug, page_title, category, meta_description, content_html,
             prev=None, nxt=None):
        depth = 0 if slug == "index" else 1
        prefix = "" if depth == 0 else "../"
        home_prefix = prefix + "../"

        logo_href = prefix + self.logo_path
        brand_href = self._nav_href(prefix, "index")
        nav_html = self._render_nav(prefix, slug)
        prev_next_html = self._render_prev_next(prefix, prev, nxt)

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title} &middot; {self.site_name} Docs</title>
<meta name="description" content="{meta_description}">
<script>
(function(){{
  try {{
    var t = localStorage.getItem('{self.storage_key}');

    if (t !== 'light' && t !== 'dark') {{
      t = window.matchMedia &&
          window.matchMedia('(prefers-color-scheme: light)').matches
        ? 'light'
        : 'dark';
    }}

    document.documentElement.setAttribute('data-theme', t);
    document.documentElement.setAttribute('data-toggle-state', t);
  }} catch(e) {{}}
}})();
</script>
<link rel="icon" href="{logo_href}">
{FONT_LINKS}
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="topbar topbar-doc">
  <div class="topbar-inner">
    <button class="menu-btn" aria-label="Toggle navigation">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 4h14M2 9h14M2 14h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>

    <a class="afx-home-link" href="{home_prefix}">
      <img src="{prefix}assets/img/afx-mark.png" alt="AFXPlugins">
      <span class="afx-home-text">AFXPlugins</span>
    </a>
    <span class="afx-sep">/</span>

    <a class="brand" href="{brand_href}">
      <img class="brand-mark" src="{logo_href}" alt="{self.logo_alt}">
      <span class="brand-label">{self.site_name}</span>
    </a>

    <span class="version-badge">v{self.version}</span>

    <div class="topbar-links">
      <a class="icon-link" href="{self.modrinth_url}" target="_blank" rel="noopener">
        <span class="link-text">Modrinth</span>
      </a>

      <a class="icon-link" href="{self.repo_url}" target="_blank" rel="noopener">
        <span class="link-text">GitHub</span>
      </a>

      {THEME_TOGGLE}
    </div>
  </div>
</header>
<div class="shell">
  <aside class="sidebar">
    {nav_html}
  </aside>
  <main>
    <div class="content">
      <span class="eyebrow">{category}</span>
      {content_html}
      {prev_next_html}
      <footer class="page-footer">
        <span>{self.site_name} v{self.version} &middot; by <a href="{home_prefix}">AFXPlugins</a></span>
        <span><a href="{self.repo_url}" target="_blank" rel="noopener">Source on GitHub</a></span>
      </footer>
    </div>
  </main>
</div>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
'''

        page_dir = self.out_dir if slug == "index" else os.path.join(self.out_dir, slug)
        os.makedirs(page_dir, exist_ok=True)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
