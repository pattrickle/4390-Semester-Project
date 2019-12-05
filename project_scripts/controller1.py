#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Controller Code
import socket
import sys
import os
import errno
import time

class Controller:
	LOCAL_IP = "10.0.0.3"
	R_IP = "10.0.0.2"
	S_IP = "10.0.0.1"

	C_SEND = (LOCAL_IP,2500)
	C_RECV = (LOCAL_IP,5000)
	R = (R_IP,5000)
	S = (S_IP,5000)
	sendSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	recvSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	COMMANDPROMPT = ("Enter the number corresponding to the desired command:\n[0] Play\n[1] Pause\n[2] Restart\n[3] Disconnect\n")
	FILEPROMPT = ("Enter the number corresponding to the desired file:")

	type = ""
	code = ""
	inPayload = ["",""]
	outPayload = ""
	disconnect = False
	streaming = False

	def __init__(self):
    	self.sendSock.bind(self.C_SEND)
    	self.recvSock.bind(self.C_RECV)
    	self.disconnect = False

	def isConnected(self):
    	if self.disconnect:
        	return False
    	else:
        	return True

	def listenCommand(self):
    	#print("Controller: Listening")

    	packet = ["","",""]
    	try:
        	rawPacket, rawIP = self.recvSock.recvfrom(2048)
    	except:
        	raise
    	if rawPacket:
        	#print "Controller: Received Message"
        	packet = rawPacket.split(" ",2)
        	self.type = packet[0] #first is type
        	self.code = packet[1] #second is type
        	if type == "STREAM" and code == "NULL":
            	self.inPayload = packet[2].split(" ",1) #will be split if type and code are stream and NULL
        	else:
            	self.inPayload[0] = packet[2]
        	#print "Controller: MESSAGE: " + self.type + " " + self.code + " " + str(self.inPayload)

	def sendCommand(self, HOST, STATUS):
    	#print "Controller: Sending"
    	localPacket = STATUS + self.outPayload
    	if HOST == "S":
        	self.sendSock.sendto(localPacket,self.S)
    	if HOST == "R":
        	self.sendSock.sendto(localPacket,self.R)

    	#print "Controller: Message Sent to " + HOST
    	#print "Controller: MESSAGE: " + localPacket

	def play(self):
    	print "Controller: PLAY"
    	self.sendCommand("S", "PLAY NULL ")

	def pause(self):
    	print "Controller: PAUSE"
    	self.sendCommand("S", "PAUSE NULL ")

	def restart(self):
    	print "Controller: RESTART"
    	self.outPayload = str(0)
    	self.sendCommand("S", "PLAY LINE ")
    	self.sendCommand("R", "PLAY LINE ")

	def disconnectF(self):
    	print "Controller: DISCONNECT"
    	self.sendCommand("S", "DISCONNECT NULL ")
    	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    	print "Controller: Disconnected"

controller = Controller()

print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

while controller.isConnected():
	#create initial frame
	controller.sendCommand("S", "CONNECT NULL ")
	prompt = ""
	controller.recvSock.setblocking(1)
	controller.listenCommand()
	controller.recvSock.setblocking(0)
	files = controller.inPayload[0].split(" ",len(controller.inPayload[0])-1)
	print controller.FILEPROMPT
	index = 0
	for f in files:
    	prompt += "[" + str(index) + "]" + " " + f + "\n"
    	index += 1
	index = int(raw_input(prompt))
	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	controller.outPayload = files[index]
	controller.sendCommand("R", "STREAM FILE ")

	#populate list frame
	#wait for selection of file by user
	while controller.isConnected():
    	try:
        	controller.listenCommand()
    	except socket.error:
        	continue #include try and catch in a loop
    	else:
        	if controller.code == "FNF":
            	break

    	controller.recvSock.setblocking(1)
    	while controller.code != "READY":
        	controller.listenCommand()

    	controller.sendCommand("S", "PLAY NULL ")
    	controller.recvSock.setblocking(0)
    	while controller.isConnected():

        	buttonPress = int(raw_input(controller.COMMANDPROMPT))
        	controller.recvSock.setblocking(0)
        	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        	if buttonPress == 0:
            	controller.play()

        	elif buttonPress == 1:
            	controller.pause()

        	elif buttonPress == 2:
            	controller.restart()

        	elif buttonPress == 3:
            	controller.disconnectF()
            	controller.disconnect = True

        	if(controller.code == "END"):
            	controller.disconnect = True
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
