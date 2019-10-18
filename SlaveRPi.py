# Import necessary packages
import RPi.GPIO as GPIO
import time
import base64
import cv2
import zmq
import socket

# Initialize Server Port 
port = 12345

# Initialize RPi GPIO Pins for connection with motor driver
m12=18
m16=23
m18=24
m22=25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m16,GPIO.OUT)
GPIO.setup(m18,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)
GPIO.output(m12,0)
GPIO.output(m16,0)
GPIO.output(m18,0)
GPIO.output(m22,0)
print("Done")

# Functions for moving bot in particular direction
def left():
    print('left')
    GPIO.output(m12,0)
    GPIO.output(m16,1)
    GPIO.output(m18,0)
    GPIO.output(m22,0)
def right():
    print('right')
    GPIO.output(m12,0)
    GPIO.output(m16,0)
    GPIO.output(m18,0)
    GPIO.output(m22,1)
def front():
    print('front')
    GPIO.output(m12,0)
    GPIO.output(m16,1)
    GPIO.output(m18,0)
    GPIO.output(m22,1)
def back():
    print('back')
    GPIO.output(m12,1)
    GPIO.output(m16,0)
    GPIO.output(m18,1)
    GPIO.output(m22,0)
def stop():
    GPIO.output(m12,0)
    GPIO.output(m16,0)
    GPIO.output(m18,0)
    GPIO.output(m22,0)

# Connecting to PC/Server for sending image frames obtained from camera
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.43.205:5555')

camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        #frame = cv2.resize(frame, (640, 480))  # resize the frame if needed
        encoded, buffer = cv2.imencode('.jpg', frame) # encoding frame to jpg format
        jpg_as_text = base64.b64encode(buffer) # encoding frame to byte string format
        footage_socket.send(jpg_as_text) # sending the encoded data

        # Recieving command messages from server
        s = socket.socket()                          
        s.connect(('192.168.43.205', port)) 
        command = s.recv(1024)
        print(control)

        # Call functions to move the bot for different command messages
        if(comand == 'left'):
            left()
        elif(command == 'right'):
            right()
        elif(command == 'front'):
            front()
        elif(command == 'back'):
            back()
        else:
            stop()
        s.close()

    except KeyboardInterrupt:
        camera.release()
        break

