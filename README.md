# ROS 2 Jazzy Robot Framework — Amru Update

A ROS 2 Jazzy service-robot stack for RoboCup@Home (UTHM): a task in plain language becomes a validated
[BehaviorTree.CPP](https://www.behaviortree.dev/) v4 plan that the robot executes, with Nav2 navigation,
YOLO11 perception, voice in/out and a safety layer in front of the motors.

**Amru Update** adds the UTHM robot's own content on top of the framework: the vaccination-centre scenario,
multilingual speech (Malay, Mandarin, Urdu, Tamil), the team's recorded audio clips, named places and a one-command
simulation launch.

> Status: Amru Update phase 1. Tested in the 2D simulator; not yet tested on the real robot.
> See [docs/amru-update/status.md](docs/amru-update/status.md).

## How it works

```
"I feel sick"  (voice or text on /bt/task)
      │
      ▼
llm_bridge     LLM (Gemma 4 via llama.cpp) picks a macro  ──►  {"macro": "vaccine_treatment_malay"}
      │
      ▼
orchestrator   expands the macro  ──►  PlayAudio(malay_follow_me.mp3) → NavigateToPlace(treatment_bed) → PlayAudio(...)
      │
      ▼
bt_validator   rejects any plan with unknown nodes, bad ports or unknown places
      │
      ▼
bt_executor    runs the tree: PlayAudio → amru_update_extension, NavigateToPlace → Nav2 → safety mux → robot
```

## Repository layout

```
├── README.md                     this file
├── LICENSE                       Apache-2.0
├── setup.sh, setup_jazzy.sh      one-shot installer (apt, rosdep, Python packages, llama.cpp, models, build)
├── launch/                       top-level launch wrappers
├── src/                          ROS 2 packages
│   ├── amru_update_config/       Amru Update: parameter folder, places, macros, simulation launch
│   ├── amru_update_extension/    Amru Update: PlayAudio behaviour-tree node + team audio clips
│   ├── bt_orchestrator/ bt_validator/ bt_executor/ bt_slm/ llm_bridge/ ...   planning pipeline
│   ├── nav_extension/ social_extension/ odom_extension/ ...                  behaviour-tree nodes
│   ├── nav_sim/                  2D simulator for testing without a robot
│   └── framework_bringup/        launch files and default parameters
├── docs/                         framework documentation
│   └── amru-update/              Amru Update documentation
├── tools/                        integration tests and utilities
└── notes/                        engineering notes
```

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy (`ros-jazzy-desktop`)
- Nav2 and slam_toolbox: `sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox`
- `ffmpeg` (for `ffplay`) and `espeak-ng`

## Install and build

```bash
git clone https://github.com/Ameru-dot/Ros2-jazzy-amru-update-.git ros2-jazzy-amru-update
cd ros2-jazzy-amru-update
./setup.sh --dry-run          # show every step first
./setup.sh                    # apt, rosdep, Python packages, llama.cpp, LLM model, build
source env.sh                 # in every new terminal
```

On a laptop without an NVIDIA GPU: `./setup.sh --backend cpu --minimal`.

## Run the vaccination-centre scenario in simulation

```bash
source env.sh
export ROS_DOMAIN_ID=77 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST     # never disturb a real robot
ros2 launch amru_update_config amru_sim.launch.py
```

In a second terminal (same two lines first):

```bash
ros2 topic pub --once /bt/task_spec std_msgs/msg/String \
  "{data: '{\"goal\": \"register\", \"steps\": [{\"macro\": \"vaccine_register_urdu\"}]}'}"
```

The robot plays the Urdu "follow me" clip, drives to `registration_counter`, then plays "please register".

With the LLM, send plain language instead of JSON. Download the smaller Q4_0 model once (2.8 GB), then:

```bash
python3 -c "from huggingface_hub import hf_hub_download as d; d('ggml-org/gemma-4-E2B-it-GGUF', 'gemma-4-E2B-it-Q4_0.gguf', local_dir='models/llm')"
llama-server -m models/llm/gemma-4-E2B-it-Q4_0.gguf --host 127.0.0.1 --port 8081 -c 6144 -np 1 --reasoning off
ros2 launch amru_update_config amru_sim.launch.py llama_url:=http://127.0.0.1:8081
ros2 topic pub --once /bt/task std_msgs/msg/String "{data: 'saya sakit'}"
```

## Amru Update documentation

| Document | Contents |
| --- | --- |
| [overview.md](docs/amru-update/overview.md) | How Amru Update plugs into the framework |
| [macros.md](docs/amru-update/macros.md) | Language and vaccination-centre macros |
| [places.md](docs/amru-update/places.md) | Named places for the simulator and the real robot |
| [comparison.md](docs/amru-update/comparison.md) | The previous ROS 1 robot code compared with this repository |
| [status.md](docs/amru-update/status.md) | What has been tested and what comes next |
| [changes.md](docs/amru-update/changes.md) | Framework files modified by Amru Update |

## Framework documentation

Start with [docs/start-here.md](docs/start-here.md), then [docs/tutorial-first-plan.md](docs/tutorial-first-plan.md),
[docs/architecture.md](docs/architecture.md), [docs/macros.md](docs/macros.md) and [docs/safety.md](docs/safety.md).

## Safety

`bt_executor` starts in dry-run by default (extension nodes only log). The software mux is not an emergency stop:
keep a hardware e-stop within reach when running on the real robot.

## License

Apache-2.0, see [LICENSE](LICENSE).
