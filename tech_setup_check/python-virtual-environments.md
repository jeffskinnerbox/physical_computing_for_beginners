
# Add This

## Git & CircuitPython
Wouldn't be nice if you had an easy way to use `git` with your CircuitPython project?
In a normal git repository, the version history is stored inside the hidden `.git` folder.
But these histories can take up a lot of space, which is a problem since CircuitPy devices only have a couple megabytes.
As an added nuisance, each commit would be a write that triggers auto-reload.
So we need a way to support `.git` but not on the `CIRCUITPY` drive.

The safest way to manage code is to keep your Git repository in a standard local directory on your development computer,
then copy your files over to the `CIRCUITPY` drive.

Let's say you have a brand new git repository for your CircuitPython project.
Perhaps you just made it and we call it `demo`.
Inside, there is a `.git` folder.

```bash
# 1. Create a local project directory on your computer and initialize
mkdir demo
cd demo
git init

# 2. Create your code file
touch code.py
```

Let's add a [Git worktree](https://git-scm.com/docs/git-worktree) with the command `git worktree add /media/jeff/CIRCUITPY`.
Now there is a new folder inside the `.git` directory called `worktrees`,
and inside that a folder named `CIRCUITPY` containing git metadata.

```bash
# FINISH THIS - NOT CORRECT YET

git worktree add -b circuitypython-branch /media/jeff/CIRCUITPY
git worktree list

cd /media/jeff/CIRCUITPY
# make changes

# force a remove of a worktree branch
git worktree remove /media/jeff/CIRCUITPY --force
git worktree list

# list the branches
git branch

# delete the branch
git branch -d circuitypython-branch
```

Source:
* [Git worktrees aren't the problem, it's your setup](https://www.youtube.com/watch?v=A2f3T1JELbo)
* [Git Worktrees Explained Simply](https://www.youtube.com/watch?v=dtCgEwRpJl8)
* [Git Worktrees Crash Course](https://www.youtube.com/playlist?list=PL4cUxeGkcC9iUtQh7Aja3TGfbdd7Z-K0W)
* [Git and CircuitPython](https://mhece.com/posts/cpgit/)
* [Developing for CircuitPython with git-worktree](https://mmm.s-ol.nu/blog/circuitpython_git_worktree/)

---

## CircUp
A tool to manage and update libraries (modules) on a CircuitPython device.

The `circup` program will look at our `code.py` file,
determine if our board needs any additional libraries in our "lib" folder,
and if so, it will find them on the Internet and automatically install them.

* [CircUp: Easily Install or Upgrade CircuitPython Libraries](https://www.youtube.com/watch?v=R9AArkVi3eE)
* [Use circup to easily keep your CircuitPython libraries up to date](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/overview)
* [Circup Documentation](https://docs.circuitpython.org/projects/circup/en/latest/)

---

```bash
# Sources:
#   An Effective Python Development Environment - https://realpython.com/effective-python-environment/
#   Python Virtual Environments: A Primer - https://realpython.com/python-virtual-environments-a-primer/
#   Managing Multiple Python Versions With pyenv - https://realpython.com/intro-to-pyenv/
#   Managing Python Projects With uv: An All-in-One Solution - https://realpython.com/python-uv/
#   Python and TOML: New Best Friends - https://realpython.com/python-toml/
#   How to Manage Python Projects With pyproject.toml - https://realpython.com/python-pyproject-toml/


# --------------------------- typical installation when using uv / pyenv --------------------------

# supply all needed dependencies
sudo apt update
sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
     curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# install uv on your system using the recommended installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# install pyenv on your system using the recommended installer
curl -fsSL https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
exec "$SHELL"     # reload your shell or alternatively you can restart your terminal


# ----------------------------- create your python version environment -----------------------------

# determine the python version you want for your development
pyenv install --list | grep -E ' 3\.([1-9][0-9]+)'

# enter your project directory
cd <project-directory>

# install the stable base release
pyenv install 3.14.0

# install the latest security and bug fix patch
pyenv install 3.14.?

# set the local version
pyenv local 3.14.0

# confirm that the local directory is now using the correct version.
cat .python-version
python --version

# ---------------------- create your development environment with uv / pyenv -----------------------

# create your virtual environment for python development
uv init                              # creates pyproject.toml and other starter files
uv sync                              # creates .venv based on pyproject.toml

# confirm that the local directory is now using uv
$ ls -a
.venv/  main.py  pyproject.toml  .python-version  README.md  uv.lock

# activate virtual environment
source .venv/bin/activate

# install you standard development tools
uv pip install flask ruff

# ------------- create your development environment for circuitpython with uv / pyenv --------------

# install the stubs for circuitpython libraries (this installs stubs for ALL boards)
uv pip install circuitpython-stubs

# -OR- if your reproducing an existing project
uv pip install -r requirements.txt

# ------------------------------ create your project with uv / pyenv -------------------------------

 # run your python code
 python code.py
 uv run copy.py

# to deactivate your vertical environment session
deactivate

# --------------------------------------------------------------------------------------------------
uv pip install pyserial matplotlib numpy
touch wireframe.py
chmod u+x wireframe.py
# --------------------------------------------------------------------------------------------------

# ---------------------- typical development workflow when using uv / pyenv ------------------------

# supply all needed dependencies (vim & nvim not included)
sudo apt install tio
sudo usermod -a -G dialout <your-username>

# load vim or nvim with your program on your pc and make your edits
vim <path-to-file>/code.py

# within vim or nvim, save your edits to your pc at the same file location
:w

# within vim or nvim, copy you program to the microprocessor's copy.py file
:!cp % /media/jeff/CIRCUITPY/code.py

# find the path to your device
tio -L

# open a terminal outside of vim or nvim and control & monitor python REPL
tio /dev/ttyACM0

# press `Ctrl+C` then `Ctrl+D` in the terminal window to restart your board
# enter `Ctrl-t q` to exit serial terminal `tio`


# ----------------------- typical close-out workflow when using uv / pyenv ------------------------

# to save your project for later use
uv pip freeze > requirements.txt
```

