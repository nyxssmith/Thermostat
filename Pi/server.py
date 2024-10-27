from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_post():
    data = request.get_json()  # Get JSON data from the request
    # Process the data as needed
    response = {"message": "Data received", "received_data": data}
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=9955,host='0.0.0.0')
