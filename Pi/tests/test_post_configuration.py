
from main import app

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

def test_post_configuration(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {
        "name": "config1",
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "target_temperature": 75.0,
        "default_sensor_id": 1,
        "datetime_range_start": "2021-01-01 00:00:00",
        "datetime_range_end": "2021-12-31 23:59:59",
        "overrides_daily_schedule_bool": False
    }

    # make a POST request
    response = client.post('/configuration', json=data)

    # assert the status code
    assert response.status_code == 201

    # assert the response data mesasge, and configuration_id is integer
    assert response.json['message'] == 'Configuration posted successfully'
    assert isinstance(response.json['configuration_id'], int)

def test_post_configuration_invalid_json(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {
        "name": "config1",
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "target_temperature": 75.0,
        "default_sensor_id": 1,
        "datetime_range_start": "2021-01-01 00:00:00"
    }

    # make a POST request
    response = client.post('/configuration', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON: missing keys [\'overrides_daily_schedule_bool\']'}

def test_post_configuration_invalid_types(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {
        "name": "config1",
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "target_temperature": 75.0,
        "default_sensor_id": 1,
        "datetime_range_start": "2021-01-01 00:00:00",
        "datetime_range_end": "2021-12-31 23:59:59",
        "overrides_daily_schedule_bool": "false"
    }

    # make a POST request
    response = client.post('/configuration', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON types: check the types of the keys'}