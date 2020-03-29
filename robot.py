import time

from pybricks.ev3devices import Motor
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port

class Robot:

    """
    This class is responsible for all basic attributes
    and functions related to the robot hardware: specifically
    motors and sensors.
    """

    def __init__(self):

        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.C)

        self.gyro = GyroSensor(Port.S4)

        self.kp = 0.01

    def reset_motor_angles(self, reset_left=None, reset_right=None):

        left_angle = reset_left if reset_left is not None else 0.
        right_angle = reset_right if reset_right is not None else 0.

        self.left_motor.reset_angle(left_angle)
        self.right_motor.reset_angle(right_angle)

    def start_drive_motors(self, speed):
        self.left_motor.run(speed)
        self.right_motor.run(speed)

    def stop_drive_motors(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def drive_straight(self, speed, target_angle):

        self.reset_motor_angles()

        self.start_drive_motors(speed)

        pos = self.left_motor.angle()
        while pos < target_angle:
            pos = self.left_motor.angle()
            time.sleep(0.25)

        self.stop_drive_motors()    

    def spin_right(self, speed, wheel_degrees):
        self.spin(speed, wheel_degrees, spin_right=True)

    def spin_left(self, speed, wheel_degrees):
        self.spin(speed, wheel_degrees, spin_right=False)

 
    def spin(self, speed, wheel_degrees, spin_right=True):

        self.reset_motor_angles()

  
        #self.start_drive_motors(speed)
        if spin_right:
            fwd_motor = self.right_motor
            rev_motor = self.left_motor
        else:
            fwd_motor = self.left_motor
            rev_motor = self.right_motor

        fwd_motor.run(speed)
        rev_motor.run(-speed)

        pos = fwd_motor.angle()
        while pos < wheel_degrees:
            print("pos: ", pos)
            pos = fwd_motor.angle()
            time.sleep(0.25)

        self.stop_drive_motors()    

    def reset_gyro_angle(self, angle=0.):
        self.gyro.reset_angle(angle)
        
    def get_gyro_angle(self):
        return self.gyro.angle()