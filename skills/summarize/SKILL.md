---
name: summarize
description: Write a structured summary of an article, document, or URL. Supports two modes — concise (default, fast overview) and verbose (in-depth tutorial-style breakdown, optionally rendered as a standalone HTML tutorial). Use when the user shares a URL, pastes text, or asks to summarize, explain, or "make a tutorial from" content.
allowed-tools: [Read, Write, WebFetch, WebSearch]
---

# summarize

Produce a structured summary of the provided article, document, or text. The goal is to preserve every key idea, argument, insight, and important context — while simplifying complex language, improving flow, and stripping unnecessary repetition or filler.

The skill has **two modes**. Pick one before drafting; do not mix them.

| Mode | When to use | Output |
|------|-------------|--------|
| **Concise** (default) | Quick reference, news pieces, blog posts, anything the user wants to skim in 1–2 minutes | Markdown summary, in chat — with a prompt to also save as `.md` file |
| **Verbose** | Long-form essays, research papers, technical deep-dives, or any request that uses words like "tutorial", "deep dive", "explain in detail", "teach me", "in depth" | Tutorial-style breakdown. Markdown by default; **HTML file** when the source is technical / instructional (code, APIs, frameworks, how-to guides) or when the user requests HTML |

If the user does not specify a mode, infer from the request:
- "summarize this", "tldr", "give me the gist" → **concise**
- "explain this in detail", "make a tutorial", "deep dive", "walk me through" → **verbose**
- Ambiguous and the source is >3000 words of technical content → ask the user which mode

## Input

The user will provide one of:
- A URL (fetch with WebFetch)
- Pasted text or a quote
- A file path (use Read)

If no content is provided, ask for it.

## Process (both modes)

1. **Read the full source.** Do not skim. For long URLs, fetch the page; if it appears truncated, fetch again with a targeted prompt to recover missing sections.
2. **Map the structure** before writing: thesis, supporting arguments, evidence, examples, caveats, conclusion.
3. **Draft** in the format for the chosen mode.
4. **Edit for clarity.** Simplify jargon where it does not lose meaning. Remove filler, hedges, repetition.
5. **Cite the source** (URL, title, author, date) at the top of every output.

---

## Mode 1 — Concise

A fast-to-read markdown summary, delivered in chat. Omit sections that genuinely do not apply.

```markdown
## [Title of Article / Document]
*Source: [URL or file name] — [Author, if known] — [Date, if known]*

### 🎯 Key Takeaways
- 3–5 bullets. The most important conclusions, insights, or action items from the piece.
- Each bullet stands alone — a reader skimming only this section should walk away with the core value.
- Lead with the most important takeaway first.

### TL;DR
One to three sentences. The core thesis or finding in prose form.

### Background & Context
What the reader needs to know to understand the piece. 2–4 sentences. Skip if the article itself supplies no prior context.

### Key Points
- Concise bullets, one idea per bullet. Preserve the author's reasoning, not just conclusions.
- Use sub-bullets only when a point has a qualification that changes its meaning.

### Notable Insights / Quotes
1–3 striking observations or well-phrased passages worth preserving verbatim (use blockquotes). Skip if nothing stands out.

### So What?
What this means in practice, or what questions it leaves open. 2–4 sentences.
```

**Rule:** Key Takeaways always comes first, immediately after the source citation. Never bury it below other sections.

Target length: roughly **5–10% of the source word count**, capped at ~600 words.

### Saving to a file

After delivering the concise summary in chat, **always ask the user**:

> Would you like me to save this summary as a markdown file? (e.g., `./<slug>-summary.md`)

- Slug = lowercased, hyphenated title, max 6 words.
- Only write the file if the user says yes. Default location is the current working directory unless the user specifies otherwise.
- Skip the prompt only if the user already said upfront they want (or don't want) a file.

---

## Mode 2 — Verbose (Tutorial)

A comprehensive, instructional breakdown. Treat the source as raw material for teaching the reader the subject — not just summarizing it. Include examples, definitions, diagrams (as ASCII or mermaid), and step-by-step explanations.

### Verbose markdown structure

```markdown
# [Title] — In-Depth Tutorial
*Source: [URL / file] — [Author] — [Date] — Estimated read time: [X min]*

## 🎯 Key Takeaways
- 5–7 bullets. The most important conclusions, insights, lessons, or action items from the source.
- Lead with the highest-impact takeaway. Each bullet should be self-contained.
- A reader who only reads this section should walk away with the core value of the entire piece.

## Overview
A 1-paragraph orientation: what the piece is about, why it matters, and what the reader will know after finishing this tutorial.

## Prerequisites
What the reader should already know (concepts, tools, vocabulary). Define unfamiliar terms inline.

## Table of Contents
- Linked list of all major sections below.

## 1. Background & Motivation
The problem the piece addresses, prior context, and why current solutions fall short. Cite specifics from the source.

## 2. Core Concepts
For each major concept introduced:
- **Definition** in plain English.
- **Why it matters** — the role it plays in the larger argument.
- **Example** — concrete illustration, ideally the author's own; if absent, generate a faithful one.
- **Common misconceptions** if the source flags any.

## 3. Detailed Walkthrough
Section-by-section breakdown of the source's argument or method. For each:
- What the author claims or does
- The evidence, reasoning, or steps they use
- Code blocks, equations, or diagrams where helpful (preserve original code verbatim; annotate it with comments)
- Edge cases, caveats, and exceptions the author notes

## 4. Worked Example(s)
If the source is technical: a full end-to-end example, with inputs, intermediate steps, and outputs. If the source is argumentative: a real-world scenario where the argument applies.

## 5. Deeper Insights
The non-obvious "aha" points and supporting reasoning behind the Key Takeaways at the top. Phrase as standalone lessons with the evidence or context that backs them up.

## 6. Limitations & Open Questions
What the source does not address, what assumptions it makes, what critics might push back on. Mark anything that is your inference (not the author's) as *[Analysis]*.

## 7. Glossary
Definitions of every term of art used in the tutorial. Alphabetical.

## 8. Further Reading
Links, citations, or related works mentioned in the source. Add 1–3 authoritative suggestions of your own only if directly relevant, marked *[Suggested]*.

## Appendix: Original Quotes
2–5 passages worth preserving verbatim, as blockquotes with section references.
```

Target length: roughly **30–60% of the source word count**. No cap — completeness over brevity. Use tables, code blocks, and diagrams freely.

### HTML tutorial output

For verbose mode, produce a **standalone HTML file** instead of (or in addition to) markdown when any of these hold:
- The user asks for HTML, a "tutorial page", or something "I can open in a browser"
- The source is technical/instructional (code, APIs, frameworks, configs, how-tos) and would benefit from syntax highlighting, collapsible sections, or anchored navigation
- The summary is long enough (>2000 words) that markdown in chat becomes unwieldy

**File:** write to `./<slug>-tutorial.html` in the current working directory (slug = lowercased, hyphenated title, max 6 words).

**HTML requirements** — single self-contained file, no external dependencies:

- `<!DOCTYPE html>`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, descriptive `<title>`.
- **Embedded CSS** in `<style>`. Clean, readable typography: system font stack, max-width ~760px centered, generous line-height (1.6+), comfortable spacing. Dark-mode aware via `@media (prefers-color-scheme: dark)`.
- **Sticky/side table of contents** with anchor links to every `<h2>`.
- **Syntax-highlighted code blocks.** Use Prism.js or highlight.js via CDN *only if* the user has network access; otherwise hand-roll minimal CSS classes for `.token-keyword`, `.token-string`, `.token-comment`, etc. Prefer the CDN route — it's smaller and more capable.
- **Callout boxes** for notes, warnings, examples (styled `<aside>` or `<div class="callout note|warning|example">`).
- **Collapsible sections** via `<details><summary>` for long appendices, glossary, and worked examples.
- **Diagrams** rendered with Mermaid (CDN) or inline SVG. Fall back to ASCII inside `<pre>` if neither is appropriate.
- **Print-friendly** via `@media print` — hide TOC, expand all `<details>`, use serif font.
- Source citation at the top in a `<header>`; "Generated [date]" footer.

After writing the file, report the absolute path and a one-line summary. Do **not** dump the full HTML into chat.

---

## Style rules (both modes)

- Write in plain English. Prefer short sentences. Avoid nominalizations ("the utilization of" → "using").
- Never editorialize or inject opinions not present in the source. Mark your own analysis as *[Analysis]* when it must be included.
- Do not pad with meta-commentary ("This article explores…", "The author argues that…") — state the idea directly.
- Preserve precision in technical material; simplify only where a simpler word carries the same meaning.
- Preserve code, equations, and quoted passages verbatim.
- When the source contradicts itself or is ambiguous, surface it — do not paper over.
