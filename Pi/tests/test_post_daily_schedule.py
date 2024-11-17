
# Import necessary libraries
from main import app

# test for creating the daily schedule
def test_post_daily_schedule(setup_db):
    # create a test client
    client = app.test_client()

    # create a configuration
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

    # prepare the data
    data = {
        "configuration_id": 1,
        "hour_start": 0,
        "hour_end": 6,
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "target_temperature": 75.0,
        "sensor_id": 1
    }

    # make a POST request
    response = client.post('/daily_schedule', json=data)

    # assert the status code
    assert response.status_code == 201

    # assert the response data
    assert response.json == {'message': 'Daily schedule posted successfully'}

def test_post_daily_schedule_invalid_json(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {
        "configuration_id": 1,
        "hour_start": 0,
        "hour_end": 6,
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "sensor_id": 1
    }

    # make a POST request
    response = client.post('/daily_schedule', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON: missing keys [\'target_temperature\']'}

def test_post_daily_schedule_invalid_types(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {
        "configuration_id": 1,
        "hour_start": 0,
        "hour_end": 6,
        "minimum_temperature": 70.0,
        "maximum_temperature": 80.0,
        "target_temperature": "WRONG",
        "sensor_id": 1
    }

    # make a POST request
    response = client.post('/daily_schedule', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON types: `configuration_id`, `hour_start`, `hour_end`, `sensor_id` must be integers and `minimum_temperature`, `maximum_temperature`, `target_temperature` must be floats'}
