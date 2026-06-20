#!/usr/bin/env python3
"""
Recreate the codespaces_mgr checkout from this local-mgr + Codespaces-only overrides.

Usage (from this Manager root):
    python3 .devcontainer-codespaces/create_codespaces_mgr.py /path/to/org_git/codespaces_mgr [--dry-run|--push|--release]

    (no flag) : sync files into target, leave staged for manual review (does NOT commit/push)
    --dry-run : show what would be copied, apply no changes
    --push    : sync + commit + push to the target repo's `dev` branch (day-to-day update)
    --release : sync + commit + push to `dev`, then merge dev->main, tag main with the
                gold-source product version, bump .devcontainer/devcontainer.json (triggers
                the repo's "Configuration change" prebuild refresh), push main + tag,
                and leave the target checked out on `dev`.

What the sync does:
    1. Copy a scoped subset of local-mgr -> target (see SYNC_PATHS below).
       Excludes basic_demo/, scaffold/, tests/, dockers/, demo_customs/, demo_eai/, venv/.
       (.devcontainer-codespaces/ IS synced — it becomes .devcontainer/ in step 2)
    2. Apply Codespaces-only overrides:
       - rename .devcontainer-codespaces -> .devcontainer
       - CLAUDE.md.append  -> prepended to CLAUDE.md (idempotent)
       - gitignore.append  -> appended to .gitignore (idempotent)
       - README.md         -> strip front matter + <style> block; inject browser/CS notes
       - .vscode/settings.json -> python.defaultInterpreterPath -> /usr/local/bin/python
       - .vscode/launch.json  -> replaced with Codespaces-trimmed 2-config version
       - samples/*/. vscode/settings.json -> same interpreter patch

--release reads the product version from this sibling file (under org_git/, alongside
codespaces_mgr) rather than from any README front matter, since that's the file Val
actually bumps for a real release:
    org_git/ApiLogicServer-src/api_logic_server_cli/api_logic_server.py  (__version__ = "...")
"""

import sys
import re
import shutil
import subprocess
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
SRC_ROOT   = SCRIPT_DIR.parent          # Manager root
OVERRIDES  = SCRIPT_DIR                 # .devcontainer-codespaces/

SYNC_PATHS = [
    ".claude",
    ".devcontainer-codespaces",
    ".env",
    ".github",
    ".gitignore",
    ".vscode",
    "CLAUDE.md",
    "CodeSpaces.md",
    "README.md",
    "readme_vibe.md",
    "samples",
    "system",
    "webgenai",
]

COPY_EXCLUDES = {
    ".git", "venv", ".venv", "__pycache__", "logs", ".DS_Store", ".devcontainer",
}

# ── helpers ──────────────────────────────────────────────────────────────────

def ignore_fn(dir_, names):
    return {n for n in names if n in COPY_EXCLUDES}


def copy_path(src: Path, dst: Path, dry_run: bool):
    if not src.exists():
        print(f"  (skip, not in local-mgr: {src.name})")
        return
    if dry_run:
        print(f"  [dry-run] would copy {src} -> {dst}")
        return
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=ignore_fn)
        print(f"  ✅ {src.name}/")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✅ {src.name}")


def find_gold_version() -> str:
    """Read __version__ from ApiLogicServer-src/api_logic_server_cli/api_logic_server.py.

    Located by walking up from SRC_ROOT to org_git/, then into ApiLogicServer-src/ —
    works regardless of whether SRC_ROOT is the BLT workspace or the seminal Manager,
    as long as both live under the same org_git/ parent as codespaces_mgr.
    """
    org_git = SRC_ROOT
    for _ in range(6):
        org_git = org_git.parent
        candidate = org_git / "ApiLogicServer-src" / "api_logic_server_cli" / "api_logic_server.py"
        if candidate.exists():
            text = candidate.read_text()
            m = re.search(r'__version__\s*=\s*"([^"]+)"', text)
            if not m:
                raise SystemExit(f"ERROR: no __version__ line found in {candidate}")
            return m.group(1)
    raise SystemExit(
        "ERROR: could not locate ApiLogicServer-src/api_logic_server_cli/api_logic_server.py "
        "by walking up from local-mgr — expected it under the same org_git/ parent as codespaces_mgr."
    )


def run_git(args, cwd: Path, check=True):
    print(f"  $ git {' '.join(args)}")
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.stdout.strip():
        print("    " + result.stdout.strip().replace("\n", "\n    "))
    if check and result.returncode != 0:
        print("    " + result.stderr.strip().replace("\n", "\n    "))
        raise SystemExit(f"ERROR: git {' '.join(args)} failed (exit {result.returncode})")
    return result


def patch_interpreter(path: Path):
    """Replace any python.defaultInterpreterPath value with /usr/local/bin/python."""
    text = path.read_text()
    new  = re.sub(
        r'"python\.defaultInterpreterPath":\s*"[^"]*"',
        '"python.defaultInterpreterPath": "/usr/local/bin/python"',
        text,
    )
    if new != text:
        path.write_text(new)
        return True
    return False


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: create_codespaces_mgr.py /path/to/org_git/codespaces_mgr [--dry-run|--push|--release]")
        sys.exit(1)

    target  = Path(sys.argv[1]).resolve()
    dry_run = "--dry-run" in sys.argv
    push    = "--push" in sys.argv
    release = "--release" in sys.argv

    if not (target / ".git").exists():
        print(f"ERROR: {target} does not look like a git checkout (no .git) — refusing.")
        sys.exit(1)

    if push or release:
        status = run_git(["status", "--porcelain"], cwd=target).stdout
        if status.strip():
            raise SystemExit(
                f"ERROR: {target} has uncommitted changes before the sync even starts — "
                "commit, stash, or discard them first, then re-run."
            )
        run_git(["checkout", "dev"], cwd=target)
        run_git(["pull", "--ff-only", "origin", "dev"], cwd=target)

    print(f"Source (local-mgr): {SRC_ROOT}")
    print(f"Target (codespaces_mgr): {target}")
    if dry_run:
        print("Mode: DRY RUN — no changes will be made")
    print()

    # ── Step 1: sync scoped subset ────────────────────────────────────────────
    print("Step 1: Syncing scoped subset...")
    for p in SYNC_PATHS:
        copy_path(SRC_ROOT / p, target / p, dry_run)

    if dry_run:
        print("\nDry run complete — no overrides applied.")
        return

    print()

    # ── Step 2: Codespaces-only overrides ────────────────────────────────────

    # .devcontainer-codespaces/ -> .devcontainer/
    print("Step 2a: Renaming .devcontainer-codespaces -> .devcontainer...")
    dc_src = target / ".devcontainer-codespaces"
    dc_dst = target / ".devcontainer"
    if dc_dst.exists():
        shutil.rmtree(dc_dst)
    dc_src.rename(dc_dst)
    print("  ✅ .devcontainer/")

    # CLAUDE.md — prepend Codespaces venv warning after title line
    print("Step 2b: Applying CLAUDE.md override...")
    claude_path   = target / "CLAUDE.md"
    claude_append = (OVERRIDES / "CLAUDE.md.append").read_text()
    claude_text   = claude_path.read_text()
    if "ApiLogicServer is pre-installed globally" not in claude_text:
        lines      = claude_text.splitlines(keepends=True)
        title_line = lines[0]
        rest       = "".join(lines[1:])
        claude_path.write_text(title_line + "\n" + claude_append + "\n" + rest)
        print("  ✅ CLAUDE.md prepended")
    else:
        print("  (already present, skipped)")

    # .gitignore — append .venv/ if not present
    print("Step 2c: Applying .gitignore override...")
    gi_path   = target / ".gitignore"
    gi_append = (OVERRIDES / "gitignore.append").read_text()
    gi_text   = gi_path.read_text()
    if ".venv/" not in gi_text.splitlines():
        if not gi_text.endswith("\n"):
            gi_path.write_text(gi_text + "\n")
        with gi_path.open("a") as f:
            f.write(gi_append)
        print("  ✅ .gitignore appended")
    else:
        print("  (already present, skipped)")

    # README.md — strip front matter + style block, inject CS/browser notes
    print("Step 2d: Patching README.md...")
    readme_path = target / "README.md"
    readme      = readme_path.read_text()

    # Strip YAML front matter
    readme = re.sub(r"^---\n.*?\n---\n", "", readme, count=1, flags=re.DOTALL)
    # Strip <style>...</style>
    readme = re.sub(r"<style>.*?</style>\n?", "", readme, count=1, flags=re.DOTALL)
    # Strip any leading blank lines left by the above
    readme = readme.lstrip("\n")
    print("  ✅ Front matter and style block stripped")

    # Inject Codespaces + browser notes inside "See it work" (idempotent)
    # Match on the stable "<summary>⚡ See it work" prefix — the text after the
    # em-dash is gold-source copy (org_git/Docs) and changes independently of this script.
    summary_re = re.compile(r"<summary>⚡ See it work[^<]*</summary>")
    if "Use Chrome or Edge" not in readme:
        cs_note = (
            "\n&nbsp;\n\n"
            "You're already running in GitHub Codespaces — a cloud VS Code environment "
            "in your browser. Nothing to install. (Use Chrome or Edge — Safari has known "
            "compatibility issues with VS Code in the browser.)\n"
        )
        match = summary_re.search(readme)
        if not match:
            raise SystemExit(
                "ERROR: no '<summary>⚡ See it work...</summary>' line found in README.md — "
                "update this script's summary_re pattern to match the current heading."
            )
        readme = readme[:match.end()] + cs_note + readme[match.end():]
        print("  ✅ Codespaces + browser notes injected")
    else:
        print("  (notes already present, skipped)")

    readme_path.write_text(readme)

    # .vscode/settings.json — global interpreter (Manager root)
    print("Step 2e: Patching .vscode/settings.json (Manager root)...")
    settings = target / ".vscode" / "settings.json"
    if patch_interpreter(settings):
        print("  ✅ Manager root settings.json patched")
    else:
        print("  (already correct, skipped)")

    # .vscode/launch.json — replace with Codespaces-trimmed 2-config version
    print("Step 2f: Replacing .vscode/launch.json with Codespaces-trimmed version...")
    shutil.copy2(OVERRIDES / "launch.json", target / ".vscode" / "launch.json")
    print("  ✅ launch.json replaced")

    # samples/*/. vscode/settings.json — global interpreter for all samples
    print("Step 2g: Patching samples/*/. vscode/settings.json...")
    for f in sorted((target / "samples").glob("*/.vscode/settings.json")):
        if patch_interpreter(f):
            print(f"  ✅ {f.parent.parent.name}")

    if not push and not release:
        print()
        print("Done. Review changes in target, then commit and push:")
        print(f"  cd {target} && git status")
        return

    # ── Step 3: commit + push to dev ─────────────────────────────────────────
    print()
    print("Step 3: Committing + pushing to dev...")
    run_git(["add", "-A"], cwd=target)
    status = run_git(["status", "--porcelain"], cwd=target).stdout
    if not status.strip():
        print("  (nothing changed — dev already up to date with local-mgr)")
    else:
        gold_version = find_gold_version()
        run_git(["commit", "-m", f"Sync from local-mgr (gold v{gold_version})"], cwd=target)
        run_git(["push", "origin", "dev"], cwd=target)
        print("  ✅ pushed to dev")

    if not release:
        print()
        print(f"Done — {target} is on dev, pushed. Re-run with --release to publish to main.")
        return

    # ── Step 4: release — merge to main, tag, bump prebuild trigger ─────────
    print()
    print("Step 4: Releasing — merging dev -> main...")
    gold_version = find_gold_version()
    existing_tags = run_git(["tag", "-l"], cwd=target).stdout.split()
    if gold_version in existing_tags:
        raise SystemExit(
            f"ERROR: tag '{gold_version}' already exists — the gold-source product version "
            f"(api_logic_server.py __version__) hasn't been bumped since the last cs-mgr "
            f"release. Bump it there first if this is meant to be a new release."
        )

    run_git(["checkout", "main"], cwd=target)
    run_git(["pull", "--ff-only", "origin", "main"], cwd=target)
    merge = run_git(["merge", "dev", "--no-edit"], cwd=target, check=False)
    if merge.returncode != 0:
        raise SystemExit(
            "ERROR: merge dev -> main failed (likely a conflict). Repo is left mid-merge on "
            "main — resolve manually, or `git merge --abort` and re-run --release.\n"
            + merge.stderr
        )

    # Bump devcontainer.json (any whitespace-only touch) to trigger the
    # "Configuration change" prebuild refresh on push.
    devcontainer_json = target / ".devcontainer" / "devcontainer.json"
    text = devcontainer_json.read_text()
    timestamp_re = re.compile(r'(// last released: )(\S+)')
    if timestamp_re.search(text):
        text = timestamp_re.sub(rf"\g<1>{gold_version}", text)
    else:
        text = f"// last released: {gold_version}\n" + text
    devcontainer_json.write_text(text)
    run_git(["add", ".devcontainer/devcontainer.json"], cwd=target)
    run_git(["commit", "-m", f"Release {gold_version}: bump devcontainer.json to refresh prebuild"], cwd=target)

    run_git(["push", "origin", "main"], cwd=target)
    run_git(["tag", gold_version], cwd=target)
    run_git(["push", "origin", gold_version], cwd=target)

    run_git(["checkout", "dev"], cwd=target)
    run_git(["merge", "main", "--no-edit"], cwd=target)
    run_git(["push", "origin", "dev"], cwd=target)

    print()
    print(f"✅ Released {gold_version}: dev -> main merged, tagged, pushed.")
    print(f"   {target} is left on dev.")
    print("   Prebuild refresh should start automatically (devcontainer.json changed on main).")


if __name__ == "__main__":
    main()
