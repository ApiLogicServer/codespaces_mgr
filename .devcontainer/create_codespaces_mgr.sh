#!/bin/bash
# Recreate the codespaces_mgr checkout from this local-mgr + Codespaces-only overrides.
#
# Usage (from this Manager root):
#   .devcontainer-codespaces/create_codespaces_mgr.sh /path/to/org_git/codespaces_mgr [--dry-run]
#
#   --dry-run : preview rsync changes only (passes -n to rsync, skips overrides
#               and does not touch the target at all)
#
# What it does:
#   1. rsync a SCOPED SUBSET of this local-mgr -> <target> (see SYNC_PATHS below).
#      codespaces_mgr is a deliberate trimmed-down trial repo, NOT a full mirror -
#      it does not include basic_demo/, scaffold/, tests/, dockers/,
#      demo_customs/, demo_eai/, or venv/.
#      (.devcontainer-codespaces/ IS synced - it becomes .devcontainer/ in step 2)
#   2. Apply Codespaces-only overrides:
#      - rename <target>/.devcontainer-codespaces -> <target>/.devcontainer
#        (overwriting any .devcontainer copied from local-mgr)
#      - CLAUDE.md.append     -> prepended to <target>/CLAUDE.md (if not already present)
#      - gitignore.append     -> appended to <target>/.gitignore (if not already present)
#      - .vscode/settings.json -> python.defaultInterpreterPath rewritten from
#        local-mgr's "${workspaceFolder}/venv/bin/python" to "/usr/local/bin/python"
#        (codespaces-mgr has no venv/ - ApiLogicServer is installed globally)
#   3. Leaves <target> staged for review/commit (does NOT commit or push)

set -euo pipefail

TARGET="${1:?Usage: create_codespaces_mgr.sh /path/to/org_git/codespaces_mgr [--dry-run]}"
DRY_RUN=""
[ "${2:-}" = "--dry-run" ] && DRY_RUN="-n"
SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERRIDES="$SRC_ROOT/.devcontainer-codespaces"

if [ ! -d "$TARGET/.git" ]; then
    echo "ERROR: $TARGET does not look like a git checkout (no .git) - refusing to overwrite."
    exit 1
fi

echo "Source (local-mgr): $SRC_ROOT"
echo "Target (codespaces_mgr): $TARGET"
[ -n "$DRY_RUN" ] && echo "Mode: DRY RUN (rsync preview only, no overrides applied)"
echo

# 1. Sync only the paths codespaces_mgr actually contains - a curated trial subset
#    of local-mgr, not a full mirror. Excludes basic_demo/, scaffold/, tests/,
#    dockers/, demo_customs/, demo_eai/, venv/ (dev/test infra not relevant to a
#    Codespaces trial repo).
#    (.devcontainer-codespaces/ IS synced - it becomes .devcontainer/ below)
SYNC_PATHS=(
    .claude
    .devcontainer-codespaces
    .env
    .github
    .gitignore
    .vscode
    CLAUDE.md
    CodeSpaces.md
    README.md
    readme_vibe.md
    samples
    system
    webgenai
)

for p in "${SYNC_PATHS[@]}"; do
    src="$SRC_ROOT/$p"
    [ -e "$src" ] || { echo "  (skip, not in local-mgr: $p)"; continue; }
    if [ -d "$src" ]; then
        rsync -av $DRY_RUN --delete \
            --exclude='.git/' \
            --exclude='venv/' \
            --exclude='.venv/' \
            --exclude='__pycache__/' \
            --exclude='logs/' \
            --exclude='.DS_Store' \
            --exclude='.devcontainer/' \
            "$src/" "$TARGET/$p/"
    else
        rsync -av $DRY_RUN "$src" "$TARGET/$p"
    fi
done

if [ -n "$DRY_RUN" ]; then
    echo
    echo "Dry run complete - no changes made, overrides (step 2) skipped."
    exit 0
fi

# 2. Apply Codespaces-only overrides

# .devcontainer-codespaces/ -> .devcontainer/ (rename, like per-project -option convention)
echo
echo "Renaming .devcontainer-codespaces -> .devcontainer..."
rm -rf "$TARGET/.devcontainer"
mv "$TARGET/.devcontainer-codespaces" "$TARGET/.devcontainer"

# CLAUDE.md - prepend Codespaces venv warning (after the title line) if not already present
echo "Applying CLAUDE.md override..."
if ! grep -q "ApiLogicServer is pre-installed globally" "$TARGET/CLAUDE.md"; then
    TITLE_LINE=$(head -1 "$TARGET/CLAUDE.md")
    {
        echo "$TITLE_LINE"
        echo
        cat "$OVERRIDES/CLAUDE.md.append"
        echo
        tail -n +2 "$TARGET/CLAUDE.md"
    } > "$TARGET/CLAUDE.md.tmp"
    mv "$TARGET/CLAUDE.md.tmp" "$TARGET/CLAUDE.md"
else
    echo "  (already present, skipped)"
fi

# .gitignore - append .venv/ if not already present
echo "Applying .gitignore override..."
if ! grep -qx ".venv/" "$TARGET/.gitignore"; then
    # ensure file ends with a newline before appending
    [ -n "$(tail -c1 "$TARGET/.gitignore")" ] && echo >> "$TARGET/.gitignore"
    cat "$OVERRIDES/gitignore.append" >> "$TARGET/.gitignore"
else
    echo "  (already present, skipped)"
fi

# .vscode/settings.json - no venv/ in codespaces-mgr; use the global interpreter
echo "Applying .vscode/settings.json override (Manager root)..."
if grep -q '"python.defaultInterpreterPath"' "$TARGET/.vscode/settings.json"; then
    sed -i.bak 's|"python.defaultInterpreterPath": ".*"|"python.defaultInterpreterPath": "/usr/local/bin/python"|' "$TARGET/.vscode/settings.json"
    rm -f "$TARGET/.vscode/settings.json.bak"
    echo "  ✅ Manager root settings.json patched"
else
    echo "  (no interpreter path found, skipped)"
fi

# .vscode/launch.json - replace with Codespaces-trimmed version (2 configs only)
# local-mgr launch.json has 40+ dev/internal configs; rsync would copy all of them
echo "Applying .vscode/launch.json override (Codespaces-trimmed version)..."
cp "$OVERRIDES/launch.json" "$TARGET/.vscode/launch.json"
echo "  ✅ launch.json replaced with Codespaces-trimmed version"

# samples/*/. vscode/settings.json - same fix for all sample projects
# (samples have ../../venv/bin/python or baked local paths - none exist in the container)
echo "Applying .vscode/settings.json override (all samples)..."
find "$TARGET/samples" -name "settings.json" -path "*/.vscode/*" | while read f; do
    if grep -q '"python.defaultInterpreterPath"' "$f"; then
        sed -i.bak 's|"python.defaultInterpreterPath": ".*"|"python.defaultInterpreterPath": "/usr/local/bin/python"|' "$f"
        rm -f "${f}.bak"
        echo "  ✅ $(basename $(dirname $(dirname $f)))"
    fi
done

echo
echo "Done. Review changes in $TARGET, then commit and push:"
echo "  cd $TARGET && git status"
