
# pytest for Flask app GET /data

import pytest
import requests
import json

# run the Flask app
from main import app

def test_get_data(setup_db):

    # create a test client
    client = app.test_client()

    # prepare the data
    data = {"sensor_id": 1, "value": 70.2}

    # make a POST request
    response = client.post('/data', json=data)

    # assert the status code
    assert response.status_code == 201

    # make a GET request
    response = client.get('/data')

    # assert the status code
    assert response.status_code == 200

    # assert the response data, with a length of each tuple to be 3
    assert len(response.json) == 1
    assert len(response.json[0]) == 3
    assert response.json[0][0] == 1
    assert response.json[0][1] == 70.2
    #make sure timestamp is valid
    assert ':' in response.json[0][2]
    assert '-' in response.json[0][2]
