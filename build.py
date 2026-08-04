#!/usr/bin/env python3
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))


def href_to(current_slug, target_slug):
    """Relative href from one generated page to another.

    Every page (including sub-pages) now lives one level deep at
    /<slug>/index.html, so this is a flat, single-level structure.
    """
    if target_slug == "index":
        if current_slug == "index":
            return "./"
        return "../"

    if current_slug == "index":
        return f"{target_slug}/"

    return f"../{target_slug}/"


def asset_path(current_slug, path):
    """Relative path to an assets/ file from the page being rendered."""
    return path if current_slug == "index" else f"../{path}"
REPO_URL = "https://github.com/AFXPlugins/CustomPlayerNametags"
MODRINTH_URL = "https://modrinth.com/plugin/customplayernametags"
VERSION = "1.0.0"

# The theme is a simple two-state Light/Dark slider toggle. On a visitor's
# very first visit (nothing saved yet) the page follows their OS/browser
# color-scheme preference (prefers-color-scheme) automatically, with no
# data-theme attribute set — that's what THEME_STORAGE_KEY absence means.
# The instant the visitor flips the slider, that explicit choice is saved
# under THEME_STORAGE_KEY and takes over from then on, on every page.
THEME_STORAGE_KEY = "customplayernametags-theme"

THEME_SWITCHER = '''<button class="theme-toggle" type="button" role="switch" aria-label="Switch between light and dark mode" data-theme-toggle>
    <span class="theme-toggle-track">
      <svg class="theme-toggle-icon theme-toggle-icon-sun" width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="3" stroke="currentColor" stroke-width="1.2"/><path d="M6.5 0.6v1.6M6.5 10.8v1.6M12.4 6.5h-1.6M2.2 6.5H0.6M10.6 2.4l-1.1 1.1M3.5 9.5l-1.1 1.1M10.6 10.6l-1.1-1.1M3.5 3.5L2.4 2.4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
      <svg class="theme-toggle-icon theme-toggle-icon-moon" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M11 7.6A5 5 0 114.4 1a4 4 0 006.6 6.6z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
      <span class="theme-toggle-thumb"></span>
    </span>
  </button>'''

NO_FLASH_SCRIPT = f'''<script>
(function(){{
  try {{
    var t = localStorage.getItem('{THEME_STORAGE_KEY}');
    if (t === 'light' || t === 'dark') {{
      document.documentElement.setAttribute('data-theme', t);
    }}

    document.documentElement.setAttribute(
      'data-toggle-state',
      t === 'light' ? 'light' : 'dark'
    );
  }} catch(e) {{}}
}})();
</script>'''

NAV = [
    ("index", "Overview", []),
    ("installation", "Installation", []),
    ("configuration", "Configuration", []),
    ("commands", "Commands", []),
    ("permissions", "Permissions", []),
    ("formatting", "Nametag Formats", []),
    ("troubleshooting", "Troubleshooting", []),
    ("changelog", "Changelog", []),
]

BRAND_SVG = '''<img class="brand-mark" src="assets/img/logo.png" alt="CustomPlayerNametags logo">'''


def nav_html(active_slug):
    groups = {
        "Getting Started": ["index", "installation"],
        "Guides": ["formatting", "configuration"],
        "Reference": ["commands", "permissions"],
        "Resources": ["troubleshooting", "changelog"],
    }
    out = []
    for label, slugs in groups.items():
        out.append(f'<div class="sidebar-group"><div class="sidebar-label">{label}</div><nav>')
        for slug in slugs:
            title = dict((s, t) for s, t, _ in NAV)[slug]
            cls = " active" if slug == active_slug else ""
            out.append(f'<a href="{href_to(active_slug, slug)}" class="link{cls}"><span class="dot"></span>{title}</a>')
        out.append('</nav></div>')
    return "\n".join(out)


def page(slug, title, eyebrow, description, content, prev=None, nxt=None):
    active_cls_js = ""
    prevnext = ""
    if prev or nxt:
        prev_html = ""
        next_html = ""
        if prev:
            p_slug, p_title = prev
            prev_html = f'<a class="pn-link pn-prev" href="{href_to(slug, p_slug)}"><div class="pn-dir">&larr; Previous</div><div class="pn-title">{p_title}</div></a>'
        else:
            prev_html = '<div></div>'
        if nxt:
            n_slug, n_title = nxt
            next_html = f'<a class="pn-link pn-next" href="{href_to(slug, n_slug)}"><div class="pn-dir">Next &rarr;</div><div class="pn-title">{n_title}</div></a>'
        else:
            next_html = '<div></div>'
        prevnext = f'<div class="prev-next">{prev_html}{next_html}</div>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · CustomPlayerNametags Docs</title>
<meta name="description" content="{description}">
{NO_FLASH_SCRIPT}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,1..1000&family=Merriweather+Sans:ital,wght@0,300..800;1,300..800&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset_path(slug, 'assets/style.css')}">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <button class="menu-btn" aria-label="Toggle navigation">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 4h14M2 9h14M2 14h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>

    <a class="brand" href="{href_to(slug, 'index')}">
      {BRAND_SVG.replace('assets/img/logo.png', asset_path(slug, 'assets/img/logo.png'))}
      CustomPlayerNametags
    </a>

    <span class="version-badge">v{VERSION}</span>

    <div class="topbar-links">
      <a class="icon-link" href="{MODRINTH_URL}" target="_blank" rel="noopener">
        <span class="link-text">Modrinth</span>
      </a>

      <a class="icon-link" href="{REPO_URL}" target="_blank" rel="noopener">
        <span class="link-text">GitHub</span>
      </a>

      {THEME_SWITCHER}
    </div>
  </div>
</header>
<div class="shell">
  <aside class="sidebar">
    {nav_html(slug)}
  </aside>
  <main>
    <div class="content">
      <span class="eyebrow">{eyebrow}</span>
      {content}
      {prevnext}
      <footer class="page-footer">
        <span>CustomPlayerNametags v{VERSION} &middot; by AFXPlugins</span>
        <span><a href="{REPO_URL}" target="_blank" rel="noopener">Source on GitHub</a></span>
      </footer>
    </div>
  </main>
</div>
<script src="{asset_path(slug, 'assets/app.js')}"></script>
</body>
</html>
'''
    # fix active class targeting (we used generic "link" class + active, but CSS expects nav a + .active)
    html = html.replace('class="link active"', 'class="active"').replace('class="link"', '')
    if slug == "index":
      output_file = os.path.join(OUT, "index.html")
    else:
        page_dir = os.path.join(OUT, slug)
        os.makedirs(page_dir, exist_ok=True)
        output_file = os.path.join(page_dir, "index.html")

    # Always overwrite existing files
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_file}")


def callout(title, body, kind=""):
    cls = f"callout {kind}".strip()
    return f'<div class="{cls}"><span class="callout-title">{title}</span><p>{body}</p></div>'


def code(lang, text, copy=True):
    btn = '<button class="copy-btn">copy</button>' if copy else ''
    return f'<div class="code-block"><pre><code class="lang-{lang}">{text}</code></pre>{btn}</div>'

def doc_image(src, alt, caption=None):
    caption_html = ""
    if caption:
        caption_html = f'<div class="doc-image-caption">{caption}</div>'

    return f'''
<div class="doc-image-frame">
  <img class="doc-image" src="{src}" alt="{alt}" loading="lazy">
  {caption_html}
</div>
'''


print("template ready")

# =========================================================================
# INDEX
# =========================================================================
index_content = f'''
<h1>CustomPlayerNametags</h1>
<p class="lede">A Paper plugin that lets you fully customize player nametags. Includes global formats, individual player formats, PlaceholderAPI support, and Bedrock compatibility.</p>
<div class="hero-buttons">
  <a class="btn btn-primary" href="{MODRINTH_URL}/versions" target="_blank" rel="noopener">Download</a>
  <a class="btn btn-ghost" href="{REPO_URL}" target="_blank" rel="noopener">View source</a>
</div>

{doc_image(
    "https://cdn.modrinth.com/data/cached_images/4314f862fdfff9a0d958a8ce345277d51b429140.png",
    "Preview of a custom player nametag."
)}

<h2 class="no-rule">What it does</h2>
<div class="grid grid-2">
  <div class="card"><h3>Fully custom nametags</h3><p>Replace the entire vanilla player nametag display entirely with a custom format using PlaceholderAPI placeholders.</p></div>
  <div class="card"><h3>Global + individual player formats</h3><p>Set one global <code>nametag-format</code> as a default format for the whole server. Additionally set custom formats for individual players.</p></div>
</div>

<h2>Requirements</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Dependency</th><th>Role</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><a href="https://modrinth.com/plugin/packetevents" target="_blank" rel="noopener">PacketEvents</a> <span class="tag req">required</span></td><td>Core packet handling</td><td>Allows editing nametag packets&mdash; the plugin will not work without it.</td></tr>
<tr><td><a href="https://modrinth.com/plugin/placeholderapi" target="_blank" rel="noopener">PlaceholderAPI</a> <span class="tag opt">strongly advised</span></td><td>Placeholder resolution</td><td>Not required for the plugin to load, but all <code>%placeholder%</code> values in any nametag formats will not be resolved without it.</td></tr>
</tbody>
</table>
</div>

<h2>Explore the Docs</h2>
<div class="grid grid-3">
  <a class="card" href="installation"><span class="card-icon">01</span><h3>Installation</h3><p>Install the plugin, dependencies, and verify everything is working.</p></a>
  <a class="card" href="formatting"><span class="card-icon">02</span><h3>Nametag Formats</h3><p>Learn how to format and customize nametags.</p></a>
  <a class="card" href="configuration"><span class="card-icon">03</span><h3>Configuration</h3><p>Guide on customizing settings, messages, and player formats.</p></a>
  <a class="card" href="commands"><span class="card-icon">04</span><h3>Commands</h3><p>View all <code>/nametags</code> commands and how to use them.</p></a>
  <a class="card" href="permissions"><span class="card-icon">05</span><h3>Permissions</h3><p>Manage access to plugin commands and features.</p></a>
  <a class="card" href="troubleshooting"><span class="card-icon">06</span><h3>Troubleshooting</h3><p>Troubleshooting tips for common plugin issues.</p></a>
</div>
'''
page("index", "Overview", "Documentation",
     "Documentation for CustomPlayerNametags.",
     index_content, nxt=("installation", "Installation"))


# =========================================================================
# INSTALLATION
# =========================================================================
installation_content = f'''
<h1>Installation</h1>
<p class="lede">Follow this guide to install CustomPlayerNametags</p>

<h2 class="no-rule">1. Install dependencies</h2>
<p>Download the following plugins and move them into <code>/plugins</code>:</p>
<div class="table-wrap">
<table>
<thead><tr><th>Plugin</th><th>Why</th></tr></thead>
<tbody>
<tr><td><a href="https://modrinth.com/plugin/packetevents" target="_blank" rel="noopener">PacketEvents</a> <span class="tag req">required</span></td><td>It allows the plugin to hide vanilla nametags and control them individually for each viewer by sending raw team packets directly to clients, something Bukkit's Scoreboard API cannot do.</td></tr>
<tr><td><a href="https://modrinth.com/plugin/placeholderapi" target="_blank" rel="noopener">PlaceholderAPI</a> <span class="tag opt">strongly advised</span></td><td>Allows parsing placeholders in the nametag format. Required for the global format to work, but individual player formats will still work without it.</td></tr>
</tbody>
</table>
</div>

<h2>2. Add the plugin</h2>
<ol>
<li>Download <a href="{MODRINTH_URL}/versions" target="_blank" rel="noopener"><code>CustomPlayerNametags</code></a>.</li>
<li>Place it in your server's <code>/plugins</code> folder, alongside PacketEvents and PlaceholderAPI.</li>
<li>Start the server.</li>
</ol>

<h2>3. Verify it loaded</h2>
<p>On startup, check your console for:</p>
{code("text", "[CustomPlayerNametags] CustomPlayerNametags enabled.")}
{callout("Troubleshooting", "If instead you see the server refuse to load the plugin, make sure the latest version of PacketEvents is installed. If it still doesn't work, see <a href='../troubleshooting/'>Troubleshooting</a>.")}
<p>Once enabled, it will generate three files in <code>/plugins/CustomPlayerNametags/</code>:</p>
<div class="table-wrap">
<table>
<thead><tr><th>File</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>config.yml</code></td><td>Used for editing the CustomPlayerNametags configuration.</td></tr>
<tr><td><code>messages.yml</code>*</td><td>Stores all plugin messages.</td></tr>
<tr><td><code>player-formats.yml</code>*</td><td>Stores individual player formats.</td></tr>
</tbody>
</table>
</div>
{callout("", "*messages.yml and player-formats.yml can be ignored as they only serve as storage for the plugin.")}
<p>Full breakdown of each file is on the <a href="../configuration/">Configuration</a> page.</p>
'''
page("installation", "Installation", "Getting started",
     "How to install CustomPlayerNametags and its dependencies.",
     installation_content, prev=("index", "Overview"), nxt=("formatting", "Nametag Formats"))


# =========================================================================
# CONFIGURATION
# =========================================================================
config_yaml_code = '''<span class="tok-com"># Global format used for all player nametags.</span>
<span class="tok-com"># Supports PlaceholderAPI placeholders and &#39;&amp;&#39; colors.</span>
<span class="tok-com"># Use \\n in the format to start a new line.</span>
<span class="tok-com"># Default: %player_name%</span>
<span class="tok-key">nametag-format:</span> <span class="tok-str">"%player_name%"</span>

<span class="tok-com"># NONE | AUTO | MANUAL &mdash; see below</span>
<span class="tok-key">nametag-dismount-mode:</span> AUTO

<span class="tok-com"># MANUAL mode only. Commands (no leading slash) that dismount the tag.</span>
<span class="tok-key">dismount-commands:</span>
  - examplecommand1
  - examplecommand2

<span class="tok-com"># How long (in ticks) the tag stays dismounted. Default: 5</span>
<span class="tok-key">dismount-duration-ticks:</span> 5

<span class="tok-com"># Maximum render distance for nametags. Default: 64 (vanilla&#39;s own value)</span>
<span class="tok-key">nametag-render-distance:</span> 64
'''

configuration_content = f'''
<h1>Configuration</h1>
<p class="lede">Guide on configuring CustomPlayerNametags.</p>

<h2 class="no-rule">config.yml</h2>
<p>Reload any change with <a href="../commands/"><code>/nametags reload</code></a>.</p>
<div class="code-block"><pre><code>{config_yaml_code}</code></pre><button class="copy-btn">copy</button></div>

<h3>nametag-format</h3>
<p>The global format applied to every player who doesn't have a custom individual format. More information is covered on the <a href="../formatting/">Nametag Formats</a> page.</p>

<h3>nametag-dismount-mode</h3>
<p>The nametag is attached to each player using an invisible passenger entity so it stays fixed above their head. Some teleport commands that move a player between worlds/dimensions can fail while that passenger is still attached. This setting controls the feature that temporarily detaches and reattaches the nametag to solve this issue.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Mode</th><th>Behavior</th></tr></thead>
<tbody>
<tr><td><code>NONE</code></td><td>Never automatically dismounts the nametag.</td></tr>
<tr><td><code>AUTO</code> <em>(default)</em></td><td>Dismounts the nametag on every command the player runs.</td></tr>
<tr><td><code>MANUAL</code></td><td>Only dismounts the nametag when the command matches an entry in <code>dismount-commands</code>.</td></tr>
</tbody>
</table>
</div>
{callout("Direct teleport handling", "Regardless of mode (as long as it isn't <code>NONE</code>), the plugin also dismounts on any <code>PlayerTeleportEvent</code> &mdash; nether/end portals, and other plugins calling the teleport API directly &mdash; not just typed commands. The tag remounts automatically the moment the world change actually happens, or when <code>dismount-duration-ticks</code> expires, whichever comes first.")}
<p>Picking a mode:</p>
<ul>
<li>No world-management plugin? Use <code>NONE</code>.</li>
<li>Using Multiverse-Core? Use <code>NONE</code> here, and set <code>passenger-mode</code> to <code>dismount_passengers</code> in Multiverse-Core's own config.</li>
<li>Using a different world/teleport plugin? Use <code>MANUAL</code> and list its teleport commands in <code>dismount-commands</code>.</li>
<li>Using Skript? Run <code>/nametags dismount &lt;player&gt;</code> from console before a cross-world teleport &mdash; see the <a href="../commands/#dismount">dismount command</a>.</li>
</ul>
{callout("AUTO", "It is recommended to not leave <code>nametag-dismount-mode</code> as <code>AUTO</code> because of minor visual bugs that can occur on commands that don't involve world changes.")}

<h3>dismount-commands</h3>
<p><code>MANUAL</code> mode only. One command per line, no leading slash.</p> 

<h3>dismount-duration-ticks</h3>
<p>How long (in ticks) a dismounted nametag stays detached before automatically remounting. Defaults at <code>5</code> ticks. You generally shouldn't need to raise this. <code>2</code> ticks is the lowest value that will work, so the value is set to <code>1</code> or lower, the plugin falls back to <code>2</code> ticks internally.</p>

<h3>nametag-render-distance</h3>
<p>Maximum distance (in blocks) at which the nametag renders for other players. Defaults to <code>64</code>, matching vanilla's own fixed nametag cutoff regardless of your server's entity-tracking-range settings.</p>

{callout("plugin-version", "config.yml also contains a <code>plugin-version</code> key used internally to migrate the file across updates. Leave it as-is.")}
<hr>
<br>
{callout("Extra Plugin Files", "The following sections describe the other two files generated by the plugin. These files don't need to be edited manually, but feel free to read how they work!" )}
<h2>messages.yml</h2>
<p>Contains all messages used by the plugin.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Key</th><th>Sent when...</th></tr></thead>
<tbody>
<tr><td><code>no-permission</code></td><td>Sender lacks the admin permission.</td></tr>
<tr><td><code>reload-success</code></td><td><code>/nametags reload</code> completes.</td></tr>
<tr><td><code>player-not-found</code></td><td>A named target player isn't online.</td></tr>
<tr><td><code>console-only</code></td><td>A player tries a console-only subcommand.</td></tr>
<tr><td><code>dismount-usage</code></td><td>The <code>dismount</code> console command is used incorrectly.</td></tr>
<tr><td><code>update-checking</code> / <code>update-check-failed</code> / <code>update-available</code> / <code>update-up-to-date</code></td><td><code>/nametags update</code> is run.</td></tr>
<tr><td><code>op-update-notice</code></td><td>An OP joins while an update is available.</td></tr>
<tr><td><code>format-view-*</code>, <code>format-set-*</code>, <code>format-reset-*</code></td><td>A <code>/nametags format</code> command is run.</td></tr>
<tr><td><code>usage-top-level</code>, <code>usage-format</code>, <code>usage-format-view</code>, <code>usage-format-set</code>, <code>usage-format-reset</code></td><td>A command is run with missing or invalid arguments.</td></tr>
</tbody>
</table>
</div>

<h2>player-formats.yml</h2>
<p>Stores each individual player nametag formats keyed by player UUID.</p>
{code("yaml", '''formats:
  069a79f4-44e9-4726-a5be-fca90e38aaf5: '&f%player_name%'
  ec561538-f3fd-461d-aff5-086b6a97e6f8: '%luckperms_prefix%%player_name%' ''')}
'''
page("configuration", "Configuration", "Guide",
     "Guide on configuring CustomPlayerNametags..",
     configuration_content, prev=("formatting", "Nametag Formats"), nxt=("commands", "Commands"))


# =========================================================================
# COMMANDS
# =========================================================================
commands_content = f'''
<h1>Commands</h1>
<p class="lede">All CustomPlayerNametags commands are under <code>/nametags</code> (alias <code>/customplayernametags</code>). All commands require the admin permission &mdash; see <a href="../permissions/">Permissions</a>.</p>

<h2 class="no-rule">Top level</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>/nametags reload</code></td><td>Reloads config.yml, messages.yml, and refreshes every online player's nametag.</td></tr>
<tr><td><code>/nametags update</code></td><td>Runs a fresh check against the plugin's Modrinth project and reports whether a newer <em>release</em>-type version is available. Pre-release/beta versions are ignored.</td></tr>
<tr><td><code>/nametags format ...</code></td><td>Manage nametag formats &mdash; see below.</td></tr>
</tbody>
</table>
</div>
{callout("Automatic update checks", "The plugin also checks Modrinth for a newer version once automatically on startup, and messages any OP who joins afterward if that check found a newer version.")}

<h2 id="format"> format &mdash; view / set / reset</h2>
<p>Every <code>format</code> subcommand branches on a target: <code>global</code> (the server-wide format) or <code>player &lt;name&gt;</code> (a specific player's individual format).</p>

<h3 id="view">view</h3>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Shows</th></tr></thead>
<tbody>
<tr><td><code>/nametags format view global unparsed</code></td><td>The raw global format exactly as stored in config.yml &mdash; literal <code>&amp;</code> codes and placeholders are shown.</td></tr>
<tr><td><code>/nametags format view global parsed &lt;player&gt;</code></td><td>The global format resolved through PlaceholderAPI using <code>&lt;player&gt;</code> as context, with colors applied (what would actually be shown as the nametag).</td></tr>
<tr><td><code>/nametags format view player &lt;unparsed|parsed&gt; &lt;player&gt;</code></td><td>The format currently in effect for <code>&lt;player&gt;</code> &mdash; their personal format if set, otherwise the global format.</td></tr>
</tbody>
</table>
</div>

<h3 id="set">set</h3>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Effect</th></tr></thead>
<tbody>
<tr><td><code>/nametags format set global &lt;format&gt;</code></td><td>Updates <code>nametag-format</code> in config.yml and refreshes every online player who has no personal override.</td></tr>
<tr><td><code>/nametags format set player &lt;player&gt; &lt;format&gt;</code></td><td>Sets a personal override for <code>&lt;player&gt;</code>, saves to <code>player-formats.yml</code>, and refreshes their nametag.</td></tr>
</tbody>
</table>
</div>

<h3 id="reset">reset</h3>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Effect</th></tr></thead>
<tbody>
<tr><td><code>/nametags format reset global</code></td><td>Resets the global format back to the default (<code>%player_name%</code>) and refreshes every player without a personal override.</td></tr>
<tr><td><code>/nametags format reset player &lt;player&gt;</code></td><td>Clears <code>&lt;player&gt;</code>'s personal override, reverting them to the global format, and refreshes their nametag.</td></tr>
</tbody>
</table>
</div>

<h2 id="dismount">dismount &mdash; console only</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>/nametags dismount &lt;player&gt;</code></td><td>Manually dismounts a player's nametag for <code>dismount-duration-ticks</code>. Console-only, and works even if <code>nametag-dismount-mode</code> is <code>NONE</code>. Intended for use with Skript when scripting cross-world teleports.</td></tr>
</tbody>
</table>
</div>

'''
page("commands", "Commands", "Reference",
     "All CustomPlayerNametags commands.",
     commands_content, prev=("configuration", "Configuration"), nxt=("permissions", "Permissions"))


# =========================================================================
# PERMISSIONS
# =========================================================================
permissions_content = f'''
<h1>Permissions</h1>
<p class="lede">CustomPlayerNametags uses a single permission for all commands.</p>

<div class="table-wrap">
<table>
<thead><tr><th>Node</th><th>Default</th><th>Grants</th></tr></thead>
<tbody>
<tr><td><code>customplayernametags.admin</code></td><td><span class="tag op">op</span></td><td>Access to all <code>/nametags</code> subcommands.</td></tr>
</tbody>
</table>
</div>

'''
page("permissions", "Permissions", "Reference",
     "The customplayernametags.admin permission.",
     permissions_content, prev=("commands", "Commands"), nxt=("troubleshooting", "Troubleshooting"))


# =========================================================================
# FORMATTING
# =========================================================================
color_table_rows = "".join(
    f'<tr><td><code>&amp;{code}</code></td><td><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:{hexv};border:1px solid var(--border);vertical-align:middle;margin-right:0.5em;"></span>{name}</td></tr>'
    for code, hexv, name in [
        ("0", "#000000", "black"), ("1", "#0000AA", "dark blue"), ("2", "#00AA00", "dark green"), ("3", "#00AAAA", "dark aqua"),
        ("4", "#AA0000", "dark red"), ("5", "#AA00AA", "dark purple"), ("6", "#FFAA00", "gold"), ("7", "#AAAAAA", "gray"),
        ("8", "#555555", "dark gray"), ("9", "#5555FF", "blue"), ("a", "#55FF55", "green"), ("b", "#55FFFF", "aqua"),
        ("c", "#FF5555", "red"), ("d", "#FF55FF", "light purple"), ("e", "#FFFF55", "yellow"), ("f", "#FFFFFF", "white"),
    ]
)

formatting_content = f'''
<h1>Nametag Formats</h1>
<p class="lede">How to customize both global and individual player nametag formats.</p>

{doc_image(
    "https://cdn.modrinth.com/data/cached_images/4314f862fdfff9a0d958a8ce345277d51b429140.png",
    "Preview of a custom player nametag."
)}

<h2 class="no-rule">Global vs. individual formats</h2>
<p>There are two types of nametag formats in CustomPlayerNametags:</p>
<ol>
<li>Global &mdash; A universal format that is applied to all players by default. It can be set by either changing the <code>nametag-format</code> in config.yml, or by using the <a href="../commands/#format">command</a>.</li>
<li>Individual &mdash; A format that is specific to a single player. It can only be set by using the <a href="../commands/#format">command</a>.</li>
</ol>
{callout("Format Priority", "An individual format will always override the global format for that player.")}

<h2>Placeholders</h2>
<p>Any PlaceholderAPI placeholder can be used in a nametag format string. A couple of common examples:</p>
{code("text", "%player_name%          the player's username\n%luckperms_prefix%      the player's LuckPerms prefix\n%essentials_nickname%   the player's Essentials nickname")}
<p>See the <a href="https://wiki.placeholderapi.com/users/using-placeholders/" target="_blank" rel="noopener">PlaceholderAPI placeholder guide</a> for the full syntax and how to properly use them. Without PlaceholderAPI installed, placeholders are left as literal text rather than being resolved.</p>

<h2>CustomPlayerNametags placeholders</h2>
<p>CustomPlayerNametags also registers its own PlaceholderAPI expansion placeholders, allowing other plugins that support PlaceholderAPI to utilize the same format without needing to duplicate it.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Placeholder</th><th>Returns</th></tr></thead>
<tbody>
<tr><td><code>%customplayernametags_format%</code></td><td>The format currently in effect for the requesting player &mdash; their individual nametag if one exists, otherwise the global <code>nametag-format</code> from <code>config.yml</code>.</td></tr>
<tr><td><code>%customplayernametags_format_global%</code></td><td>The global <code>nametag-format</code> from config.yml.</td></tr>
</tbody>
</table>
</div>
{callout("Example Plugin Integration", "One use case for these placeholders is with the AFXPlugins plugin, <a href=\"https://modrinth.com/plugin/customadvancementmessages\" target=\"_blank\" rel=\"noopener\">CustomAdvancementMessages</a>. By using one of these placeholders in the CustomAdvancmentMessages <code>player-name-format</code> config option, you can reuse the same format across both plugins without needing to duplicate it.")}

<h2 id="multiple-lines">Multiple lines</h2>
<p>Put <code>\\n</code> anywhere in a format to start a new line:</p>
{code("text", "%luckperms_prefix%&e%essentials_nickname%\\n&6(&b%player_name%&6)")}
{doc_image(
    "../assets/img/image1.png",
    "Preview of multi-line nametag format.",
    "Example output from format listed above."
)}
<p>This works with both global and individual nametag formats, and there is no limit to the number of lines you can create.</p>

<h2 class="no-rule">Color and style codes</h2>
<p>Key for all Minecraft '&' color and style codes:</p>
<div class="table-wrap">
<table><thead><tr><th>Code</th><th>Color</th></tr></thead><tbody>{color_table_rows}</tbody></table>
</div>
<div class="table-wrap">
<table>
<thead><tr><th>Code</th><th>Style</th></tr></thead>
<tbody>
<tr><td><code>&amp;l</code></td><td><strong>bold</strong></td></tr>
<tr><td><code>&amp;o</code></td><td><i>italic</i></td></tr>
<tr><td><code>&amp;n</code></td><td><u>underline</u></td></tr>
<tr><td><code>&amp;m</code></td><td><s>strikethrough</s></td></tr>
<tr><td><code>&amp;r</code></td><td>reset color and styles</td></tr>
</tbody>
</table>
</div>

<h2>How often it refreshes</h2>
<p>Nametags automatically refresh once per second for every online player, so placeholders that change over time stay up to date without needing a manual reload.</p>
'''
page("formatting", "Nametag Formats", "Guide",
     "How to format player nametags in CustomPlayerNametags.",
     formatting_content, prev=("installation", "Installation"), nxt=("configuration", "Configuration"))


# =========================================================================
# CROSS-PLAY
# =========================================================================
crossplay_content = f'''
<h1>Bedrock &amp; Cross-Play</h1>
<p class="lede">CustomPlayerNametags works for both Java Edition players, and Bedrock players connecting through Geyser.</p>

<h2 class="no-rule">How Bedrock players are detected</h2>
<p>If a plugin named <code>floodgate</code> is installed and enabled, CustomPlayerNametags asks its API whether each connected player is a Floodgate (Bedrock) player. If Floodgate isn't installed, every player is simply treated as Java.</p>

<h2>Why Bedrock needs a different offset</h2>
<p>The nametag is a display entity mounted above the player as a passenger, positioned at a fixed height offset. Geyser's client-side handling of passenger/display-entity positioning doesn't line up the same with vanilla Java rendering, so the plugin applies a small additional correction specifically for viewers detected as Bedrock, so the tag sits at the same visual height it would on Java.</p>

<h2>Dismount windows</h2>
<p>The brief window where a tag is dismounted and remounted around a teleport (see <a href="../configuration/">nametag-dismount-mode</a>) also gets its own small Bedrock-only height correction, so the remount doesn't produce a visible flicker for Bedrock viewers.</p>

'''
page("cross-play", "Bedrock & Cross-Play", "Resource",
     "How CustomPlayerNametags detects Bedrock/Geyser players.",
     crossplay_content, prev=("troubleshooting", "Troubleshooting"))


# =========================================================================
# TROUBLESHOOTING
# =========================================================================
troubleshooting_content = f'''
<h1>Troubleshooting</h1>
<p class="lede">Common issues and how to fix them.</p>

<h2 class="no-rule">Plugin won't enable</h2>
<p>Check your console for a message about a missing dependency. <code>PacketEvents</code> is a required dependency &mdash; if it isn't installed and enabled, CustomPlayerNametags won't start.</p>

<h2>Placeholders show up as literal text</h2>
<p>If placeholders appear unparsed above a player's head instead of resolving, PlaceholderAPI either isn't installed, isn't enabled, or doesn't have the specific expansion registered (e.g. the LuckPerms expansion for <code>%luckperms_prefix%</code>). Make sure PlaceholderAPI is installed and that there are no errors in the console. Next check your placeholder with <code>/papi parse &lt;username&gt; &lt;placeholder&gt;</code> in-game to confirm PlaceholderAPI itself can resolve it.</p>

<h2>Cross-world teleportation not working</h2>
<p>The tag is a passenger entity, and cross-world/dimension teleport commands can fail while it's still attached. This is exactly what <code>nametag-dismount-mode</code> exists to solve &mdash; see the full explanation on the <a href="../configuration/">Configuration</a> page.</p>

<h2>Tag height looks slightly off for Bedrock players</h2>
<p>Confirm Floodgate is installed and enabled &mdash; that's how the plugin tells Bedrock viewers apart from Java oness. See <a href="../cross-play/">Bedrock &amp; Cross-Play</a>.</p>

<h2>Nametag not visible</h2>
<ul>
<li>Confirm PacketEvents is actually enabled (not just installed) &mdash; check its own console output on startup.</li>
<li>Try <code>/nametags reload</code>, then have the player rejoin.</li>
</ul>
<hr>
{callout("Still stuck?", "Submit an <a href=\"{REPO_URL}/issues\" target=\"_blank\" rel=\"noopener\">issue</a> on the CustomPlayerNametags GitHub repository and include details about the problem and how to reproduce it.")}

'''
page("troubleshooting", "Troubleshooting", "Resource",
     "Fixes for common CustomPlayerNametags problems.",
     troubleshooting_content, prev=("permissions", "Permissions"), nxt=("changelog", "Changelog"))


# =========================================================================
# CHANGELOG
# =========================================================================
changelog_content = f'''
<h1>Changelog</h1>
<p class="lede">Notable changes to CustomPlayerNametags, newest first.</p>

<div class="changelog">

<div class="changelog-entry">
<div class="changelog-heading"><span class="changelog-version">1.0.0</span></div>
<ul>
<li><strong>New:</strong> initial release.</li>
</ul>
</div>

</div>
'''
page("changelog", "Changelog", "Resource",
     "What's changed in CustomPlayerNametags.",
     changelog_content, prev=("troubleshooting", "Troubleshooting"))

print("All pages generated.")