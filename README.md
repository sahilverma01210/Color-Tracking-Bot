# Color-Tracking-Bot
Bot on wheels detects object with a particular color using OpenCV running on PC and follows it.
# Bot on Wheels
<img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Bot.jpg"/>
# Components
1. Raspberry Pi 3 B+
2. LM293D Motor Driver
3. Camera (can use Pi-Cam)
4. Two DC Motors
5. Car/Bot Chassis
6. Host PC or Laptop
7. Wires
# Circuit
Pins can be updated in SlaveRPi.py script according to the pin configuration shown in bellow circuit diagram.
<img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Circuit.jpg"/>
# Detecting Blue Objects
Frames from camera connected to Raspberry Pi is sent using SlaveRPi.py and received by MasterPC.py listning on port 5555 of host PC using zmq sockets.
Recieved frames are processed on host (MasterPC.py) and command messge is sent in the same loop using another socket on 12345 PC port to Bot (raspberry pi) to move in direction of object detected.
Also image frames showing detected objects are being hosted on PC localhost on a LAN Network using flask.
So, devices conneted on same LAN as of PC and RPi can see detected object on their browsers.
<img src="https://github.com/SahilVerma0651/Color-Tracking-Bot/blob/master/Blue%20Color%20Detect.png"/>
