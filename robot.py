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

        # what is the min. speed that we can supply
        # the run() method, and our robot still moves?
        self.min_speed = 50.

        # if we are ramping up our speed as we start from zero,
        # then ramping down our speed to come to a stop,
        # at what point in our journey do we want to reach
        # our max speed, and at what point should we start
        # slowing down?  These can also be though of as percentages.
        self.ramp_up_ratio = .10
        self.ramp_down_ratio = .80

    def reset_motor_angles(self, reset_left=None, reset_right=None):
        "Resets the drive motor encoders"
        left_angle = reset_left if reset_left is not None else 0.
        right_angle = reset_right if reset_right is not None else 0.

        self.left_motor.reset_angle(left_angle)
        self.right_motor.reset_angle(right_angle)

    def start_drive_motors(self, speed):
        "Applies given speed to drive motors"
        self.left_motor.run(speed)
        self.right_motor.run(speed)

    def stop_drive_motors(self):
        "Stops drive motors with default of brake"
        self.left_motor.stop()
        self.right_motor.stop()

    def drive_straight(self, speed, target_angle):
        "Drives robot straigt at given speed for given rotations"
        self.reset_motor_angles()

        self.start_drive_motors(speed)

        pos = self.left_motor.angle()
        while pos < target_angle:
            pos = self.left_motor.angle()
            time.sleep(0.25)

        self.stop_drive_motors()    

    def drive_straight_with_gyro(self, speed, target_angle, ramp=True):
        """
        Drives robot straigt at given speed for given rotations,
        but keeps robot straight using the gyro sensor, and includes
        option for ramping speeds up then down again (also to help
        robot go straight)
        """
        self.reset_motor_angles()
        target_angle = self.get_gyro_angle()
        correction = 0

        # self.start_drive_motors(speed)

        # if we ramp speeds, we'll need to save this
        cruising_speed = speed

        # use the left motor to track the encoder values
        pos = self.left_motor.angle()

        # keep going till we reach our given number of
        # motor rotations
        while pos < target_angle:

            # apply optional ramping
            if ramp:
                # how far have come on our journey?
                # 0: we haven't started
                # 1: we finished
                dist_ratio = pos / target_angle

                # ramp up speed?
                if dist_ratio < self.ramp_up_ratio:
                    # Ex: we are 5% there, and we ramp up
                    # our speed in the first 10% of our journey.
                    # In that 10%, ramp up the speed from
                    # min to max linearly.
                    this_ratio = dist_ratio / self.ramp_up_ration
                    speed = max(self.min_speed, speed*this_ratio)    

                # ramp down speed?                    
                elif dist_ratio > self.ramp_down_ratio:
                    # Ex: we are 85% there, and we want to ramp
                    # down the last 20% of our journey.
                    # At 85%, we are 25% done ramping down already,
                    # so we want our power to be at 75%.
                    # this_ratio = (dist_ratio - self.ramp_down_ratio)/(100.-self.ramp_dow_ratio)
                    this_ratio = (100 - dist_ratio)/(100.-self.ramp_down_ratio)
                    speed = max(self.min_speed, speed*this_ratio)
                else:
                    # we aren't ramping up or down, but are at our 
                    # cruising speed
                    speed = cruising_speed

            # calculate the correction, base on our error
            angle = self.get_gyro_angle()
            error = angle - target_error
            correction = self.kp * error

            # apply the correction to keep us going straight
            left_speed = speed + correction
            right_speed = speed - correction

            self.left_motor.run(left_speed)
            self.right_motor.run(right_speed)
            
            # have we gone far enough?
            pos = self.left_motor.angle()
            wait(50)

        self.stop_drive_motors()

    def spin_right(self, speed, wheel_degrees):
        "Spins robot right, for given rotation of motor"
        self.spin(speed, wheel_degrees, spin_right=True)

    def spin_left(self, speed, wheel_degrees):
        "Spins robot left, for given rotation of motor"
        self.spin(speed, wheel_degrees, spin_right=False)

 
    def spin(self, speed, wheel_degrees, spin_right=True):
        "Spins robot left or right, for given rotation of motor"
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
        "Whatever direction the gyro is pointing at, is the given angle now"
        self.gyro.reset_angle(angle)

    def get_gyro_angle(self):
        "Returns the direction the gyro is currently pointing at"
        return self.gyro.angle()

    def spin_right_to_angle(self, speed, target_angle):
        "Spins robot to the right, using gyro sensor"

        start_angle = self.get_gyro_angle()
        
        if start_angle >= target_angle:
            print("ERROR: we cant spin right to this angle")
            return

        # how far do we have to go?
        angle_dist = target_angle - start_angle

        angle = start_angle
        while angle < target_angle:
            # ramp down the speed, the closer we get to our target
            fraction_complete = (angle - start_angle)/angle_dist
            turn_speed = max(selfmin_speed, (1 - fraction_complete)*speed)
            self.right_motor.run(turn_speed)
            self.left_motor.run(-turn_speed)

        self.stop_drive_motors()    

    def spin_left_to_angle(self, speed, target_angle):
        "Spins robot to the right, using gyro sensor"

        start_angle = self.get_gyro_angle()
        
        if start_angle <= target_angle:
            print("ERROR: we cant spin left to this angle")
            return

        # how far do we have to go?
        angle_dist = target_angle - start_angle

        angle = start_angle
        while angle > target_angle:
            # ramp down the speed, the closer we get to our target
            fraction_complete = (angle - start_angle)/angle_dist
            turn_speed = max(selfmin_speed, (1 - fraction_complete)*speed)
            self.right_motor.run(-turn_speed)
            self.left_motor.run(turn_speed)

        self.stop_drive_motors()          