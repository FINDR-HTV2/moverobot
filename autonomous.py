import RPi.GPIO as IO
import time
import csv
import numpy as np
# BOARD/PIN NUMBERING STYLE
IO.setmode(IO.BOARD)
# PIN 12 and 16 - RIGHT WHEEL
IO.setup(12, IO.OUT)
IO.setup(16, IO.OUT)
# PIN 18 and 22 - LEFT WHEEL
IO.setup(18, IO.OUT)
IO.setup(22, IO.OUT)
# Initialize Pins 12,16,18,22 as PWM for driving the wheels
# fw,rv = forward, reverse r,l = right, left
fw_r = IO.PWM(12, 100)
rv_r = IO.PWM(16, 100)
fw_l = IO.PWM(18, 100)
rv_l = IO.PWM(22, 100)

# Ultrasonic Sensor 1 - LEFT SENSOR SETUP
left_trigger = 11
left_echo = 19
IO.setup(left_trigger, IO.OUT)
IO.setup(left_echo, IO.IN)

IO.output(left_trigger, False)
print("Waiting for left sensor")
time.sleep(0.5)

# Ultrasonic Sensor 2 - RIGHT SENSOR SETUP
right_trigger = 13
right_echo = 23
IO.setup(right_trigger, IO.OUT)
IO.setup(right_echo, IO.IN)

IO.output(left_trigger, False)
print("Waiting for right sensor")
time.sleep(0.5)

# Start pins 12,16,18,22 with 0% duty cycle
fw_r.start(0)
rv_r.start(0)
fw_l.start(0)
rv_l.start(0)


def getDistance(trigger, echo):
    # Clear previous trigger HIGH calls, especially if run within loop
    IO.output(trigger, False)
    # Keep delay from clear to HIGH minimal
    time.sleep(0.000002)
    # Set right or left trigger to HIGH
    IO.output(trigger, True)
    # 0.01ms set right or left trigger to LOW
    time.sleep(0.00001)
    # Stop the ultrasonic trigger
    IO.output(trigger, False)
    # Initialize start and stop times
    start_time = time.time()
    stop_time = time.time()
    # log start_time while echo is not present
    while IO.input(echo) == 0:
        start_time = time.time()
    # log time of echo at which echo arrives
    while IO.input(echo) == 1:
        stop_time = time.time()
    # diff. between initial start and stop time of echo
    diff_time = stop_time - start_time
    # multiply time by speed of sound and round to nearest cm
    distance_to_return = int(((diff_time * 34300) / 2))
    # Within use cases sensor accurate to 4-5 metres, so remove basic outlier
    # values greater than 5m
    if(distance_to_return > 500):
        distance_to_return = getDistance(trigger, echo)
    return distance_to_return


def turn(direction, turn_time):
    # Go forward a bit further before turn
    print("going further")
    time.sleep(0.40)
    # log the movement to csv
    movement = ["forward", 0.40]
    csvData.append(movement)
    stop(1)
    if direction == "left":
        fw_r.ChangeDutyCycle(80)
        rv_l.ChangeDutyCycle(80)
    elif direction == "right":
        rv_r.ChangeDutyCycle(80)
        fw_l.ChangeDutyCycle(80)
    else:
        pass
    # Completing the turn with given time
    time.sleep(turn_time)
    movement = [direction, turn_time]
    csvData.append(movement)
    stop(1)
    print ("turning")
    # Go in to the room
    print("going in straight")
    goStraight("forward")
    time.sleep(1)
    # Append movement to csv
    movement = ["forward", 1]
    csvData.append(movement)
    stop(2)
    # The following code was buggy with the current setup and we chose
    # to omit this functionality for the demo, however with proper hardware
    # implementation can be useful, especially to gain a wide scan of the room
    # Uncomment to use
    # # Scan Left
    # print("scanning left")
    # fw_r.ChangeDutyCycle(80)
    # rv_l.ChangeDutyCycle(80)
    # time.sleep(0.5)
    # stop(1)
    # # Scan Right
    # print ("scanning right")
    # rv_r.ChangeDutyCycle(80)
    # fw_l.ChangeDutyCycle(80)
    # time.sleep(1)
    # stop(1)
    # # Readjust
    # print ("readjusting")
    # fw_r.ChangeDutyCycle(80)
    # rv_l.ChangeDutyCycle(80)
    # time.sleep(0.5)
    # stop(1)
    # Backing out
    print("backing out")
    goStraight("backward")
    time.sleep(1.2)
    # Append movement to CSV
    movement = ["backward", 1]
    csvData.append(movement)
    stop(2)
    print("turning out")
    if direction == "left":
        # Right Wheel turning backwards, left in opposite direction
        rv_r.ChangeDutyCycle(80)
        fw_l.ChangeDutyCycle(80)
    elif direction == "right":
        rv_l.ChangeDutyCycle(80)
        fw_r.ChangeDutyCycle(80)
    else:
        pass
    # Completing the turn
    time.sleep(turn_time + 0.4)
    # Appending movement to csv
    movement = [str("reverse"+direction), turn_time + 0.4]
    csvData.append(movement)
    # Turn completed
    stop(1)


def stop(stoptime):
    # Set all pins to 0% duty cycle
    fw_r.ChangeDutyCycle(0)
    rv_r.ChangeDutyCycle(0)
    fw_l.ChangeDutyCycle(0)
    rv_l.ChangeDutyCycle(0)
    time.sleep(stoptime)


def goStraight(direction):
    # Pins 12 and 18 control forward movement in this setup
    if (direction == "forward"):
        fw_r.ChangeDutyCycle(80)
        fw_l.ChangeDutyCycle(80)
    # Pins 16 and 22 control backwards movement in this setup
    elif (direction == "backward"):
        rv_l.ChangeDutyCycle(80)
        rv_r.ChangeDutyCycle(80)
    else:
        pass

# Following two functions, retrieved from
# Source: https://www.datacrucis.com/research/find-outliers-in-an-array.html
# Intended to find indices in the array in which outliers are present.
# Implementation removed in a previous commit due to bugs but can be useful.
# Thought Process:
# ie. pass in distance array lists, get indices of outliers, if outliers are
# less than 1-2 and within index 1 or 2 (more likely 2, otherwise would turn),
# remove value, shift array to keep data succession and continue.


def is_outlier(value, p25, p75):
    lower = p25 - 1.5 * (p75 - p25)
    upper = p75 + 1.5 * (p75 - p25)
    return value <= lower or value >= upper


def get_indices_of_outliers(values):
    p25 = np.percentile(values, 25)
    p75 = np.percentile(values, 75)

    indices_of_outliers = []
    for ind, value in enumerate(values):
        if is_outlier(value, p25, p75):
            indices_of_outliers.append(ind)
    return indices_of_outliers


# Initialized to go straight
fw_r.ChangeDutyCycle(80)
fw_l.ChangeDutyCycle(80)
# Initialize left array
dist_array_left = [0, 0, 0, 0]
# Initialize right array
dist_array_right = [0, 0, 0, 0]
# Initialize csv data list
csvData = []
start = time.time()
# Initialize loop start time as 0 for initial relief period between scans
loop_start_time = 0
# Initialize Threshold value (in cm), this is assuming an array of 4
# ie. 200/4 = 50. So 50 cm is the actual threshold value
thold = 200
# Initialize Relief Period (seconds)
relief = 2.25
try:
    while True:
        # Move detected senor values sequentially to the left
        # (initially 0s so first run is neglible)
        dist_array_left[0] = dist_array_left[1]
        dist_array_left[1] = dist_array_left[2]
        dist_array_left[2] = dist_array_left[3]
        # Assign the last index of the array with the sensor value
        dist_array_left[3] = getDistance(left_trigger, left_echo)
        # Display Sensor Output for debug
        print(dist_array_left)
        time.sleep(0.1)
        # Move detected senor values sequentially to the left
        # (initially 0s so first run is neglible)
        dist_array_right[0] = dist_array_right[1]
        dist_array_right[1] = dist_array_right[2]
        dist_array_right[2] = dist_array_right[3]
        # Assign the last index of the array with the sensor value
        dist_array_right[3] = getDistance(right_trigger, right_echo)
        print(dist_array_right)
        time.sleep(0.1)
        # Calculate the elapsed time since last loop iteration
        last_loop = time.time() - loop_start_time
        # Add distance values to be averaged
        sum_dist_right = (dist_array_left[0] + dist_array_left[1] +
                          dist_array_left[2] + dist_array_left[3])
        if ((sum_dist_right > threshold) and (last_loop > relief)):
            end = time.time()
            movement = ["forward", end - start]
            csvData.append(movement)
            turn("left", 0.8)
            loop_start_time = time.time()
            stop(1)
            start = time.time()
            goStraight("forward")
        elif ((sum_dist_right > threshold) and (last_loop > relief)):
            end = time.time()
            movement = ["forward", end - start]
            csvData.append(movement)
            turn("right", 0.7)
            loop_start_time = time.time()
            stop(1)
            start = time.time()
            goStraight("forward")
        else:
            pass
        # Additonally an extra check can be implemented for higher
        # accuracy and also to work with even more arbitrary sensor values
        # Sample implementation from previous commit, now removed
        # if abs(prev_dist_right - curr_dist_right) > 50:
        #   turn("right", turn_time(what value is chosen))
        #   stop(1)
        #   goStraight("forward")
        # else:
        #   pass

except KeyboardInterrupt:
    # Append/write to csv
    movement = ["forward", time.time()-start]
    csvData.append(movement)
    myFile = open('movementMap.csv', 'w+')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(csvData)
    myFile.close()
    # Cleanup GPIO signals so pin states are cleared and ready on close
    IO.cleanup()
