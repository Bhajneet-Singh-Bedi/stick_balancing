#!/usr/bin/env python3
# This lanch file is for launching gazebo which contains the model and controller configuration also started..

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node



def generate_launch_description():
    pkg_name=get_package_share_directory('stick_balancing')

    # Launch gazebo.launch.py
    gz_launch=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_name, 'launch',
                         'gazebo.launch.py'),
        )
    )

    # Launch joint_state_broadcaster
    joint_state_broadcaster_spawner=Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager","/controller_manager"],
    )


    # Launch joint_trajectory_controller for the stick (robot)
    robot_controller_spawner=Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "-c", "/controller_manager"],
    )


    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[robot_controller_spawner],
            )
        ),

        gz_launch,
        joint_state_broadcaster_spawner
    ])


