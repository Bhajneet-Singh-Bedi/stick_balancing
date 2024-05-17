from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import IncludeLaunchDescription ,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution,LaunchConfiguration, PythonExpression
import os
import xacro
from ament_index_python.packages import get_package_share_directory,get_package_prefix


def generate_launch_description():
    share_dir = get_package_share_directory('stick_balancing')

    xacro_file = os.path.join(share_dir, 'urdf','stick.xacro')
    assert os.path.exists(xacro_file), "The stick.xacro file does not exists in "+str(xacro_file)

    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()
    print(robot_urdf)
    world_file_name = 'gazebo.world'
    world_path = os.path.join(share_dir, 'worlds','gazebo.world'), ''
    
    install_dir = get_package_prefix('stick_balancing')
  
    world = LaunchConfiguration('world')
    

 
    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load')
 



    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'pause': 'false',
             world: 'world'
        }.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )



    return LaunchDescription([
        declare_world_cmd, 
        gazebo_server,
        gazebo_client,
    ])