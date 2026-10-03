---
name: answer-me-with-html
description: Render complex explanations as single-file HTML pages.
version: 0.2.2-hermes.1
author: QingYunA (@QingYunA), Hermes Agent adaptation
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [html, visualization, explainer, diagram, report]
    category: web-development
---

# Answer me with HTML Skill

Turn complex explanations into one self-contained HTML page. Hermes writes a compact extended-Markdown content draft; the bundled renderer owns layout, themes, diagrams, SVG placement, and STE writing checks. Keep this as a presentation layer: failure to render must never block the user's primary task.

## When to Use

Use this skill when at least one condition is true:

- The user explicitly asks for HTML, a visual explanation, a diagram, or a one-page explainer.
- The answer has at least three related concepts whose relationships matter.
- The answer describes a branched workflow, protocol, architecture, call chain, or state transition.
- The answer compares options across at least three dimensions.
- The answer explains a hierarchy, timeline, staged plan, or incident sequence.

Do not use it for short answers, copy-paste commands, routine code edits, casual chat, or when the user asks for plain text.

This skill is **not always-on**. A normal Hermes answer remains text unless the information benefits materially from a visual review surface.

## Prerequisites

- Node.js 20 or newer.
- Hermes' `terminal` tool.
- The bundled renderer at `${HERMES_SKILL_DIR}/scripts/am.mjs`.

The renderer is a prebuilt single file and needs no runtime package install or network access.

## How to Run

Invoke the bundled renderer through `terminal`. Default to `--no-open` so background, gateway, and remote sessions never steal focus:

````bash
AM='node "${HERMES_SKILL_DIR}/scripts/am.mjs"'
$AM render - --no-open <<'AM_EOF'
---
title: Example
---
## A Core answer
```callout ok Conclusion
The important point goes here.
```
AM_EOF
````

The renderer prints `✓ <path>` on success. Return the normal text conclusion first, then include the generated page path.

## Quick Reference

| Information shape | Component | Use for |
|---|---|---|
| Architecture or branching | `flow [LR]` | nodes, edges, decisions, fan-out |
| Messages over time | `sequence [num]` | request/response or actor interactions |
| Hierarchy | `tree [list]` | modules, folders, categories |
| Evolution | `timeline [v]` | incidents, phases, history |
| Values versus limits | `limits` | quotas or measured thresholds |
| Inline critique | `annot` | phrase-by-phrase notes |
| Metadata | `kv [cols=2]` | compact facts or status |
| Conclusion or warning | `callout` | the first thing the reader should see |
| Multi-dimensional comparison | Markdown table | trade-offs and can/cannot matrices |

Useful renderer commands:

```bash
node "${HERMES_SKILL_DIR}/scripts/am.mjs" list
node "${HERMES_SKILL_DIR}/scripts/am.mjs" help format
node "${HERMES_SKILL_DIR}/scripts/am.mjs" help flow
node "${HERMES_SKILL_DIR}/scripts/am.mjs" config
```

Do not change renderer config unless the user asks.

## Procedure

1. **Answer first.** Decide the core conclusion before designing the page.
2. **Choose 2-8 panels.** Each panel answers one sub-question; do not add panels just for decoration.
3. **Match shape to component.** Prefer `flow`, `sequence`, `tree`, `timeline`, `limits`, `annot`, `kv`, `callout`, or Markdown tables.
4. **Draft content only.** Do not hand-author layout, CSS, or SVG coordinates.
5. **Render once with `--no-open`.** Read the renderer output.
6. **Repair narrowly.** If the renderer reports a line/component error or STE warning, fix only the affected draft. Retry at most twice.
7. **Report compactly.** Give the user the key conclusion and the HTML path. The HTML is a review surface, not a replacement for the conversational answer.

A minimal draft looks like this:

````markdown
---
template: sheet
theme: blueprint
title: System overview
cols: 3
---
The system has one critical path and two non-blocking side paths.

## A Conclusion {span=2}
```callout ok Main point
Keep the critical path small; render diagnostics off to the side.
```

## B Architecture
```flow LR
Input -> Core: required
Core --> Audit: non-blocking
Core --> Report: non-blocking
```
````

## Pitfalls

- **Do not make it a pipeline dependency.** Rendering failure must not fail research, coding, backtests, monitoring, or message delivery.
- **Do not enable high-frequency/always-on behavior by default.** Use the decision rules above.
- **Do not auto-open pages by default.** Use `--no-open`; open only when the user explicitly asks.
- **Do not invent numbers.** Use `limits` only with real values, and label illustrative data as illustrative.
- **Do not hand-write HTML/CSS/SVG** when a built-in component can express the idea.
- **Avoid raw `html`/`svg` passthrough for untrusted markup.** Prefer renderer components; never inject untrusted user markup as executable HTML.
- **Do not hide the answer in the artifact.** The chat reply must still state the main conclusion.
- **Do not retry indefinitely.** Two render repairs are enough; preserve the useful text answer if the artifact remains imperfect.

## Verification

Check the bundled renderer:

```bash
node "${HERMES_SKILL_DIR}/scripts/am.mjs" --version
```

Expected version: `0.2.2`.

Then render a smoke page with `--no-open` and verify that:

1. the command exits with status 0;
2. stdout starts with `✓` and names an HTML file;
3. the file is self-contained and opens without a CDN;
4. the primary Hermes answer still works if the render step is skipped or fails.

Upstream: https://github.com/QingYunA/answer-me-with-html (MIT). The bundled renderer is upstream version 0.2.2; this file only adapts invocation and usage policy for Hermes.
