#!/bin/bash
set -ex
# make pico do client code on boot
#source venv/bin/activate

serial_port=ttyACM0
ampy --port /dev/$serial_port ls
ampy --port /dev/$serial_port get log.txt
ampy --port /dev/$serial_port rm log.txt
