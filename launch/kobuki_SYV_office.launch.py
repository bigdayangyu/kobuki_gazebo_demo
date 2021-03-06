import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.actions import SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
	
	use_sim_time = LaunchConfiguration('use_sim_time', default='True')
	kobuki_gazebo_demo_path = get_package_share_directory('kobuki_gazebo_demo')
	world = os.path.join(kobuki_gazebo_demo_path, 'worlds', "SYV_office.world")
	gazebo_model_path = os.path.join(kobuki_gazebo_demo_path,'models')
	launch_file_dir = os.path.join(get_package_share_directory('kobuki_gazebo_demo'), 'launch','includes')

	return LaunchDescription([
		SetEnvironmentVariable(
            'GAZEBO_MODEL_PATH', gazebo_model_path),

		DeclareLaunchArgument(
           'use_sim_time', 
           default_value='True',
           description='Use simulation (Gazebo) clock if true'),

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