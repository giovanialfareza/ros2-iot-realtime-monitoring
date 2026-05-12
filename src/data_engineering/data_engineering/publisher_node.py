import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import json
from datetime import datetime


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        # Publisher ke topic
        self.publisher_ = self.create_publisher(
            String,
            '/iot/data',
            10
        )

        # Timer publish tiap 1 detik
        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

        self.count = 0

        self.get_logger().info(
            'Publisher node started'
        )

    def timer_callback(self):

        # Payload simulasi sensor IoT
        payload = {
            "temperature": 29 + self.count,
            "humidity": 70,
            "ldr": 300,
            "timestamp": datetime.now().isoformat()
        }

        # Convert JSON ke String ROS2
        msg = String()
        msg.data = json.dumps(payload)

        # Publish data
        self.publisher_.publish(msg)

        # Logging terminal
        self.get_logger().info(
            f'Publish: "{msg.data}"'
        )

        self.count += 1


def main(args=None):

    rclpy.init(args=args)

    node = PublisherNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()