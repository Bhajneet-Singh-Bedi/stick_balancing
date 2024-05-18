import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess

def generate_launch_description():

  # Replace with the actual name of your robot description package (assuming it's within the workspace)
  robot_description_package = 'stick_balancing'

  # Path to the URDF file within the package
  xacro_file = os.path.join(get_package_share_directory('stick_balancing'), 'urdf', 'stick.xacro')  
  assert os.path.exists(xacro_file), "The builder_bot.xacro doesnt exist in "+str(xacro_file) 
#   robot_description_file = robot_description_package + '/urdf/box.xacro'
  
  # Launch arguments for Gazebo
  use_sim_time = LaunchConfiguration('use_sim_time', default='true')
  gui = LaunchConfiguration('gui', default='true')  # Optional (headless or GUI)

  gazebo_world_path = os.path.join(get_package_share_directory('stick_balancing'), 'worlds', 'empty_world.world')


  return LaunchDescription([
      DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock if true'),
      DeclareLaunchArgument('gui', default_value='true', description='Start Gazebo in GUI mode'),

      # Launch Gazebo with the empty world
      ExecuteProcess(
        cmd=['gazebo', '--verbose', gazebo_world_path],
        output='screen'
      ),
      # Spawn the box model using robot_state_publisher
      Node(
          package='robot_state_publisher',
          executable='robot_state_publisher',
          name='robot_state_publisher',
          output='screen',
          parameters=[{'robot_description': xacro.process_file(xacro_file).toxml()}]
      )
  ])
