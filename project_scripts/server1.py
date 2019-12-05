#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Server Code

import socket
import sys
import os
import time
from os import listdir
from os.path import isfile, join

class Server:
	#assign values
	LOCAL_IP = "10.0.0.1" #local
	R_IP = "10.0.0.2"
	C_IP = "10.0.0.3"

	C = (C_IP,5000) #tuple object
	R = (R_IP,5000)
	S = (LOCAL_IP,5000)

	serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, udp
	type = ""
	code = ""
	inPayload = ["",""]
	outPayload = ""
	selectFile = None
	switchVar = 4 #escape
	lineCount = 0
	totalLines = 0
	filePath = "/home/milo/Documents/Final/Text/"
	disconnect = False
	pause = False

	def __init__(self):
    	self.serverSock.bind(self.S)
    	self.disconnect = False

	def isConnected(self):
    	if self.disconnect:
        	return False
    	else:
        	return True

	def isPaused(self):
    	return self.pause

	def listenCommand(self):
    	print "Server: Listening"
    	try:
        	rawPacket = self.serverSock.recv(2048)
    	except:
        	raise
    	if rawPacket:
        	print "Server: Received Message"
        	packet = rawPacket.split(" ",2)
        	self.type = packet[0] #first is type
        	self.code = packet[1] #second is code
        	if type == "STREAM" and code == "NULL":
            	self.inPayload = packet[2].split(" ",1) #will be split if type and code are stream and NULL
        	else:
            	self.inPayload[0] = packet[2]
        	if type == "PAUSE" and code == "NULL":
            	self.pause = True
        	else:
            	self.pause = False

        	print "Server: MESSAGE: " + self.type + " " + self.code + " " + str(self.inPayload)


	def sendCommand(self, HOST, STATUS): #work on
    	print "Server: Sending"

    	localPacket = STATUS + str(self.outPayload)

    	if HOST == "R":
        	self.serverSock.sendto(localPacket,self.R) #host and port
    	if HOST == "C":
        	self.serverSock.sendto(localPacket,self.C)

    	print "Server: Message Sent to " + HOST
    	print "Server: MESSAGE: " + localPacket


	#switch statement
	def case0(self): #CONNECT
    	print "Server: Case 0 - CONNECT"
    	self.outPayload = ""

    	arr = os.listdir(self.filePath) #directory of files

    	for x in arr: #goes through file
        	self.outPayload += " " + x #names of files
    	self.outPayload = self.outPayload[1:]

    	self.sendCommand("C", "CONNECT ACK ")
    	self.type = "PAUSE"
    	self.code = "NULL"

	def case1(self): #STREAM
    	print "Server: Case 1 - STREAM"

    	arr = os.listdir(self.filePath) #directory of files

    	for x in arr: #goes through file, then opens
        	if os.path.exists(self.filePath + self.inPayload[0]): #adding to full file path
            	self.selectFile = open(self.filePath + "/" + self.inPayload[0],'r')
    	#opened file
    	if self.selectFile != None: #FIX
        	line = self.selectFile.readline() #first line
        	while line:

            	self.lineCount += 1 #increment total totalLines
            	line = self.selectFile.readline()

        	self.outPayload = self.lineCount
        	self.sendCommand("R", "STATUS READY ")

    	else:
        	self.sendCommand("R", "STATUS FNF ")

    	self.lineCount = 0
    	self.selectFile.seek(0) #restart file pointer
    	self.type = "PAUSE"
    	self.code = "NULL"

	def case2(self): #PLAY/NULL
    	print "Server: Case 2 - PLAY"

    	line = self.selectFile.readline()
    	if line:
        	self.outPayload = str(self.lineCount)
        	self.outPayload = self.outPayload + " "
        	self.outPayload = self.outPayload + line
        	self.sendCommand("R","STREAM NULL ")

        	self.lineCount += 1
        	time.sleep(.5) #delay of 1/10s
    	else:
        	self.sendCommand("R","STATUS END ")

        	self.type = "PAUSE"
        	self.code = "NULL"

	def case3(self): #PLAY/LINE
    	print "Server: Case 3 - PLAY LINE"
    	self.selectFile.seek(0)
    	lineRequest = int(self.inPayload[0])

    	x = 0

    	while (x < lineRequest):
        	line = self.selectFile.readline() #store current line indexed by # x
        	x += 1

    	self.lineCount = lineRequest

    	self.type = "PLAY"
    	self.code = "NULL"

	def case4(self): #PAUSE, DEFAULT
    	if self.isPaused():
        	print "Server: Case 4 - PAUSE"

    	self.type = "PAUSE"
    	self.code = "NULL"

	def case5(self): #DISCONNECT
    	print "Server: Case 5 - DISCONNECT"

    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.disconnect = True
    	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    	print "Server: Disconnected"


server = Server()
server.serverSock.setblocking(0)
print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
print "Server: Connected"
while server.isConnected():
	time.sleep(.5)

	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"


	try:

    	server.listenCommand()
	except socket.error:
    	pass


	if server.type == "CONNECT":
    	server.switchVar = 0
	if server.type == "STREAM":
    	server.switchVar = 1
	if server.type == "PLAY" and server.code == "NULL":
    	server.switchVar = 2
	if server.type == "PLAY" and server.code == "LINE":
    	server.switchVar = 3
	if server.type == "PAUSE":
    	server.switchVar = 4
	if server.type == "DISCONNECT":
    	server.switchVar = 5

	if server.switchVar == 0:
    	server.case0()
	elif server.switchVar == 1:
    	server.case1()
	elif server.switchVar == 2:
    	server.case2()
	elif server.switchVar == 3:
    	server.case3()
	elif server.switchVar == 4:
    	server.case4()
	elif server.switchVar == 5:
    	server.case5()
