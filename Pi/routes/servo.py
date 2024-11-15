from flask import request, jsonify
import servo_control

# calibration step
# 0 == not active
# 1 == move up until at 80
# 2 == move down until at 50
calibration_step = 0

def servo_position():
    if request.method == "GET":
        # servo positions are the internal degrees counts of the servo
        # during calibration, 60 degrees on the temp dial is set to 0 servo degrees
        # then 80F on dial is set to N servo degrees and 50F on dial is set to M servo degrees
        # also return the servo modules value
        response = {"current_position": servo_control.get_servo_position(),"current_value": servo_control.get_servo_value(),"current_angle":servo_control.get_servo_angle(),"desired_position":servo_control.get_desired_position()}
    else:
        # assume post
        data = request.get_json()
        # get the "value" from the post request
        if "value" in data:
            # set the servo value
            # in a comment put the curl command to send "value":0.1 to the servo endpoint
            # curl -X POST -H "Content-Type: application/json" -d '{"value":0.1}' http://
            servo_control.set_servo_value(data["value"])
            response = {"message": f"Servo value set to {data['value']}"}
        elif "angle" in data:
            # set the servo angle
            # in a comment put the curl command to send "angle":50 to the servo endpoint
            # curl -X POST -H "Content-Type: application/json" -d '{"angle":50}' http://
            servo_control.set_servo_angle(data["angle"])
            response = {"message": f"Servo angle set to {data['angle']}"}
        else:
            response = {"message": "No value received"}
        
    return jsonify(response)

def desired_temperature():
    # TODO: Implement this function for post and get
    response = {"message": "todo"}
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
    # file will contain calibration step
    calibration_step = servo_control.get_calibration_step()
    print(f"calibration step: {calibration_step}")

    # if doing get either tell the user that calibration is active or the current step to do
    if request.method == "GET":
        if calibration_step:
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
        # start calibration
        calibration_step = 1
        servo_control.set_calibration_step(calibration_step)
        return jsonify({"message": "Calibration started"})
    elif data["command"] == "cancel":
        # turn off calibration
        calibration_step = 0
        servo_control.set_calibration_step(calibration_step)
        return jsonify({"message": "Calibration cancelled"})
    elif data["command"] == "next":
        # called to move servo to next step during calibration 
        if calibration_step == 1:
            # move up from 60
            servo_control.change_servo_position(True)
            return jsonify({"message": f"servo moved for {servo_control.servo_sleep_time}s up"})
        elif calibration_step == 2:
            # move down to 60
            servo_control.change_servo_position(False)
            return jsonify({"message": f"servo moved for {servo_control.servo_sleep_time}s down"})    
        else:
            return jsonify({"message": "Not right time for \"next\" command"})
    elif data["command"] == "at 80":
        # called to save servo position for 80 degrees
        if calibration_step == 1:
            # save servo position for 80 degrees
            servo_control.update_config({"servo_degrees_max_temp":servo_control.get_servo_position()})
            calibration_step = 2
            servo_control.set_calibration_step(calibration_step)
            return jsonify({"message": "Saved servo position for 80 degrees"})
        else:
            return jsonify({"message": "Not right time for \"at 80\" command"})
    elif data["command"] == "at 50":
        # called to save servo position for 50 degrees
        if calibration_step == 2:
            # save servo position for 50 degrees
            servo_control.update_config({"servo_degrees_min_temp":servo_control.get_servo_position()})
            calibration_step = 0
            servo_control.set_calibration_step(calibration_step)
            return jsonify({"message": "Saved servo position for 50 degrees, calibration complete"})
        else:
            return jsonify({"message": "Not right time for \"at 80\" command"})

def get_servo_config():
    response = servo_control.get_config()
    return jsonify(response)

def set_servo_config():
    data = request.get_json()
    response = servo_control.update_config(data)
    return jsonify(response)
