import RPi.GPIO as IO
# import time
import time
# BOARD/PIN NUMBERING STYLE
IO.setmode(IO.BOARD)
# PIN 12 and 16 - RIGHT WHEEL
IO.setup(12, IO.OUT)
IO.setup(16, IO.OUT)
# PIN 18 and 22 - LEFT WHEEL
IO.setup(18, IO.OUT)
IO.setup(22, IO.OUT)
# Initialize Pins 12,16,18,22 as PWM for driving the wheels
pin12 = IO.PWM(12, 100)
pin16 = IO.PWM(16, 100)
pin18 = IO.PWM(18, 100)
pin22 = IO.PWM(22, 100)

# UNCOMMENT THE FOLLOWING LINES OF CODE ONCE WIRING IS DETERMINED

# Ultrasonic Sensor 1 - LEFT SENSOR
left_trigger = 11
left_echo = 19
IO.setup(left_trigger, IO.OUT)
IO.setup(left_echo, IO.IN)

# Ultrasonic Sensor 2 - RIGHT SENSOR
# right_trigger = 
# right_echo =
# IO.setup(right_trigger, IO.OUT)
# IO.setup(right_echo, IO.IN)

# Start pins 12,16,18,22 with 0% duty cycle
pin12.start(0)
pin16.start(0)
pin18.start(0)
pin22.start(0)

def getDistance(trigger, echo):
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
    distance_to_return = (diff_time * 34300) / 2
    return distance_to_return
    
# While loop for initial test
while True:
	# # Go forward both wheels
	# pin12.ChangeDutyCycle(50)
	# pin18.ChangeDutyCycle(50)
	# # sleep 1 second
	# time.sleep(1)
	# # Go stop the wheels with a 0% duty cycle
	# pin12.ChangeDutyCycle(0)
	# pin18.ChangeDutyCycle(0)
	# # delay 1 second
	# time.sleep(1)

	# Uncomment when we get distance up and running
	# Right Distance:
	# print (getDistance(right_trigger, right_echo))
	# Left Distance:  
	print (getDistance(left_trigger, left_echo))
