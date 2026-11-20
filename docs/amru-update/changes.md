# Files changed by Amru Update

Amru Update adds two packages and replaces the top-level `README.md`. The framework packages under `src/` are
unchanged.

## Added

| Path | Contents |
| --- | --- |
| `src/amru_update_config/` | Parameter folder, places, macros, LLM knowledge, simulation launch |
| `src/amru_update_extension/` | PlayAudio node and team audio clips |
| `docs/amru-update/` | This documentation |

## Modified copies

`src/amru_update_config/param/` started as a copy of `src/framework_bringup/param/` at the revision in
`FRAMEWORK_REV`. The original files in `framework_bringup` are untouched. In the copy:

| File | Change |
| --- | --- |
| `places.yaml` | Added the vaccination-centre places |
| `macros.yaml` | Added the `speak_*` and `vaccine_*` macros and their whitelist entries |
| `llm_knowledge.md` | Added places, languages and example requests |
| `pipeline.yaml` | `knowledge_file`, `macros_file`, `memory_places_file`, `dry_run_exempt` |
| `extensions.yaml` | `places_file` |

New in the copy: `places_old_competition_map.yaml`, `FRAMEWORK_REV`.

## Replaced

| File | Change |
| --- | --- |
| `README.md` | Rewritten to describe the repository and Amru Update |
