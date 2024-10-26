# TODO List

Pi boots and connects with a static IP, can ssh in with creds

## Basic Functions / Py files

- Read I2C temp sensor for pi and pico
- Move servo (Pi)
  - keep track (ish) of temp
- Webserver (Pi)
  - `POST` data to it
  - has history
- Remote Sensor (Pico)
  - Connect to wifi on boot
  - Can send data over ???
  - Handles random reboots of self with interval
- Sensor Server (Pi)
  - Can receive data from remote sensors and `POST` to localhost to translate to webserver
  - Can handle interruptions and N sensors

## Data Formats

For webserver accepted requests:

- `POST` data format `{"sensor_id":1,"value":70.2}`

also, @nyxssmith is **hot**
