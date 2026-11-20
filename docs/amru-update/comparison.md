# Previous robot code vs this repository

## Summary

The previous code (2021–2022) was a set of Python 2 scripts for ROS 1 that waited for fixed keywords. This repository
moves the robot's content (places, the vaccination-centre scenario, languages, audio clips) to ROS 2 Jazzy, on a
framework that plans each task as a behaviour tree and validates it before the robot moves.

## Comparison

| Topic | Previous code (ROS 1) | This repository (ROS 2) |
| --- | --- | --- |
| ROS / OS | Melodic, Ubuntu 18.04 (end of life) | **Jazzy, Ubuntu 24.04** (supported until 2029) |
| Python | Python 2, mixed tabs and spaces | Python 3.12 |
| Code organisation | Scripts spread over several folders, many `(copy).py` duplicates | One Git repository with documentation |
| How the robot decides | `if 'RE' in words and counter == 1:` inside one long script | Task → macro → **behaviour tree** → validator → executor |
| Adding a task | Write new Python code | Add a macro to `macros.yaml` (a few lines of YAML) |
| Locations | Coordinates hard-coded in the scripts | Named places in `places.yaml` |
| Understanding requests | Fixed keywords only | Free language through an LLM (Gemma 4): "I feel sick" → `vaccine_treatment_malay` |
| Languages | Recorded clips + gTTS (needs internet) | Recorded clips (`PlayAudio`) + espeak-ng **offline** for Malay, Mandarin, Urdu, Tamil |
| Plan checking | None: wrong code runs anyway | The validator rejects plans with unknown nodes or places |
| Safety | No dedicated layer | Dry-run mode, velocity mux with watchdog, emergency halt |
| Simulation | TurtleBot3 in Gazebo (after a Noetic upgrade) | `nav_sim` 2D simulator + Nav2 with the robot's places |
| Tests | Almost none | Simulation test scripts; framework CI |

## The vaccination-centre scenario, then and now

Then: one script listened on `/lm_data`, and a `counter` variable decided the next step. One wrong `counter` value
(for example starting at 10) meant the spoken dialogue was never reached.

Now: every step is an independent macro.

| Visitor says | Macro | Robot does |
| --- | --- | --- |
| "I want to register" / "RE" | `vaccine_register_urdu` | Urdu clip → drives to `registration_counter` → "please register" clip |
| "wo xiang jiezhong yimiao" | `vaccine_injection_mandarin` | Mandarin clip → drives to `vaccination_point` → "please wait" clip |
| "saya sakit" | `vaccine_treatment_malay` | Malay clip → drives to `treatment_bed` → "please lie down" clip |
| "run the vaccination centre demo" | `vaccine_demo` | The whole scenario in order |

## Reused from the previous code

- The team's recorded audio clips (Urdu, Mandarin, Malay), renamed in English
- The vaccination-centre scenario and its dialogue order
- The old competition-map poses (`places_old_competition_map.yaml`, quaternions converted to yaw)

## Not done yet

- Find My Mate and Receptionist (phase 2)
- A Gazebo house world with a camera (phase 3)
- Hand-sign and visitor recognition (YOLO) in ROS 2 (phase 4)
- UTHM hardware drivers and tests on the real robot (phase 5)
