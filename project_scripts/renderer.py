#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Renderer Code

import socket
import sys
import os

class Renderer:
	C_IP = "10.0.0.3"
	LOCAL_IP = "10.0.0.2"
	S_IP = "10.0.0.1"

	C = (C_IP,5000) #tuple object
	R = (LOCAL_IP,5000)
	S = (S_IP,5000)

	rendererSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, udp

	outPayload = ""
	currentLine = 0
	inPayload = []
	type = ""
	code = ""
	switchVar = -1
	lineCount = 0
	totalLines = 0
	disconnect = False

	def __init__(self):
    	self.rendererSock.bind(self.R)
    	self.disconnect = False

	def isConnected(self):
    	if self.disconnect:
        	return False
    	else:
        	return True

	def listenCommand(self):
    	#print "Renderer: Listening"
    	try:
        	rawPacket, rawIP = self.rendererSock.recvfrom(2048)
    	except:
        	raise
    	if rawPacket:
        	#print "Renderer: Received Message"
        	packet = rawPacket.split(" ",2)
        	self.type = packet[0] #first is type
        	self.code = packet[1] #second is code
        	if type == "STREAM" and code == "NULL":
            	self.inPayload = packet[2].split(" ",1) #will be split if type and code are stream and NULL
        	else:
            	self.inPayload = packet[2]
        	#print "Renderer: MESSAGE: " + self.type + " " + self.code + " " + str(self.inPayload)

	def sendCommand(self, HOST, STATUS):
    	#print "Renderer: Sending"

    	localPacket = STATUS + self.outPayload
    	if HOST == "S":
        	self.rendererSock.sendto(localPacket,self.S) #host and port
    	if HOST == "C":
        	self.rendererSock.sendto(localPacket,self.C)

    	#print "Renderer: Message Sent to " + HOST
    	#print "Renderer: MESSAGE: " + localPacket

	def case0(self):
    	#print "Renderer: Case 0 - FILE"
    	self.outPayload = self.inPayload
    	self.sendCommand("S", "STREAM FILE ")
    	self.outPayload = ""
    	self.sendCommand("C", "STREAM ACK ")
    	self.switchVar = -1

	def case1(self):
    	#print "Renderer: Case 1 - READY"
    	self.totalLines = int(self.inPayload[:2])
    	self.outPayload = ""
    	self.sendCommand("C", "STATUS READY ")
    	self.switchVar = -1

	def case2(self):
    	#print "Renderer: Case 2 - FNF"
    	self.outPayload = ""
    	self.sendCommand("C", "STATUS FNF ")
    	self.switchVar = -1

	def case3(self):
    	#print "Renderer: Case 3 - PLAY"
    	tempLine = int(self.inPayload[:2])
    	line = self.inPayload[2:]

    	if tempLine != self.currentLine :
        	self.outPayload = str(self.currentLine)
        	self.sendCommand("S", "PLAY LINE ")
    	else:
        	print(line.rstrip('\n'))

        	self.currentLine += 1
    	self.switchVar = -1

	def case4(self):
    	#print "Renderer: Case 4 - RESTART"
    	self.currentLine = 0
    	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    	self.switchVar = -1

	def case5(self):
    	#print "Renderer: Case 5 - END"

    	if self.currentLine == self.totalLines :
        	self.outPayload = ""
        	print "\n\nThe End"
    	else :
        	self.outPayload = str(self.currentLine)
        	self.sendCommand("S", "PLAY LINE ")
    	self.switchVar = -1

	def case6(self):
    	self.outPayload = ""
    	self.sendCommand("C", "DISCONNECT ACK ")
    	self.disconnect = True
    	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    	print "Renderer: Disconnected"


	#create Frame
renderer = Renderer()
print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

while renderer.isConnected():
	#print("Renderer Main loop begun")

	renderer.listenCommand()


	if renderer.type == "STREAM":
    	if renderer.code == "FILE":
        	renderer.switchVar = 0
    	else:
        	renderer.switchVar = 3
	if renderer.type == "STATUS":
    	if renderer.code == "READY":
        	renderer.switchVar = 1
    	if renderer.code == "FNF":
        	renderer.switchVar = 2
    	if renderer.code == "END":
        	renderer.switchVar = 5
	if renderer.type == "PLAY":
    	renderer.switchVar = 4
	if renderer.type == "DISCONNECT":
    	renderer.switchVar = 6

	if renderer.switchVar == 0:
    	renderer.case0()
	elif renderer.switchVar == 1:
    	renderer.case1()
	elif renderer.switchVar == 2:
    	renderer.case2()
	elif renderer.switchVar == 3:
    	renderer.case3()
	elif renderer.switchVar == 4:
    	renderer.case4()
	elif renderer.switchVar == 5:
    	renderer.case5()
	elif renderer.switchVar == 6:
    	renderer.case6()
