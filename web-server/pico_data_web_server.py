'''
    Author: Bryan Hyland <bryan.hyland32@gmail.com>

    This file is the server side that recieves the data from a single
    Raspberry Pi Pico W and updates the soil_moisture_data.txt file,
    which is then read by the website that's hosted on Nginx (or any other webserver of your choosing).
    
    This file must be ran under sudo to updated the soil_moisture_data.txt file. If someone figures out
    how to not have to run it under sudo, please let me know and I will make changes accordingly.

    NOTE: I use multiple versions of this file for each type of veggie, fruit, etc. I'm growing
    and update the name of the file accordingly along with the "Getting Soil Moisture Data..."
    message to reflect the name of the area I'm monitoring.

    This is provided for free, as is, without warranty. The author
    is not responsible for anything that occurs with your machine
    when using this software. The author is also not responsible
    for maintaing the code. Pull requests can be made if changes
    need to be made to the base code, and the author will get to
    it if they so choose and/or get time.

    This code was inspired by the following projects:
        https://peppe8o.com/capacitive-soil-moisture-sensor-with-raspberry-pi-pico-wiring-code-and-calibrating-with-micropython/
        https://picockpit.com/raspberry-pi/stream-sensor-data-over-wifi-with-raspberry-pi-pico-w/
        https://howchoo.com/pi/how-to-power-the-raspberry-pi-pico
'''

import socket
import sys
import time
from struct import unpack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000 # The port must match the port you gave to the pico w's main.py file
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

while True:
    # Wait for message
    message, address = sock.recvfrom(4096)
    if address == "":
        print(f'Waiting on moisture sensor to connect...', end='\r')
    else:
        # When a moisture sensor is connected, these two message flash between each other
        print(f'Client {address} has connected...', end='\r')
        time.sleep(1)
        print('Getting Soil Moisture Data...               ', end='\r')
    # Unpack the message recieved from the Raspberry Pi Pico W
    moisture = unpack('1f', message)

    # Update the soil_moisture_data.txt file for the web page hosted in your web server.
    # Update the path if it differs from mine.
    with open('/var/www/moisture_sensors/soil_moisture_data.txt', 'w') as writer:
        writer.write(f'Current Moisture Level: ' + "%.2f" % moisture + "%")
        
    
