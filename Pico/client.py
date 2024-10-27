# client code to send a post request from micropython on the pico to a server on boot

# working curl cmd
# curl -X POST http://127.0.0.1:9955/ -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}'

import socket
import json
# network skip for local debug
skip_network = False
try:
    import network
except ImportError as i:
    skip_network = True
    pass
import os


# TODO move to common lib file
def log(string):
    string = str(string)
    with open("log.txt","a") as l:
        l.write(string)
        l.write("\n")
    print(string)
    
# TODO move to common lib file
def do_connect(ssid,password):
    if skip_network:
        return
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        #print('connecting to network...')
        log('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid,password)
        while not sta_if.isconnected():
            pass
    log(f"network config:{sta_if.ipconfig('addr4')}")


# wifi details
ssid= None
password= None
with open("network_config.json","r") as f:
    config = json.load(f)
    ssid = config["ssid"]
    password = config["password"]
log("wifi creds loaded")
# connect
do_connect(ssid,password)
log("connected to wifi")
# Server details
host= None
port= None
with open("client_config.json","r") as f:
    config = json.load(f)
    host = config["address"]
    port = config["port"]
log("server creds loaded")

# Data to send
data = {"key":"value"}# json.dumps({"key1": "value1", "key2": "value2"})
data_length = len(data)
# Create a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
log("with socket")
s.connect((host, port))
log("socket connected")

