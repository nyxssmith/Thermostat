
# Import necessary libraries
from flask import config
from main import app

# test for getting the daily schedules by configuration ID
def test_get_daily_schedules(setup_db):
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

    # assert the status code
    assert response.status_code == 201

    config_id = response.json['configuration_id']

    # prepare the data
    data = {
        "configuration_id": config_id,
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

    # make a GET request with the configuration ID
    response = client.get('/daily_schedule?configuration_id=' + str(config_id))

    # assert the status code
    assert response.status_code == 200

    # assert the response data
    assert len(response.json) == 1

    # assert the response data
    assert response.json[0]['configuration_id'] == config_id
    assert response.json[0]['hour_start'] == 0
    assert response.json[0]['hour_end'] == 6
    assert response.json[0]['minimum_temperature'] == 70.0
    assert response.json[0]['maximum_temperature'] == 80.0
    assert response.json[0]['target_temperature'] == 75.0
    assert response.json[0]['sensor_id'] == 1



