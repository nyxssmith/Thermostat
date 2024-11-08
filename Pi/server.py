from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_post():
    data = request.get_json()  # Get JSON data from the request
    # Process the data as needed
    response = {"message": "Data received", "received_data": data}
    return jsonify(response)

@app.route("/servo_position", methods=["GET"])
def get_servo_position():
    # TODO link into servo.py
    response = {"message": "Data received to get servo position"}
    return jsonify(response)

@app.route("/desired_temperature", methods=["GET","POST"])
def desired_temperature():
    # TODO: Implement this function for post and get
    response = {"message": "Data received to get servo position"}
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=9955,host='0.0.0.0')
