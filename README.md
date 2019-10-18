# Color-Tracking-Bot
Bot on wheels detects object with a particular color using OpenCV running on PC and follows it.
# Bot on Wheels
<img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Bot.jpg" /><br/>
# Components
<br/>1. Raspberry Pi 3 B+
<br/>2. LM293D Motor Driver
<br/>3. Camera (can use Pi-Cam)
<br/>4. Two DC Motors
<br/>5. Car/Bot Chassis
<br/>6. Power source for raspberry pi
<br/>7. Host PC or Laptop
<br/>8. Wires<br/>
# Circuit
Pins can be updated in SlaveRPi.py script according to the pin configuration shown in bellow circuit diagram.
<br/><br/><img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Circuit.jpg"/><br/>
# Detecting Blue Objects
<br/>Frames from camera connected to Raspberry Pi are sent over the loop using SlaveRPi.py and received by MasterPC.py listning on one port (5555 here) of host PC using zmq sockets.
<br/><br/>Recieved frames are processed on host PC (MasterPC.py) and command messge is sent in the same loop using another socket on another port (12345 here) of host PC to Bot (raspberry pi) to move in direction of object detected.
<br/><br/>Also image frames showing detected objects are being hosted on PC localhost on yet another port (8000 here) a LAN Network using flask.
<br/><br/>Devices connected on same LAN as of PC and RPi can see detected object on their respective browsers.
<br/><br/><br/><img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Blue%20Color%20Detect.png"/><br/>
