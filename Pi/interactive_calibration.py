# has a server ip variable
# first sends a get request to /calibrate to check if calibration is active
# if is active sends post request to /calibrate with cancel command to cancel calibration
# prompts user to manually move to 60 degrees on the dial
# sends a post request to /calibrate with command "start" to start calibration
# enters a loop where 
#   prompt user if dial is at 80 yet
#   prompt defaults to y/N with N being the default if no input is given
#   if user says yes, sends a post request to /calibrate with "at 80" command
#       prompts user if dial is at 50 yet
#       prompt defaults to y/N with N being the default if no input is given
#       if user says yes, sends a post request to /calibrate with "at 50" command
#           calibration is complete

import requests
server_ip = "192.168.1.177:5000"
server_ip = "127.0.0.1:5000"
def main():
    # check if calibration is active
    response = requests.get(f"http://{server_ip}/calibrate")
    if response.json()["message"] == "Calibration is active":
        # calibration is active, cancel it
        response = requests.post(f"http://{server_ip}/calibrate", json={"command": "cancel"})
        print(response.json()["message"])
        print("Calibration cancelled")
        return
    else:
        print("Calibration is not active")

    # prompt user to manually move to 60 degrees on the dial
    print("Please manually move the dial to 60 degrees")
    input("Press enter when ready")
    # TODO need to check if real servo needs to reset its self.angle to 0 here
    
    # start calibration
    response = requests.post(f"http://{server_ip}/calibrate", json={"command": "start"})
    print(response.json()["message"])

    # loop until calibration is complete
    while True:
        # prompt user if dial is at 80 yet
        user_input = input("Is the dial at 80 degrees? [y/N]: ")
        if user_input.lower() == "y":
            response = requests.post(f"http://{server_ip}/calibrate", json={"command": "at 80"})
            print(response.json()["message"])
            break
        else:
            response = requests.post(f"http://{server_ip}/calibrate", json={"command": "next"})
            print(response.json()["message"])
            
    while True:
        # prompt user if dial is at 50 yet
        user_input = input("Is the dial at 50 degrees? [y/N]: ")
        if user_input.lower() == "y":
            response = requests.post(f"http://{server_ip}/calibrate", json={"command": "at 50"})
            print(response.json()["message"])
            break
        else:
            response = requests.post(f"http://{server_ip}/calibrate", json={"command": "next"})
            print(response.json()["message"])
            
    print("Calibration complete")

main()