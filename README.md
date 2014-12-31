# Remote Lights
<h5>...Or, more accurately, remote Firmata control</h5>

I needed a way to control my RGB LED strip over the internet without giving out my house's public IP address. 

There are two servers in this implementation. The first runs flask\_server.py, is publically accessible, and hosts (guess what!) a flask server. Anyone can access this serer, choose a color value, and hit the submit button. When they do, this server sends a message over TCP *(Try saying RGB LED TCP 10 times fast)* to the computer running, tcp\_server.py, which then converts the hex color value to pure RGB, and finally transmits that via USB _(RGB LED TCP USB!)_ to a connected Arduino (Which is running the FIRMATA protocal). 

Does this have to be used to control LEDs? Nope, it could pretty easily be modified to send a command to rotate a servo or something, FIRMATA is cool like that. Heck, the Arduino protion could be removed entirely and you could just use this to send messages back and forth between two computers. 

### Version
1.0

### Sources I Stole Code From:

* [JSColor] - A fantastically simple JS color picker
* [Tino's pyFirmata Library] - Tino's FIRMATA library for Python. Be sure to use the Python 3 specific branch
* [Matt Richardson's Flask Tutorial] - a great set of instructions on setting up Flask on the Raspberry Pi
* [jQuery] - duh
* [The Python Docs] - Man, those examples on socket servers are really useful.

[JSColor]:http://jscolor.com
[Tino's pyFirmata Library]:https://github.com/tino/pyFirmata/
[The Python Docs]:https://docs.python.org/3/library/socketserver.html
[Matt Richardson's Flask Tutorial]:http://mattrichardson.com/Raspberry-Pi-Flask/
[jQuery]:http://jquery.com
