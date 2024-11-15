from flask import request, jsonify
import servo_control


def servo_position():
    if request.method == "GET":
        # get if its at min or max
        response = {"current_position": servo_control.get_servo_position(),"desired_position":servo_control.get_desired_position()}
    else:
        # assume post
        data = request.get_json()
        # pass command to servo pos changer and make the servo move to min or max
        # ignores desired position 
        if "command" in data:
            response = servo_control.change_servo_position({"max":True,"min":False}[data["command"]])
    
    return jsonify(response)


# tell servo module about temperature
def desired_temperature():
    # get or set the servo config
    if request.method == "GET":
        response = servo_control.get_desired_temperature()
        return jsonify(response)
    else:
        data = request.get_json()
        response = servo_control.set_desired_temperature(data["temperature"])
        return jsonify(response)

def current_temperature():
    # get or set the servo config
    if request.method == "GET":
        response = servo_control.get_current_temperature()
        return jsonify(response)
    else:
        data = request.get_json()
        response = servo_control.set_current_temperature(data["temperature"])
        return jsonify(response)


def servo_config():
    # get or set the servo config
    if request.method == "GET":
        response = servo_control.get_config()
        return jsonify(response)
    else:
        data = request.get_json()
        response = servo_control.update_config(data)
        return jsonify(response)
