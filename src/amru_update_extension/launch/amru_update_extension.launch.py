"""PlayAudio executor (needs ffplay from ffmpeg)."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([Node(respawn=True, respawn_delay=3.0, package='amru_update_extension',
                                   executable='amru_update_extension_node', output='screen')])
