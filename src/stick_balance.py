#!/usr/bin/env python3

""" How this will work:-
First get position from "/joint_state" topic.
After this give velocity commands using "/velocity_controller/commands" topic.

In between there will be a PID controller implemented which will ensure that the stick is balanced.
"""
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from time import sleep

class BalanceStick(Node):

    def __init__(self):
        super().__init__('stick_balance')
        self.subscription = self.create_subscription(JointState, 'joint_states', self.velocity_listener_callback, 5)
        self.kp = 1.0
        self.kd = 0.1
        self.ki = 0.0000
        self.error = 0.0
        self.prev_error = 0.0
        # Time.nanoseconds
        time = self.get_clock().now()
        self.prev_time=time.nanoseconds
        # self.get_logger().info('Goal rejected '+ str(self.prev_time))



    def velocity_listener_callback(self, msg):
        current_position = msg.position  # Assuming position data is in the first element
        # self.get_logger().info('Position message {0}'.format(current_position[0]))
        # print(type(current_position))
        # Calculate error (desired position - current position)
        desired_position = -3.14# Your desired position for the stick (replace with actual value)
        self.error = desired_position - current_position[0]

        # Calculate PID control output
        # (These calculations can be further optimized based on your needs)
        delta_error = self.error - self.prev_error  # Calculate change in error
        self.prev_error = self.error  # Update previous error for next iteration
        velocity_command = self.kp * self.error + self.ki * self.integral(delta_error) + self.kd * self.derivative(delta_error)
        self.get_logger().info('Velocity Command '+ str(velocity_command))
        
        # Now publish velocity commands
        publisher = self.create_publisher(Float64MultiArray, "/velocity_controller/commands", 10)
        # Define velocity commands message
        commands = Float64MultiArray()
        commands.data = [velocity_command]
        publisher.publish(commands)
        sleep(0.5)
        # Updation
        self.prev_time=self.get_clock().now().nanoseconds

        
    def integral(self, error):
        # Simple integration for demonstration (replace with more robust implementation if needed)
        dt = self.get_clock().now().nanoseconds-self.prev_time
        return error * dt  # Adjust time constant as needed

    def derivative(self, error):
        # Simple differentiation for demonstration (replace with more robust implementation if needed)
        dt = self.get_clock().now().nanoseconds-self.prev_time
        return (error - self.prev_error) / dt  # Adjust time constant as needed


def main(args=None):
    rclpy.init(args=args)

    stick_balance = BalanceStick()

    rclpy.spin(stick_balance)

    stick_balance.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()