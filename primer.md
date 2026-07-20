# CCA-F Primer — One Question, One Answer

Rapid-recall drill for **Claude Certified Architect – Foundations (CCA-F)**, built from Exam Guide v1.0 (Effective July 2026) task statements 1.1–5.6 and the §17 Appendix.

Format: one question, one short answer + a one-line reason. The real exam is scenario-based multiple choice — this primer covers the *facts and judgment rules* those scenarios are built on.

| Domain | Weight | Questions |
|---|---|---|
| D1 Agentic Architecture & Orchestration | 27% | 46 |
| D2 Tool Design & MCP Integration | 18% | 27 |
| D3 Claude Code Configuration & Workflows | 20% | 36 |
| D4 Prompt Engineering & Structured Output | 20% | 33 |
| D5 Context Management & Reliability | 15% | 34 |
| **Total** | | **176** |

11 questions were added after cross-checking against a practice exam to close gaps in coverage.

---

## Domain 1 — Agentic Architecture & Orchestration (27%)

### 1.1 Agentic loops

**Q1.** Which response field tells your agentic loop whether to keep going?
**A.** `stop_reason` — `"tool_use"` means continue the loop, `"end_turn"` means stop.

**Q2.** What must you append to the conversation before the next iteration of an agentic loop?
**A.** The tool results — the model can only reason about the next step if results are in context.

**Q3.** Why is parsing Claude's natural-language output to decide when to stop an anti-pattern?
**A.** It's probabilistic — `stop_reason` is the deterministic signal designed for it.

**Q4.** In model-driven decision-making, who chooses which tool to call?
**A.** Claude does — you supply tool definitions, not a hardcoded call sequence.

**Q5.** Your loop terminates early even though the task is incomplete. First thing to check?
**A.** Whether the loop stops on anything other than `stop_reason` — e.g. text matching or a fixed iteration cap.

**Q6.** What role does `max_tokens` play in an agentic loop failure?
**A.** Truncation mid-tool-call — the response ends with `stop_reason: "max_tokens"`, not a usable tool call.

**Q7.** Tool result blocks must be sent in which role?
**A.** A `user` message containing `tool_result` blocks matching the `tool_use` ids.

**Q8.** Your agent averages 4+ API round-trips per resolution because it requests `get_customer` and `lookup_order` in separate sequential turns. Fix?
**A.** Prompt Claude to batch tool requests in a single turn and return all tool results together before the next API call.

**Q9.** Multiple `tool_use` blocks in one assistant response — how many `tool_result` blocks come back?
**A.** All of them, in one `user` message — one `tool_result` per `tool_use` id.

**Q10.** Latency problem is round-trips, not model speed. Is "switch to a faster model" the answer?
**A.** No — reduce round-trips by parallelizing tool calls within a turn.

### 1.2 Coordinator–subagent orchestration

**Q11.** What is the standard multi-agent topology on this exam?
**A.** Hub-and-spoke — all inter-subagent communication routes through the coordinator.

**Q12.** Why route everything through the coordinator instead of letting subagents talk to each other?
**A.** Observability, consistent error handling, and a single point of aggregation.

**Q13.** Do subagents inherit the coordinator's conversation history?
**A.** No — subagents run with isolated context and only see what the prompt gives them.

**Q14.** What are the coordinator's four jobs?
**A.** Task decomposition, delegation, result aggregation, and deciding when work is complete.

**Q15.** What is the risk of a coordinator that decomposes too narrowly?
**A.** Incomplete coverage — whole facets of the query never get researched.

**Q16.** Two research subagents return near-identical findings. Design fix?
**A.** Partition scope explicitly — assign each subagent distinct subtopics/sources.

**Q17.** Synthesis output has gaps. What should the coordinator do?
**A.** Run an iterative refinement loop — evaluate the synthesis, then dispatch follow-up subagents for the gaps.

**Q18.** Should a coordinator prompt give subagents step-by-step procedures?
**A.** No — specify research goals and quality criteria so the subagent can adapt.

### 1.3 Subagent invocation & context passing

**Q19.** What mechanism spawns a subagent?
**A.** The `Task` tool — and `Task` must be in the parent's `allowedTools`; without it the model can't spawn subagents at all.

**Q20.** How do you run subagents in parallel?
**A.** Emit multiple `Task` tool calls in a *single* coordinator response.

**Q21.** A subagent doesn't know what the previous agent found. Why?
**A.** Context isn't automatic — prior findings must be included explicitly in the subagent's prompt.

**Q22.** What does `AgentDefinition` configure?
**A.** Description, system prompt, and tool restrictions for a subagent type.

**Q23.** How should findings be passed between agents to keep them usable?
**A.** As structured data separating content from metadata (source URLs, document names, dates).

**Q24.** You want two subagents to explore divergent approaches from the same analysis baseline. Mechanism?
**A.** Fork-based session management (`fork_session`) — both branches start from the shared state.

### 1.4 Enforcement & handoff

**Q25.** A refund over $500 must *never* be processed automatically. Prompt instruction or hook?
**A.** Hook — "must/always/never" requirements need programmatic enforcement, not probabilistic compliance.

**Q26.** What guarantees identity verification happens before a financial operation?
**A.** A programmatic prerequisite gate that blocks the downstream tool call until verification completes.

**Q27.** What belongs in a structured escalation handoff?
**A.** Customer ID, root cause, amounts, actions already taken, and recommended resolution.

**Q28.** A customer message contains three separate issues. Correct handling?
**A.** Decompose into distinct items and investigate each — don't answer only the first.

**Q29.** Single-concern requests resolve at 94%, multi-concern requests degrade badly. Fix?
**A.** Few-shot examples showing the correct reasoning *and tool sequence* for multi-concern messages.

**Q30.** How should the investigation of those decomposed concerns run?
**A.** In parallel, over shared customer context, then synthesize one resolution — not three separate mini-conversations.

**Q31.** Resolution is technically correct but CSAT is 15% lower on complex cases. Fix?
**A.** Add a self-critique step: the agent evaluates its draft for completeness, relevant context, and likely follow-up questions.

### 1.5 Hooks

**Q32.** Which hook transforms a tool's result before the model sees it?
**A.** `PostToolUse` — e.g. normalizing Unix timestamps and ISO dates into one format.

**Q33.** Which hook blocks a policy-violating action?
**A.** A tool-call interception hook (`PreToolUse`) that inspects and rejects the outgoing call.

**Q34.** Hooks vs. system prompt instructions — what's the actual difference?
**A.** Hooks are deterministic; prompt instructions are probabilistic and can be violated.

**Q35.** Three backend tools return dates in three formats. Cleanest fix?
**A.** A `PostToolUse` hook that normalizes them — not asking the model to handle every format.

### 1.6 Task decomposition

**Q36.** When is a fixed sequential pipeline (prompt chaining) the right pattern?
**A.** When the steps are known in advance and every input needs the same passes.

**Q37.** When is dynamic adaptive decomposition right instead?
**A.** When subtasks depend on what earlier steps discover (e.g. open-ended investigations).

**Q38.** How do you decompose a large multi-file code review?
**A.** Per-file local analysis passes **plus** a separate cross-file integration pass.

**Q39.** "Add comprehensive tests to a legacy codebase." First decomposition step?
**A.** Survey the codebase to identify what needs coverage, then generate subtasks from that.

### 1.7 Session management

**Q40.** What flag continues the most recent session?
**A.** `--continue` — resumes the most recent session in the current directory immediately, no picking.

**Q41.** What do you use to resume a *specific* prior session?
**A.** `--resume <session-name>` — selects by name/ID rather than recency.

**Q42.** What creates an independent branch from a shared analysis baseline?
**A.** `fork_session` — the original session stays intact.

**Q43.** You resume a session after the codebase changed significantly. What must you do?
**A.** Tell the agent which specific files changed so it re-analyzes those, rather than trusting stale context.

**Q44.** Prior context is mostly stale. Resume or start fresh?
**A.** Start fresh with a structured summary of prior findings — more reliable than dragging stale context.

**Q45.** You want to compare two testing strategies in parallel. Mechanism?
**A.** `fork_session` — two branches from the same baseline analysis.

**Q46.** "Resumable" implies "should resume"?
**A.** No — resume only when prior context is still mostly valid.

---

## Domain 2 — Tool Design & MCP Integration (18%)

### 2.1 Tool interface design

**Q47.** What is the primary mechanism the model uses to pick a tool?
**A.** The tool description — minimal descriptions cause misrouting.

**Q48.** What should a good tool description contain beyond a one-liner?
**A.** Input formats, example queries, edge cases, and explicit boundaries vs. sibling tools.

**Q49.** `analyze_content` and `process_document` get confused with each other. Fix?
**A.** Rename and rewrite descriptions to eliminate functional overlap.

**Q50.** A tool with a great description still isn't being called. What else could be overriding it?
**A.** Keyword-sensitive wording in the system prompt creating a competing selection rule.

**Q51.** One generic tool handles four unrelated jobs badly. Fix?
**A.** Split it into purpose-specific tools with defined input/output contracts.

### 2.2 Structured error responses

**Q52.** What MCP flag communicates a tool failure back to the agent?
**A.** `isError` — set true on the tool result.

**Q53.** Name the three error categories the exam expects.
**A.** Transient (timeouts/unavailable), validation (bad input), and permission/business-rule.

**Q54.** Why is a generic `"Operation failed"` response harmful?
**A.** The agent can't decide whether to retry, fix input, or escalate.

**Q55.** What field tells the agent not to retry a business-rule rejection?
**A.** `retriable: false`, plus a customer-friendly explanation it can relay. (A structured-error design convention, not a field defined in the MCP spec.)

**Q56.** A search returns zero rows vs. the search service times out. Must these look different?
**A.** Yes — a valid empty result is not an access failure, and conflating them corrupts the coordinator's decision.

**Q57.** Where should transient failures be handled first?
**A.** Locally inside the subagent; only propagate what it can't recover from.

### 2.3 Tool distribution & tool_choice

**Q58.** What happens when an agent gets 18 tools instead of 4–5?
**A.** Tool selection accuracy degrades — scope tools to the agent's role.

**Q59.** A synthesis agent has web search and starts re-researching. Fix?
**A.** Remove out-of-role tools; give a narrow scoped alternative like `verify_fact` if the need is real.

**Q60.** Three values of `tool_choice`?
**A.** `"auto"` (may reply with text), `"any"` (must call some tool), and forced `{"type":"tool","name":"..."}`.

**Q61.** How do you guarantee the model calls a tool instead of chatting?
**A.** `tool_choice: "any"`.

**Q62.** How do you guarantee a *specific* tool is called first?
**A.** Forced selection: `tool_choice: {"type": "tool", "name": "get_customer"}`.

**Q63.** `fetch_url` lets an agent pull anything off the web. Least-privilege replacement?
**A.** A constrained tool like `load_document(doc_id)` scoped to the approved corpus.

### 2.4 MCP servers, resources, and scope

**Q64.** The agent repeatedly calls a tool just to list what's available. Fix?
**A.** Expose a **resource** — resources publish catalogs upfront without a tool round-trip.

**Q65.** MCP tool vs. MCP resource in one line each?
**A.** Tool = an action the model executes; resource = readable content the server exposes.

**Q66.** Where do you configure an MCP server for the whole team?
**A.** Project-scoped `.mcp.json`, committed to version control.

**Q67.** Where does a personal or experimental MCP server go?
**A.** User-scoped `~/.claude.json` — not shared with the team.

**Q68.** How do you put a GitHub token in `.mcp.json` without committing a secret?
**A.** Environment variable expansion — `${GITHUB_TOKEN}`.

**Q69.** When are tools from configured MCP servers discovered?
**A.** At connection time — all servers' tools are available simultaneously in the session.

**Q70.** Standard integration (GitHub, Slack…) — build custom or adopt community?
**A.** Adopt the existing community MCP server; custom builds are the over-engineered answer.

### 2.5 Built-in tools

**Q71.** Grep vs. Glob?
**A.** Grep searches file *contents*; Glob matches file *paths* (e.g. `**/*.test.tsx`).

**Q72.** `Edit` fails because the anchor text isn't unique. Fallback?
**A.** `Read` the file, then `Write` the full corrected contents.

**Q73.** Standard order for exploring an unfamiliar codebase?
**A.** Grep/Glob to narrow down → Read the specific files — incremental, not read-everything.

---

## Domain 3 — Claude Code Configuration & Workflows (20%)

### 3.1 CLAUDE.md hierarchy

**Q74.** Name the CLAUDE.md hierarchy levels.
**A.** User (`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md`) → directory-level files.

**Q75.** A new teammate isn't getting your conventions. Most likely cause?
**A.** They live in `~/.claude/CLAUDE.md` — user-level settings apply only to that user.

**Q76.** What command shows which memory files are actually loaded?
**A.** `/memory` — use it to diagnose inconsistent behavior across a repo.

**Q77.** How do you keep CLAUDE.md modular instead of monolithic?
**A.** Import external standards files with `@path/to/file` (e.g. `@docs/testing-standards.md`) — often called "@import syntax" informally.

**Q78.** A 900-line CLAUDE.md covers testing, styling, and infra. Better structure?
**A.** Split into topic files under `.claude/rules/` (testing.md, styling.md…).

**Q79.** What's the hidden cost of putting everything in CLAUDE.md?
**A.** It's always loaded — it burns context on every task regardless of relevance.

### 3.2 Slash commands & skills

**Q80.** Where do team-shared slash commands live?
**A.** `.claude/commands/` — shared via version control.

**Q81.** Where do personal slash commands live?
**A.** `~/.claude/commands/` — not shared.

**Q82.** What file defines a skill?
**A.** `SKILL.md` in `.claude/skills/`, with YAML frontmatter.

**Q83.** A skill produces huge exploratory output that pollutes the main conversation. Frontmatter fix?
**A.** `context: fork` — runs the skill in an isolated sub-agent context.

**Q84.** Which frontmatter field restricts what tools a skill may use?
**A.** `allowed-tools`.

**Q85.** Which frontmatter field prompts the developer for required parameters?
**A.** `argument-hint`.

**Q86.** How do you customize a team skill just for yourself without forking the repo?
**A.** Create a personal skill with the **same name** under `~/.claude/skills/<skill-name>/SKILL.md` — on a name collision, personal overrides project. Skill precedence: enterprise > personal > project > plugins. Note this is the *opposite* of settings precedence (where project overrides user), which is why it's a common trap.

**Q87.** Skill vs. CLAUDE.md — decision rule?
**A.** Skill = long procedure loaded on demand; CLAUDE.md = short conventions needed always.

**Q88.** 2–3 full exemplar implementations help when generating new API endpoints, but are useless for bug fixes and reviews. Where do they go?
**A.** In a skill that references the exemplars — on-demand, so the tokens are spent only on endpoint work.

**Q89.** A team skill has three problems: invoked without arguments, floods the conversation, and touches files it shouldn't. Three frontmatter fixes?
**A.** `argument-hint` for parameters, `context: fork` for isolation, `allowed-tools` to restrict writes.

### 3.3 Path-specific rules

**Q90.** What frontmatter field scopes a rule file to certain files?
**A.** `paths:` with glob patterns, e.g. `paths: ["terraform/**/*"]`.

**Q91.** When do path-scoped rules load?
**A.** Only when the file being edited matches the glob — saving context the rest of the time.

**Q92.** Conventions apply to all `*.tsx` files scattered across many directories. Rules glob or per-directory CLAUDE.md?
**A.** `.claude/rules/` glob — directory CLAUDE.md can't span directories by file type.

### 3.4 Plan mode vs. direct execution

**Q93.** When is plan mode the right call?
**A.** Large-scale changes, multiple valid approaches, architectural implications, many files.

**Q94.** When is direct execution right?
**A.** Simple, well-scoped, well-understood changes — a single-file bug fix, one validation rule.

**Q95.** What does the Explore subagent buy you?
**A.** It isolates verbose discovery output and returns a summary, preserving the main context window.

**Q96.** Model answer for a large migration?
**A.** Explore subagent to investigate → plan mode to design → direct execution to implement.

**Q97.** "Switch to a model with a bigger context window" — how often is this the right answer?
**A.** Almost never — it's the standard distractor for context problems.

### 3.5 Iterative refinement

**Q98.** Most effective way to communicate an expected transformation?
**A.** 2–3 concrete input/output examples — better than more prose description.

**Q99.** What is test-driven iteration with Claude Code?
**A.** Write the test suite first, then iterate by feeding failures back as guidance.

**Q100.** What is the interview pattern?
**A.** Have Claude ask *you* questions to surface considerations you hadn't specified.

**Q101.** Five bugs that interact with each other. Report separately or together?
**A.** Together, in one detailed message — interacting fixes need to be reasoned about jointly.

**Q102.** Five independent, unrelated bugs?
**A.** Fix them one at a time to keep each change verifiable.

### 3.6 CI/CD integration

**Q103.** What flag runs Claude Code non-interactively in a pipeline?
**A.** `-p` / `--print` — prevents hangs waiting for input.

**Q104.** How do you get machine-parseable output in CI?
**A.** `--output-format json`, with `--json-schema` to enforce the shape.

**Q105.** Minimum-privilege tool grant for a CI review job?
**A.** `--allowedTools "Read,Grep"` — `--dangerously-skip-permissions` is the over-privileged distractor. (Strictly, `--allowedTools` is the *no-prompt* allowlist and `--tools` restricts availability; in headless `-p` mode there's nobody to approve a prompt, so `--allowedTools` effectively restricts.)

**Q106.** Why not have the session that wrote the code review it?
**A.** It retains its own generation reasoning and is less likely to spot its own flawed assumptions.

**Q107.** Where do CI review standards, fixtures, and test conventions belong?
**A.** In CLAUDE.md, so every pipeline run has the project context.

**Q108.** Re-running a review after new commits — how do you stop repeat comments?
**A.** Include the prior findings in context and instruct it to report only new or unresolved issues.

**Q109.** Generated tests duplicate existing ones. Fix?
**A.** Put the existing test files in context so it can see what's already covered.

---

## Domain 4 — Prompt Engineering & Structured Output (20%)

### 4.1 Explicit criteria

**Q110.** "Be conservative" / "only report high-confidence findings" — why do these fail?
**A.** They give the model no shared definition of the threshold; behavior stays inconsistent.

**Q111.** What replaces them?
**A.** Explicit criteria — which categories to report, which to skip, with concrete code examples per severity.

**Q112.** Why do false positives matter more than raw recall in code review?
**A.** They destroy developer trust, and a distrusted reviewer gets ignored entirely.

**Q113.** One check category produces most of your false positives. Pragmatic move?
**A.** Temporarily disable that category to restore trust while you refine its criteria.

### 4.2 Few-shot prompting

**Q114.** Single most effective technique for consistent output format and judgment?
**A.** Few-shot examples.

**Q115.** How many examples for an ambiguous scenario?
**A.** 2–4 targeted ones per Exam Guide v1.0 §4.2 — but the number matters far less than *targeting ambiguous cases and showing the reasoning*. (Archived practice items used "4–6"; if an option pairs a slightly larger count with explicit reasoning, that beats a smaller count without it.)

**Q116.** Few-shot examples that just show correct answers vs. ones that show why the alternative was rejected?
**A.** Show the rejected alternative — that's what generalizes to novel ambiguous cases.

**Q117.** Why do few-shot examples beat more rules for edge cases?
**A.** They let the model generalize judgment to novel patterns rather than pattern-match a list.

**Q118.** Extraction hallucinates on documents with unusual layouts. Fix?
**A.** Few-shot examples showing correct extraction from those varied formats.

### 4.3 Structured output via tool use

**Q119.** Most reliable way to guarantee schema-compliant output?
**A.** `tool_use` with a JSON schema — it eliminates JSON syntax errors outright.

**Q120.** Does strict schema enforcement prevent wrong values?
**A.** No — it eliminates *syntax* errors, not *semantic* ones (well-formed but incorrect data).

**Q121.** Multiple extraction schemas exist and the model sometimes replies in prose. Fix?
**A.** `tool_choice: "any"` — forces some tool call, and it picks the fitting schema.

**Q122.** How do you stop the model inventing values absent from the source document?
**A.** Make those schema fields optional/nullable so "not present" is representable.

**Q123.** How do you handle a category field that can't cover every real case?
**A.** An enum with `"other"` plus a free-text detail field (and `"unclear"` for ambiguity).

**Q124.** Dates arrive in six formats across documents. Schema or prompt?
**A.** Both — the schema constrains the field, and prompt-level normalization rules dictate the target format.

**Q125.** `tool_choice: "auto"` risk in an extraction pipeline?
**A.** The model may return conversational text instead of calling the extraction tool.

### 4.4 Validation, retry, feedback loops

**Q126.** Schema validation fails. What do you send on retry?
**A.** The original document, the failed extraction, and the specific validation errors.

**Q127.** When is retrying pointless?
**A.** When the information simply isn't in the source — retries then invite fabrication; return null.

**Q128.** Line items don't sum to the stated total. Self-correction design?
**A.** Extract `calculated_total` alongside `stated_total` and flag mismatches for review.

**Q129.** How do you analyze *which* code constructs trigger false positives?
**A.** Add a `detected_pattern` field to each finding and aggregate it.

**Q130.** Semantic vs. syntactic validation error?
**A.** Syntactic = malformed/schema-violating; semantic = valid shape, wrong values or field placement.

### 4.5 Batch processing

**Q131.** Cost advantage of the Message Batches API?
**A.** 50% cheaper than synchronous.

**Q132.** Processing window and SLA?
**A.** Up to 24 hours, with no guaranteed completion time.

**Q133.** Key functional limitation of the Batches API?
**A.** No multi-turn tool calling within a single request — it can't run an agentic loop.

**Q134.** How do you correlate batch requests with responses?
**A.** `custom_id` on each request.

**Q135.** 12 documents fail in a 1,000-document batch. Recovery?
**A.** Resubmit only the failed `custom_id`s, with corrections — not the whole batch.

**Q136.** Blocking pre-merge CI review — batch or synchronous?
**A.** Synchronous — someone is waiting on the result.

**Q137.** Overnight report generation over 50k documents?
**A.** Batches — latency-tolerant and half the cost.

**Q138.** How do you avoid burning a whole batch on a bad prompt?
**A.** Refine the prompt on a small sample first, then submit at volume.

### 4.6 Multi-instance & multi-pass review

**Q139.** Why is a second, independent instance better at reviewing generated code?
**A.** It has no generation reasoning to defend, so it questions assumptions the author baked in.

**Q140.** Structure for reviewing a huge multi-file PR?
**A.** Per-file passes for local issues + a separate cross-file pass for integration issues.

**Q141.** Developers must click into every finding to read the reasoning before triaging. Fix?
**A.** Require reasoning and a confidence assessment *inline* with each finding — the bottleneck is investigation time, not finding count.

**Q142.** What does a verification pass with self-reported confidence buy you?
**A.** Triage signal for routing review attention — but it needs calibration before it can gate anything (see Q168).

---

## Domain 5 — Context Management & Reliability (15%)

### 5.1 Preserving critical context

**Q143.** What does progressive summarization tend to destroy?
**A.** Exact numbers — amounts, percentages, dates, order numbers, customer-stated expectations.

**Q144.** What is the "lost in the middle" effect?
**A.** Models attend most reliably to the beginning and end of long inputs; middle content degrades.

**Q145.** Practical consequence for aggregated inputs?
**A.** Put key findings summaries at the top and organize details behind them.

**Q146.** How do you keep transactional facts safe across a long conversation?
**A.** Extract them into a persistent structured "case file" outside the conversation.

**Q147.** Verbose tool outputs are eating the window. Fix?
**A.** Trim to the relevant fields before they enter context.

**Q148.** Do you resend full conversation history on each API request?
**A.** Yes — the API is stateless; omitted turns are simply lost.

**Q149.** How do you stop upstream agents from handing you unusable prose?
**A.** Make them return structured data — key facts, citations, relevance scores.

### 5.2 Escalation & ambiguity

**Q150.** Customer explicitly asks for a human. Correct action?
**A.** Escalate immediately — don't attempt resolution first.

**Q151.** Policy is silent on the customer's request (e.g. a competitor price match). Escalate?
**A.** Yes — policy gaps and exceptions are escalation triggers.

**Q152.** Why are sentiment and self-reported confidence bad escalation triggers?
**A.** They're unreliable proxies — frustration isn't inability, and self-scored confidence isn't calibrated.

**Q153.** Customer is frustrated but the issue is squarely within the agent's ability. Action?
**A.** Acknowledge the frustration and resolve it — frustration alone isn't an escalation trigger.

**Q154.** `get_customer` returns three matches. Action?
**A.** Ask for an additional identifier — never guess which record is right.

**Q155.** How do you make escalation criteria actually stick?
**A.** Explicit criteria in the system prompt with few-shot examples of escalate vs. resolve.

### 5.3 Error propagation in multi-agent systems

**Q156.** What belongs in a subagent's error report to the coordinator?
**A.** Failure type, what was attempted, any partial results, and alternative approaches.

**Q157.** Why is `"search unavailable"` a bad error message?
**A.** It hides the context the coordinator needs to decide between retry, reroute, and proceed-with-gaps.

**Q158.** Worst two failure-handling patterns in multi-agent systems?
**A.** Silently returning empty results as success, and killing the whole workflow on one subagent failure.

**Q159.** How should synthesis output represent missing coverage?
**A.** Coverage annotations — which findings are well-supported and which areas have gaps from unavailable sources.

### 5.4 Large codebase exploration

**Q160.** Symptom of context degradation in a long session?
**A.** Inconsistent answers and contradictions about material it already analyzed.

**Q161.** What persists key findings across context boundaries?
**A.** Scratchpad files the agent writes to and re-reads.

**Q162.** What command reduces context usage mid-session?
**A.** `/compact`.

**Q163.** How do you keep verbose exploration out of the main agent's context?
**A.** Delegate to subagents with narrow questions ("find all test files") and take back summaries.

**Q164.** Crash recovery design for a long multi-agent exploration?
**A.** Each agent exports structured state to a known location (a manifest) the coordinator can reload.

**Q165.** Correct sequencing between exploration phases?
**A.** Summarize phase-1 findings *before* spawning phase-2 subagents.

### 5.5 Human review & confidence calibration

**Q166.** Overall extraction accuracy is 97%. Why is that not enough to automate?
**A.** Aggregates mask poor performance on specific document types or fields.

**Q167.** How do you keep measuring error rates once high-confidence extractions are auto-approved?
**A.** Stratified random sampling of those high-confidence outputs.

**Q168.** What makes a confidence score usable as a routing threshold?
**A.** Calibration against a labeled validation set — raw self-reported confidence isn't calibrated.

**Q169.** What should be routed to human review?
**A.** Low model confidence, and ambiguous or internally contradictory source documents.

**Q170.** What analysis must precede automating high-confidence extractions?
**A.** Accuracy broken down by document type and by field.

### 5.6 Provenance & uncertainty

**Q171.** Where is source attribution usually lost?
**A.** In summarization steps that compress findings without carrying the citations along.

**Q172.** What must subagents output to preserve provenance?
**A.** Structured claim-source mappings — source URL/document name per claim.

**Q173.** Two credible sources report different statistics. Correct handling?
**A.** Report both, annotated with source and date — don't silently pick one or average them.

**Q174.** How do you prevent temporal confusion in synthesized reports?
**A.** Require publication/collection dates in every subagent's structured output.

**Q175.** How should a report separate certainty levels?
**A.** Explicit sections for well-established findings vs. contested/uncertain ones.

**Q176.** Financial data vs. narrative findings in a synthesis output?
**A.** Render by content type — tables for financial data, prose for narrative.

---

## Appendix — Quick Reference Tables

### Flags

| Purpose | Flag |
|---|---|
| Resume most recent session in the current directory | `--continue` |
| Resume a named/specific session | `--resume <session-name>` |
| Branch from shared baseline | `--fork-session` (with `--resume` / `--continue`) |
| Non-interactive / headless | `-p` / `--print` |
| JSON output | `--output-format json` |
| Enforce output schema | `--json-schema` (print mode `-p` only) |
| Least-privilege tools | `--allowedTools "Read,Grep"` |

Notes:

- `--fork-session` is the **CLI** flag. The Agent SDK option is `fork_session` (Python) / `forkSession` (TypeScript) — Q24 / Q42 / Q45 are SDK context.
- `--allowedTools` controls which tools run *without a permission prompt*; `--tools` restricts which tools are *available at all*. In headless `-p` mode `--allowedTools` effectively restricts, because prompts can't be approved — which is why it's the exam answer for CI least-privilege.

### Slash commands

| Command | Purpose |
|---|---|
| `/memory` | Show which memory files are loaded |
| `/compact` | Reduce context usage mid-session |

### tool_choice

| Value | Behavior |
|---|---|
| `"auto"` | May return text instead of calling a tool |
| `"any"` | Must call some tool |
| `{"type":"tool","name":"x"}` | Must call tool `x` |
| `"none"` | Prevents all tool use — text-only reply |

### Config mechanisms

| Mechanism | Shared with team? | Loaded when? |
|---|---|---|
| `./CLAUDE.md` | Yes (git) | Always |
| `~/.claude/CLAUDE.md` | No (personal) | Always |
| `.claude/rules/` + `paths:` | Yes | Only on matching file edits |
| `.claude/skills/SKILL.md` | Yes | On demand |
| `.claude/commands/` | Yes | Explicit invocation |
| `.mcp.json` | Yes | At connection |
| `~/.claude.json` | No (personal) | At connection |

Skill precedence on a same-name collision: **enterprise > personal > project > plugins**. (Opposite direction from settings precedence, where project overrides user.)

### Distractor patterns to eliminate on sight

- Switch to a larger model / bigger context window
- Adjust temperature
- Add an instruction to the system prompt (when a *guarantee* is required)
- Send everything to human review (disproportionate)
- Keep retrying (when the information isn't in the source)
- Return an empty result on error (indistinguishable from a valid empty result)
- Grant all tools / `--dangerously-skip-permissions`
- "Project skills always override personal ones" (backwards — personal wins on a name collision)

### Out of scope — don't over-study

Fine-tuning, API auth/billing, MCP server hosting & infra, model internals, RLHF/Constitutional AI, embeddings & vector DBs, computer use, vision, streaming/SSE, rate limits & pricing, OAuth/key rotation, cloud provider config, benchmarking, prompt-caching internals, tokenization.

---

*Source: Claude Certified Architect – Foundations Exam Guide v1.0 (Effective July 2026), §5 scenarios, §6 task statements 1.1–5.6, §17 Appendix.*
