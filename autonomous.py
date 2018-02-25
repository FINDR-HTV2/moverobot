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

# Ultrasonic Sensor 1 - LEFT SENSOR
left_trigger = 11
left_echo = 19
IO.setup(left_trigger, IO.OUT)
IO.setup(left_echo, IO.IN)

IO.output(left_trigger, False)
print("waiting for sensor")
time.sleep(2)

# Ultrasonic Sensor 2 - RIGHT SENSOR
# right_trigger = 
# right_echo =
# IO.setup(right_trigger, IO.OUT)
# IO.setup(right_echo, IO.IN)

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
	stop(1)
	if direction == "left":
		# Forward
		fw_r.ChangeDutyCycle(80)
		# Backwards
		rv_l.ChangeDutyCycle(80)
	else:
		# Backwards
		rv_r.ChangeDutyCycle(80)
		# Forwards
		fw_l.ChangeDutyCycle(80)
	time.sleep(sleep_time)

def stop(stoptime):
	fw_r.ChangeDutyCycle(0)
	rv_r.ChangeDutyCycle(0)
	fw_l.ChangeDutyCycle(0)
	rv_l.ChangeDutyCycle(0)
	time.sleep(stoptime)

def goStraight():
	fw_r.ChangeDutyCycle(80)
	fw_l.ChangeDutyCycle(80)

fw_r.ChangeDutyCycle(80)
fw_l.ChangeDutyCycle(80)

prev_dist = 0
curr_dist = 0

# While loop for initial test
while True:
	# curr_dist = getDistance(left_trigger, left_echo)
	# if abs(prev_dist - curr_dist) > 50:
	# 	turn("left")
	# 	stop(1)
	# 	goStraight()
	# prev_dist = curr_dist 
	# print (getDistance(left_trigger, left_echo))
	# time.sleep(0.1)
	turn("left", 0.6)
	goStraight()
	turn("right", 0.6)
	goStraight()

	