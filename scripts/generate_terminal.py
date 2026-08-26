#!/usr/bin/env python3
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = ROOT / "profile.json"
OUTPUT_PATH = ROOT / "assets" / "terminal.svg"

WIDTH = 1000
LEFT = 38
LINE_H = 25

def t(x, y, cls, value, anchor=None):
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{anchor_attr}>{escape(str(value))}</text>'

def status_class(status):
    return {
        "RUNNING": "green",
        "READING": "yellow",
        "PAUSED": "dim",
        "DONE": "accent",
    }.get(status.upper(), "mono")

with PROFILE_PATH.open(encoding="utf-8") as f:
    p = json.load(f)

identity = p["identity"]
systems = p.get("systems", {})
research = p.get("research", {})
projects = p.get("projects", [])
stack = p.get("stack", [])

rows = []
y = 78

rows.append(t(LEFT, y, "title", f'{identity["username"]}@{identity["terminal_host"]}'))
y += 27
rows.append(t(LEFT, y, "dim", "────────────────────────────────────────────────────────────────────────────"))

y += 38
rows.append(t(LEFT, y, "prompt", "$ whoami"))
for key, value in [
    ("Role", identity.get("role", "")),
    ("University", identity.get("university", "")),
    ("Lab", identity.get("lab", "")),
    ("Location", identity.get("location", "")),
]:
    y += 30 if key == "Role" else LINE_H
    rows.append(t(LEFT, y, "mono", f"{key:<11} {value}"))

y += 44
rows.append(t(LEFT, y, "prompt", "$ systems --list"))
y += 30
rows.append(t(LEFT, y, "mono", f'{"OS":<11} {" · ".join(systems.get("os", []))}'))

y += 44
rows.append(t(LEFT, y, "prompt", "$ research --current"))
for item in research.get("current", []):
    y += LINE_H
    status = item.get("status", "").upper()
    label = item.get("label", "")
    rows.append(t(LEFT, y, status_class(status), f"[{status}] {label}"))

description = research.get("description", [])
if description:
    y += 44
    rows.append(t(LEFT, y, "prompt", "$ cat research.txt"))
    for line in description:
        y += LINE_H
        rows.append(t(LEFT, y, "mono", line))

if projects:
    y += 44
    rows.append(t(LEFT, y, "prompt", "$ projects --active"))
    y += 30
    rows.append(t(LEFT, y, "dim", "PID   PROJECT                         STATUS"))
    for project in projects:
        y += LINE_H
        rows.append(t(
            LEFT, y, "mono",
            f'{project.get("pid",""):<5} {project.get("name",""):<31} {project.get("status","")}'
        ))

if stack:
    y += 44
    rows.append(t(LEFT, y, "prompt", "$ stack --list"))
    y += 30
    rows.append(t(LEFT, y, "mono", " · ".join(stack)))

y += 44
rows.append(t(LEFT, y, "prompt", "$"))
cursor_y = y - 14
height = y + 30

svg = f"""<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; }}
    .border {{ stroke: #30363d; stroke-width: 2; }}
    .mono {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      fill: #c9d1d9;
    }}
    .title {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 17px;
      font-weight: 700;
      fill: #58a6ff;
    }}
    .prompt {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      font-weight: 700;
      fill: #58a6ff;
    }}
    .dim {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      fill: #8b949e;
    }}
    .green {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      fill: #3fb950;
    }}
    .yellow {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      fill: #d29922;
    }}
    .accent {{
      font-family: "SFMono-Regular", "SF Mono", "Cascadia Code", "Roboto Mono",
                   "Liberation Mono", Menlo, Consolas, monospace;
      font-size: 15px;
      fill: #bc8cff;
    }}
    .cursor {{
      fill: #c9d1d9;
      animation: blink 1s steps(2, start) infinite;
    }}
    @keyframes blink {{
      50% {{ opacity: 0; }}
    }}
  </style>

  <rect x="1" y="1" width="{WIDTH-2}" height="{height-2}" rx="14" class="bg border"/>
  <circle cx="28" cy="28" r="6" fill="#ff5f56"/>
  <circle cx="49" cy="28" r="6" fill="#ffbd2e"/>
  <circle cx="70" cy="28" r="6" fill="#27c93f"/>
  {t(WIDTH//2, 34, "dim", f'{identity["username"]} — research-terminal', "middle")}

  {"".join(rows)}
  <rect x="58" y="{cursor_y}" width="9" height="18" rx="1" class="cursor"/>
</svg>
"""

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(svg, encoding="utf-8")
print(f"Generated {OUTPUT_PATH}")
