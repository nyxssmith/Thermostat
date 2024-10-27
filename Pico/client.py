# client code to send a post request from micropython on the pico to a server on boot

# working curl cmd
# curl -X POST http://127.0.0.1:9955/ -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}'

import socket
import json

# Server details
host = '127.0.0.1'  # Localhost
port = 9955  # Port the Flask app is listening on

# Data to send
data = json.dumps({"key1": "value1", "key2": "value2"})
data_length = len(data)
print("test")
# Create a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    # Create HTTP POST request
    request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {data_length}\r\n"
        f"Connection: close\r\n\r\n"
        f"{data}"
    )
    
    # Send the request
    s.sendall(request.encode())

    # Receive the response
    response = s.recv(4096).decode()
    print("Response from server:")
    print(response)
