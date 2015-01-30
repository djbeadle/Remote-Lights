#!/usr/bin/env python

'''
Python 3 required!

This program hosts a simple webpage on your remote server (The one publically accessible) via flask where users can select a color value. When the user presses the submit button this server sends out TCP packets to the local server (TCP_server.py) with the hex value of the selected color. 

The whole point of this is to have a publically accessible control mechanism without revealing your private IP address.

If your domain name was FlaskServer.me the link you would need to go to would be:
FlaskServer.me:5000/lights
Flask defaults to port 5000, you can lookup how to change it elsewhere.
'''

# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request

# This is used to easily convert the color values back and forth between hex and RGB (Hex for HTML, RGB for LEDs)
import webcolors

# This is how we send the data back to the local server. This program, app3.py, is the flask server and socket client.
import socket
HOST = '111.222.333.444' # Your public IP address goes here
PORT = 1701 # The port you're using goes here. Needs to be the same as the one tcp_server.py is listening on

# This is used for.... something. I'm not sure exactly how the TCP client works, I just figured out that the pieces work together
import sys

# This has to be declared globally so that it's value stays the same between different instances of the /lights page being loaded
hexColor = "FFFFFF"

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!" # Simply return a string

# route for handling ALL OF THE LIGHTS!
@app.route('/lights', methods=['GET', 'POST'])
def lights():
    global hexColor

    if request.method == 'POST':
        print("******************")

        hexColorNew = request.form['colorValue'] # hexColorNew gets run through error checking first before being assigned to hexColor (Which gets carried over on reload)
        print("Raw Hex Color: " + hexColorNew)

        if len(hexColorNew) != 6: # Error checking in case the value isn't equal to 6 characters
            difference = 6 - len(hexColorNew)

            while difference > 0: # If it's less than 6 characters, fill the remainder with zeros 
                hexColorNew = hexColorNew + "0"
                difference = difference - 1

            if difference < 0: # If it's more than 6 characters, cut it down to 6
                hexColorNew = hexColorNew[:6]
        print("Trimmed Hex Color: " + hexColorNew)
        try:
            rgb = webcolors.hex_to_rgb("#" + hexColorNew)
        except:
            print("ERROR: hexColorNew -> rgb failed!")
            return render_template('colorpickertest.html', HTMLhexColor = hexColor)

        # At this point we can be confident that hexColorNew is/has been converted to a valid color value
        hexColor = hexColorNew #hexColor gets carried over on the page refresh, hexColorNew doesn't
        print("Final Hex Color Value: " + hexColor)
        r, g, b = rgb
        print(r)
        print(g)
        print(b)

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(hexColor, "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
        finally:
            sock.close()

        print("Sent:     {}".format(hexColor))
        print("Received: {}".format(received))
    return render_template('colorpickertest.html', HTMLhexColor = hexColor)

# start the server with the 'run()' method
if __name__=='__main__':
    app.run(host='0.0.0.0')
