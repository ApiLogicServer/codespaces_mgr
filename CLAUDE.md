@.github/copilot-instructions.md

## ⚠️ Codespaces: ApiLogicServer is pre-installed globally — no venv
This devcontainer is built `FROM apilogicserver/api_logic_server`, which already has
`ApiLogicServer` (and `als`, `genai-logic`, `logicbank`, `safrs`, `Flask`, etc.) installed
at `/usr/local/bin/python`.

- Do NOT create a `venv/` or `.venv/`, do NOT `pip install ApiLogicServer` — it's already there.
- Just run `als` / `genai-logic` / `python` directly — they resolve to the global install.
- If a command appears "not found," the issue is PATH/shell state, not a missing install —
  check `which als` / `which python` (should be `/usr/local/bin/...`) before assuming
  anything needs installing.
- If a debug/run session shows missing modules (e.g. `ModuleNotFoundError: No module
  named 'yaml'`) that work fine from a plain terminal, check for a stray
  `/workspaces/<repo>/.venv` or `venv` that VS Code is auto-activating
  (`python.terminal.activateEnvironment`). **Delete the stray venv** —
  do not `pip install` into it.

---


## Claude Code — dev-architecture context

**Explicit trigger only:** if the user says "load dev architecture", "load
dev-architecture.md", or any similar explicit phrase, read
`system/ApiLogicServer-Internal-Dev/dev-architecture.md` now and follow its mandatory
load sequence (see its header). Treat this phrase as a hard trigger, not a suggestion:
do it even if you believe the file is already in context.

Do NOT auto-load this file based on directory ancestry or "start of session" — only
the explicit phrase above triggers it. (Removed a prior ancestor-directory
auto-detection that fired on ANY first message in a session rooted under an
`ApiLogicServer-dev` checkout — including lightweight tasks like drafting a demo
prompt — silently costing a multi-thousand-line read the user never asked for. Val
confirmed explicit-only, 2026-09-03, after catching it firing during an unrelated
RFI-prompt demo session.)

**Confirmation must be ONE short line, nothing more** — no summary of what the file
contains, no list of what was learned, no restating the trigger back to the user.
Just: "Dev-architecture context loaded — gold-source workflow confirmed." (or equally
terse, but it MUST name the gold-source workflow specifically, not just "loaded"). Do
not explain, do not elaborate, do not offer next steps unless asked.

**Why the confirmation names the workflow specifically:** dev-architecture.md contains
a "GOLD SOURCE, EVERY EDIT" operating rule (its own header, near the top) — this
workspace is Val's test bench, not the product; edits made here without also fixing
gold source (`org_git/ApiLogicServer-src`, `org_git/Docs`) are invisible to every future
BLT run and every user. This rule has been silently skipped before even when the file
was nominally "loaded" (Aug 2026 incident — a CE fix landed 3 layers downstream of gold
before the gap was caught). A generic "context loaded" confirmation doesn't prove the
rule actually registered — naming it specifically gives Val something concrete to check
for. If the confirmation doesn't name it, that's the signal to ask for a retry.
