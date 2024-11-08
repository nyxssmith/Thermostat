
from main import app

# get the configuration data by making a GET request using a CONFIGURATION_ID
def test_get_configuration(setup_db):
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

    # get the configuration_id
    configuration_id = response.json['configuration_id']

    # make a GET request
    response = client.get(f'/configuration/{configuration_id}')

    # assert the status code
    assert response.status_code == 200

    # assert the response data
    assert response.json['configuration']['id'] == configuration_id
    assert response.json['configuration']['name'] == "config1"
    assert response.json['configuration']['minimum_temperature'] == 70.0
    assert response.json['configuration']['maximum_temperature'] == 80.0
    assert response.json['configuration']['target_temperature'] == 75.0
    assert response.json['configuration']['default_sensor_id'] == 1
    assert response.json['configuration']['datetime_range_start'] == "2021-01-01 00:00:00"
    assert response.json['configuration']['datetime_range_end'] == "2021-12-31 23:59:59"
    assert response.json['configuration']['overrides_daily_schedule_bool'] == False

def test_get_configuration_invalid_id(setup_db):
    # create a test client
    client = app.test_client()

    # make a GET request
    response = client.get('/configuration/1')

    # assert the status code
    assert response.status_code == 404
    assert response.json == {'message': 'Configuration not found'}

def test_get_configuration_with_daily_schedules(setup_db):
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

    # get the configuration_id
    configuration_id = response.json['configuration_id']

    # prepare the data
    data = {
        "configuration_id": configuration_id,
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

    # make a GET request
    response = client.get(f'/configuration/{configuration_id}')

    # assert the status code
    assert response.status_code == 200

    # assert the response data
    assert response.json['configuration']['id'] == configuration_id
    assert response.json['configuration']['name'] == "config1"
    assert response.json['configuration']['minimum_temperature'] == 70.0
    assert response.json['configuration']['maximum_temperature'] == 80.0
    assert response.json['configuration']['target_temperature'] == 75.0
    assert response.json['configuration']['default_sensor_id'] == 1
    assert response.json['configuration']['datetime_range_start'] == "2021-01-01 00:00:00"
    assert response.json['configuration']['datetime_range_end'] == "2021-12-31 23:59:59"
    assert response.json['configuration']['overrides_daily_schedule_bool'] == False
    assert response.json['configuration']['daily_schedules'][0]['id'] == 1
    assert response.json['configuration']['daily_schedules'][0]['configuration_id'] == configuration_id
    assert response.json['configuration']['daily_schedules'][0]['hour_start'] == 0
    assert response.json['configuration']['daily_schedules'][0]['hour_end'] == 6
    assert response.json['configuration']['daily_schedules'][0]['minimum_temperature'] == 70.0
    assert response.json['configuration']['daily_schedules'][0]['maximum_temperature'] == 80.0
    assert response.json['configuration']['daily_schedules'][0]['target_temperature'] == 75.0
    assert response.json['configuration']['daily_schedules'][0]['sensor_id'] == 1
