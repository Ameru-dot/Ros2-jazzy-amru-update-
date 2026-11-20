# Named places

`NavigateToPlace` and the `go_to_place` macro use the names in `src/amru_update_config/param/places.yaml`.

## Simulator (`places.yaml`)

For the `nav_sim` sample map (`test_room`: 12 x 8 m, x from -1 to 11, y from -1 to 7, two rooms joined by a door at
x = 5). Every point was checked against the map image: at least 0.9 m from any obstacle.

| Place | x | y | yaw | Room |
| --- | --- | --- | --- | --- |
| `home` | 0.5 | 0.5 | 0.0 | left (same as `start`) |
| `registration_counter` | 2.5 | 6.0 | 1.57 | left |
| `waiting_area` | 1.5 | 3.5 | 3.14 | left |
| `vaccination_point` | 7.0 | 4.5 | 0.0 | right |
| `treatment_bed` | 9.5 | 2.0 | 0.0 | right |

The general places (`start`, `left_room`, `door`, `right_room`, `far_corner`) are kept because the examples in
`llm_knowledge.md` use them.

## Real robot (`places_old_competition_map.yaml`)

Poses from the previous ROS 1 robot on the old competition map. Orientation quaternions (z, w) were converted to
`yaw = 2 * atan2(z, w)`.

To use: copy it over `places.yaml` and run navigation with the same map. A new ROS 2 map usually differs from the old
one, so the poses will most likely need to be measured again.

## Measure a new place

1. Drive the robot to the spot, facing the right way.
2. `ros2 run tf2_ros tf2_echo map base`
3. Copy `x`, `y` and the yaw angle (radians) into `places.yaml`.

Names may contain letters, digits, `_` and `-`. Add every new name to the "Named places" line in `llm_knowledge.md`.
