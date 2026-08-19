#!/usr/bin/env bash
#
# setup-gethub.sh
#
# ============================================================================
# PURPOSE
# ============================================================================
# Interactively sets up local git version control for the CURRENT WORKING
# DIRECTORY (wherever you run it from — not the directory this script lives
# in) and (optionally) creates a matching GitHub repository, using the
# GitHub CLI (`gh`) for all GitHub interactions.
#
# The script is SAFE TO RE-RUN: it detects existing state (local git repo,
# existing remote, existing GitHub repo, `gh` auth status) and only performs
# the actions you actually confirm. It will never silently overwrite or
# reinitialize something that already exists.
#
# ============================================================================
# WHAT IT DOES (in order)
# ============================================================================
#   1. Checks prerequisites: `git` and `gh` are installed; `gh` is
#      authenticated (or offers to run `gh auth login`).
#   2. Detects current state:
#        - Is this directory already a git repo? (checks for .git)
#        - Does it already have a remote named "origin"?
#        - Is there an existing .gitignore?
#   3. Prompts you for the information needed to proceed, e.g.:
#        - Git user.name / user.email for this repo (if not already set)
#        - Whether to create a local git repo (if not already one)
#        - Initial commit message
#        - GitHub repo name, description, visibility (public/private)
#        - Whether to add/overwrite a .gitignore
#        - Whether to push and set the upstream branch
#   4. Prints a SUMMARY of every planned action and asks you to confirm
#      (type "yes") before touching anything.
#   5. Only after confirmation does it perform the requested actions:
#        - `git init` (only if not already a repo)
#        - `git add` / `git commit` (only if you asked for an initial commit)
#        - `gh repo create` (only if you asked to create a GitHub repo and
#          one does not already exist / is not already linked as "origin")
#        - `git push -u origin <branch>` (only if you asked to push)
#
# ============================================================================
# OPTIONS
# ============================================================================
#   -n, --dry-run   Run through all the same prompts and print the same
#                    SUMMARY, but stop there — no confirmation prompt, and
#                    NO git/gh commands are executed and no files are
#                    written. Use this to preview what the script would do.
#   -h, --help       Print usage and exit.
#
# ============================================================================
# WHAT IT DOES NOT DO
# ============================================================================
#   - It never force-pushes, deletes, or resets anything.
#   - It never overwrites an existing .gitignore without asking first.
#   - It never re-runs `git init` on an existing repo.
#   - It never creates a GitHub repo if "origin" is already configured;
#     it will tell you and skip that step.
#
# ============================================================================
# USAGE
# ============================================================================
#   1. Review this script before running it (you're doing that now).
#   2. Make it executable (already done, but if needed):
#        chmod +x tech_setup_check/setup-gethub.sh
#   3. Run it from anywhere on your filesystem — you can invoke it by full
#      or relative path (e.g. `~/some/where/setup-gethub.sh` or
#      `../tech_setup_check/setup-gethub.sh`). It always operates on your
#      CURRENT WORKING DIRECTORY (i.e. wherever you ran it FROM), not on
#      the directory the script itself lives in. cd into the directory you
#      want to turn into a git repo / GitHub repo first, then run it:
#        cd /path/to/the/project/you/want/to/set/up
#        /path/to/tech_setup_check/setup-gethub.sh
#   4. Answer the prompts. Press Enter to accept any shown default.
#   5. Review the printed summary carefully.
#   6. Type "yes" to proceed, or anything else to abort with no changes made.
#
#   To preview without making any changes, add -n / --dry-run:
#        /path/to/tech_setup_check/setup-gethub.sh --dry-run
#   This still asks all the same prompts (so the summary reflects real
#   answers) but stops after printing the summary — nothing is written,
#   committed, created, or pushed.
#
# ============================================================================
# REQUIREMENTS
# ============================================================================
#   - git      (https://git-scm.com/)
#   - gh       (GitHub CLI, https://cli.github.com/) — must be authenticated
#              via `gh auth login` before this script can create a repo.
#
# ============================================================================

set -euo pipefail

# ----------------------------------------------------------------------------
# Resolve project root: the directory the script was RUN FROM (the caller's
# current working directory), not the directory this script lives in. This
# lets the script be invoked from anywhere and act on whatever directory
# you're standing in.
# ----------------------------------------------------------------------------
PROJECT_ROOT="$(pwd)"

# ----------------------------------------------------------------------------
# Option parsing (via getopt(1) — supports both short and long options)
# ----------------------------------------------------------------------------
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

usage() {
    cat <<USAGE
Usage: ${SCRIPT_NAME} [-n|--dry-run] [-h|--help]

  -n, --dry-run   Show prompts and the planned-actions summary, but don't
                  execute anything (no git/gh commands, no files written).
  -h, --help      Show this help and exit.
USAGE
}

PARSED_OPTS="$(getopt -o nh --long dry-run,help -n "$SCRIPT_NAME" -- "$@")" \
    || { usage; exit 1; }
eval set -- "$PARSED_OPTS"

DRY_RUN=0
while true; do
    case "$1" in
        -n|--dry-run)
            DRY_RUN=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done

# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
info()  { printf '\n[INFO] %s\n' "$*"; }
warn()  { printf '\n[WARN] %s\n' "$*"; }
err()   { printf '\n[ERROR] %s\n' "$*" >&2; }
abort() { err "$*"; exit 1; }

ask() {
    # ask "Prompt text" "default value" -> echoes answer
    local prompt="$1"
    local default="${2:-}"
    local answer
    if [[ -n "$default" ]]; then
        read -r -p "$prompt [$default]: " answer
        echo "${answer:-$default}"
    else
        read -r -p "$prompt: " answer
        echo "$answer"
    fi
}

ask_yes_no() {
    # ask_yes_no "Prompt text" "y|n default" -> returns 0 for yes, 1 for no
    local prompt="$1"
    local default="${2:-n}"
    local answer
    read -r -p "$prompt [y/n, default: $default]: " answer
    answer="${answer:-$default}"
    case "$answer" in
        y|Y|yes|YES|Yes) return 0 ;;
        *) return 1 ;;
    esac
}

# ----------------------------------------------------------------------------
# 1. Prerequisite checks
# ----------------------------------------------------------------------------
command -v git >/dev/null 2>&1 || abort "git is not installed. Install it and re-run."
command -v gh  >/dev/null 2>&1 || abort "GitHub CLI (gh) is not installed. Install it from https://cli.github.com/ and re-run."

info "Operating on current directory: $PROJECT_ROOT"
[[ "$DRY_RUN" -eq 1 ]] && info "DRY RUN MODE: prompts and summary only — nothing will be executed."

GH_AUTHENTICATED=0
if gh auth status >/dev/null 2>&1; then
    GH_AUTHENTICATED=1
    info "gh is already authenticated as: $(gh api user --jq .login 2>/dev/null || echo 'unknown')"
else
    warn "gh is not authenticated."
    if [[ "$DRY_RUN" -eq 1 ]]; then
        info "(dry run — skipping 'gh auth login'; treating as not authenticated for this preview)"
    elif ask_yes_no "Run 'gh auth login' now?" "y"; then
        gh auth login
        gh auth status >/dev/null 2>&1 && GH_AUTHENTICATED=1
    fi
fi

# ----------------------------------------------------------------------------
# 2. Detect existing state
# ----------------------------------------------------------------------------
ALREADY_GIT_REPO=0
if [[ -d "${PROJECT_ROOT}/.git" ]]; then
    ALREADY_GIT_REPO=1
    info "This directory is already a git repository (found .git/)."
else
    info "This directory is NOT yet a git repository."
fi

EXISTING_REMOTE_URL=""
if [[ "$ALREADY_GIT_REPO" -eq 1 ]]; then
    EXISTING_REMOTE_URL="$(git -C "$PROJECT_ROOT" remote get-url origin 2>/dev/null || true)"
    if [[ -n "$EXISTING_REMOTE_URL" ]]; then
        info "An 'origin' remote is already configured: $EXISTING_REMOTE_URL"
    fi
fi

EXISTING_GITIGNORE=0
if [[ -f "${PROJECT_ROOT}/.gitignore" ]]; then
    EXISTING_GITIGNORE=1
    info "A .gitignore file already exists."
fi

# ----------------------------------------------------------------------------
# 3. Prompts (only for actions that are actually still needed)
# ----------------------------------------------------------------------------
DO_GIT_INIT=0
if [[ "$ALREADY_GIT_REPO" -eq 0 ]]; then
    if ask_yes_no "Initialize a local git repository in the current directory ($PROJECT_ROOT)?" "y"; then
        DO_GIT_INIT=1
    fi
fi

GIT_USER_NAME=""
GIT_USER_EMAIL=""
if [[ "$DO_GIT_INIT" -eq 1 ]]; then
    CURRENT_NAME="$(git config --global user.name 2>/dev/null || true)"
    CURRENT_EMAIL="$(git config --global user.email 2>/dev/null || true)"
    GIT_USER_NAME="$(ask "Git user.name for commits" "$CURRENT_NAME")"
    GIT_USER_EMAIL="$(ask "Git user.email for commits" "$CURRENT_EMAIL")"
fi

GITIGNORE_ACTION="skip"
if [[ "$EXISTING_GITIGNORE" -eq 0 ]]; then
    if ask_yes_no "Create a basic .gitignore (Python/CircuitPython/OS/editor cruft)?" "y"; then
        GITIGNORE_ACTION="create"
    fi
else
    if ask_yes_no "A .gitignore already exists. Overwrite it?" "n"; then
        GITIGNORE_ACTION="overwrite"
    fi
fi

DO_INITIAL_COMMIT=0
COMMIT_MESSAGE=""
if [[ "$DO_GIT_INIT" -eq 1 ]] || ask_yes_no "Stage and create a commit of current changes?" "y"; then
    DO_INITIAL_COMMIT=1
    COMMIT_MESSAGE="$(ask "Commit message" "Initial commit")"
fi

DO_GH_CREATE=0
REPO_NAME=""
REPO_DESC=""
REPO_VISIBILITY=""
DO_PUSH=0
BRANCH_NAME=""
if [[ -n "$EXISTING_REMOTE_URL" ]]; then
    info "'origin' remote already set — skipping GitHub repo creation step."
    if ask_yes_no "Push current branch to the existing 'origin' remote?" "y"; then
        DO_PUSH=1
        BRANCH_NAME="$(git -C "$PROJECT_ROOT" branch --show-current 2>/dev/null || echo "main")"
    fi
else
    if [[ "$GH_AUTHENTICATED" -eq 1 ]]; then
        if ask_yes_no "Create a new GitHub repository via 'gh repo create'?" "y"; then
            DO_GH_CREATE=1
            DEFAULT_REPO_NAME="$(basename "$PROJECT_ROOT")"
            REPO_NAME="$(ask "GitHub repository name" "$DEFAULT_REPO_NAME")"
            REPO_DESC="$(ask "Repository description" "Physical Computing for Beginners - Makersmiths course materials")"
            while true; do
                REPO_VISIBILITY="$(ask "Visibility (public/private)" "public")"
                case "$REPO_VISIBILITY" in
                    public|private) break ;;
                    *) warn "Please enter 'public' or 'private'." ;;
                esac
            done
            if ask_yes_no "Push to the new GitHub repo after creating it?" "y"; then
                DO_PUSH=1
                BRANCH_NAME="$(ask "Branch name to push" "main")"
            fi
        fi
    else
        warn "Skipping GitHub repo creation: gh is not authenticated."
    fi
fi

# ----------------------------------------------------------------------------
# 4. Summary + confirmation
# ----------------------------------------------------------------------------
echo
echo "============================================================"
echo " SUMMARY OF PLANNED ACTIONS"
echo "============================================================"
echo "Current directory:         $PROJECT_ROOT"
echo "------------------------------------------------------------"
if [[ "$DO_GIT_INIT" -eq 1 ]]; then
    echo "git init:                   YES"
    echo "  user.name (local repo):   ${GIT_USER_NAME:-<unset>}"
    echo "  user.email (local repo):  ${GIT_USER_EMAIL:-<unset>}"
else
    echo "git init:                   NO (repo already exists or declined)"
fi
echo "------------------------------------------------------------"
case "$GITIGNORE_ACTION" in
    create)    echo ".gitignore:                 CREATE (new file)" ;;
    overwrite) echo ".gitignore:                 OVERWRITE (existing file replaced)" ;;
    skip)      echo ".gitignore:                 no change" ;;
esac
echo "------------------------------------------------------------"
if [[ "$DO_INITIAL_COMMIT" -eq 1 ]]; then
    echo "git add + commit:           YES"
    echo "  commit message:            \"$COMMIT_MESSAGE\""
else
    echo "git add + commit:           NO"
fi
echo "------------------------------------------------------------"
if [[ "$DO_GH_CREATE" -eq 1 ]]; then
    echo "gh repo create:              YES"
    echo "  name:                      $REPO_NAME"
    echo "  description:               $REPO_DESC"
    echo "  visibility:                $REPO_VISIBILITY"
elif [[ -n "$EXISTING_REMOTE_URL" ]]; then
    echo "gh repo create:              NO (origin already set: $EXISTING_REMOTE_URL)"
else
    echo "gh repo create:              NO"
fi
echo "------------------------------------------------------------"
if [[ "$DO_PUSH" -eq 1 ]]; then
    echo "git push:                    YES"
    echo "  branch:                    $BRANCH_NAME"
else
    echo "git push:                    NO"
fi
echo "============================================================"
echo

if [[ "$DRY_RUN" -eq 1 ]]; then
    info "Dry run complete. No changes made. Re-run without --dry-run to execute."
    exit 0
fi

if ! ask_yes_no "Proceed with the actions above?" "n"; then
    info "Aborted. No changes made."
    exit 0
fi

# ----------------------------------------------------------------------------
# 5. Execute
# ----------------------------------------------------------------------------
if [[ "$DO_GIT_INIT" -eq 1 ]]; then
    info "Running: git init"
    git -C "$PROJECT_ROOT" init
    [[ -n "$GIT_USER_NAME" ]]  && git -C "$PROJECT_ROOT" config user.name "$GIT_USER_NAME"
    [[ -n "$GIT_USER_EMAIL" ]] && git -C "$PROJECT_ROOT" config user.email "$GIT_USER_EMAIL"
fi

if [[ "$GITIGNORE_ACTION" != "skip" ]]; then
    info "Writing .gitignore"
    cat > "${PROJECT_ROOT}/.gitignore" <<'EOF'
# Python / CircuitPython
__pycache__/
*.pyc
.venv/
venv/

# OS cruft
.DS_Store
Thumbs.db

# Editor cruft
.vscode/
.idea/
*.swp

# Backup files created by AI-assisted edits
*.bak
EOF
fi

if [[ "$DO_INITIAL_COMMIT" -eq 1 ]]; then
    info "Running: git add -A"
    git -C "$PROJECT_ROOT" add -A
    info "Running: git commit -m \"$COMMIT_MESSAGE\""
    git -C "$PROJECT_ROOT" commit -m "$COMMIT_MESSAGE"
fi

if [[ "$DO_GH_CREATE" -eq 1 ]]; then
    info "Running: gh repo create $REPO_NAME --$REPO_VISIBILITY --description \"$REPO_DESC\" --source=. --remote=origin"
    gh repo create "$REPO_NAME" "--${REPO_VISIBILITY}" --description "$REPO_DESC" --source="$PROJECT_ROOT" --remote=origin
fi

if [[ "$DO_PUSH" -eq 1 ]]; then
    info "Running: git push -u origin $BRANCH_NAME"
    git -C "$PROJECT_ROOT" push -u origin "$BRANCH_NAME"
fi

info "Done."
