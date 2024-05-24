#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from time import sleep

def main():
  rclpy.init()
  node = Node("velocity_test_node")

  # Create publisher for velocity commands
  publisher = node.create_publisher(Float64MultiArray, "/velocity_controller/commands", 10)

  # Log node creation
  node.get_logger().info("Node created")

  # Define velocity commands message
  commands = Float64MultiArray()

  # Set velocities and publish at 1 second intervals
  for velocity in [0.0, 1.0, -1.0, 0.0]:
    commands.data = [velocity]
    publisher.publish(commands)
    sleep(1.0)

  # Shutdown ROS node
  rclpy.shutdown()

if __name__ == '__main__':
  main()
