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
