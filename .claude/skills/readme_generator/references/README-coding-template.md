# {{Project Name}}
{{project status banner}}

{{One to three paragraphs on what this project does, how does it do it, and what is it's for.}}

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Build from Source](#build-from-source)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
State how these features supports "what this project does"
and then describe the key capabilities in a list below

- Key capability one
- Key capability two

## Installation
State what the overall installation methodology is,
describe the workflow, and then give the specific commands below:

```bash
# Python
pip install -r requirements.txt

# or via package
pip install project-name
```

## Usage
State how you expect this project will be used
describe the usage workflow, and then give the specific commands below:

```bash
python -m project_name --input data.csv --output result.json
```

```python
from project_name import Thing
Thing().run()
```

## Build from Source
State what the build methodology is,
describe the usage workflow, and then give the specific commands below:

```bash
git clone https://github.com/USER/REPO.git
cd REPO
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)
```

## Configuration
State how the project is configured for use
(e.g. via command line, via environmental variables, via configuration file, etc.).

If there are configuration file, environmental variables, etc. that inform/control this project,
then they should be listed in seperate tables below.

| Variable | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Logging verbosity |


## Project Structure
State the high level structure of the project code, and point out, if the exist, any unique or non-typical features.

```
.
├── src/           # C++ core
├── project_name/  # Python package
├── scripts/       # Bash utilities
├── tests/
└── CMakeLists.txt
```

## Testing
State the testing methodology that will be used, what parts of the system are being tested, what may not be tested.
The list below details on how the project will be tested in part or as a whole.

```bash
pytest tests/
ctest --test-dir build
```

## Contributing
Generally, this section is not needed, include if the user request it.
Short note + link to CONTRIBUTING.md if it exists.

## License
Generally, this section is not needed, include if the user request it.
[MIT](LICENSE) — or whatever applies.

