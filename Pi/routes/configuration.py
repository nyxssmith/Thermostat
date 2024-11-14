
from flask import request, jsonify
from setupdb import get_db_connection

# post route to write configuration data to the database
# data format: {
#       "name": "config1",
#       "minimum_temperature": 70.0,
#       "maximum_temperature": 80.0,
#       "target_temperature": 75.0,
#       "default_sensor_id": 1,
#       "datetime_range_start": "2021-01-01 00:00:00",
#       "datetime_range_end": "2021-12-31 23:59:59", (optional)
#       "overrides_daily_schedule_bool": false}
def post_configuration():
    """
    Handles POST requests to the /configuration endpoint.

    This function retrieves JSON data from the request, inserts it into the database,
    and returns a success message.

    Returns:
        Response: A JSON response with a success message and HTTP status code 201.
    """
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    # validate the keys and types
    required_keys = [   'name',
                        'minimum_temperature',
                        'maximum_temperature',
                        'target_temperature',
                        'default_sensor_id',
                        'datetime_range_start',
                        'overrides_daily_schedule_bool']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({'message': 'Invalid JSON: missing keys {}'.format(missing_keys)}), 400

    if (not isinstance(data['minimum_temperature'], float) or
        not isinstance(data['maximum_temperature'], float) or
        not isinstance(data['target_temperature'], float) or
        not isinstance(data['default_sensor_id'], int) or
        not isinstance(data['datetime_range_start'], str) or
        not isinstance(data['name'], str) or
        not isinstance(data['overrides_daily_schedule_bool'], bool)):
        return jsonify({'message': 'Invalid JSON types: check the types of the keys'}), 400

    # optional validate datetime_range_end
    if 'datetime_range_end' in data and not isinstance(data['datetime_range_end'], str):
        return jsonify({'message': 'Invalid JSON types: `datetime_range_end` must be a string'}), 400

    # check that the name is unique
    cur.execute('SELECT * FROM configuration WHERE name = ?', (data['name'],))
    if cur.fetchone():
        return jsonify({'message': 'Invalid JSON: name already exists'}), 400

    cur.execute('INSERT INTO configuration (name, minimum_temperature, '
                'maximum_temperature, target_temperature, default_sensor_id, '
                'datetime_range_start, datetime_range_end, overrides_daily_schedule_bool) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (data['name'],
                 data['minimum_temperature'],
                 data['maximum_temperature'],
                 data['target_temperature'],
                 data['default_sensor_id'],
                 data['datetime_range_start'],
                 data['datetime_range_end'],
                 data['overrides_daily_schedule_bool']))

    # Get the ID of the created record
    created_id = cur.lastrowid

    conn.commit()
    conn.close()

    return jsonify({'message': 'Configuration posted successfully', 'configuration_id': created_id}), 201

# get route to retrieve configuration data from the database
# data format: {
#       "configuration_id": 1}
def get_configuration(
        configuration_id: int
):
    """
    Handles GET requests to the /configuration endpoint.

    This function retrieves configuration data from the database based on the configuration ID.

    Returns:
        Response: A JSON response with the configuration data and HTTP status code 200.
    """

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM configuration WHERE id = ?', (configuration_id,))
    row = cur.fetchone()

    # get column names from the cursor description
    columns = [column[0] for column in cur.description]

    # create a dictionary from the column names and row data
    configuration = dict(zip(columns, row)) if row else None



    if not configuration:
        return jsonify({'message': 'Configuration not found'}), 404

    # load daily schedules
    cur.execute('SELECT * FROM daily_schedule WHERE configuration_id = ?', (configuration_id,))
    rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    daily_schedules = [dict(zip(columns, row)) for row in rows]

    configuration['daily_schedules'] = daily_schedules

    conn.close()
    return jsonify({'configuration': configuration}), 200

