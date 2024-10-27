
# setup the tables for `data.db` sqlite3 database
import sqlite3

# setup the main db, or the test db
def setup_database(name='data.db'):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS data (sensor_id INTEGER, value REAL)')
    conn.commit()
    conn.close()