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

STAIC IP:

```bash
nyxandaria@thermostat:~ $ cat /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source /etc/network/interfaces.d/*

auto wlan0
iface wlan0 inet static
    address 192.168.1.177
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 192.168.1.1
```

Pi-Setup:
0. ssh to
1. add your .pub keys to ~/.ssh/authorized_keys
2. generate pub key:
  1. `ssh-keygen -o`
3. upload id_rsa.pub to [github-settings](https://github.com/settings/keys)

4. `sudo apt update`
5. `apt install git python3-pip`
7. add to `~/.bashrc`
  1. `export PATH=$PATH:/home/nyxandaria/.local/bin`
7. `mkdir ~/server && cd server`
8. `git clone https://github.com/nyxssmith/Thermostat && cd Thermostat`
9. `pip install -r requirements.txt`

## to auto-load server on boot ##

To Setup the RaspPI to autoload this server on boot:

1. `sudo nano /etc/systemd/system/my_python_server.service`
2.
```bash
[Unit]
Description=Start Python Server with Virtual Environment
After=network.target

[Service]
ExecStart=/home/nyxandaria/server/Thermostat/.venv/bin/python /home/nyxandaria/server/Thermostat/Pi/main.py
WorkingDirectory=/home/nyxandaria/server/Thermostat/Pi
Restart=always
User=nyxandaria

# Logging output
StandardOutput=append:/var/log/my_python_server.log
StandardError=append:/var/log/my_python_server.log

[Install]
WantedBy=multi-user.target
```

4. setup the logs:
```bash
sudo touch /var/log/my_python_server.log
sudo chown nyxandaria:nyxandaria /var/log/my_python_server.log
```


5. apply changes:
```bash
sudo systemctl daemon-reload
sudo systemctl restart my_python_server.service
```

6. check status:
```bash
sudo systemctl status my_python_server.service
```
