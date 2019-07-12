import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
	use_sim_time = LaunchConfiguration('use_sim_time', default='True')
	kobuki_nav_prefix = get_package_share_directory('kobuki_navigation')
	kobuki_urdf = os.path.join(kobuki_nav_prefix,'urdf', 'kobuki_gazebo_carto.urdf')
	return LaunchDescription([
        DeclareLaunchArgument(
           'use_sim_time', 
           default_value='true',
           description='Use simulation (Gazebo) clock if true'),

        Node(
            package="tf2_ros",
            node_executable="static_transform_publisher",
            arguments=['0.1','0', '0', '0','0','0','1', 'base_link', 'laser']
            ),

        Node(
            package='robot_state_publisher',
            node_executable='robot_state_publisher',
            node_name="robot_state_publisher",
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
			      arguments=[kobuki_urdf])
])