"""Amru Update in simulation: nav_sim (2D robot + Nav2/AMCL) + extensions + planning pipeline + TTS + PlayAudio.

  ros2 launch amru_update_config amru_sim.launch.py                   # the simulated robot moves (dry_run:=false)
  ros2 launch amru_update_config amru_sim.launch.py dry_run:=true     # plans are only logged, the robot stays still
  ros2 launch amru_update_config amru_sim.launch.py llama_url:=http://127.0.0.1:8081   # with the LLM

Then, in another terminal:
  ros2 topic pub --once /bt/task_spec std_msgs/msg/String "{data: '{\\"goal\\": \\"demo\\", \\"steps\\": [{\\"macro\\": \\"vaccine_demo\\"}]}'}"

Parameters: the Amru Update parameter folder in amru_update_config/param (places, macros, LLM knowledge).
Those files use @PARAMS_DIR@ for paths; this launch writes a ready-to-use copy to ~/.ros/amru_update_params.
Without llama_url the LLM emergency halt (halt_on_all_down) is switched off so that task specs can run.
"""
import os

from ament_index_python.packages import get_package_share_directory as share
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PLACEHOLDER = '@PARAMS_DIR@'


def prepare_params_dir(with_llm):
    """Copy the Amru Update parameters to ~/.ros/amru_update_params and fill in @PARAMS_DIR@.

    Without an LLM, halt_on_all_down is turned off: otherwise llm_bridge halts every plan
    (EMERGENCY halt) after startup_grace_sec because no LLM server answers."""
    src = os.path.join(share('amru_update_config'), 'param')
    dst = os.path.expanduser('~/.ros/amru_update_params')
    for root, _, files in os.walk(src):
        out = os.path.join(dst, os.path.relpath(root, src))
        os.makedirs(out, exist_ok=True)
        for f in files:
            with open(os.path.join(root, f), 'rb') as fh:
                data = fh.read()
            if f.endswith(('.yaml', '.md')):
                data = data.replace(PLACEHOLDER.encode(), dst.encode())
            if f == 'pipeline.yaml' and not with_llm:
                data = data.replace(b'halt_on_all_down: true', b'halt_on_all_down: false')
            with open(os.path.join(out, f), 'wb') as fh:
                fh.write(data)
    return dst


def _actions(context):
    llama_url = LaunchConfiguration('llama_url').perform(context)
    params = prepare_params_dir(bool(llama_url))
    fw = os.path.join(share('framework_bringup'), 'launch')

    def include(path, **args):
        return IncludeLaunchDescription(PythonLaunchDescriptionSource(path),
                                        launch_arguments={'params_dir': params, **args}.items())

    pipeline_args = {'start_llama_server': 'false',
                     'dry_run': LaunchConfiguration('dry_run').perform(context)}
    if llama_url:
        pipeline_args['llama_url'] = llama_url

    return [
        include(os.path.join(fw, 'nav_sim.launch.py')),
        # the safety mux publishes to the simulated robot's cmd_vel; no arm and no camera in the 2D sim
        include(os.path.join(fw, 'extensions.launch.py'), enable_arm='false', enable_pose='false',
                scan_required='false', scan_yaw_offset='0.0', cmd_vel_topic='cmd_vel'),
        include(os.path.join(fw, 'pipeline.launch.py'), **pipeline_args),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(
            os.path.join(share('tts_pipeline'), 'launch', 'tts_pipeline.launch.py')),
            launch_arguments={'engine': 'espeak'}.items()),
        Node(package='amru_update_extension', executable='amru_update_extension_node', output='screen',
             respawn=True, respawn_delay=3.0),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('dry_run', default_value='false',
                              description='false: the simulated robot moves; true: plans are only logged'),
        DeclareLaunchArgument('llama_url', default_value='',
                              description='llama-server URL, e.g. http://127.0.0.1:8081 ("" = no LLM)'),
        OpaqueFunction(function=_actions),
    ])
