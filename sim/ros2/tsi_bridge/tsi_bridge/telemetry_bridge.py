import json
import math
import time

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class TelemetryBridge(Node):
    def __init__(self):
        super().__init__("tsi_telemetry_bridge")
        self.publisher = self.create_publisher(String, "/tsi/telemetry", 10)
        self.create_subscription(Odometry, "/odom", self.on_odom, 10)
        self.create_subscription(LaserScan, "/scan", self.on_scan, 10)
        self.timer = self.create_timer(0.1, self.publish_telemetry)

        self.started_at = time.monotonic()
        self.last_odom_at = 0.0
        self.last_scan_at = 0.0
        self.speed = 0.0
        self.nearest_range = 4.0

    def on_odom(self, message):
        linear = message.twist.twist.linear
        self.speed = math.sqrt(linear.x * linear.x + linear.y * linear.y)
        self.last_odom_at = time.monotonic()

    def on_scan(self, message):
        ranges = [
            value
            for value in message.ranges
            if math.isfinite(value) and message.range_min <= value <= message.range_max
        ]
        if ranges:
            self.nearest_range = min(ranges)
            self.last_scan_at = time.monotonic()

    def publish_telemetry(self):
        now = time.monotonic()
        age = now - max(self.last_odom_at, self.last_scan_at, self.started_at)
        battery = max(12.0, 94.0 - ((now - self.started_at) / 90.0))
        link_quality = max(35.0, 100.0 - age * 18.0)
        latency = min(260.0, 42.0 + age * 34.0)

        payload = {
            "latencyMs": round(latency, 1),
            "linkQuality": round(link_quality, 1),
            "battery": round(battery, 1),
            "humanDistance": round(self.nearest_range, 2),
            "speed": round(self.speed, 3),
            "tiltDeg": 2.4,
            "motorTemp": round(39.0 + self.speed * 18.0, 1),
            "humanAngle": 0.3,
        }

        self.publisher.publish(String(data=json.dumps(payload)))


def main(args=None):
    rclpy.init(args=args)
    node = TelemetryBridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
