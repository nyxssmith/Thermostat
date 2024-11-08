
# pytest for Flask app POST /data
# run the Flask app
from main import app

def test_post_data(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {"sensor_id": 1, "value": 70.2}

    # make a POST request
    response = client.post('/data', json=data)

    # assert the status code
    assert response.status_code == 201

    # assert the response data
    assert response.json == {'message': 'Data posted successfully'}

def test_post_data_invalid_json(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {"sensor_id": 1}

    # make a POST request
    response = client.post('/data', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON: missing keys `sensor_id` and/or `value`'}

def test_post_data_invalid_types(setup_db):
    # create a test client
    client = app.test_client()

    # prepare the data
    data = {"sensor_id": 1, "value": "70.2"}

    # make a POST request
    response = client.post('/data', json=data)

    # assert the status code
    assert response.status_code == 400

    # assert the response data
    assert response.json == {'message': 'Invalid JSON types: `sensor_id` must be an integer and `value` must be a float'}