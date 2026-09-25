---
name: problem-statement-generator
description: Explores the dataset(s) in a project directory and drafts a Problem_Statement.md that articulates what the project is trying to solve. Use this whenever the user asks "what is the problem statement of this project," "what is this project trying to solve," "what problem does this project address," or otherwise wants a data project's purpose/goal articulated in writing. Also use if the user asks to (re)generate, write, or update a project's problem statement. Always inspects actual file contents (not just filenames) before writing, and always checks in with the user for a bit of extra context before drafting.
---

# Problem Statement Generator

Generates a `Problem_Statement.md` file for a data project by actually inspecting the data in the project directory, asking the user a couple of clarifying questions, and synthesizing both into a clear, well-written problem statement.

## When this triggers

- "What is the problem statement of this project?"
- "What is this project trying to solve?"
- "What problem does this data address?"
- "Can you write/generate a problem statement for this project?"
- Any request to create, refresh, or rewrite a project's problem statement document.

## Workflow

### Step 1: Check for an existing Problem_Statement.md

Look in the project directory (the directory containing the dataset(s) — usually the current working directory or the folder the user points to) for a file named `Problem_Statement.md` (case-insensitive match is fine, e.g. `problem_statement.md`).

- **If it already exists**: read it, show the user a brief summary of what's already there, and ask whether they want to overwrite it, revise it, or leave it alone. Do not proceed to regenerate it until they confirm they want a new/updated version.
- **If it doesn't exist**: proceed to Step 2.

### Step 2: Explore the dataset

Find the data files in the project directory (csv, tsv, xlsx, json, parquet, sqlite/db, txt logs, etc. — whatever is there). For each relevant file, actually inspect its contents, not just its name:

- Column/field names and inferred types
- Row/record counts and general shape
- A sample of actual rows/values
- Obvious quality signals worth noting (missing values, date ranges, categorical distributions, notable outliers)
- If there are multiple files, how they relate to each other (shared keys, apparent joins, separate domains)

Use bash/pandas (or equivalent) for this rather than guessing from filenames alone — the goal is to understand what the data actually contains before drafting anything. If the directory has a README, data dictionary, or similar doc, read that too.

Keep this exploration efficient: skim/sample large files rather than loading everything, and summarize what you learn as you go so you can report it back to the user.

### Step 3: Ask the user for context

Before drafting, always ask the user 1–2 short questions to fill in what the data alone can't tell you — things like:

- Who is this project for, or what decision/action will it inform?
- Is there a specific business question, goal, or hypothesis driving this?
- Any known constraints, scope boundaries, or things to explicitly exclude?

Tailor the questions to what's actually ambiguous after Step 2 — if the data exploration already made the domain and goal fairly obvious, keep the questions light (e.g., a single confirming question) rather than asking generic ones. Use `ask_user_input_v0` if available so the user can answer quickly; otherwise ask inline in the conversation. Wait for their reply before writing the file.

### Step 4: Draft the problem statement

Write `Problem_Statement.md` in the project directory. There's no fixed template — use your judgment on structure based on the project, but a strong problem statement typically covers:

- **What the project is about** — plain-language framing grounded in what the data actually contains
- **The core problem/question** being addressed
- **Why it matters** — who cares about the answer and what they'll do with it
- **Scope** — what's in bounds and out of bounds, if relevant
- **What the data offers** — a brief, honest note on what's available to work with (and any notable gaps or limitations found during exploration)

Write it as prose a stakeholder could read cold — clear and specific, grounded in real details from the data (actual column names, real ranges/counts, real categories) rather than generic boilerplate. Avoid padding it with sections that don't add value for this particular project.

### Step 5: Save and confirm

Save the file as `Problem_Statement.md` in the project directory (overwriting only after the Step 1 confirmation, if applicable). Let the user know it's there and briefly summarize what you wrote, so they can quickly sanity-check it against what they know.

## Notes

- Never fabricate details about the data or the project's purpose — everything in the statement should trace back either to something actually found in the data or something the user told you.
- If the project directory has no data files at all, say so plainly and ask the user what they'd like the problem statement to be based on, rather than inventing a dataset.
