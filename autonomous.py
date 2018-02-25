import RPi.GPIO as IO
# import time
import time
# BOARD NUMBERING
IO.setmode(IO.BOARD)
# PIN 12 and 16
IO.setup(12, IO.OUT)
IO.setup(16, IO.OUT)
# PIN 18 and 22
IO.setup(18, IO.OUT)
IO.setup(22, IO.OUT)
# Initialize Pins 12,16,18,22 as PWM
pin12 = IO.PWM(12, 100)
pin16 = IO.PWM(16, 100)
pin18 = IO.PWM(18, 100)
pin22 = IO.PWM(22, 100)
# Start pins 12,16,18,22 with 0% duty cycle
pin12.start(0)
pin16.start(0)
pin18.start(0)
pin22.start(0)

# While loop for initial test
while True:
	# Go forward both wheels
	pin12.ChangeDutyCycle(100)
	pin18.ChangeDutyCycle(100)
	# sleep 1 second
	time.sleep(1)
	pin12.ChangeDutyCycle(0)
	pin18.ChangeDutyCycle(0)
	time.sleep(1)
