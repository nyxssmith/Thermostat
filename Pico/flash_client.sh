#!/bin/bash
set -ex
# make pico do client code on boot
#source venv/bin/activate

serial_port=ttyACM0
python_file=client.py
cp $python_file main.py
ampy --port /dev/$serial_port put client_config.json
ampy --port /dev/$serial_port put log.txt
ampy --port /dev/$serial_port put network_config.json
ampy --port /dev/$serial_port put main.py
ampy --port /dev/$serial_port run main.py

# if stuck in read only, reflash via bootsel
# hold button when plug in, drag uf2 file to it, wait for reboot then rerun
