# Package Name

[![Build](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?branch=main)](https://github.com/USER/REPO/actions)
[![License](https://img.shields.io/github/license/USER/REPO)](LICENSE)
[![ROS2](https://img.shields.io/badge/ROS2-Humble%20%7C%20Jazzy-blue)](https://docs.ros.org)

One or two sentences: what this package does in the robot system.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Nodes](#nodes)
- [Topics, Services, Actions](#topics-services-actions)
- [Parameters](#parameters)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- Key capability one
- Key capability two

## Requirements
- ROS 2 Humble / Jazzy (specify)
- Ubuntu 22.04 / 24.04
- Dependencies: listed in `package.xml`

## Installation

```bash
# clone into your workspace src/
cd ~/ros2_ws/src
git clone https://github.com/USER/REPO.git

# install dependencies
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# build
colcon build --packages-select package_name
source install/setup.bash
```

## Usage

```bash
ros2 launch package_name bringup.launch.py
```

```bash
ros2 run package_name node_name --ros-args -p param_name:=value
```

## Nodes

### `node_name`
Brief description of what the node does.

**Subscribes:**

| Topic | Type | Description |
|---|---|---|
| `/input_topic` | `sensor_msgs/msg/Image` | ... |

**Publishes:**

| Topic | Type | Description |
|---|---|---|
| `/output_topic` | `geometry_msgs/msg/Twist` | ... |

## Topics, Services, Actions

| Name | Type | Interface | Description |
| --- | --- | --- | --- |
| `/example_service` | Service | `example_interfaces/srv/Trigger` | ... |
| `/example_action` | Action | `example_interfaces/action/Fibonacci` | ... |

## Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `update_rate` | `10.0` | Loop rate in Hz |
| `frame_id` | `base_link` | TF frame used |

Set via YAML:

```yaml
node_name:
  ros__parameters:
    update_rate: 20.0
```

## Project Structure

```
.
├── package_name/       # Python nodes (ament_python) or src/ for C++ (ament_cmake)
├── launch/             # .launch.py files
├── config/             # YAML params
├── msg/ srv/ action/   # custom interfaces, if any
├── test/
├── package.xml
└── CMakeLists.txt      # or setup.py
```

## Testing

```bash
colcon test --packages-select package_name
colcon test-result --verbose
```

## Contributing
Short note + link to CONTRIBUTING.md if it exists.

## License
[Apache-2.0](LICENSE) — or whatever applies.
