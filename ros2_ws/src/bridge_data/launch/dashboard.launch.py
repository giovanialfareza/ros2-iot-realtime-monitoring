# program menjalankan node dan rosbridge

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. Custom Data Bridge Node (File Python kita)
        Node(
            package='bridge_data',
            # PERHATIAN: Nama executable ini harus cocok persis dengan yang ada 
            # di entry_points pada file setup.py ('data_publisher')
            executable='data_publisher',
            name='iot_data_publisher',
            output='screen',
            emulate_tty=True,
        ),
        
        # 2. ROS Bridge WebSocket Server
        ExecuteProcess(
            cmd=['ros2', 'run', 'rosbridge_server', 'rosbridge_websocket',
                 '--port', '9090',
                 '--max_message_size', '10000000'],
            output='screen',
            shell=True,
        ),
    ])