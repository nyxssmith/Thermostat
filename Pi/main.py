# basic Flask API app with SQLite3 database

from flask import Flask

app = Flask(__name__)

from routes import data, configuration, daily_schedule, servo

#always run the setup_database function
from setupdb import setup_database
setup_database()

# - `POST` data format `{"sensor_id":1,"value":70.2}`
# use the routes/data.py file
app.route('/data', methods=['POST'])(data.post_data)
app.route('/data', methods=['GET'])(data.get_data)
app.route("/servo", methods=["GET","POST"])(servo.servo_position)
app.route("/desired_temperature", methods=["GET","POST"])(servo.desired_temperature)
app.route("/calibrate", methods=["GET","POST"])(servo.calibrate)
app.route("/get_servo_config", methods=["GET"])(servo.get_servo_config)
app.route("/set_servo_config", methods=["POST"])(servo.set_servo_config)


# - `POST` configuration data format `{"name":"config1",
# "minimum_temperature":70.0,"maximum_temperature":80.0,
# "target_temperature":75.0,"default_sensor_id":1,
# "datetime_range_start":"2021-01-01 00:00:00",
# "datetime_range_end":"2021-12-31 23:59:59",
# "overrides_daily_schedule_bool":false}`
app.route('/configuration', methods=['POST'])(configuration.post_configuration)
app.route('/configuration/<int:configuration_id>', methods=['GET'])(configuration.get_configuration)

# - `POST` daily_schedule data format `{"configuration_id":1,
# "hour_start":0,"hour_end":6,
# "minimum_temperature":70.0,"maximum_temperature":80.0,
# "target_temperature":75.0,"sensor_id":1}`
app.route('/daily_schedule', methods=['POST'])(daily_schedule.post_daily_schedule)
app.route('/daily_schedule', methods=['GET'])(daily_schedule.get_daily_schedule)

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0') # pragma: no cover
    app.run(debug=False, host='0.0.0.0') # pragma: no cover

