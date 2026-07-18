#!/usr/bin/env python3
"""Build index.html from primer.md.

Single self-contained HTML, no CDN, works over file:// and GitHub Pages.
Run after editing primer.md:  python3 build_page.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "primer.md"
OUT = ROOT / "index.html"

Q_RE = re.compile(r"^\*\*Q(\d+)\.\*\*\s*(.+)$")
A_RE = re.compile(r"^\*\*A\.\*\*\s*(.+)$")


def inline(text):
    """Minimal inline markdown -> HTML (escaped first)."""
    t = html.escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def parse(md):
    """Split primer.md into (domains, tail_markdown)."""
    lines = md.split("\n")
    domains, domain, section = [], None, None
    tail, in_tail = [], False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and "Domain" not in line:
            in_tail = True
        if in_tail:
            tail.append(line)
            i += 1
            continue
        if line.startswith("## Domain"):
            domain = {"title": line[3:].strip(), "sections": []}
            domains.append(domain)
            section = None
        elif line.startswith("### ") and domain is not None:
            section = {"title": line[4:].strip(), "items": []}
            domain["sections"].append(section)
        else:
            m = Q_RE.match(line)
            if m and domain is not None:
                answer = ""
                if i + 1 < len(lines):
                    a = A_RE.match(lines[i + 1])
                    if a:
                        answer = a.group(1)
                        i += 1
                if section is None:
                    section = {"title": "", "items": []}
                    domain["sections"].append(section)
                section["items"].append(
                    {"n": int(m.group(1)), "q": inline(m.group(2)), "a": inline(answer)}
                )
        i += 1
    return domains, tail


def render_markdown(lines):
    """Minimal block markdown -> HTML for the reference tail (tables, lists, headings)."""
    out, i = [], 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line or line.startswith("---"):
            i += 1
            continue
        if line.startswith("#"):
            lvl = len(line) - len(line.lstrip("#"))
            out.append(f"<h{min(lvl,4)}>{inline(line.lstrip('# ').strip())}</h{min(lvl,4)}>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                    for r in rows[1:]
                )
                out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        elif re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            items = []
            while i < len(lines) and (
                re.match(r"^\s*[-*]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])
            ):
                items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", lines[i].rstrip()))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].lstrip()[0] in "|#-*":
                para.append(lines[i].strip())
                i += 1
            if para:
                out.append(f"<p>{inline(' '.join(para))}</p>")
            else:
                i += 1
    return "\n".join(out)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CCA-F Primer &mdash; One Question, One Answer</title>
<style>
  :root {
    --bg: #ffffff; --fg: #1a1a1a; --muted: #6b6b6b; --line: #e4e4e4;
    --accent: #b8552b; --card: #fafafa; --code-bg: #f0f0ee;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #16161a; --fg: #e8e6e3; --muted: #9a9a9a; --line: #2e2e34;
      --accent: #e08a5c; --card: #1e1e24; --code-bg: #2a2a31;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--fg);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Noto Sans JP", sans-serif;
  }
  .wrap { max-width: 820px; margin: 0 auto; padding: 0 20px 100px; }
  header { padding: 40px 0 20px; border-bottom: 1px solid var(--line); }
  h1 { font-size: 26px; margin: 0 0 6px; letter-spacing: -0.01em; }
  .sub { color: var(--muted); font-size: 14px; margin: 0; }
  .bar {
    position: sticky; top: 0; z-index: 10; background: var(--bg);
    border-bottom: 1px solid var(--line); padding: 12px 0;
    display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
  }
  button {
    font: inherit; font-size: 14px; padding: 7px 14px; border-radius: 6px;
    border: 1px solid var(--line); background: var(--card); color: var(--fg); cursor: pointer;
  }
  button:hover { border-color: var(--accent); color: var(--accent); }
  .count { margin-left: auto; color: var(--muted); font-size: 13px; }
  h2 {
    font-size: 19px; margin: 46px 0 4px; padding-top: 14px;
    border-top: 2px solid var(--accent);
  }
  h3 { font-size: 14px; margin: 28px 0 10px; color: var(--muted); font-weight: 600;
       text-transform: uppercase; letter-spacing: 0.06em; }
  .qa {
    border: 1px solid var(--line); border-radius: 8px; background: var(--card);
    margin: 8px 0; overflow: hidden;
  }
  .q {
    display: flex; gap: 10px; padding: 13px 15px; cursor: pointer; user-select: none;
    align-items: baseline;
  }
  .q:hover { color: var(--accent); }
  .num { color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums;
         min-width: 34px; flex-shrink: 0; }
  .a {
    display: none; padding: 0 15px 14px 59px; color: var(--fg);
    border-top: 1px solid var(--line); margin-top: 0; padding-top: 12px;
  }
  .qa.open .a { display: block; }
  .qa.open .q { color: var(--accent); }
  .a::before { content: "A. "; color: var(--accent); font-weight: 600; }
  code {
    background: var(--code-bg); padding: 1px 5px; border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.88em;
  }
  .ref { margin-top: 70px; padding-top: 10px; border-top: 2px solid var(--accent); }
  .ref h2 { border: 0; margin-top: 30px; padding-top: 0; }
  .ref table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 14px; }
  .ref th, .ref td { border: 1px solid var(--line); padding: 7px 10px; text-align: left; vertical-align: top; }
  .ref th { background: var(--card); font-weight: 600; }
  .ref li { margin: 3px 0; }
  footer { margin-top: 50px; color: var(--muted); font-size: 13px; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>CCA-F Primer</h1>
    <p class="sub">Claude Certified Architect &ndash; Foundations (CCAR-F) &middot; one question, one answer</p>
  </header>

  <div class="bar">
    <button id="showAll">Show all answers</button>
    <button id="hideAll">Hide all answers</button>
    <span class="count" id="count"></span>
  </div>

  <main id="content"></main>

  <div class="ref">__TAIL__</div>

  <footer>Built from primer.md &middot; Exam Guide v1.0 (Effective July 2026)</footer>
</div>

<script>
const DATA = __DATA__;

const content = document.getElementById('content');
let total = 0;

for (const domain of DATA) {
  const h2 = document.createElement('h2');
  h2.textContent = domain.title;
  content.appendChild(h2);

  for (const section of domain.sections) {
    if (section.title) {
      const h3 = document.createElement('h3');
      h3.textContent = section.title;
      content.appendChild(h3);
    }
    for (const item of section.items) {
      total++;
      const card = document.createElement('div');
      card.className = 'qa';
      const q = document.createElement('div');
      q.className = 'q';
      q.innerHTML = '<span class="num">Q' + item.n + '</span><span>' + item.q + '</span>';
      const a = document.createElement('div');
      a.className = 'a';
      a.innerHTML = item.a;
      q.addEventListener('click', () => card.classList.toggle('open'));
      card.appendChild(q);
      card.appendChild(a);
      content.appendChild(card);
    }
  }
}

document.getElementById('count').textContent = total + ' questions';

const cards = () => document.querySelectorAll('.qa');
document.getElementById('showAll').addEventListener('click', () =>
  cards().forEach(c => c.classList.add('open')));
document.getElementById('hideAll').addEventListener('click', () =>
  cards().forEach(c => c.classList.remove('open')));
</script>
</body>
</html>
"""


def main():
    md = SRC.read_text(encoding="utf-8")
    domains, tail = parse(md)
    n = sum(len(s["items"]) for d in domains for s in d["sections"])
    out = (
        TEMPLATE
        .replace("__DATA__", json.dumps(domains, ensure_ascii=False))
        .replace("__TAIL__", render_markdown(tail))
    )
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(domains)} domains, {n} questions")


if __name__ == "__main__":
    main()
