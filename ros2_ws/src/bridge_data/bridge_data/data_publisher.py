# =========================================================
# data_publisher.py
# Realtime IoT Monitoring ROS2 Node
# =========================================================

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Float32, Int32

from rclpy.qos import QoSProfile

import json
from datetime import datetime
import math


class IoTDataPublisher(Node):

    def __init__(self):
        super().__init__('iot_data_publisher')

        # =================================================
        # QoS Configuration
        # =================================================
        qos = QoSProfile(depth=10)

        # =================================================
        # Publisher (Dikirim ke Frontend Vue.js / ROSBridge)
        # =================================================
        self.pub_dashboard = self.create_publisher(
            String,
            '/iot/data',
            qos
        )

        # =================================================
        # Subscriber (Data dari Gateway / micro-ROS)
        # Pastikan nama topic sama dengan ESP32/Arduino
        # =================================================
        self.sub_suhu = self.create_subscription(
            Float32,
            '/gateway/temperature',
            self.cb_suhu,
            qos
        )

        self.sub_kelembapan = self.create_subscription(
            Float32,
            '/gateway/humidity',
            self.cb_kelembapan,
            qos
        )

        self.sub_ldr = self.create_subscription(
            Int32,
            '/gateway/ldr',
            self.cb_ldr,
            qos
        )

        # =================================================
        # Variabel Penyimpanan Data Sensor
        # =================================================
        self.temperature = 0.0
        self.humidity = 0.0
        self.ldr = 0

        self.get_logger().info(
            'IoT Data Publisher Node Started!'
        )

    # =====================================================
    # Callback Temperature
    # =====================================================
    def cb_suhu(self, msg):

        # Validasi data
        if math.isnan(msg.data):
            self.get_logger().warning(
                'Temperature data invalid!'
            )
            return

        if msg.data < -50 or msg.data > 100:
            self.get_logger().warning(
                f'Temperature out of range: {msg.data}'
            )
            return

        self.temperature = round(msg.data, 2)

        self.get_logger().info(
            f'Suhu diterima: {self.temperature} C'
        )

        self.publish_dashboard()

    # =====================================================
    # Callback Humidity
    # =====================================================
    def cb_kelembapan(self, msg):

        if math.isnan(msg.data):
            self.get_logger().warning(
                'Humidity data invalid!'
            )
            return

        if msg.data < 0 or msg.data > 100:
            self.get_logger().warning(
                f'Humidity out of range: {msg.data}'
            )
            return

        self.humidity = round(msg.data, 2)

        self.get_logger().info(
            f'Kelembapan diterima: {self.humidity}%'
        )

        self.publish_dashboard()

    # =====================================================
    # Callback LDR
    # =====================================================
    def cb_ldr(self, msg):

        if msg.data < 0:
            self.get_logger().warning(
                f'LDR invalid: {msg.data}'
            )
            return

        self.ldr = int(msg.data)

        self.get_logger().info(
            f'LDR diterima: {self.ldr}'
        )

        self.publish_dashboard()

    # =====================================================
    # Publish Semua Data ke Dashboard
    # =====================================================
    def publish_dashboard(self):

        # Status Monitoring
        status = "AMAN"

        if self.temperature >= 35:
            status = "PANAS"

        if self.ldr < 100:
            kondisi_cahaya = "GELAP"
        else:
            kondisi_cahaya = "TERANG"

        # Payload JSON
        payload = {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "ldr": self.ldr,
            "light_status": kondisi_cahaya,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

        # Convert ke JSON String
        msg = String()
        msg.data = json.dumps(payload)

        # Publish
        self.pub_dashboard.publish(msg)

        self.get_logger().info(
            f'Data dashboard dikirim: {msg.data}'
        )


# =========================================================
# Main
# =========================================================
def main(args=None):

    rclpy.init(args=args)

    node = IoTDataPublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            'Node dihentikan oleh user.'
        )

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()