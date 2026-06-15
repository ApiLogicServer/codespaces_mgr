We have a running app on CodeSpaces, so, it works.  It uses our docker container.

I believe making the *Manager* available will:

* promote trials
* be interesting to acquistors - zero friction, cloud on-ramp, way better than low-code or generic ai storefront for ent apps

Here are issues to work:

## 1. venv

Needs to work without fiddling.  It should - it's the global Python.

**Findings:**
- `.vscode/settings.json` already points to `${workspaceFolder}/venv/bin/python` — correct.
- But every `.devcontainer-option/devcontainer.json` (basic_demo, scaffold, samples/*, tests/*) hardcodes `"python.defaultInterpreterPath": "/usr/local/bin/python"` — leftover from when each sample was a standalone project with its own venv. Wrong for the Manager layout.
- No `.devcontainer` exists at the Manager root at all, so Codespaces falls back to a default Python, requiring manual interpreter selection.

**Recommendation:** Add a root-level `.devcontainer/devcontainer.json` with `python.defaultInterpreterPath` set to `${containerWorkspaceFolder}/venv/bin/python`, and a `postCreateCommand` that creates/primes `venv` before VS Code's Python extension first scans. Linked to issue 6 (Reload Window) — likely same root cause/fix.

**Manager venv creation command (confirmed from current Manager venv):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install ApiLogicServer
```
- Current Manager venv: Python 3.13.5, `ApiLogicServer==17.0.34` (pulls in `logicbank`, `safrs`, `Flask`, etc. as transitive deps — no `requirements.txt` at Manager root).
- `postCreateCommand` for the new devcontainer: `python3 -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install ApiLogicServer`

---

## ⏯️ Pick up here (next session)

**Status:** Plan agreed — copy this Manager to a new sibling project `mgr-for-cs` (under `build_and_test/`), excluding `venv/` (387M, local/platform-specific — recreated fresh via the command above), add a root `.devcontainer/devcontainer.json` (renamed from a new `-option` template) with the corrected `python.defaultInterpreterPath` + `postCreateCommand` above, `git init`, then push to a new GitHub repo and test in real Codespaces.

**Not yet done:** no copy, no `.devcontainer`, no `git init`, no push.

**Next steps:**
1. `rsync` copy `genai-logic/` → `../mgr-for-cs/` excluding `venv/`, `__pycache__/`, `logs/`
2. Create `mgr-for-cs/.devcontainer/devcontainer.json` (base on `basic_demo/.devcontainer-option/devcontainer.json`, fix `python.defaultInterpreterPath` → `${containerWorkspaceFolder}/venv/bin/python`, add `postCreateCommand` from above)
3. `git init` in `mgr-for-cs/`, commit
4. Create GitHub repo, push (confirm with user before push)
5. Open in Codespaces, verify: venv auto-selected, no "Reload Window" needed (issues #1 + #6)

## 2. samples / debugger

We want to be able to run the samples, with debug.  In local version, approach was open new vsc instance - sounds yucky for cs.  `als run` should work, but no debugger...

**Findings:**
- `.vscode/launch.json` (33K, many configs) is scoped to the Manager root — assumes debugging from here, not from a reopened sample folder.
- "Open new VSC instance" per sample = new browser tab/window in Codespaces — clunky, and likely related to issue 6.
- `als run` starts the server but attaches no debugger. No existing "attach to running process" (debugpy attach-by-port) launch config found.

**Recommendation:** Stay in the single Manager-root window. Add launch.json entries that:
  - target `<sample>/api_logic_server_run.py` directly with `cwd` set to the sample dir (debug samples without reopening), and/or
  - "Attach" config (debugpy attach-by-port) for a server already started via `als run --debug` (or equivalent), so no reopen is needed either way.

## 3. OBX / Tutorial

Manager readme says start here.  I have a sense that is proper for downloaders (== motivated), but a web tire-kicker might want something more shock & awe, ala  samples/prompts/genai_demo.prompt.  But, what of the tutorial?

**Findings:**
- README's "🚀 First Time Here?" (line 56) already splits "Do it" (basic_demo + guided tour, 30-45 min) vs. "Understand it" (basic_demo_logic_gov readme).
- `samples/prompts/genai_demo.prompt` is just a 5-line input spec — not shock & awe itself. The wow is the *output* of running `genai-logic create` against it (full API + Admin UI + rules in ~5 sec), but that's buried in README line 126 under "Additional Demos."

**Recommendation:** For Codespaces, pre-build a demo during container creation (`postCreateCommand` runs `genai-logic create` against genai_demo.prompt or basic_demo) so a working Admin UI/API is *already running* when the browser VS Code loads — tire-kicker sees a live system within seconds. Tutorial/OBX remains the "go deeper" path for motivated users — keep both, just sequence shock-and-awe first for Codespaces.

## 4. Kafka and Keycloak

Sound pretty heavy... maybe out of scope?  But, they are prominent in the mgr readme.

**Findings:**
- Both require `docker compose up` for a second container — heavy for a quick Codespaces trial; default Codespaces resource tier may struggle running devcontainer + Kafka + Keycloak together.
- Both are core to 2 of the 6 "Strategic Use Cases" in the README (EAI/Kafka demo, security/Keycloak demo).

**Recommendation:** Don't remove from the main catalog — instead mark Kafka/Keycloak demos as "**Local/Docker only — not yet in Codespaces**" in a Codespaces-specific README section (see issue 5), so expectations are set without losing the content.

## 5. OBX / Readme

So, do preceding 2 issues mean we want a tweaked readme

**Recommendation:** Yes — a separate, short `README-codespaces.md` (or a top section in the existing README, shown only in Codespaces) that:
  - Leads with the pre-built running demo (shock & awe, from issue 3)
  - Points to OBX/tutorial as the "go deeper" path for motivated downloaders
  - Flags Kafka/Keycloak demos as out-of-scope for the Codespaces quick path (issue 4)
  - Skips/abbreviates the existing "Setup Codespaces" section (README.md:766), which explains *how to get into* Codespaces — moot once you're already there.

## 6. Reliability

Both tries, I had to: Cmd+Shift+P → type "Reload Window" → Enter.

Can we allow for this?

**Findings:**
- No `.devcontainer` exists at Manager root — Codespaces likely falls back to a generic Python devcontainer/image, and the Python extension doesn't pick up `venv/bin/python` until a manual reload forces re-discovery.
- Open question: does `venv/` pre-exist (committed) or get created by a `postCreateCommand` *after* VS Code starts scanning for interpreters? If the latter, that's the classic race causing the reload requirement.

**Recommendation:** Same fix as issue 1 — root-level `.devcontainer/devcontainer.json` with correct interpreter path + `postCreateCommand` that primes the venv before first interpreter scan. Verify venv creation timing relative to VS Code startup.

## 7. AI Model

Is < Claude Sonnet 4.6.... up to the task??

**Findings:**
- README.md:48 already states: "We get consistently good results with Claude Sonnet 4.6 (GitHub Copilot or Claude Code extension). 'Ask' mode will not work — use Agent mode." This is an explicit, documented floor.
- Given the volume/complexity of the CE files (2000+ line copilot-instructions, mandatory multi-step "STOP ✋" protocols, strict rule-dependency-tracking conventions), smaller/older models are likely to skip steps.

**Recommendation:** Treat as already answered by the README — no further action unless an A/B test against a specific smaller model is wanted.

---

## Suggested priority order

1. **Root `.devcontainer/devcontainer.json`** — fixes #1 (venv/global Python) and #6 (Reload Window reliability) together; likely same root cause.
2. **Samples/debugger launch configs** (#2) — next-highest impact on "promote trials."
3. **Shock & awe pre-build + tweaked Codespaces README** (#3 + #5) — content/UX exercise, depends on #1 being solid.
4. **Kafka/Keycloak scoping note** (#4) — simple documentation change, can ride along with #5.
5. **AI Model** (#7) — no action needed; already documented.

---

## Repo / README changes log (from live Codespaces testing)

Tracking edits made to the repo as issues are found during real Codespaces sessions
(repo: `ApiLogicServer/codespaces_mgr`).

- `.devcontainer/devcontainer.json` — replaced unofficial `atariq11700.debugpy-old` with
  official `ms-python.debugpy`; fixed a total VS Code window hang on first file open.
- `.vscode/settings.json` — removed `workbench.editorAssociations` forcing `*.md` into
  the markdown-preview webview (was hanging on open). `.md` now opens as text; Preview
  button itself still doesn't render — **deferred** (UX issue, not session-blocking).
- `.vscode/launch.json` — moved "API Logic Server Run (run project from manager)" config
  to the top of the `configurations` array, so it's the default F5 target.
- `CLAUDE.md` — added note that ApiLogicServer is pre-installed globally in the
  Codespaces container (`/usr/local/bin/python`); agents should not create a `venv/` or
  `pip install ApiLogicServer`.
- `README.md` (AI Assistance section) — added note that the Chat panel may default to a
  non-Claude model in Codespaces; user must manually pick Claude Sonnet 4.6 via the model
  picker each session (no workspace-default setting exists for this in VS Code).
