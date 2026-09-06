#!/usr/bin/env python3
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from common import Site, callout, code, doc_image

OUT = os.path.join(BASE_DIR, "customadvancementmessages")

REPO_URL = "https://github.com/AFXPlugins/CustomAdvancementMessages"
MODRINTH_URL = "https://modrinth.com/plugin/customadvancementmessages"
VERSION = "1.0.2"

NAV = [
    ("Getting Started", [("index", "Overview"), ("installation", "Installation")]),
    ("Guides", [("configuration", "Configuration"), ("placeholders", "Placeholders & Colors")]),
    ("Reference", [("commands", "Commands"), ("permissions", "Permissions")]),
    ("Resources", [("troubleshooting", "Troubleshooting"), ("changelog", "Changelog")]),
]

site = Site(
    out_dir=OUT,
    site_slug="customadvancementmessages",
    site_name="CustomAdvancementMessages",
    storage_key="afxplugins-theme",
    repo_url=REPO_URL,
    modrinth_url=MODRINTH_URL,
    version=VERSION,
    nav_groups=NAV,
    logo_path="assets/img/logo-advancements.png",
    logo_alt="CustomAdvancementMessages logo",
)

PREVIEW_IMG = "https://cdn.modrinth.com/data/cached_images/1b94b374acb542b59663a5edbfbb67882336817c.png"

# =========================================================================
# INDEX
# =========================================================================
index_content = f'''
<h1>CustomAdvancementMessages</h1>
<p class="lede">A Paper plugin that allows full customization of advancement messages. Includes PlaceholderAPI integration to allow customizing the player name in advancement messages.</p>
<div class="hero-buttons">
  <a class="btn btn-primary" href="{MODRINTH_URL}/versions" target="_blank" rel="noopener">Download</a>
  <a class="btn btn-ghost" href="{REPO_URL}" target="_blank" rel="noopener">View source</a>
</div>

{doc_image(PREVIEW_IMG, "Preview of a customized advancement message.")}
<h2 class="no-rule">What it does</h2>
<div class="grid grid-2">
  <div class="card"><h3>Custom player names</h3><p>Create a global format with any PlaceholderAPI placeholder to show custom names instead of the player's raw username in advancement messages.</p></div>
  <div class="card"><h3>Custom phrases &amp; colors</h3><p>Individually customize the phrase and color for all three advancement message types.</p></div>
</div>

<h2>Requirements</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Dependency</th><th>Role</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><a href="https://modrinth.com/plugin/packetevents" target="_blank" rel="noopener">PacketEvents</a> <span class="tag req">required</span></td><td>Core packet handling</td><td>Lets the plugin intercept and rewrite the advancement chat packet before it reaches players.</td></tr>
<tr><td><a href="https://modrinth.com/plugin/placeholderapi" target="_blank" rel="noopener">PlaceholderAPI</a> <span class="tag req">required</span></td><td>Placeholder resolution</td><td>Lets the plugin resolve <code>%placeholder%</code> values that are used in the <code>player-name-format</code>.</td></tr>
</tbody>
</table>
</div>

<h2>Explore the Docs</h2>
<div class="grid grid-3">
  <a class="card" href="installation"><span class="card-icon">01</span><h3>Installation</h3><p>Install the plugin, dependencies, and verify everything is working.</p></a>
  <a class="card" href="configuration"><span class="card-icon">02</span><h3>Configuration</h3><p>Set the player name format and per-type message phrases.</p></a>
  <a class="card" href="placeholders"><span class="card-icon">03</span><h3>Placeholders &amp; Colors</h3><p>Learn how placeholders, colors, and advancement types resolve.</p></a>
  <a class="card" href="commands"><span class="card-icon">04</span><h3>Commands</h3><p>View all <code>/advancements</code> commands and how to use them.</p></a>
  <a class="card" href="permissions"><span class="card-icon">05</span><h3>Permissions</h3><p>Manage access to plugin commands.</p></a>
  <a class="card" href="troubleshooting"><span class="card-icon">06</span><h3>Troubleshooting</h3><p>Troubleshooting tips for common plugin issues.</p></a>
</div>
'''
site.page("index", "Overview", "Documentation",
          "Documentation for CustomAdvancementMessages.",
          index_content, nxt=("installation", "Installation"))


# =========================================================================
# INSTALLATION
# =========================================================================
installation_content = f'''
<h1>Installation</h1>
<p class="lede">Follow this guide to install CustomAdvancementMessages.</p>

<h2 class="no-rule">1. Install dependencies</h2>
<p>Download the following plugins and move them into <code>/plugins</code>:</p>
<div class="table-wrap">
<table>
<thead><tr><th>Plugin</th><th>Why</th></tr></thead>
<tbody>
<tr><td><a href="https://modrinth.com/plugin/packetevents" target="_blank" rel="noopener">PacketEvents</a> <span class="tag req">required</span></td><td>Allows intercepting and editing the advancement messages before they reach players and needed for the plugin to function properly.</td></tr>
<tr><td><a href="https://modrinth.com/plugin/placeholderapi" target="_blank" rel="noopener">PlaceholderAPI</a> <span class="tag req">required</span></td><td>Allows resolving any placeholder used in <code>player-name-format</code>.</td></tr>
</tbody>
</table>
</div>

<h2>2. Add the plugin</h2>
<ol>
<li>Download <a href="{MODRINTH_URL}/versions" target="_blank" rel="noopener"><code>CustomAdvancementMessages</code></a>.</li>
<li>Place it in your server's <code>/plugins</code> folder, alongside PacketEvents and PlaceholderAPI.</li>
<li>Start the server.</li>
</ol>

<h2>3. Verify it loaded</h2>
<p>On startup, check your console for:</p>
{code("text", "[CustomAdvancementMessages] CustomAdvancementMessages enabled.")}
{callout("Troubleshooting", "If there is an error loading the plugin, make sure the latest version of PacketEvents is installed. If it still doesn't work, see <a href='../troubleshooting/'>Troubleshooting</a>.")}
<p>Once enabled, it will generate one file in <code>/plugins/CustomAdvancementMessages/</code>:</p>
<div class="table-wrap">
<table>
<thead><tr><th>File</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>config.yml</code></td><td>Used for editing the player name format and each advancement message.</td></tr>
</tbody>
</table>
</div>
'''
site.page("installation", "Installation", "Getting started",
          "How to install CustomAdvancementMessages and its dependencies.",
          installation_content, prev=("index", "Overview"), nxt=("configuration", "Configuration"))


# =========================================================================
# CONFIGURATION
# =========================================================================
config_yaml_code = '''<span class="tok-com"># Format for the player name in advancement messages.</span>
<span class="tok-com"># Supports any PlaceholderAPI placeholder, the built-in &#123;player&#125; placeholder</span>
<span class="tok-com"># (the player&#39;s username), and &#39;&amp;&#39; colors.</span>
<span class="tok-com"># Default: {player}</span>
<span class="tok-com"># Example: %luckperms_prefix%{player}</span>
<span class="tok-key">player-name-format:</span> <span class="tok-str">"{player}"</span>

<span class="tok-com"># Advancement message formats. Each phrase supports &#39;&amp;&#39; colors.</span>
<span class="tok-key">messages:</span>
    <span class="tok-key">task:</span>
        <span class="tok-key">phrase:</span> <span class="tok-str">"&amp;fhas made the advancement"</span>

    <span class="tok-key">goal:</span>
        <span class="tok-key">phrase:</span> <span class="tok-str">"&amp;fhas reached the goal"</span>

    <span class="tok-key">challenge:</span>
        <span class="tok-key">phrase:</span> <span class="tok-str">"&amp;fhas completed the challenge"</span>
'''

configuration_content = f'''
<h1>Configuration</h1>
<p class="lede">Guide on configuring CustomAdvancementMessages.</p>

<h2 class="no-rule">config.yml</h2>
<p>Reload any change with <a href="../commands/"><code>/advancements reload</code></a>.</p>
<div class="code-block"><pre><code>{config_yaml_code}</code></pre><button class="copy-btn">copy</button></div>

<h3>player-name-format</h3>
<p>The format used for a player's name in an advancement message. Supports any PlaceholderAPI placeholder, the built-in <code>{{player}}</code> placeholder (the player's username), and <code>&amp;</code> colors. See <a href="../placeholders/">Placeholders &amp; Colors</a> for more information.</p>

<h3>messages</h3>
<p>Individualy customize phrases for rach advancement type: &mdash; <code>task</code>, <code>goal</code>, and <code>challenge</code>.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Key</th><th>Purpose</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>messages.task.phrase</code></td><td>Shown for regular advancements.</td><td><code>&amp;fhas made the advancement</code></td></tr>
<tr><td><code>messages.goal.phrase</code></td><td>Shown for goal-type advancements.</td><td><code>&amp;fhas reached the goal</code></td></tr>
<tr><td><code>messages.challenge.phrase</code></td><td>Shown for challenge-type advancements.</td><td><code>&amp;fhas completed the challenge</code></td></tr>
</tbody>
</table>
</div>
<p>The full rebuilt message is always assembled in this order:</p>
{code("text", "<player name> <phrase> <advancement name>")}
{callout("Preview command", 'See <a href="../commands/">commands</a> to learn how to preview advancment messages with your current config.')}
'''
site.page("configuration", "Configuration", "Guide",
          "Guide on configuring CustomAdvancementMessages.",
          configuration_content, prev=("installation", "Installation"), nxt=("placeholders", "Placeholders & Colors"))


# =========================================================================
# PLACEHOLDERS & COLORS
# =========================================================================
color_table_rows = "".join(
    f'<tr><td><code>&amp;{code_}</code></td><td><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:{hexv};border:1px solid var(--border);vertical-align:middle;margin-right:0.5em;"></span>{name}</td></tr>'
    for code_, hexv, name in [
        ("0", "#000000", "black"), ("1", "#0000AA", "dark blue"), ("2", "#00AA00", "dark green"), ("3", "#00AAAA", "dark aqua"),
        ("4", "#AA0000", "dark red"), ("5", "#AA00AA", "dark purple"), ("6", "#FFAA00", "gold"), ("7", "#AAAAAA", "gray"),
        ("8", "#555555", "dark gray"), ("9", "#5555FF", "blue"), ("a", "#55FF55", "green"), ("b", "#55FFFF", "aqua"),
        ("c", "#FF5555", "red"), ("d", "#FF55FF", "light purple"), ("e", "#FFFF55", "yellow"), ("f", "#FFFFFF", "white"),
    ]
)

placeholders_content = f'''
<h1>Placeholders &amp; Colors</h1>
<p class="lede">How player names, phrase colors, and advancement types resolve into the final message.</p>

{doc_image(PREVIEW_IMG, "Preview of a customized advancement message.")}

<h2 class="no-rule">Player name placeholders</h2>
<p>Any PlaceholderAPI placeholder can be used in <code>player-name-format</code>, alongside the plugin's own built-in <code>{{player}}</code> placeholder, which always resolves to the player's username.</p>
<p>See the <a href="https://wiki.placeholderapi.com/users/using-placeholders/" target="_blank" rel="noopener">PlaceholderAPI placeholder guide</a> for in-depth info on using PlaceholderAPI placeholders.</p>

<h2 class="no-rule">Color and style codes</h2>
<p>Any <code>phrase</code> in <code>config.yml</code> supports all Minecraft <code>&amp;</code> color and style codes:</p>
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

<h2>Hover text stays vanilla</h2>
<p>Hovering over the advancement name in chat still shows Minecraft's normal tooltip (the advancement's title and description) exactly as vanilla would show it.</p>
'''
site.page("placeholders", "Placeholders & Colors", "Guide",
          "How placeholders, colors, and advancement types resolve in CustomAdvancementMessages.",
          placeholders_content, prev=("configuration", "Configuration"), nxt=("commands", "Commands"))


# =========================================================================
# COMMANDS
# =========================================================================
commands_content = f'''
<h1>Commands</h1>
<p class="lede">All CustomAdvancementMessages commands are under <code>/advancements</code> (alias <code>/customadvancementmessages</code>). All commands require the <a href="../permissions/">admin permission</a>.</p>

<h2 class="no-rule">Top level</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Command</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>/advancements reload</code></td><td>Reloads config.yml and applies changes.</td></tr>
<tr><td><code>/advancements update</code></td><td>Runs a fresh check against the plugin's Modrinth project and reports whether a newer <em>release</em>-type version is available. Pre-release/beta versions are ignored.</td></tr>
<tr><td><code>/advancements preview [task|goal|challenge]</code></td><td>Sends the player a mock advancement message built from their current config.</td></tr>
</tbody>
</table>
</div>
{callout("Automatic update checks", 'The plugin also checks Modrinth for a newer version once automatically on startup, and messages any player that joins with the permission <code>customadvancementmessages.updatenotify</code> if there is a new version available.')}

<h2 id="preview">preview</h2>
<p><code>/advancements preview [task|goal|challenge]</code>. Sends a fake advancement message to yourself only (nothing is sent to anyone else, and no real advancement progress is granted) built with your exact <code>config.yml</code> settings. If no type is given, it defaults to <code>task</code>.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Type</th><th>Example vanilla advancement used</th></tr></thead>
<tbody>
<tr><td><code>task</code></td><td>Diamonds! &mdash; <em>Acquire diamonds</em></td></tr>
<tr><td><code>goal</code></td><td>The End... Again... &mdash; <em>Respawn the ender dragon</em></td></tr>
<tr><td><code>challenge</code></td><td>Adventuring Time &mdash; <em>Discover every biome</em></td></tr>
</tbody>
</table>
</div>
<p>The message will look the exact same as the real advancement message.</p>

'''
site.page("commands", "Commands", "Reference",
          "All CustomAdvancementMessages commands.",
          commands_content, prev=("placeholders", "Placeholders & Colors"), nxt=("permissions", "Permissions"))


# =========================================================================
# PERMISSIONS
# =========================================================================
permissions_content = f'''
<h1>Permissions</h1>
<p class="lede">CustomAdvancementMessages uses two permissions.</p>

<div class="table-wrap">
<table>
<thead><tr><th>Node</th><th>Default</th><th>Grants</th></tr></thead>
<tbody>
<tr><td><code>customadvancementmessages.admin</code></td><td><span class="tag op">op</span></td><td>Access to all <code>/advancements</code> subcommands.</td></tr>
<tr><td><code>customadvancementmessages.updatenotify</code></td><td><span class="tag op">op</span></td><td>Receive a message on join when a plugin update is available.</td></tr>
</tbody>
</table>
</div>

'''
site.page("permissions", "Permissions", "Reference",
          "The customadvancementmessages.admin permission.",
          permissions_content, prev=("commands", "Commands"), nxt=("troubleshooting", "Troubleshooting"))


# =========================================================================
# TROUBLESHOOTING
# =========================================================================
troubleshooting_content = f'''
<h1>Troubleshooting</h1>
<p class="lede">Potential issues and how to fix them.</p>

<h2 class="no-rule">Plugin won't enable</h2>
<li>Make sure the latest versions of <code>PacketEvents</code> and <code>PacketEvents</code> are installed. They are both required dependencies, and CustomAdvancementMessages won't start without them.</li>

<h2>Placeholders show up as literal text</h2>
<li>Confirm that PlaceholderAPI itself can resolve the placeholder with <code>/papi parse &lt;username&gt; &lt;placeholder&gt;</code>.</li>
<li>Make sure any PlaceholderAPI expansions for the placeholder are installed (e.g., the LuckPerms expansion for <code>%luckperms_prefix%</code>). Download expansions with <code>/papi ecloud download &lt;expansion&gt;</code>.</li>
<br>
<br>
<hr>
{callout("Still stuck?", f'Submit an <a href="{REPO_URL}/issues" target="_blank" rel="noopener">issue</a> on the CustomAdvancementMessages GitHub repository and include any console errors, details about the problem, and how to reproduce it.')}

'''
site.page("troubleshooting", "Troubleshooting", "Resource",
          "Fixes for common CustomAdvancementMessages problems.",
          troubleshooting_content, prev=("permissions", "Permissions"), nxt=("changelog", "Changelog"))


# =========================================================================
# CHANGELOG
# =========================================================================
changelog_content = f'''
<h1>Changelog</h1>
<p class="lede">Notable changes to CustomAdvancementMessages, newest first.</p>

<div class="changelog">

<div class="changelog-entry">
<div class="changelog-heading"><span class="changelog-version">1.0.2</span></div>
<ul>
<li>Made performance improvements.</li>
</ul>
</div>

<div class="changelog-entry">
<div class="changelog-heading"><span class="changelog-version">1.0.1</span></div>
<ul>
<li>Added support for more Minecraft versions (1.20 and newer).</li>
<li>Built-in <code>{{player}}</code> placeholder for <code>player-name-format</code>, which returns the player's username.</li>
<li><code>customadvancementmessages.updatenotify</code> permission that controls who gets notified when an update is available.</li>
<li>PlaceholderAPI is now a required dependency and the plugin won't enable without it.</li>
</ul>
</div>

<div class="changelog-entry">
<div class="changelog-heading"><span class="changelog-version">1.0.0</span></div>
<ul>
<li>Initial release.</li>
</ul>
</div>

</div>
'''
site.page("changelog", "Changelog", "Resource",
          "What's changed in CustomAdvancementMessages.",
          changelog_content, prev=("troubleshooting", "Troubleshooting"))


print("CustomAdvancementMessages site generated.")