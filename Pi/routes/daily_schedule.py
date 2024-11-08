
# routes to POST and GET daily_schedule data
from flask import request, jsonify
from main import app
from setupdb import get_db_connection

# create the daily_schedule table
    #  configuration_id: the configuration ID (FOREIGN KEY)
    #  id: the daily schedule ID (PRIMARY KEY)
    #  hour_start: hour_value,
    #  hour_end: hour_value,
    #  minimum_temperature: temp_value,
    #  maximum_temperature: temp_value,
    #  target_temperature: temp_value,
    #  sensor_id: sensor_id_value

def post_daily_schedule():
    # get the data from the request
    data = request.json

    required_keys = [
        'configuration_id',
        'hour_start',
        'hour_end',
        'minimum_temperature',
        'maximum_temperature',
        'target_temperature',
        'sensor_id'
    ]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({'message': 'Invalid JSON: missing keys {}'.format(missing_keys)}), 400

    if not all([
        isinstance(data['configuration_id'], int),
        isinstance(data['hour_start'], int),
        isinstance(data['hour_end'], int),
        isinstance(data['minimum_temperature'], float),
        isinstance(data['maximum_temperature'], float),
        isinstance(data['target_temperature'], float),
        isinstance(data['sensor_id'], int)
    ]):
        return jsonify({'message': 'Invalid JSON types: `configuration_id`, `hour_start`, `hour_end`, `sensor_id` '
         'must be integers and `minimum_temperature`, `maximum_temperature`, `target_temperature` must be floats'}), 400


    # connect to the database
    conn = get_db_connection()
    cur = conn.cursor()

    # make sure the configuration_id exists
    cur.execute('SELECT id FROM configuration WHERE id = ?', (data['configuration_id'],))
    if not cur.fetchone():
        return jsonify({'message': 'Invalid configuration_id'}), 400

    # insert the data into the database
    cur.execute('''
        INSERT INTO daily_schedule (
            configuration_id,
            hour_start,
            hour_end,
            minimum_temperature,
            maximum_temperature,
            target_temperature,
            sensor_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['configuration_id'],
        data['hour_start'],
        data['hour_end'],
        data['minimum_temperature'],
        data['maximum_temperature'],
        data['target_temperature'],
        data['sensor_id']
    ))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

    return jsonify({'message': 'Daily schedule posted successfully'}), 201

def get_daily_schedule():
    # get the configuration_id from the query parameters
    configuration_id = request.args.get('configuration_id')

    # connect to the database
    conn = get_db_connection()
    cur = conn.cursor()

    # get the daily schedule data
    cur.execute('''
        SELECT * FROM daily_schedule
        WHERE configuration_id = ?
        ''', (configuration_id,))

    # fetch all the data
    rows = cur.fetchall()

    # get column names
    column_names = [desc[0] for desc in cur.description]

    # convert rows to list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # close the connection
    conn.close()

    return jsonify(data), 200