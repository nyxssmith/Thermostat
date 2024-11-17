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
    from gpiozero import Servo
    servo = Servo(pin=pin_number,initial_value=None)

    # /home/nyxandaria/server/Thermostat/.venv/lib/python3.11/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from lgpio: No module named 'lgpio'
    # warnings.warn(
    # /home/nyxandaria/server/Thermostat/.venv/lib/python3.11/site-packages/gpiozero/output_devices.py:1509: PWMSoftwareFallback: To reduce servo jitter, use the pigpio pin factory.See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo for more info
except:
    servo=MockServo(pin_number)

sleep(0.1)

# track current status between boots
config_file = "config.json"

servo_position_file = "servo_position.txt"
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



# calibration settings
default_current_temperature = 60

def load_config():
    with open(config_file, "r") as f:
        config = json.load(f)
        global servo_move_time
        # timeout on the function that moves the servo
        servo_move_time = config["servo_move_time"]
        
def get_config():
    print("servo_move_time: ", servo_move_time)
    return {
        "servo_move_time": servo_move_time,
    }

# update the config from partial config
def update_config(new_partial_config):
    config = None
    with open(config_file, "r") as f:
        config = json.load(f)
        # only update the values that are valid
        if "servo_move_time" in new_partial_config:
            config["servo_move_time"] = new_partial_config["servo_move_time"]
        
    # save edits
    with open(config_file, "w") as f:
        json.dump(config, f)
    # update global variables
    load_config()

    return get_config()


def get_servo_position():
    # servo is either at min or max position
    with open(servo_position_file, "r") as f:
        return f.read()

def save_servo_position(pos):
    # servo is either at min or max position
    with open(servo_position_file, "w") as f:
        f.write({True:"max",False:"min"}[pos])

# move position up or down and save angle
def change_servo_position(up=True):
    if {True:"max",False:"min"}[up] == get_servo_position():
        print("already at target position")
        return {"current_position":get_servo_position()}
    # set value to pos or negative
    # set value to None to stop control
    if up:
        servo.value = -1
        sleep(servo_move_time)
        servo.value = None
    else:
        servo.value = 1
        sleep(servo_move_time)
        servo.value = None
    
    save_servo_position(up)
    return {"current_position":get_servo_position()}

def get_desired_position():
    # if temp is low, set to max, if temp is high, set to min
    if get_current_temperature() < get_desired_temperature():
        return "max"
    else:
        return "min"

def get_current_temperature():
    with open(current_temperature_file, "r") as f:
        return float(f.read())

def get_desired_temperature():
    with open(desired_temperature_file, "r") as f:
        return float(f.read())

def set_current_temperature(temp):
    with open(current_temperature_file, "w") as f:
        f.write(str(temp))

def set_desired_temperature(temp):
    with open(desired_temperature_file, "w") as f:
        f.write(str(temp))

# function to set the servo to either min or max based on the current temp and desired temp
# if current < desired, set to max if not yet at max position
# if current > desired, set to min if not yet at min position
def set_servo_to_desired_position():
    # reload config in case it was updated by a post request
    load_config()
    if get_current_temperature() < get_desired_temperature():
        if get_servo_position() == "min":
            change_servo_position(up=True)
    else:
        if get_servo_position() == "max":
            change_servo_position(up=False)


# startup
def startup():
    load_config()

startup()  

