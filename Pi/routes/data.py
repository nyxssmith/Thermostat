
from flask import request, jsonify
from setupdb import get_db_connection

def post_data():
    """
    Handles POST requests to the /data endpoint.

    This function retrieves JSON data from the request, inserts it into the database,
    and returns a success message.

    Returns:
        Response: A JSON response with a success message and HTTP status code 201.
    """
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    #validate `sensor_id` and `value` keys, and their types
    if 'sensor_id' not in data or 'value' not in data:
        return jsonify({'message': 'Invalid JSON: missing keys `sensor_id` and/or `value`'}), 400

    if not isinstance(data['sensor_id'], int) or not isinstance(data['value'], float):
        return jsonify({'message': 'Invalid JSON types: `sensor_id` must be an integer and `value` must be a float'}), 400

    cur.execute('INSERT INTO data (sensor_id, value) VALUES (?, ?)', (data['sensor_id'], data['value']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data posted successfully'}), 201

def get_data():
    """
    Handles GET requests to the /data endpoint.

    This function retrieves all data from the database and returns it as a JSON response.

    Returns:
        Response: A JSON response with all data from the database and HTTP status code 200.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    data = cur.fetchall()
    conn.close()
    return jsonify(data), 200