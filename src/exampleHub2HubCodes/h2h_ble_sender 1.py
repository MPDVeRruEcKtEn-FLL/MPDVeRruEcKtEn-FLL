from hub2hub import BLEnetwork
from time import sleep_ms
from spike import DistanceSensor

## Initialize Sensor
myDistance = DistanceSensor('A')

## Initialize ble network
network = {
#Name: Address
    'A': '0',
    'B': '1',
}

ble = BLEnetwork('A', network)

# Set on receive function: this function is executed when a message is received
def on_response(message,child,state):
    print('response', message)

## Initialize
mySwitch = 0

ble.set_on_response(on_response)

## establish connection
ble.connect()

print('Receiver connected!')

## main program
while ble.is_connected():
    if (myDistance.get_distance_cm() < 10) and (mySwitch < 1):
        message = {'X': 1}
        ble.request_child('B', message)
        print ("send: " + str(message))
        mySwitch = 1


    # Small delay to not overload the BLE network
    sleep_ms(100)

