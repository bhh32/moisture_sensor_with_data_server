'''
    Author: Bryan Hyland <bryan.hyland32@gmail.com>

    This file is for the raspberry pi pico w's.
    Change the XXX.XXX.XXX.XXX to the correct server IP address
    for your use case.

    NOTE: I use multiple versions of this file for each type of veggie, fruit, etc. I'm growing
    that has it's own moisture sensor. The file must be named main.py when put onto the Rasberry Pi Pico W.
    However, as annotated below, you can change the message to have more information sent to the server than
    what's provided here.

    This is provided for free, as is, without warranty. The author
    is not responsible for anything that occurs with your machine
    when using this software. The author is also not responsible
    for maintaing the code. Pull requests can be made if changes
    need to be made to the base code, and the author will get to
    it if they so choose and or get time.

    This code was inspired by the following projects:
        https://peppe8o.com/capacitive-soil-moisture-sensor-with-raspberry-pi-pico-wiring-code-and-calibrating-with-micropython/
        https://picockpit.com/raspberry-pi/stream-sensor-data-over-wifi-with-raspberry-pi-pico-w/
        https://howchoo.com/pi/how-to-power-the-raspberry-pi-pico
'''

import network
import socket
import utime
import secrets
import machine
from machine import ADC, Pin
import rp2
import random
from struct import pack

rp2.country('US')

# Setup the wifi chip
wlan = network.WLAN(network.STA_IF)

# Active the wifi chip
wlan.active(True)

# Function to connect to the wifi
def wifi_connect():
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    connect_wait = 10
    while connect_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        connect_wait -= 1
        print('Waiting for connection', end='\r')
        utime.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')
    else:
        print('connected')
        ip = wlan.ifconfig()[0]
        print("IP: ", ip)

# Function to setup the data socket
def setup_socket():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # NOTE: Use any port your like, this is what I used. Just make
    # sure that it matches the server's opened port within its file.
    host, port = 'XXX.XXX.XXX.XXX', 65000
    
    return (sock, host, port)

# Connect to the wifi
wifi_connect()

# Setup the socket
skt, host, port = setup_socket()
# Get the server address from the setup_socket function
server_address = (host, port)

# Setup moisture sensor
soil = ADC(Pin(26))

# This may need to be readjusted for your moisture sensors
# Look at the moisture sensor project reference on how to
# do this.
min_moisture = 18644
max_moisture = 43674

# How often a reading is taken
read_delay = 0.5

# Main loop
while True:
    # Get the moisture data from the moisture sensor
    moisture = (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)

    # Package it up to send to the server
    # NOTE: You can add more information to the message if needed.
    # For example, mine looks something like the following...
    # message = pack('Tomato Soil Moisture Level: 1f' moisture)
    message = pack('1f', moisture)
    # Send the data to the server
    skt.sendto(message, server_address)
    
    # Print debug message (only works if you're hooked up through Thonny)
    # Used for moisture sensor calibration.
    print("moisture: " + "%.2f" % moisture + "%(adc: " + str(soil.read_u16()) + ")")
    
    # Ensure you're still hooked up to the wifi
    # If you're not, reconnect to wifi
    if wlan.status() != 3:
        wifi_connect()
        
    # Delay the next reading by the time given in read_delay
    utime.sleep(read_delay)