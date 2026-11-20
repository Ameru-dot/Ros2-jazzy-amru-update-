# Amru Update: overview

Amru Update adds the UTHM robot's content through two mechanisms the framework already provides, so the framework's
own packages stay unchanged:

1. **A replacement parameter folder** (`params_dir:=`), in `src/amru_update_config/param/`.
2. **An extension** (`amru_update_extension`): a manifest the framework discovers automatically, which adds the
   `PlayAudio` behaviour-tree node to the validator, the LLM schema and the executor.

## Packages

| Package | Type | Contents |
| --- | --- | --- |
| `amru_update_config` | ament_cmake | Parameter folder (places, macros, LLM knowledge), `amru_sim.launch.py` |
| `amru_update_extension` | ament_python | `PlayAudio` node, 14 team audio clips |

## Parameter folder

`src/amru_update_config/param/` is a full copy of `framework_bringup/param/` (the revision is recorded in
`FRAMEWORK_REV`), with the changes listed in [changes.md](changes.md).

Framework parameter files are loaded as-is, without variable substitution. So the Amru Update files write
`@PARAMS_DIR@` where a path is needed, and `amru_sim.launch.py`:

1. copies `share/amru_update_config/param` to `~/.ros/amru_update_params`,
2. replaces `@PARAMS_DIR@` with that folder,
3. starts the framework with `params_dir:=~/.ros/amru_update_params`.

| Parameter | Node | Points to |
| --- | --- | --- |
| `places_file` | nav_extension_node | Amru Update `places.yaml` |
| `memory_places_file` | orchestrator_node | Amru Update `places.yaml` |
| `macros_file` | orchestrator_node, bt_validator_node | Amru Update `macros.yaml` |
| `knowledge_file` | llm_bridge_node | Amru Update `llm_knowledge.md` |
| `dry_run_exempt` | bt_executor_node | `[social_extension, amru_update_extension]`: sound still plays in a dry run |

When started without `llama_url`, the launch also sets `halt_on_all_down: false`. Otherwise `llm_bridge` would halt
every plan 60 s after start-up because no LLM server answers.

## PlayAudio

- Manifest: `config/amru_update_extension.yaml` declares `PlayAudio` (ports `file`, `wait`).
- The handler plays the clip with `ffplay` and stops at once when the tree is halted.
- Only file names inside `audio/` are accepted; any path is rejected.

## Simulation launch

`amru_sim.launch.py` starts:

| Part | From |
| --- | --- |
| 2D robot, lidar, odometry, Nav2 + AMCL on the `test_room` map | `framework_bringup/nav_sim.launch.py` |
| Framework extensions (navigation, speech, odometry, PID, safety mux) | `framework_bringup/extensions.launch.py` |
| LLM bridge, SLM, validator, orchestrator, executor | `framework_bringup/pipeline.launch.py` |
| espeak-ng text-to-speech | `tts_pipeline` |
| PlayAudio | `amru_update_extension` |

The 2D simulator has no camera and no arm.
