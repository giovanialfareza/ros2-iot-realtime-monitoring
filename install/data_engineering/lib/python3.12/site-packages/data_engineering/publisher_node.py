import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')

        # Publisher ke topic
        self.publisher_ = self.create_publisher(
            String,
            '/sensor/data',
            10
        )

        # Timer publish tiap 1 detik
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.count = 0
        self.get_logger().info('Publisher node started')

    def timer_callback(self):
        msg = String()
        msg.data = f'Data ke-{self.count}'
        self.publisher_.publish(msg)

        self.get_logger().info(f'Publish: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)

    node = PublisherNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
