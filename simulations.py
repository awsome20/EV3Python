"""
Python module for running robot in sim mode
"""

from robot import Robot

def sim1():
    robot = Robot(debug=False)

    inches = 5.
    robot.drive_straight_inches(100., inches)
    inchesTraveled = robot.left_motor.get_total_inches_traveled(robot.wheel_radius)
    print("inches traveled: ", inchesTraveled)
    robot.release()

def main():
    sim1()

if __name__ == '__main__':
    main()