from time import sleep
import json
import os

class MockServo:
    def __init__(self, pin_number):
        self.angle = 0
        self.value = None
    # mock change angles
    def max(self):
        self.angle += 10
        print("servo max")
    def min(self):
        self.angle -= 10
        print("servo min")

pin_number = 25

# only run this if on Pi
try:
    from gpiozero import Servo,AngularServo
    servo = AngularServo(pin_number, min_angle=-90, max_angle=90)
    servo.angle = 0
    servo.max()

    # /home/nyxandaria/server/Thermostat/.venv/lib/python3.11/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from lgpio: No module named 'lgpio'
    # warnings.warn(
    # /home/nyxandaria/server/Thermostat/.venv/lib/python3.11/site-packages/gpiozero/output_devices.py:1509: PWMSoftwareFallback: To reduce servo jitter, use the pigpio pin factory.See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo for more info
except:
    servo=MockServo(pin_number)
sleep(0.1)

# track current status between boots
config_file = "config.json"
position_file = "servo_position.txt"
calibration_step_file = "calibration_step.txt"
current_temperature_file = "current_temperature.txt"
desired_temperature_file = "desired_temperature.txt"

# TODO maybe this
"""
def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        with open(fname, 'a')as f:
            f.write("0")
            f.close()

def ensure_files():
    if not os.path.exists(os.path.join(os.getcwd(),config_file)):
        touch(config_file)
    if not os.path.exists(os.path.join(os.getcwd(),position_file)):
        touch(position_file)
    if not os.path.exists(os.path.join(os.getcwd(),calibration_step_file)):
        touch(calibration_step_file)
    if not os.path.exists(os.path.join(os.getcwd(),current_temperature_file)):
        touch(current_temperature_file)
    if not os.path.exists(os.path.join(os.getcwd(),desired_temperature_file)):
        touch(desired_temperature_file)
#ensure_files()
"""

# servo parameters
# run the min or max cmd for this amount of time, then save the position
servo_sleep_time = 0.01
# degrees for when the servo has set the dial to max and min temp
servo_degrees_max_temp = 90
servo_degrees_min_temp = -90
# how much slop to allow when checking if the servo is at the desired position
servo_degrees_allowed_slop = 3
# THESE WILL ALL BE SET BY CONFIG FILE ^


# calibration settings
default_servo_position = 0
default_current_temperature = 60


def get_calibration_step():
    with open(calibration_step_file, "r") as f:
        return int(f.read())

def set_calibration_step(step):
    with open(calibration_step_file, "w") as f:
        f.write(str(step))

def load_config():
    with open(config_file, "r") as f:
        config = json.load(f)
        global servo_sleep_time, servo_degrees_max_temp, servo_degrees_min_temp, servo_degrees_allowed_slop, default_servo_position
        servo_sleep_time = config["servo_sleep_time"]
        servo_degrees_max_temp = config["servo_degrees_max_temp"]
        servo_degrees_min_temp = config["servo_degrees_min_temp"]
        servo_degrees_allowed_slop = config["servo_degrees_allowed_slop"]
        default_servo_position = config["default_servo_position"]

def get_config():
    print("servo_sleep_time: ", servo_sleep_time)
    print("servo_degrees_max_temp: ", servo_degrees_max_temp)
    print("servo_degrees_min_temp: ", servo_degrees_min_temp)
    print("servo_degrees_allowed_slop: ", servo_degrees_allowed_slop)
    print("default_servo_position: ", default_servo_position)
    return {
        "servo_sleep_time": servo_sleep_time,
        "servo_degrees_max_temp": servo_degrees_max_temp,
        "servo_degrees_min_temp": servo_degrees_min_temp,
        "servo_degrees_allowed_slop": servo_degrees_allowed_slop,
        "default_servo_position": default_servo_position
    }

# update the config from partial config
def update_config(new_partial_config):
    config = None
    with open(config_file, "r") as f:
        config = json.load(f)
        # only update the values that are valid
        if "servo_sleep_time" in new_partial_config:
            config["servo_sleep_time"] = new_partial_config["servo_sleep_time"]
        if "servo_degrees_max_temp" in new_partial_config:
            config["servo_degrees_max_temp"] = new_partial_config["servo_degrees_max_temp"]
        if "servo_degrees_min_temp" in new_partial_config:
            config["servo_degrees_min_temp"] = new_partial_config["servo_degrees_min_temp"]
        if "servo_degrees_allowed_slop" in new_partial_config:
            config["servo_degrees_allowed_slop"] = new_partial_config["servo_degrees_allowed_slop"]
        if "default_servo_position" in new_partial_config:
            config["default_servo_position"] = new_partial_config["default_servo_position"]
    # save edits
    with open(config_file, "w") as f:
        json.dump(config, f)
    # update global variables
    load_config()

# servo position 
def get_servo_position():
    with open(position_file, "r") as f:
        return int(f.read())

# update servo class with the saved position from last run
def set_servo_position(position):
    servo.angle = position
    
def save_servo_position():
    print(f"servo angle now {servo.angle}")
    with open(position_file, "w") as f:
        f.write(str(servo.angle))

# move position up or down and save angle
def change_servo_position(up=True):
    # try servo.value

    if up:
        servo.max()
        sleep(servo_sleep_time)
    else:
        servo.min()
        sleep(servo_sleep_time)
    save_servo_position()

def get_desired_position():
    if get_current_temperature() < get_desired_temperature():
        return servo_degrees_max_temp
    else:
        return servo_degrees_min_temp

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
    # reload config in case it was updated by a post request
    load_config()
    if get_current_temperature() < get_desired_temperature():
        if not servo_position_close_enough(servo_degrees_max_temp):
            change_servo_position(up=True)
    else:
        if not servo_position_close_enough(servo_degrees_min_temp):
            change_servo_position(up=False)


# startup
# TODO more here
def startup():
    load_config()
    servo.value = None
    #set_servo_position(default_servo_position)

startup()  

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
