import scipy
import math
import numpy
from math import sqrt
from scipy.constants import G
from math import sin, cos, pi


def menu():
    choice = input('''1: Schwarzschild Radius Calculator 
2: Escape Velocity Calculator [WIP Major error] 
3: Rocket Equation Calculator 
4: Trajectory calculator 
5. Drop energy calculator 
6. Orbital satellite height calculator 
7. Orbital speed calculator 
8. Orbital Period Earth Calculator 
9. Orbital Period Calculator
10. Sphere of Influence (SOI)\n''')
    if choice == "1":
        srcalc()
    if choice == "2":
        evcalc()
    if choice == "3":
        recalc()
    if choice == "4":
        tcalc2()
    if choice == "5":
        dcalc()
    if choice == "6":
        ocalc()
    if choice == "7":
        oscalc()
    if choice == "8":
        opecalc()
    if choice == "9":
        opcalc()
    if choice == "10":
        soicalc()


def srcalc():
    g = scipy.constants.G

    c = scipy.constants.c

    M = input("Enter mass of body: ")

    top = 2 * float(g) * float(M)

    bottom = float(c) ** 2

    rs = top / bottom

    print("Scwarzschild radius is " + str(rs) + " metres.")


def evcalc():
    M = input("Enter mass of body: ")

    R = input("Enter radius of body: ")

    g = scipy.constants.G

    ev = math.sqrt(2 * float(g) * float(M) / float(R))

    print("Escape Velocity is: " + str(ev) + "")


def recalc():
    stages = int(input("input stages: "))

    finalv = []

    for i in range(1, stages + 1):
        print("\nSTAGE " + str(i) + ":\n")

        sm = float(input("Enter starting mass (metric tonnes): "))

        fm = float(input("Enter final mass (metric tonnes): "))

        a = float(input("Exhaust velocity (m/s): "))

        b = numpy.log(sm / fm)

        dv = float(a) * float(b)

        print("Delta V = " + str(dv) + " m/s.")

        finalv.append(dv)

    print("The total delta v is: " + str(sum(finalv)) + " m/s")


def tcalc(angle, velocity, gravity):
    # defining gravity

    # converting angle to radians
    angle = angle * pi / 180

    # calculating horizontal and vertical components of the velocity
    velocity_h = velocity * cos(angle)
    velocity_v = velocity * sin(angle)

    # computing time and distance of flight
    time_of_flight = 2 * float(velocity_v) / gravity
    Range = float(time_of_flight) * velocity_h

    return Range, time_of_flight


def tcalc2():
    angle = input("Enter angle of launch (Degrees please): ")
    velocity = input("Enter initial velocity (m/s please): ")
    gravity = input("Enter gravity on planetary body (also m/s please): ")

    ans_range, ans_tof = tcalc(float(angle), float(velocity), float(gravity))
    print("the range is %.1f metres and time of flight is %.0f  seconds" % (ans_range, ans_tof))


def dcalc():
    ##
    # Python program to calculate the speed of an object when it hits the ground after being dropped.
    ##

    # Define the constant
    GRAVITY = 9.80665

    # Read the input from user
    height = float(input("Height from which object is dropped (Metres Please): "))

    # Calculate the velocity
    velocity = sqrt(2 * GRAVITY * height)

    # Display the result
    print("Object will hit the ground at %.4f m/s." % velocity)

    # Get the mass
    mass = float(input("Mass of the object (Kilograms Please): "))

    # Get the energy
    energy = .5 * (mass * (velocity ** 2))

    Nuke = energy / 4184000000000

    # print the result
    print("The total energy is %.4f j." % energy)

    print("This is the equivalent of %f kilotons of TNT." % Nuke)


def ocalc():
    ri = float(input("Enter radius of celestial body (kilometres please): "))
    n = float(input("Enter Number of Satellites: "))
    # Cmass = float(input("Enter Mass of the celestial body(kilograms please): "))
    # Smass = float(input("Enter Mass of the satellite: "))

    a = n - 2
    b = 180
    C = a * b
    theta = (C / n)
    d = math.sin(math.radians(theta / 2))
    ro = ri / d

    print("The lowest possible orbit of these satellites is " + str(ro) + " kilometres. \n")

    # e = 2 * math.pi

    # print(T)


def oscalc():
    M = float(input("Enter mass of central body (kilograms please): "))
    R = float(input("Input radius of celestial body (kilometres please): "))

    top = scipy.constants.G * M
    v = sqrt(float(top) / R)

    print("The orbital speed of your satellite is " + str(v) + "m/s.")


def opecalc():
    print("DISCLAIMER: This calculator will ONLY work for Earth")
    h = input("Enter height from earth's surface (Subtract Earth radius from orbit radius): ")
    v = input("Enter Orbital Velocity (m/s please): ")

    top = 6378.14 + float(h)
    outer = 2 * math.pi
    inner = top / float(v)
    P = outer * inner

    print("Your Earth orbital period is " + str(P) + " seconds.")


def opcalc():
    r = input("Please input radius of orbit (Kilometres please): ")
    m = input("Please enter mass (kilograms please): ")

    top = 4 * (pi ** 2) + (float(r) ** 3)
    bottom = 0.00000000006674 * float(m)
    t = top / bottom
    # testing  -  5970000000000000000000000
    print("The orbital period is " + str(t) + "")

def soicalc():
    a = float(input("Please input major axis of celestially body. "))

if __name__ == "__main__":
    menu()
