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

**Best-effort auto-load:** at the start of this session, check if any ancestor directory
of the current workspace is literally named `ApiLogicServer-dev` (framework dev checkout
signal, not an end-user Manager clone or Codespaces workspace). If so, silently read
`system/ApiLogicServer-Internal-Dev/dev-architecture.md` and follow its own mandatory
load sequence (see its header) — no need to ask first, just do it. Confirm with ONE
short line, e.g. "Dev-architecture context loaded." Then continue normally — this
never suppresses or replaces the `.github/copilot-instructions.md` welcome/activation
flow above; both can apply to the same first message.

If no such ancestor exists, skip this entirely — do not mention it.

**Reliable fallback trigger:** the auto-load above depends on the model treating it as
an unconditional first action, which doesn't always happen. If the user says "load dev
architecture", "load dev-architecture.md", or any similar explicit phrase — regardless
of whether the auto-load above already ran this session — read
`system/ApiLogicServer-Internal-Dev/dev-architecture.md` now and follow its mandatory
load sequence. Treat this phrase as a hard trigger, not a suggestion: do it even if you
believe the file is already in context.

**Confirmation must be ONE short line, nothing more** — no summary of what the file
contains, no list of what was learned, no restating the trigger back to the user.
Just: "Dev-architecture context loaded." (or equally terse). Do not explain, do not
elaborate, do not offer next steps unless asked.
