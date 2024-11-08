
# setup the tables for `data.db` sqlite3 database
import sqlite3
import os

# pragma: no cover
def get_db_connection():
    if 'TESTING' in os.environ:
        conn = sqlite3.connect('tests/test.db')
    else:
        conn = sqlite3.connect('data.db') # pragma: no cover
    return conn

# setup the main db, or the test db
def setup_database(name='data.db'):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    # create the `data` table
    # sensor_id: the sensor ID
    # value: the sensor value
    # timestamp: the timestamp when the data was inserted
    cur.execute('''
        CREATE TABLE IF NOT EXISTS data (
            sensor_id INTEGER,
            value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # create the configuration table
    # id: the configuration ID
    # name: the configuration name (UNIQUE)
    # minimum_temperature: the minimum temperature threshold
    # maximum_temperature: the maximum temperature threshold
    # target_temperature: the target temperature
    # default_sensor_id: the default sensor ID
    # datetime_range_start: the start of the datetime range
    # datetime_range_end: the end of the datetime range (nullable)
    # overrides_daily_schedule_bool: whether to override the daily schedule

    cur.execute('''
        CREATE TABLE IF NOT EXISTS configuration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            minimum_temperature REAL,
            maximum_temperature REAL,
            target_temperature REAL,
            default_sensor_id INTEGER,
            datetime_range_start DATETIME,
            datetime_range_end DATETIME,
            overrides_daily_schedule_bool BOOLEAN
        )
    ''')

    # create the daily_schedule table
    #  configuration_id: the configuration ID
    #  id: the daily schedule ID
    #  hour_start: hour_value,
    #  hour_end: hour_value,
    #  minimum_temperature: temp_value,
    #  maximum_temperature: temp_value,
    #  target_temperature: temp_value,
    #  sensor_id: sensor_id_value
    #
    cur.execute('''
        CREATE TABLE IF NOT EXISTS daily_schedule (
            configuration_id INTEGER,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour_start INTEGER,
            hour_end INTEGER,
            minimum_temperature REAL,
            maximum_temperature REAL,
            target_temperature REAL,
            sensor_id INTEGER
        )
    ''')

    conn.commit()
    conn.close()