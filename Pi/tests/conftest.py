#setup the test database
import pytest
from setupdb import setup_database

# set environment to testing
import os
os.environ['TESTING'] = 'True'

@pytest.fixture(scope='session')
def setup_db():
    setup_database('tests/test.db')

    yield

    # after all tests, delete the test database
    import os
    os.remove('tests/test.db')
