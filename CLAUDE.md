# Manager Workspace — Claude Code Instructions

## ⚠️ Codespaces: ApiLogicServer is pre-installed globally — no venv
This devcontainer is built `FROM apilogicserver/api_logic_server`, which already has
`ApiLogicServer` (and `als`, `genai-logic`, `logicbank`, `safrs`, `Flask`, etc.) installed
at `/usr/local/bin/python`.

- Do NOT create a `venv/`, do NOT `pip install ApiLogicServer` — it's already there.
- Just run `als` / `genai-logic` / `python` directly — they resolve to the global install.
- If a command appears "not found," the issue is PATH/shell state, not a missing install —
  check `which als` / `which python` (should be `/usr/local/bin/...`) before assuming
  anything needs installing.

---

## ⚠️ NEVER run `genai-logic genai`
Not the preferred approach. Do not run it, even for prompt files.

---

## ⚠️ PATH RULE for Manager root
All file operations use the project subdirectory as prefix — you are running from the Manager root, not inside the project:
- sqlite3 commands:    `sqlite3 <name>/database/db.sqlite "..."`
- genai-logic rebuild: `cd <name> && genai-logic rebuild-from-database --db_url=sqlite:///database/db.sqlite && cd ..`
- python seed:         `cd <name> && PROJECT_DIR=$(pwd) python database/test_data/alp_init.py && cd ..`
- file reads/writes:   `<name>/logic/logic_discovery/...`, `<name>/database/...`

---

## Follow the Manager CE (Method 4)
For all domain project creation, follow the Method 4 sequence in `.github/.copilot-instructions.md` exactly — STEP 1 through STEP 5, uninterrupted.

⚠️ STEP 5 is mandatory — do not skip it. Write `<name>/docs/requirements/readme.md` (provenance) and `<name>/docs/requirements/ad-libs.md` (every assumption or guess made beyond the prompt spec) before telling the user the project is done.
