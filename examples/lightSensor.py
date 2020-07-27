# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait, print


def displayLightValue(port):
    "Continously prints all values from color sensor at given port"

    # creat the sensor object from the ColorSensor class
    sensor = ColorSensor(port)

    while True:
        # have four different ways of using this
        # sensor!
        color = sensor.color()
        reflection = sensor.reflection()
        ambient = sensor.ambient()
        rgb = sensor.rgb()
        print("color: ", color)
        print("reflection: ", reflection)
        print("ambient: ", ambient)
        print("rgb: ", rgb)
        wait(1000)
