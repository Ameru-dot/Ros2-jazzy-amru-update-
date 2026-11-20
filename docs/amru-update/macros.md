# Amru Update macros

All macros below are in `src/amru_update_config/param/macros.yaml` and in its `whitelist`, so the LLM and task
specs can call them. The framework's own macros (`go_to_place`, `say`, `meet_guest`, ...) remain available.

## Languages

| Macro | Argument | espeak-ng voice | Example |
| --- | --- | --- | --- |
| `speak_malay` | `text` | `ms` | `{"text": "Selamat datang ke UTHM"}` |
| `speak_mandarin` | `text` (pinyin) | `cmn` | `{"text": "ni hao"}` |
| `speak_urdu` | `text` (romanised) | `ur` | `{"text": "shukriya"}` |
| `speak_tamil` | `text` | `ta` | `{"text": "vanakkam"}` |

## Vaccination centre

Ported from the previous robot's competition scenario. Every macro plays the team's recorded clips, and the ones
that move drive to a place in `places.yaml`.

| Macro | Steps | Trigger in the old code |
| --- | --- | --- |
| `vaccine_greet_urdu` | `urdu_greeting.mp3` | YOLO class `pakistani` |
| `vaccine_register_urdu` | `urdu_follow_me.mp3` → `registration_counter` → `urdu_please_register.mp3` | keyword `RE` |
| `vaccine_thanks_urdu` | `urdu_thank_you.mp3` | keyword `BOHOT` |
| `vaccine_greet_mandarin` | `mandarin_greeting.mp3` | YOLO class `chineese` |
| `vaccine_injection_mandarin` | `mandarin_follow_me.mp3` → `vaccination_point` → `mandarin_please_wait.mp3` | keyword `XIANG` |
| `vaccine_thanks_mandarin` | `mandarin_thank_you.mp3` | keyword `XIE` |
| `vaccine_greet_malay` | `malay_greeting.mp3` | YOLO class `malaysian` |
| `vaccine_treatment_malay` | `malay_follow_me.mp3` → `treatment_bed` → `malay_please_lie_down.mp3` | keyword `SAKIT` |
| `vaccine_done_malay` | `malay_you_are_welcome.mp3` → `waiting_area` | keyword `LINABOT` after treatment |
| `vaccine_demo` | All of the above in order, then `home` | — |

The old code ran one script that waited for keywords and tracked progress in a `counter` variable. Now every step is
a separate task, and the LLM picks the macro from what the visitor says (examples in `llm_knowledge.md`).

## Test one macro

```bash
ros2 topic pub --once /bt/task_spec std_msgs/msg/String \
  "{data: '{\"goal\": \"test\", \"steps\": [{\"macro\": \"vaccine_treatment_malay\"}]}'}"
```

## Add a macro

1. Write the macro at the end of `macros.yaml` (format: [../macros.md](../macros.md) and
   [../task-spec-grammar.md](../task-spec-grammar.md)).
2. Add its name to `whitelist:`.
3. Add one or two `Example:` lines to `llm_knowledge.md` so the LLM knows when to use it.
4. `colcon build --symlink-install --packages-select amru_update_config`, then relaunch.
