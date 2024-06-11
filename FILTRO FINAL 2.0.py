# The nececary libraries are imported
import serial
import numpy as np
import time
import math as mt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# The serial port is configured to stablish communication with the Arduino
ser = serial.Serial("COM5", 115200)
ser.flushInput()
previous_time = time.time()

# We definie initial values for the starting angles of gyroscope
angleYgyro_prev = 0
angleXgyro_prev = 0
angleZgyro_prev = 0
Angle_Y_prev = 0
Angle_X_prev = 0
Angle_Z_prev = 0

# We define the lists to store the obtanied data
times = []
angleYacc_data = []
angleXacc_data = []
angleZacc_data = []
angleYgyro_data = []
angleXgyro_data = []
angleZgyro_data = []
Angle_Y_data = []
Angle_X_data = []
Angle_Z_data = []

start_time = time.time()

# We set up the graphs parameters and configuration
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

line_angleXacc, = ax1.plot([], [], label="X angle with acceleration")
line_angleXgyro, = ax1.plot([], [], label="X angle with gyroscope")
line_Angle_X, = ax1.plot([], [], label="X angle with complementary filter",linestyle="--", linewidth=2.5, color="red")

line_angleYacc, = ax2.plot([], [], label="Y angle with acceleration")
line_angleYgyro, = ax2.plot([], [], label="Y angle with gyroscope")
line_Angle_Y, = ax2.plot([], [], label="Y angle with complementary filter", linestyle="--", linewidth=2.5, color="red") 

line_angleZacc, = ax3.plot([], [], label="Z angle with acceleration")
line_angleZgyro, = ax3.plot([], [], label="Z angle with gyroscope")
line_Angle_Z, = ax3.plot([], [], label="Z angle with complementary filter", linestyle="--", linewidth=2.5, color="red")

ax1.legend(loc="upper right")
ax1.set_ylabel("Angle X (°)")
ax1.set_xlabel("Time (s)")

ax2.legend(loc="upper right")
ax2.set_ylabel("Angle Y (°)")
ax2.set_xlabel("Time (s)")

ax3.legend(loc="upper right")
ax3.set_ylabel("Angle Z (°)")
ax3.set_xlabel("Time (s)")

 # We define a formula to handle errors when calculating the angles with the accelerometer
def calculate_angles(ax, ay, az):
    # Calculate angleYacc
    try:
        angleYacc = mt.atan(-ax / mt.sqrt(ay**2 + az**2)) * 180 / mt.pi
    except ZeroDivisionError:
        angleYacc = 0.0

    # Calculate angleXacc
    try:
        angleXacc = mt.atan(ay / mt.sqrt(ax**2 + az**2)) * 180 / mt.pi
    except ZeroDivisionError:
        angleXacc = 0.0

    # Calculate angleZacc
    try:
        angleZacc = mt.atan(mt.sqrt(ax**2 + ay**2) / az) * 180 / mt.pi
    except ZeroDivisionError:
        angleZacc = 0.0

    return angleYacc, angleXacc, angleZacc

# We define the complementary filter function
def Complementary_Filter(angleYacc, gy, angleXacc, gx, angleZacc, gz, dt, Angle_Y_prev, Angle_X_prev, Angle_Z_prev):

    Angle_Y = 0
    Angle_X = 0
    Angle_Z = 0
    A = 0.96 # This value can be modified to change the filter response, this was the value that gave the best results

    Angle_Y =  A* (Angle_Y_prev + ((gy/16.4)*dt)) + (1-A) * angleYacc
    Angle_X =  A* (Angle_X_prev + ((gx/16.4)*dt)) + (1-A) * angleXacc
    Angle_Z =  A* (Angle_Z_prev + ((gz/16.4)*dt)) + (1-A) * angleZacc

    return Angle_Y, Angle_X, Angle_Z


# We define the update function for the animation, which itslef will update the data and the graphs
def update(frame):
    global times, previous_time, angleYacc_data, angleXacc_data, angleZacc_data, angleYgyro_data, angleXgyro_data, angleZgyro_data, Angle_Y_data, Angle_X_data, Angle_Z_data, angleYgyro_prev, angleXgyro_prev, angleZgyro_prev
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").rstrip()
        data = line.split(",")
        if len(data) == 6:  
            try:
                ax, ay, az, gx, gy, gz = map(float, data)
            except ValueError:
                print(data)
            else:

                # Formulas to calculate the angles with the accelerometer
                angleYacc, angleXacc, angleZacc = calculate_angles(ax, ay, az)
               
                # Formulas to calculate the angles with the gyroscope
                dt = time.time() - previous_time
                previous_time = time.time()
                angleYgyro = ((gy/16.4)*dt) + angleYgyro_prev
                angleXgyro = ((gx/16.4)*dt) + angleXgyro_prev
                angleZgyro = ((gz/16.4)*dt) + angleZgyro_prev

                angleYgyro_prev = angleYgyro
                angleXgyro_prev = angleXgyro
                angleZgyro_prev = angleZgyro

                # We apply the complementary filter to the angles, using the angles obtained by the accelerometer and the gyroscope data
                global Angle_Y_prev, Angle_X_prev, Angle_Z_prev

                Angle_Y, Angle_X, Angle_Z = Complementary_Filter(angleYacc, gy, angleXacc, gx, angleZacc, gz, dt, Angle_Y_prev, Angle_X_prev, Angle_Z_prev)

                Angle_Y_prev = Angle_Y
                Angle_X_prev = Angle_X
                Angle_Z_prev = Angle_Z

                # We store the data in the previously defined lists
                current_time = time.time() - start_time
                times.append(current_time)
                angleYacc_data.append(angleYacc)
                angleXacc_data.append(angleXacc)
                angleZacc_data.append(angleZacc)
                angleYgyro_data.append(angleYgyro)
                angleXgyro_data.append(angleXgyro)
                angleZgyro_data.append(angleZgyro)
                Angle_Y_data.append(Angle_Y)
                Angle_X_data.append(Angle_X)
                Angle_Z_data.append(Angle_Z)

                # We stablish a limit for the stored data to improve the performance of the program
                max_data_points = 30
                times = times[-max_data_points:]
                angleYacc_data = angleYacc_data[-max_data_points:]
                angleXacc_data = angleXacc_data[-max_data_points:]
                angleZacc_data = angleZacc_data[-max_data_points:]
                angleYgyro_data = angleYgyro_data[-max_data_points:]
                angleXgyro_data = angleXgyro_data[-max_data_points:]
                angleZgyro_data = angleZgyro_data[-max_data_points:]
                Angle_Y_data = Angle_Y_data[-max_data_points:]
                Angle_X_data = Angle_X_data[-max_data_points:]
                Angle_Z_data = Angle_Z_data[-max_data_points:]

               
                # We update the graphs with the data stored in the defined lists
                line_angleYacc.set_xdata(times)
                line_angleYacc.set_ydata(angleYacc_data)

                line_angleXacc.set_xdata(times)
                line_angleXacc.set_ydata(angleXacc_data)

                line_angleZacc.set_xdata(times)
                line_angleZacc.set_ydata(angleZacc_data)

                line_angleYgyro.set_xdata(times)
                line_angleYgyro.set_ydata(angleYgyro_data)

                line_angleXgyro.set_xdata(times)
                line_angleXgyro.set_ydata(angleXgyro_data)

                line_angleZgyro.set_xdata(times)
                line_angleZgyro.set_ydata(angleZgyro_data)

                line_Angle_Y.set_xdata(times)
                line_Angle_Y.set_ydata(Angle_Y_data)

                line_Angle_X.set_xdata(times)
                line_Angle_X.set_ydata(Angle_X_data)

                line_Angle_Z.set_xdata(times)
                line_Angle_Z.set_ydata(Angle_Z_data)

                #We use this code to update the graphs scales based on the displayed data
                ax1.relim()
                ax1.autoscale_view()
                ax2.relim()
                ax2.autoscale_view()
                ax3.relim()
                ax3.autoscale_view()
        else:
            print(f": {line}")

# The animation that will update the graphs, and loop the code
ani = FuncAnimation(fig, update, interval=50)

plt.tight_layout()
plt.show()

ser.close()  

    