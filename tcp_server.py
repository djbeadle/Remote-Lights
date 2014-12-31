#!/usr/bin/env python

'''
Python 3 required!

TCP LED Server! That's a nice tounge twister.

This runs on your local server, located at your private IP address (The one you don't want to make publically accessible) and is directly connected via USB to an Arduino running Firmata.

This requires the following modules:
webcolors
socketserver
pyfirmata -> I've been using Tino's pyFirmata library. https://github.com/tino/pyFirmata/ As of Dec 31st 2014, you need to manually download and install the branch compatible with Python 3 from his Github page. ALSO, an eccentricity I've found is that you need to extract it to the same root directory as your program otherwise it will give you an error ending with, "ImportError: No module named 'boards'"
'''

# Color convertor stuff
import webcolors
# This has to be declared globally so that it's value stays the same between different instances of the /lights page being loaded
hexColor = "FFFFFF"

# Talking to the Arduino
from pyfirmata import Arduino, util
board = Arduino('/YOUR/PORT/GOES.HERE') # For Rpi it's ttyACM0
pin3 = board.get_pin('d:3:p') # This sets digital pin #3 to PWM mode
pin5 = board.get_pin('d:5:p')
pin6 = board.get_pin('d:6:p')

# Socket server stuff
import socketserver
numConnections = 0 # This is just the counter for the total number of requests

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global hexColor
        global numConnections
        # self.request is the TCP socket connected to the client
        print("Connection Number: ", numConnections)
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
        numConnections = numConnections+1

        hexColor = str(self.data).strip("'b")

        print(hexColor)
        rgb = webcolors.hex_to_rgb("#" + hexColor)
        r, g, b = rgb
        print(r)
        print(g)
        print(b)
        print("-------------")
        pin6.write(float(r)/float(256))
        pin5.write(float(g)/float(256))
        pin3.write(float(b)/float(256))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1701 # You can change this port value to whatever you want, but the 0.0.0.0 needs to stay put. This port value needs to be the same here and on lin e

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print("Server Online, port: ", PORT)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
