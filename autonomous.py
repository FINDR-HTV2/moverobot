import RPi.GPIO as IO
# import time
import time
import thread
# BOARD/PIN NUMBERING STYLE
IO.setmode(IO.BOARD)
# PIN 12 and 16 - RIGHT WHEEL
IO.setup(12, IO.OUT)
IO.setup(16, IO.OUT)
# PIN 18 and 22 - LEFT WHEEL
IO.setup(18, IO.OUT)
IO.setup(22, IO.OUT)
# Initialize Pins 12,16,18,22 as PWM for driving the wheels
fw_r = IO.PWM(12, 100)
rv_r = IO.PWM(16, 100)
fw_l = IO.PWM(18, 100)
rv_l = IO.PWM(22, 100)

# UNCOMMENT THE FOLLOWING LINES OF CODE ONCE WIRING IS DETERMINED

# Ultrasonic Sensor 1 - LEFT SENSOR SETUP
left_trigger = 11
left_echo = 19
IO.setup(left_trigger, IO.OUT)
IO.setup(left_echo, IO.IN)

IO.output(left_trigger, False)
print("waiting for sensor")
time.sleep(2)

# Ultrasonic Sensor 2 - RIGHT SENSOR SETUP
right_trigger = 13
right_echo = 21
IO.setup(right_trigger, IO.OUT)
IO.setup(right_echo, IO.IN)

# Start pins 12,16,18,22 with 0% duty cycle
fw_r.start(0)
rv_r.start(0)
fw_l.start(0)
rv_l.start(0)

def getDistance(trigger, echo):
	# Clear 
	IO.output(trigger, False)
	time.sleep(0.000002)
	# Set right or left trigger to high
	IO.output(trigger, True)
	# 0.01ms set right or left trigger to LOW
	time.sleep(0.00001)
	IO.output(trigger, False)
	start_time = time.time()
	stop_time = time.time()
	# log start_time
	while IO.input(echo) == 0:
	    start_time = time.time()
	# log time of echo to arrive
	while IO.input(echo) == 1:
	    stop_time = time.time()
	# diff. between initial start and stop time of echo
	diff_time = stop_time - start_time
	distance_to_return = int(((diff_time * 34300) / 2))
	if(distance_to_return > 500):
		distance_to_return = getDistance(trigger, echo)
	return distance_to_return

# def moveRightLeft(right_dist, left_dist):
# 	# Decide which way has a greater value and decide which way SAR should turn
# 	# True = Left, False = Right
# 	direction = left_dist > right_dist
# 	if (direction and (left_dist < ))

def turn(direction, sleep_time):
	# go a bit further before turn
	time.sleep(0.40)
	stop(1)
	if direction == "left":
		# Forward
		fw_r.ChangeDutyCycle(80)
		# Backwards
		rv_l.ChangeDutyCycle(80)
	elif direction == "right":
		# Backwards
		rv_r.ChangeDutyCycle(80)
		# Forwards
		fw_l.ChangeDutyCycle(80)
	else:
		pass
	# Turning the thing
	time.sleep(sleep_time)
	stop(0.5)
	# Scan Left
	fw_r.ChangeDutyCycle(80)
	rv_l.ChangeDutyCycle(80)
	time.sleep(0.5)
	stop(0.5)
	# Scan Right
	rv_r.ChangeDutyCycle(80)
	fw_l.ChangeDutyCycle(80)
	time.sleep(1)
	stop(0.5)
	# Readjust
	fw_r.ChangeDutyCycle(80)
	rv_l.ChangeDutyCycle(80)
	time.sleep(0.5)
	stop(0.5)
	# Backing out
	if direction == "left":
		# Everything else stationary
		# Right Wheel turning
		rv_r.ChangeDutyCycle(80)
	elif direction == "right":
		rv_l.ChangeDutyCycle(80)
		# Everything else stationary
	else:
		pass
	# Turning the thing
	time.sleep(sleep_time)
	stop(0.5)

def stop(stoptime):
	fw_r.ChangeDutyCycle(0)
	rv_r.ChangeDutyCycle(0)
	fw_l.ChangeDutyCycle(0)
	rv_l.ChangeDutyCycle(0)
	time.sleep(stoptime)

def goStraight(direction):
	if (direction == "forward"):
		fw_r.ChangeDutyCycle(80)
		fw_l.ChangeDutyCycle(80)
	elif (direction == "backward"):
		rv_l.ChangeDutyCycle(80)
		rv_r.ChangeDutyCycle(80)
	else:
		pass


# Initially goes straight
fw_r.ChangeDutyCycle(80)
fw_l.ChangeDutyCycle(80)

prev_dist_left = 0
curr_dist_left = 0
prev_dist_right = 0
curr_dist_right = 0


# While loop for initial test
try:
	while True:
		curr_dist_left = getDistance(left_trigger, left_echo)
		print(curr_dist_left)
		time.sleep(0.1)
		curr_dist_right = getDistance(right_trigger, right_echo)	
		print(curr_dist_right)
		time.sleep(0.1)
		if abs(prev_dist_left - curr_dist_left) > 50:
			turn("left", 0.20)
			stop(1)
			goStraight("forward")
		elif abs(prev_dist_right - curr_dist_right) > 50:
			turn("right", 0.20)
			stop(1)
			goStraight("forward")
		else:
			pass
		prev_dist_left = curr_dist_left
		# prev_dist_right = curr_dist_right
except KeyboardInterrupt:
	IO.cleanup()