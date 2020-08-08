# EV3 Python

## Introduction

This is my attempt at learning EV3 MicroPython, using the 2019 FLL competition as a context: reimplementing the student's block code using Python.

## Goals

We would like to replicate all the functionality from the 2019 FLL season.  This includes, from the lowest level to the highest:

   * Navigation: basic movement with drive motors
   * Navigation: moving straight with the gyro sensor
   * Navigation: spinning to exact angles with the gyro sensor
   * Navigation: line following and aligning along lines
   * Gyro testing and calibration 
   * Launches (for solving missions)
   * Menu program (for starting launches interactively during competition)

As of this writting, this code repository has completed all of the above goals minus the actual launches for solving missions.
   
## Design

Place UML Here

## Results

We ran our simulation code, as well as the same code on the robot ourselves, and captured the print outs from the code.  We then made
some simple plots of these results to illustrate that our fundamental
algorithms worked.

Below we have two simple tests:
   * driving straight with gyro sensor and speed ramping
   * spinning using the gyro sensor

### Simulations

We can see from the plots below that our code fundamentally works.  The motor speed seems to ramp up and down correctly, and we cover
the distance we commanded.

Atrifacts from the simulations:
   * not surprisingly, our gyro error is almost always zero when driving straight.
   * motor angles aren't always smooth: this is an artifact of how we simulate their behavior

#### Driving straight

Motor speeds ramp up in the first 10% of the journey, then ramp down 
to a minimum speed in the last 30%.

<img src="./data/dist vs base speed (sim3_out).png" alt="./data/dist vs base speed (sim3_out).png" width="500">

<img src="./data/dist vs speeds (sim3_out).png" alt="./data/dist vs speeds (sim3_out).png" width="500">

#### Spinning

We can see clearly how the motor speeds drop down to a minimum value as we approach our target angle.

<img src="./data/index vs all (simSpinRight_out).png" alt="index vs all (testSpinRight_out).png" width="500">

<img src="./data/angle vs speed (simSpinRight_out).png" alt="data/angle vs speed (testSpinRight_out).png" width="500">

### Robot

These results come fron actually running the code on the robot.  Note that we get smoother results from the real motor angles, but that we see actual errors from the gyro sensor during straight motion.

Otherwise, we see that we get the same basic results as we got from the simulations.

#### Driving straight 

  * Using gyro sensor, proportional gain of 0.7.
  * Ramping speed up and down.

<img src="./data/dist vs base speed (testDriveK=0_7_out).png" alt="dist vs base speed (testDriveK=0_7_out).png" width="500">

<img src="./data/dist vs speeds (testDriveK=0_7_out).png" alt="dist vs speeds (testDriveK=0_7_out).png" width="500">

### Spinning

Spinning right to 90 degrees.

<img src="./data/index vs all (testSpinRight_out).png" alt="index vs all (testSpinRight_out).png" width="500">

<img src="./data/angle vs speed (testSpinRight_out).png" alt="data/angle vs speed (testSpinRight_out).png" width="500">
