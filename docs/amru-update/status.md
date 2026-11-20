# Status

Updated: November 2026.

## Phases

| Phase | Work | Status |
| --- | --- | --- |
| 1 | Places, multilingual speech, PlayAudio, vaccination-centre scenario | Built; runs in the simulator up to the navigation goal; the simulated robot does not drive yet (under investigation) |
| 2 | Find My Mate and Receptionist as macros / behaviour trees | Not started |
| 3 | Gazebo house world + robot model with a camera | Not started |
| 4 | Hand-sign recognition as a ROS 2 perception node | Not started |
| 5 | UTHM hardware drivers (Kobuki, Astra, RPLidar) | Not started; can only be tested in the lab |

## Verified (in the nav_sim simulator)

- `amru_update_config` and `amru_update_extension` build with `colcon build`.
- The 14 Amru Update macros load in the framework's macro library and are whitelisted.
- `PlayAudio` appears in the validator catalogue (`validate_bt --list-nodes`).
- The task spec `vaccine_register_urdu` becomes a **valid plan on the first attempt**.
- The executor runs `PlayAudio` (Urdu clip), then sends `NavigateToPlace(registration_counter)`.
- `speak_malay` sends `Speak` with `voice=ms`.
- espeak-ng has the `ms`, `cmn`, `ur` and `ta` voices.
- Framework dry-run test: the validator rejects a plan that uses an unknown node.

## Not verified yet

- **The simulated robot reaching an Amru Update place.** The navigation goal is sent, but the robot pose did not
  change within 3 minutes. The Nav2 → velocity mux → `nav_sim` chain is under investigation.
- The LLM picking the right macro from Malay, Mandarin and Urdu sentences (the Gemma 4 E2B Q4_0 model is
  downloaded, not tested yet).
- Anything on the real robot.

## Known limits

- `nav_sim` is 2D: no camera, people or objects. Visitor recognition (YOLO) cannot be tested there.
- Without `llama_url`, `amru_sim.launch.py` turns off the LLM emergency halt (`halt_on_all_down`).
- espeak-ng sounds robotic in Malay, Mandarin and Urdu; the team recordings are used for the main dialogue.
- Development laptop: WSL with about 3.7 GB RAM and no NVIDIA GPU.
