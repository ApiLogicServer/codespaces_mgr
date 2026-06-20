# Codespaces Prebuilds for codespaces_mgr

**Why:** `cs-mgr` (`codespaces_mgr` repo) gets frequent, casual edits — samples, CE, README.
Prebuilds make new codespaces start faster (cached container image), but cost storage +
Actions minutes every time they rebuild. We don't want a rebuild on every push, and there's
no "manual-only" trigger option — only **Every push**, **Configuration change**, or **Scheduled**.

`cs-mgr` has no branches (everything happens on `main`), so **Scheduled** risks freezing a
mid-edit, broken `main` on whatever day the schedule fires. **Configuration change** instead
only rebuilds when `.devcontainer/devcontainer.json` (or its referenced Dockerfile) changes —
never on ordinary content edits. That gives us an explicit, deliberate trigger under our
control, without GitHub's "manual" UI button being the only option.

**Where this is set:** GitHub web UI only — no REST API or `gh` CLI support exists for
managing or triggering prebuilds (confirmed via GitHub community discussion #55760).

## One-time setup (already done)

Repo → Settings → Codespaces → Prebuilds → configure for `main`, trigger = **Configuration
change**, region = US East.

## To refresh the prebuild after real changes

1. Finish your edits to `cs-mgr` and push to `main` as usual (no rebuild triggered).
2. When ready for a fresh prebuild: edit any line in `.devcontainer/devcontainer.json`
   (e.g. bump a comment) and push. This is the trigger — no script needed.
3. Confirm in repo → Settings → Codespaces → Prebuilds that a new run started.

## Also available

The prebuild's "⋯" menu has a "Manually trigger" action that works regardless of the
configured trigger type — an alternative to step 2 if you'd rather click a button.
