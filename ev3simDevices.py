"""
Python module for simulating ev3 hardware.
"""

import threading
import time
import math

class SimMotor:

    """
    This class provides the same interface as the ev3device.Motor,
    but uses a Timer thread to advance what the motor rotation would
    be using the rotational speed.
    """

    def __init__(self, port):
        self.port = port

        # init key attributes
        # angle()
        self.degrees = 0
        # speed()
        self.degrees_per_sec = 0

        self.total_degrees = 0.

        # manage time
        now = time.time()
        self.start_time = now
        self.last_time = now
        self.total_elapsed_time = 0
        self.elapsed_time = 0

        # setup period callbacks to advance motor state
        self.timer_wait = 0.1
        self.timer_thread = threading.Timer(self.timer_wait, self.on_timer)
        self.timer_thread.start()
        self.die = False

    def __del__(self):
        "__del__ does not seem to get called, so this doesn't help"
        print("__del__")
        self.die = True
        self.timer_thread.cancel()

    def update_time(self):
        "updates time variables based of when __init__ and last update were called"

        now = time.time()
        self.total_elapsed_time = now - self.start_time
        self.elapsed_time = now - self.last_time
        self.last_time = now

    def on_timer(self):
        "makes sure we get called periodically"
        # print("on_timer")

        # stop timer?
        if self.die:
            print("trying to die")
            return

        # see how time advances
        self.update_time()

        # advance motor state: angle, etc
        self.step_motor_state()
        
        # make sure we call ourselves again
        self.timer_thread = threading.Timer(self.timer_wait, self.on_timer)
        self.timer_thread.start()

    def step_motor_state(self):
        "Updates the state of the motor according to how much time has elapsed"

        # we must update the angle.
        # how far has it gone since last time?
        # units: degrees = secs * (degrees/secs)
        delta_angle = self.elapsed_time * self.degrees_per_sec

        # update the angle 
        self.degrees += delta_angle
        self.total_degrees += delta_angle

    def get_total_inches_traveled(self, wheel_radius_inches):
        radians = (math.pi/180.) * self.total_degrees
        return radians * wheel_radius_inches

    # **** begin ev3device.Motor interface

    def reset_angle(self, angle=0):
        self.degrees = angle

    def stop(self):
        self.set_speed(0)

    def run(self, speed):
        self.set_speed(speed)

    def set_speed(self, speed):
        self.degrees_per_sec = speed

    def angle(self):
        return self.degrees

    def speed(self):
        return self.degrees_per_sec    

class SimGyro:
    
    """
    Presents identical interface as the ev3device.GyroSensor.
    It can't simulate itself because that depends on the motion
    of the robot.
    """

    def __init__(self, port):
        self.port = 0

    def angle(self):
        pass

    def reset_angle(self):
        pass

# self test:
if __name__ == '__main__':
    motor = SimMotor('A')
    motor.run(0)
    time.sleep(3)
    # angle should be 0
    print("angle: ", motor.angle())
    motor.run(100)
    time.sleep(4)
    # angle should be 100*4= 400
    print("angle: ", motor.angle())
    motor.stop()
    time.sleep(2)
    # angle should be same
    print("angle: ", motor.angle())
    motor.reset_angle()
    motor.run(-300)
    time.sleep(2)
    # angle will be 2*300 = -600
    print("angle: ", motor.angle())
    # exit
    motor.timer_thread.cancel()
    print(motor.total_elapsed_time, motor.last_time)
    print("done")            