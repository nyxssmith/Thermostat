
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

    # assert the response data
    assert response.json == [[1, 70.2]]