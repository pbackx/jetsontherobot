import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from .jetson_tracks import Tracks

class JetsonCmdVelSubscriber(Node):

    def __init__(self):
        super().__init__('jetson_cmd_vel_listener')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        self.tracks = Tracks()

    def cmd_vel_callback(self, msg):
        # since we can't configure the starting speed and turn in teleop,
        # this is a temp workaround to have manageable values
        linear_speed=msg.linear.x / 1.5
        angular_speed=msg.angular.z * 1.5

        if angular_speed != 0:
                # We turn
            if angular_speed > 0:
                self.tracks.go_left(abs(angular_speed))
            else:
                self.tracks.go_right(abs(angular_speed))
        else:
            if linear_speed > 0:
                self.tracks.go_forward(abs(linear_speed))
            elif linear_speed < 0:
                self.tracks.go_backward(abs(linear_speed))
            else:
                self.tracks.stop()


def main(args=None):
    rclpy.init(args=args)

    jeston_cmd_vel_subscriber = JetsonCmdVelSubscriber()

    rclpy.spin(jeston_cmd_vel_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    jeston_cmd_vel_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()