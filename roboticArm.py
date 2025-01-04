import matplotlib.pyplot as plt #to draw and visualize the robotic arm as a series of lines and points on a graph
import numpy as np              #provides mathematical functions ( used here for trigonometric calculations to determine joint positions)
from gpiozero import Servo      #to control hardware connected to Raspberry Pi GPIO pins (servo)
from time import sleep          # to pause the program for a short duration to allow physical the servosto move

'''NOTE: Servo Motors are small motors that can rotate to specific angles, used to move the robotic arm joints.'''

'''
For successful use, you should run program and a window will pop up shoing the default position of the arm
close this window and use the terminal to be able to control the arm movement
you should close the window so that you can access controling options
'''



# Mock Servo Class
class MockServo:
    def __init__(self, pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000):
        print(f"Mock servo initialized on pin {pin}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        print(f"Mock servo set to {val}")

# Setting up servo motors
servo1 = MockServo(17,min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)# Joint 1
servo2 = MockServo(27,min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)# Joint 2
servo3 = MockServo(22,min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)# Joint 3


#convert degrees to radians (radians are required for trigonometric calculations)
def deg_to_rad(degrees):
    return degrees * (np.pi / 180)

# calculate the positions of the robotic arm(to know where each joint ends up based on angles)
# Angles determine the direction of each segment
# Lengths represent the size of each arm segment

def calculate_positions(angles):
    lengths = [1, 1, 1]  # Length of each arm segment

    x = [0]  # Starting x-coordinate of the base
    y = [0]  # Starting y-coordinate of the base

    for i in range(3):  # Loop through each joint
        # Calculate the angle from the base to the current joint
        theta = sum(deg_to_rad(angles[j]) for j in range(i + 1))
        # Calculate the new x and y coordinates for the joint
        x.append(x[-1] + lengths[i] * np.cos(theta))  # Update x-coordinate
        y.append(y[-1] + lengths[i] * np.sin(theta))  # Update y-coordinate

    return x, y

# convert angles (0-180) to servo positions (-1 to 1) *to control the physical movement of the servos*

def angle_to_servo_position(angle):
    return (angle / 180.0) * 2 - 1

# move servos to the given angles
# Updates the servo motor positions to match the desired angles
# The sleep function gives time for the servos to physically move

def set_servo_angles(angles):
    print("Moving servos to new positions...")
    servo1.value = angle_to_servo_position(angles[0])  # Move servo 1
    servo2.value = angle_to_servo_position(angles[1])  # Move servo 2
    servo3.value = angle_to_servo_position(angles[2])  # Move servo 3
    sleep(0.5)  # Wait for servos to move

# draw the robotic arm on the screen
# The arm is visualized as a series of connected lines

def plot_arm(x, y):
    print("Drawing the arm...")
    plt.figure()
    plt.plot(x, y, '-o', linewidth=2, markersize=8)  # Draw the arm segments
    plt.xlim(-3, 3)  # Limit the x-axis view
    plt.ylim(-3, 3)  # Limit the y-axis view
    plt.grid()  # Add a grid to the plot for clarity
    plt.title("Robotic Arm Position")  # Add a title to the plot
    plt.xlabel("X-axis")  # Label for the x-axis
    plt.ylabel("Y-axis")  # Label for the y-axis
    plt.show()  # Display the plot

# Function to ask the user for an angle and validate it
# Ensures the user inputs a valid angle between 0 and 180 degrees

def get_joint_angle(joint_number):
    while True:  # Keep asking until a valid angle is entered
        try:
            angle = float(input(f"Enter angle for Joint {joint_number} (0-180°): "))
            if 0 <= angle <= 180:  # Check if the angle is within range
                return angle  # Return the valid angle
            else:
                print("Invalid angle! Please enter a value between 0 and 180.")
        except ValueError:
            print("That's not a number! Please enter a valid angle.")


#MAIN

angles = [90, 90, 90]  # Starting angles for all joints

while True:
    print("\nCurrent angles:", angles)  # Display the current angles
    x, y = calculate_positions(angles)  # Get the positions of the joints
    plot_arm(x, y)  # Visualize the arm on the screen

    print("Options:") 
    print("1. Set Joint Angles")  
    print("2. Reset to Default Position")
    print("3. Exit") 

    choice = input("Choose an option (1/2/3): ")  # Get the user's choice

    if choice == '1':
        # Ask the user to enter new angles for each joint
        for i in range(3):
            angles[i] = get_joint_angle(i + 1)  # Get new angles from the user
        set_servo_angles(angles)  # Move servos to new angles
    elif choice == '2':
        # Reset the angles to the default position
        angles = [90, 90, 90]  # Default angles
        set_servo_angles(angles)  # Move servos to default position
    elif choice == '3':
        print("Exiting...")  
        break 
    else:
        print("Invalid option! Please try again.") 


