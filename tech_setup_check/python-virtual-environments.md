

```bash
# Sources:
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


# ---------------------- create your development environment with uv / pyenv -----------------------

# determine the python version you want for your development
pyenv install --list | grep -E ' 3\.([1-9][0-9]+)'

# enter your project directory
cd <project-directory>

# select the version of python you will use
pyenv install 3.13.7                 # released on August 14, 2025
pyenv local 3.13.7

# create your virtual environment for python development
uv init                              # creates pyproject.toml and other starter files
uv sync                              # creates .venv based on pyproject.toml

# activate virtual environment
source .venv/bin/activate

# install you standard development tools
uv pip install flask ruff

 # run your python code
 python code.py
 uv run copy.py

# to deactivate your vertical environment session
deactivate

# install the stubs for circuitpython libraries (this installs stubs for ALL boards)
uv pip install circuitpython-stubs

# -OR- if your reproducing an existing project
uv pip install -r requirements.txt


# ---------------------- typical development workflow when using uv / pyenv -----------------------

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

