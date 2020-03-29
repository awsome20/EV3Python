from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait

# local imports
from robot import Robot
from launches import launch1

def menu():
    """
    Provides a menu on the brick screen from which users
    can run launches.
    """

    # initialize the robot we'll be using for our
    # missions
    robot = Robot()

    # show the menu until user exits
    # brick.display.clear()
    print_menu(clear_screen=True)

    # don't exit program until this goes to False
    notDone = True
    while notDone:

        buttonsPressed = brick.buttons()

        # if they didn't press a button, check again
        if len(buttonsPressed) == 0:
            # wait long enough to reduce the flickering?
            # no, because you can't get button presses, while
            # you are in a wait
            # wait(50)
            continue

        # make sure they don't hit more then one button
        if len(buttonsPressed) > 1:
            # print an error message long enough for them to see it
            # brick.display.text("Too many buttons pressed", (last_line, 0))
            print_message("2 many buttons!")
            print("too many buttons pressed")
            
            # then check again
            continue

        # finally, this was a legal button press
        button = buttonsPressed[0]   

        # first case is special: user wants to quit
        if button == Button.LEFT_UP:
            # TBF: looks like this just quits program!
            # print that we're leaving
            # brick.display.text("Quitting ...", (last_line, 0))
            # print("quiting")
            # wait(1000)
            # and leave!
            notDone = False
            continue

        # now map buttons' to launches
        if button == Button.LEFT:
            print("launch1")
            # brick.display.text("Launch1 launching ...", (last_line, 0))
            print_message("Launching Launch1 ...", resume_menu=False)
            
            launch1(robot)
            print("launch 1 done")
            print_menu(clear_screen=True)
        else:
            # print an error message that there
            # are no launches for this button
            # brick.display.text("There are no launches for this button", (last_line, 0))
            print_message("No launches 4 button")
        

def print_message(msg, waitSec=1, resume_menu=True):
    "Messages are printed below the menu"
    # last_line = 100
    # blank = " "*177
    # brick.display.text(blank, (0, last_line))
    # brick.display.text(msg, (0, last_line))    
    print(msg)
    brick.display.clear()
    brick.display.text(msg)
    wait(waitSec*1000)
    if resume_menu:
        brick.display.clear()
        print_menu()

def print_menu(clear_screen=False):
    "Prints the menu for competition on brick screen"

    maxX = 177
    maxY = 127

    # we want to display:
    choices = [
        "LEFT: launch1",
        "RIGHT: launch2",
        "BOTTOM: launch3",
        "TOP: launch4",
        "CENTER: launch5",
    ]

    if clear_screen:
        brick.display.clear()

    # TBF: how to print with a larger font?
    for i, choice in enumerate(choices):
        # just print each one on the next line
        brick.display.text(choice) #, (i, 0))
        