from flask import request, jsonify
import Pi.routes.servo_control as servo_control

# calibration step
# 0 == not active
# 1 == move up until at 80
# 2 == move down until at 50
calibration_step = 0

def get_servo_position():
    response = {"current_position": servo_control.get_servo_position(),"desired_position":servo_control.get_desired_position()}
    return jsonify(response)

def desired_temperature():
    # TODO: Implement this function for post and get
    response = {"message": "Data received to get servo position"}
    return jsonify(response)

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
def calibrate():
    # if doing get either tell the user that calibration is active or the current step to do
    if request.method == "GET":
        if calibration_active:
            return jsonify({"message": "Calibration is active"})
        else:
            return jsonify({"message": "Calibration is not active"})
    # if is post
    data = request.get_json()  # Get JSON data from the request
    # safeties
    if not data:
        return jsonify({"message": "No data received"})
    if "command" not in data:
        return jsonify({"message": "No command received"})
    # command processing
    if data["command"] == "start":
        calibration_active = 1
        return jsonify({"message": "Calibration started"})
    elif data["command"] == "cancel":
        calibration_active = 0
        return jsonify({"message": "Calibration cancelled"})    

def get_servo_config():
    response = servo_control.get_config()
    return jsonify(response)

def set_servo_config():
    data = request.get_json()
    response = servo_control.update_config(data)
    return jsonify(response)
