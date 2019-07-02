import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
	use_sim_time = LaunchConfiguration('use_sim_time', default='True')
	world = os.path.join(get_package_share_directory('kobuki_gazebo'), 'worlds', "empty.world")
	launch_file_dir = os.path.join(get_package_share_directory('kobuki_gazebo'), 'launch','includes')
	return LaunchDescription([
		ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so'],
			output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
			output='screen'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
			),

		])