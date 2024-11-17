#setup the test database
import pytest
from setupdb import setup_database

# set environment to testing
import os
os.environ['TESTING'] = 'True'

@pytest.fixture(scope='function')
def setup_db():
    setup_database('tests/test.db')

    yield

    # after each test, delete the test database
    os.remove('tests/test.db')
