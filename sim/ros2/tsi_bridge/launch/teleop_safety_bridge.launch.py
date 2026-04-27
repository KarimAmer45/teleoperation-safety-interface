from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    bridge_config = LaunchConfiguration("bridge_config")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "bridge_config",
                default_value="sim/gazebo/bridge.yaml",
                description="Path to the ros_gz_bridge YAML configuration.",
            ),
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                parameters=[{"config_file": bridge_config}],
                output="screen",
            ),
            Node(
                package="rosbridge_server",
                executable="rosbridge_websocket",
                parameters=[{"port": 9090}],
                output="screen",
            ),
            Node(
                package="tsi_bridge",
                executable="telemetry_bridge",
                output="screen",
            ),
        ]
    )
