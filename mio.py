from firebase import firebase
import RPi.GPIO as IO
import time
firebase = firebase.FirebaseApplication('https://sarhtv2.firebaseio.com', None)

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

# Start pins 12,16,18,22 with 0% duty cycle
fw_r.start(0)
rv_r.start(0)
fw_l.start(0)
rv_l.start(0)


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


try:
    while True:
        result = str(firebase.get('/myoEvents', None)).split("'")
        if result[3] == "fist":
            stop(.05)
        if result[3] == "waveIn":
            goStraight("forward")
            time.sleep(.05)
        if result[3] == "waveOut":
            goStraight("backward")
            time.sleep(.05)
        if result[3] == "doubleTap":
            pass
        if result[3] == "fingers":
            pass

except KeyboardInterrupt:
    IO.cleanup()