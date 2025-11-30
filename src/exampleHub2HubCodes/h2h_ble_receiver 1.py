from hub2hub import BLEnetwork
from time import sleep_ms
from spike import Motor

## Initialize Sensor
myMotor = Motor('B')

## Initialize ble network
network = {
#Name: Address
    'A': '0',
    'B': '1',
}

ble = BLEnetwork('B', network, state={'X' : 0})

# Set on receive function: this function is executed when a message is received
def on_response(message,child,state):
    print('response', message)

def on_request(message, state):
    # Action:
    if 'X' in message.keys():
        state['X'] = message['X']

    respond_message = {'B': 1}
    return respond_message

ble.set_on_request(on_request)




## Initialize
mySwitch = 0

ble.set_on_response(on_response)

## establish connection
ble.connect()

print('Receiver connected!')

## main program
while ble.is_connected():
    if (ble.state['X'] > 0) and (mySwitch < 1):
        myMotor.run_for_degrees(360)
        mySwitch =1

    # Small delay to not overload the BLE network
    sleep_ms(100)

