# import necessary packages
from flask import Response
from flask import Flask
from flask import render_template
import socket
import cv2
import zmq
import base64
import numpy as np
import threading 

# connect to recieve frames
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://192.168.43.205:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
print("Done")

# initialize command message
mess='stop'

# connect to send commands to rpi using socket
s = socket.socket()		 
print("Socket successfully created")
port = 12345				
s.bind(('', port))		 
print("socket binded to %s" %(port)) 
s.listen(5)	 
print("socket is listening")			

# define range of blue color in HSV
l_b = np.array([100,200,200])
u_b = np.array([150,255,255])

# initialize the output frame
frame = None

# initialize a flask object
app = Flask(__name__)

@app.route("/")
def index():
        # return the rendered template
        return render_template("index.html")        
		
def generate():
        # grab global references to the output frame and lock variables
        global frame, mess

        # loop over frames from the output stream
        while True:
                if frame is None:
                        continue
                        
			# encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", frame)

                        # ensure the frame was successfully encoded
                if not flag:
                        continue

                # yield the output frame in the byte format
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
        # return the response generated along with the specific media
        # type (mime type) 
        return Response(generate(),mimetype = "multipart/x-mixed-replace; boundary=frame")


 

def pitalk(): 
        # grab global references to the output frame and lock variables
        global frame, mess

	# loop over frames to detect objects of color range and send command messages to rpi
        while True:
                try:
                        oframe = footage_socket.recv_string()
                        img = base64.b64decode(oframe)
                        npimg = np.fromstring(img, dtype=np.uint8)
                        oframe = cv2.imdecode(npimg, 1)
                        hsv = cv2.cvtColor(oframe, cv2.COLOR_BGR2HSV)
                        mask = cv2.inRange(hsv, l_b, u_b)
                        contours,hierarchy1= cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                        for c in contours:
                                rect = cv2.boundingRect(c)
                                x,y,w,h = rect
                                area = w * h
                                epsilon = 0.08 * cv2.arcLength(c, True)
                                approx = cv2.approxPolyDP(c, epsilon, True)
                                if area > 1000:
                                        #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 5)
                                        cv2.rectangle(oframe, (x, y), (x+w, y+h), (0, 255, 0), 5)
                                        print('mid', int(round(x+(w/2))), w)
                                        cv2.circle(oframe, (int(round(x+(w/2))),int(round(y+(h/2)))), 30, (0,0,255), -1)
                                        j=int(round(x+(w/2)))
                                        k=int(w)
                                        if(j < 280):
                                                mess = 'left'
                                        elif(j > 320):
                                                mess = 'right'
                                        elif(k>450):
                                                mess='front'
                                        else:
                                                mess='stop'
                        c, addr = s.accept()
                        print('Got connection from', addr)
                        c.send(mess.encode())
                        c.close()
                        frame=oframe

                except KeyboardInterrupt:
                        break

def web_page():
        # start the flask app
        app.run(host='192.168.43.205', port='8000', debug=True,threaded=True, use_reloader=False)

if __name__ == "__main__": 
	# creating thread 
	t1 = threading.Thread(target=pitalk) 
	t2 = threading.Thread(target=web_page) 

	# starting thread 1 
	t1.start() 
	# starting thread 2 
	t2.start() 

	# wait until thread 1 is completely executed 
	t1.join() 
	# wait until thread 2 is completely executed 
	t2.join() 

	# both threads completely executed 
	print("Done!") 

