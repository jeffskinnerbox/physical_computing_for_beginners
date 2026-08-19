
* [Git worktree like a boss](https://dev.to/metal3d/git-worktree-like-a-boss-2j1b)

* [Claude Code & Git Worktrees: How to Run Claude Code in parallel with Git Worktrees](https://www.youtube.com/watch?v=an-Abb7b2XM)
* [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
* [The Claude Code Git Worktree Pattern: A Primer for Builders](https://www.mindstudio.ai/blog/what-is-claude-code-git-worktree-pattern-parallel-feature-branches)
* [Parallel Vibe Coding: Using Git Worktrees with Claude Code](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)


`git worktree` is a native Git feature that allows you to check out
multiple branches of the same repository simultaneously in separate directories.
Instead of using `git stash`` or cloning the repository multiple times to switch context,
all worktrees share the exact same`.git` history database.
This saves disk space and eliminates the need to re-download files.

Core Benefits
* **No Stashing**: Fix emergency bugs instantly in a side folder without messing up uncommitted work on your current feature branch.
* **Parallel Processing**: Run long-running test suites or complex builds in one folder while continuing to write code in another.
* **Simultaneous Review**: Open two distinct branches side-by-side in your IDE to compare code logic or database states directly.

Crucial Limitations
* **Branch Exclusivity**: You cannot check out the same exact branch in two different worktrees at the same time to prevent data corruption.
* **Dependency Overhead**: Each worktree contains a separate set of un-tracked environment files, meaning you must
  run `npm install` or `pip install` separately in each folder.

```bash
# Add a worktree: Creates a new directory and checks out the specified branch into it. If the branch does not exist, Git creates it.
git worktree add <path> <branch>

# List active worktrees: Displays all current working trees linked to the repository, along with their paths and checked-out commits.
git worktree list

# Remove a worktree: Safely deletes the specified worktree directory and unlinks it from the main Git repository.
git worktree remove <path>

# Prune administrative files: Cleans up any background Git data left behind by worktrees that were manually deleted using standard file managers.
git worktree prune
```

Here is a step-by-step example of setting up and using your first Git worktree to fix an urgent bug without losing your current progress.
You are actively working on a feature branch called `feature-login` in a directory named `project-repo`.
Suddenly, a critical bug appears on the main branch that requires an immediate fix.

```bash
# --- Step 1: Check Your Current StatusVerify your location and current active branch.

# Open your terminal.

# Navigate to your main repository folder:
cd /path/to/project-repo

# Confirm your branch: it should show `feature-login`
git branch

# --- Step 2: Create a Separate Worktree Folder
# Create a new directory outside of your current folder to house the hotfix.

# Run the command to create a new worktree branch:
git worktree add ../project-hotfix main
# What this does: It creates a brand-new folder named `project-hotfix` one level up from your current folder,
# downloads the main branch into it, and keeps your `feature-login` work completely untouched.

# --- Step 3: Switch folders and Fix the Bug
# Navigate to your newly created directory to write the hotfix code.

# Change directories:
cd ../project-hotfix

# Create a new branch specifically for the fix:
git checkout -b bugfix-login-error

# Modify your files, fix the bug, and commit your changes:
git commit -am "Fix critical login loop issue"

# Push the code to your remote repository or merge it into main.

# --- Step 4: Return to Your Feature
# Switch back to your original folder to resume your previous work right where you left off.

# Navigate back to the original repository:
cd ../project-repo

# Run `git status` to see that your `feature-login`s branch and all uncommitted files are exactly as you left them.

# --- Step 5: Clean Up
# Once the hotfix is merged and complete, safely delete the temporary worktree directory.

# Run the removal command from your main repository folder:
git worktree remove ../project-hotfix

# What this does: This safely deletes the `project-hotfix` folder and cleans up the Git administrative references.
```

Managing dependencies across multiple Git worktrees requires care to avoid corrupting shared caches,
breaking local environments, or wasting massive amounts of disk space.
Here is how to manage dependencies safely based on your specific programming language environment.

Python virtual environments should never be shared globally across worktrees if the branches have different dependencies.

* **Create independent environments**: Create a dedicated virtual environment inside or next to each specific worktree folder.

```bash
# Inside project-hotfix worktree
python -m venv .venv-hotfix
source .venv-hotfix/bin/activate
pip install -r requirements.txt
```

* **Configure Poetry**: If using Poetry, force it to create virtual environments inside the specific worktree folder by running
`poetry config virtualenvs.in-project true` before running `poetry install`.
