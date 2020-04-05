"""
Python module for running robot in sim mode
"""

from robot import Robot

def simDriveStraight():
    robot = Robot(debug=True)

    inches = 10.
    robot.drive_straight_inches(200., inches)
    inchesTraveled = robot.left_motor.get_total_inches_traveled(robot.wheel_radius)
    print("inches traveled: ", inchesTraveled)
    robot.release()

def simSpinRight():
    robot = Robot(debug=True)
    robot.spin_right_to_angle(200., 90)
    robot.release()

def main():
    simSpinRight()

if __name__ == '__main__':
    main()