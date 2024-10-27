# client code to send a post request from micropython on the pico to a server on boot

# working curl cmd
# curl -X POST http://127.0.0.1:9955/ -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}'

import socket
import json
import network
import os
import machine
import time

def blink(t=0.5):
    pin = machine.Pin("LED", machine.Pin.OUT)
    pin.toggle()
    time.sleep(t)
    pin.toggle()
    time.sleep(t)

# TODO move to common lib file
def log(string):
    string = str(string)
    with open("log.txt","a") as l:
        l.write(string)
        l.write("\n")
    print(string)
    
# TODO move to common lib file
def connect_wifi(ssid,password):
    try:
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            log('connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid,password)
            tries = 0
            max_tries = 100
            while not sta_if.isconnected():
                # blink fast while connecting
                blink(0.1)
                tries+=1
                if tries >= max_tries:
                    sta_if.active(False)
                    connect_wifi(ssid,password)
                    break
                pass
        log(f"network config:{sta_if.ipconfig('addr4')}")
        # led on = has wifi
        pin = machine.Pin("LED", machine.Pin.OUT)
        pin.toggle()
        # blink 2x to confirm connect
        blink()
        blink()
    except Exception as e:
        log(e)
        raise e
        
# wifi details
ssid= None
password= None
with open("network_config.json","r") as f:
    config = json.load(f)
    ssid = config["ssid"]
    password = config["password"]
log("wifi creds loaded")
# connect
connect_wifi(ssid,password)
log("connected to wifi")
# Server details
host= None
port= None
route= None
with open("client_config.json","r") as f:
    config = json.load(f)
    host = config["address"]
    port = config["port"]
    route = config["route"]
log("server creds loaded")

# Data to send
data = json.dumps({"sensor_id": 2, "value": 69.69})
data_length = len(data)
# Create a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.connect((host, port))
log("socket connected")
# Create HTTP POST request
request = f"POST {route} HTTP/1.1\r\nHost:{host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {data_length}\r\nConnection: close\r\n\r\n{data}"

log(request)
# Send the request
encoded = request.encode('utf-8')
s.sendall(request.encode())

# Receive the response
response = s.recv(4096).decode()
log("Response from server:")
log(response)

s.close()
# long blink after program exit
blink(2)