import time
import math

try:
    from pybricks.ev3devices import Motor
    from pybricks.ev3devices import GyroSensor
    from pybricks.parameters import Port
    from pybricks.tools import print, wait

    portB = Port.B 
    portC = Port.C
    port4 = Port.S4

    SIM = False

except:
    print("Could not import pybricks")
    print("Setting up for Simulation Mode")

    from ev3simDevices import SimMotor as Motor
    from ev3simDevices import SimGyro as GyroSensor
    portB = 'B'
    portC = 'C'
    port4 = 'S4'

    SIM = True

class RobotGyro:

    """
    This is a facade class for interacting either with
    the ev3brick Gyro, or our simulated Gyro, 
    which needs details about the robot to figure out
    what angle it should be reading.
    """

    def __init__(self, port, left_motor, right_motor, wheel_radius, axis_radius, debug=False):

        self.port = port

        self.left_motor = left_motor
        self.right_motor = right_motor
        self.wheel_radius = wheel_radius
        self.axis_radius = axis_radius
        
        self.debug = debug

        # either connect to real hardware, or our dummy sim class
        self.gyro = GyroSensor(self.port)
        self.degrees = int(0)

    def reset_gyro_angle(self):
        self.gyro.reset_angle(0)
        self.degrees = 0

    def angle(self):

        if not SIM:
            # not a simulation, so return what the hardware
            # is reading
            self.degrees = self.gyro.angle()
            return self.degrees

        # in simulation mode, the angle returned by the gyro sensor
        # depends on how our sim motors are moving.
        # If they have moved identically all the time,
        # our sim angle will always be zero
        left_angle = self.left_motor.angle()
        right_angle = self.right_motor.angle()
        
        tol = 1.
        angle_diff = abs(left_angle - right_angle)
        if angle_diff < tol:
            return int(0)

        # TBF: how to compute this angle?
        # print("Cannot compute angle", angle_diff)
        # return None
    
        # we'll only compute spinnging angles: angles from
        # two motors are close to eachother but in opposite directions
        return self.compute_robot_spin_degrees(left_angle, right_angle)

    def compute_robot_spin_degrees(self, left_angle, right_angle):
        "Uses configuration of robot and math to figure out gyro value"

        if self.debug:
            print("compute spin degrees", left_angle, right_angle)

        # assert ((right_angle >= 0 and left_angle <= 0) or (right_angle <= 0 and left_angle >= 0))

        spin_left = right_angle > 0
        positive_wheel_degrees = right_angle if right_angle > 0 else left_angle

        # how far has the wheel going forward moved?
        # C = 2*pi*r
        # distance wheel traveled = (radians traveled)*wheel_radius
        # wheel_distance = self.deg2rad(positive_wheel_degrees) * self.wheel_radius
        # print("Forward wheel has moved (inches)", wheel_distance)

        # so, one wheel has gone part of circle the above distance;
        # what angle for this zero-radius turn has it gone?
        # C = 2*pi*r
        # part of circle = (radians traveled on circle) * (radius of circle)
        # robot_spin_degrees = wheel_distance / self.axis_radius
        # print("my robot_spin_degrees: ", robot_spin_degrees)

        # I keep screwing this up, so here's it explained, and simplified:
        # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=12&ved=2ahUKEwi8y-K0pM_oAhVAgXIEHdapC8cQFjALegQIAxAB&url=https%3A%2F%2Fsheldenrobotics.com%2Ftutorials%2FDetailed_Turning_Tutorial.pdf&usg=AOvVaw3FCQ_gyV_xrhMu2iZsDdBl
        # Number of Degrees to Program = (Cturn) / (Cwheel) x (theta)
        # positive_wheel_degrees = (self.axis_radius/self.wheel_radius) * robot_spin_degree
        robot_spin_degrees = positive_wheel_degrees * (self.wheel_radius / self.axis_radius)

        return robot_spin_degrees if not spin_left else -robot_spin_degrees

    def deg2rad(self, degrees):
        return degrees * (math.pi/180.)

    def rad2deg(self, radians):
        return radians * (180./math.pi)

class Robot:

    """
    This class is responsible for all basic attributes
    and functions related to the robot hardware: specifically
    motors and sensors.
    """

    def __init__(self, debug=False):

        self.debug = debug

        # mechanical configuration    
        self.wheel_radius = 1.0 # inches
        self.axis_radius = 2.0 # inches

        # wiring:
        self.left_motor = Motor(portB)
        self.right_motor = Motor(portC)
        self.gyro = RobotGyro(port4,
                              self.left_motor,
                              self.right_motor,
                              self.wheel_radius,
                              self.axis_radius)

        self.kp = 0.7

        # what is the min. speed that we can supply
        # the run() method, and our robot still moves?
        self.min_speed = 50.

        # if we are ramping up our speed as we start from zero,
        # then ramping down our speed to come to a stop,
        # at what point in our journey do we want to reach
        # our max speed, and at what point should we start
        # slowing down?  These can also be though of as percentages.
        self.ramp_up_ratio = .10
        self.ramp_down_ratio = .70

    def wait(self, msecs):
        if SIM:
            time.sleep(msecs/1000.) # convert to secs
        else:
            wait(msecs)

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

    def robot_inches_to_wheel_degrees(self, inches):
        "Use geometry to convert how for wheel should got to how much it will turn"

        # Circumfrance = 2*pi*WheelRadius
        radians = inches / self.wheel_radius
        return radians * (180./math.pi)

    def drive_straight_inches(self, speed, inches, gyro=True, ramp=True):
        "Drive the robot straight for given distance at given speed"

        target_angle = self.robot_inches_to_wheel_degrees(inches)
        if gyro:
            self.drive_straight_with_gyro(speed, target_angle, ramp=ramp)
        else:
            self.drive_straight(speed, target_angle)

    def drive_straight_with_gyro(self, speed, target_angle, ramp=True):
        """
        Drives robot straigt at given speed for given rotations,
        but keeps robot straight using the gyro sensor, and includes
        option for ramping speeds up then down again (also to help
        robot go straight)
        """

        if self.debug:
            print("drive_straight_with_gyro: ", speed, target_angle, ramp)

        self.reset_motor_angles()
        target_gyro_angle = self.get_gyro_angle()
        correction = 0

        # self.start_drive_motors(speed)

        # if we ramp speeds, we'll need to save this
        cruising_speed = speed

        # use the left motor to track the encoder values
        pos = self.left_motor.angle()
        if self.debug: 
            print("wheel angle: ", pos)

        # keep going till we reach our given number of
        # motor rotations
        while pos < target_angle:

            if self.debug:
                print("wheel angle: ", pos)

            # apply optional ramping
            if ramp:
                # how far have come on our journey?
                # 0: we haven't started
                # 1: we finished
                dist_ratio = pos / target_angle

                if self.debug:
                    print("dist_ratio:", dist_ratio)

                # ramp up speed?
                if dist_ratio < self.ramp_up_ratio:
                    # Ex: we are 5% there, and we ramp up
                    # our speed in the first 10% of our journey.
                    # In that 10%, ramp up the speed from
                    # min to max linearly.
                    this_ratio = dist_ratio / self.ramp_up_ratio
                    speed = max(self.min_speed, cruising_speed*this_ratio)    
                    
                    if self.debug:
                        print("ramp up this_ratio:", this_ratio)

                # ramp down speed?                    
                elif dist_ratio > self.ramp_down_ratio:
                    # Ex: we are 85% there, and we want to ramp
                    # down the last 20% of our journey.
                    # At 85%, we are 25% done ramping down already,
                    # so we want our power to be at 75%.
                    # this_ratio = (dist_ratio - self.ramp_down_ratio)/(100.-self.ramp_dow_ratio)
                    this_ratio = (1. - dist_ratio)/(1. - self.ramp_down_ratio)
                    speed = max(self.min_speed, cruising_speed*this_ratio)
                              
                    if self.debug:
                        print("ramp down this_ratio:", this_ratio)

                else:
                    # we aren't ramping up or down, but are at our 
                    # cruising speed
                    speed = cruising_speed

            if self.debug:
                print("base speed:", speed)

            # calculate the correction, base on our error
            angle = self.get_gyro_angle()
            error = angle - target_gyro_angle
            correction = self.kp * error

            # apply the correction to keep us going straight
            left_speed = speed + correction
            right_speed = speed - correction

            if self.debug:
                print("gyro error: ", error)
                print("correction: ", correction)
                print("left speed:", left_speed)
                print("right speed:", right_speed)

            self.left_motor.run(left_speed)
            self.right_motor.run(right_speed)
            
            # have we gone far enough?
            pos = self.left_motor.angle()
            self.wait(50)

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

    def spin_left_to_angle(self, speed, target_angle):
        "Spins robot to the left, using gyro sensor"

        if self.debug:
            print("spin_left_to_ang:", speed, target_angle)

        start_angle = self.get_gyro_angle()
        
        if start_angle <= target_angle:
            print("ERROR: we cant spin left to this angle", start_angle, target_angle)
            return

        # how far do we have to go?
        angle_dist = target_angle - start_angle

        angle = start_angle
        while angle > target_angle:
            # ramp down the speed, the closer we get to our target
            fraction_complete = (angle - start_angle)/angle_dist
            turn_speed = max(self.min_speed, (1 - fraction_complete)*speed)
            self.right_motor.run(turn_speed)
            self.left_motor.run(-turn_speed)
            angle = self.get_gyro_angle()
            self.wait(50)
            if self.debug:
                print("turn_speed: ", turn_speed)
                print("angle: ", angle)


        self.stop_drive_motors()    

    def spin_right_to_angle(self, speed, target_angle):
        "Spins robot to the right, using gyro sensor"

        if self.debug:
            print("spin_right_to_ang:", speed, target_angle)

        start_angle = self.get_gyro_angle()
        
        if start_angle >= target_angle:
            print("ERROR: we cant spin right to this angle", start_angle, target_angle)
            return

        # how far do we have to go?
        angle_dist = target_angle - start_angle

        angle = start_angle
        while angle < target_angle:
            # ramp down the speed, the closer we get to our target
            fraction_complete = (angle - start_angle)/angle_dist
            turn_speed = max(self.min_speed, (1 - fraction_complete)*speed)
            self.right_motor.run(-turn_speed)
            self.left_motor.run(turn_speed)
            angle = self.get_gyro_angle()
            if self.debug:
                print("turn_speed: ", turn_speed)
                print("angle: ", angle)
            self.wait(50)

        self.stop_drive_motors()          

    def release(self):
        "release any resources that might not want to die"
        if SIM:
            self.left_motor.timer_thread.cancel()
            self.right_motor.timer_thread.cancel()

# Test in simulation mode:

if __name__ == '__main__':

    # robot = RobotGyro(None, None, 1., 2.)  
    # degs = 360.*1.
    # deg = robot.compute_robot_spin_degrees(degs, -degs)
    # print(deg)
    
    robot = Robot()
    time.sleep(2)
    print(robot.left_motor.angle())
    robot.start_drive_motors(100)
    time.sleep(2)      
    print("now left motor angle: ", robot.left_motor.angle())
    print("gyro should be zero: ", robot.get_gyro_angle())
    robot.reset_motor_angles()
    print("spinng left")
    robot.spin_left_to_angle(100, 90.)
    print("left motor angle: ", robot.left_motor.angle())
    print("gyro should be close to 90: ", robot.get_gyro_angle())

    robot.reset_motor_angles()
    print("spinng left")
    robot.spin_right_to_angle(100, -90.)
    print("left motor angle: ", robot.left_motor.angle())
    print("gyro should be close to 90: ", robot.get_gyro_angle())

    # TBF: need a release method!
    robot.left_motor.timer_thread.cancel()
    robot.right_motor.timer_thread.cancel()
    print("done")