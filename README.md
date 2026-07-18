# CCA-F Primer

One-question-one-answer primer for the **Claude Certified Architect – Foundations** exam (CCAR-F), built from Exam Guide v1.0 (Effective July 2026).

176 questions across the five exam domains, plus quick-reference tables and a weak-spot index derived from a past practice attempt.

## Files

| File | Purpose |
|---|---|
| `primer.md` | The source of truth. Edit questions here. |
| `index.html` | Generated page. Answers hidden by default; click a question to reveal, or use **Show all / Hide all**. |
| `build_page.py` | Regenerates `index.html` from `primer.md`. |

## Usage

Open `index.html` directly in a browser, or serve it via GitHub Pages (Settings → Pages → deploy from `master` / root).

After editing `primer.md`:

```bash
python3 build_page.py
```

No dependencies, no CDN — `index.html` is fully self-contained and works over `file://`.

## Question format

```markdown
**Q1.** Which response field tells your agentic loop whether to keep going?
**A.** `stop_reason` — `"tool_use"` means continue the loop, `"end_turn"` means stop.
```

Questions live under `## Domain N — ...` and `### <task statement>` headings; the builder uses those for page structure. Numbering is sequential across the whole file. Everything after the last domain section is rendered as static reference material.
