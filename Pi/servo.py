from gpiozero import Servo,AngularServo
from time import sleep

pin_number = 25

servo = AngularServo(pin_number, min_angle=-90, max_angle=90)
servo.angle = 0
servo.max()
sleep(0.1)

# track current status between boots
position_file = "servo_position.txt"
current_temperature_file = "current_temperature.txt"
desired_temperature_file = "desired_temperature.txt"

# servo parameters
# TODO load from json that can be posted to to update
# run the min or max cmd for this amount of time, then save the position
servo_sleep_time = 0.01
# degrees for when the servo has set the dial to max and min temp
servo_degrees_max_temp = 90
servo_degrees_min_temp = -90
# how much slop to allow when checking if the servo is at the desired position
servo_degrees_allowed_slop = 3

# calibration settings
default_servo_position = 0
default_current_temperature = 70

# servo position 
def get_servo_position():
    with open(position_file, "r") as f:
        return int(f.read())

# update servo class with the saved position from last run
def set_servo_position(position):
    servo.angle = position
    
def save_servo_position():
    print(servo.angle)
    with open(position_file, "w") as f:
        f.write(str(servo.angle))

# move position up or down and save angle
def change_servo_position(up=True):
    if up:
        servo.max()
        sleep(servo_sleep_time)
    else:
        servo.min()
        sleep(servo_sleep_time)
    save_servo_position()

def get_current_temperature():
    with open(current_temperature_file, "r") as f:
        return float(f.read())

def get_desired_temperature():
    with open(desired_temperature_file, "r") as f:
        return float(f.read())

def servo_position_close_enough(desired_position):
    return abs(get_servo_position() - desired_position) < servo_degrees_allowed_slop

# function to set the servo to either min or max based on the current temp and desired temp
# if current < desired, set to max if not yet at max position
# if current > desired, set to min if not yet at min position
def set_servo_to_desired_position():
    if get_current_temperature() < get_desired_temperature():
        if not servo_position_close_enough(servo_degrees_max_temp):
            change_servo_position(up=True)
    else:
        if not servo_position_close_enough(servo_degrees_min_temp):
            change_servo_position(up=False)

# calibration function to set the servo degrees to temp values
# if /calibrate is called via post "start" it will enter calibration mode
# if /calibrate is called via post "at 80" it will save servo position as max temp position
# if /calibrate is called via post "at 50" it will save servo position as min temp position
# if /calibrate is called via get it will return the next step to take
# if /calibrate is called via post "next" it will step call change_servo_position to move the servo
# prompt user to set the dial to 70 then send a post request to trigger next step
# when user sends post request to /calibrate, move servo up until post request contains value of "at 80"
# then move servo down until post request contains value of "at 50"
# save the values that the servo is at for 80 and 50 to min and max temp config file
