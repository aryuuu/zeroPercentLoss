#!/usr/bin/python3
import socket
from packethandler import *



#create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set host, port and message
host = input("host >> ")
port = int(input("port >> "))
filename = input("filename >> ")

#read the file, than split it into packet sized data
# content = str(open(filename).read()).encode().hex()
# print(content[:100])
content = open(filename).read()
content = [content[i:i+MAX_DATA_SIZE] for i in range(0,len(content), MAX_DATA_SIZE)]
print("content length :", len(content))
#set the metadata
ID = generate_id(filename)
SEQUENCE_NUMBER = 0




done = False
while (not done):
	#set the other metadata
	print("SEQUENCE_NUMBER+1 :", SEQUENCE_NUMBER+1, "== banyak packet :", len(content))
	if (SEQUENCE_NUMBER+1 == len(content)):
		TYPE = FIN
	else:
		TYPE = DATA
	print("TYPE :", TYPE)
	print("ID :", ID)
	packet = build_packet(TYPE, ID, SEQUENCE_NUMBER, content[SEQUENCE_NUMBER]) #build the packet

	s.sendto(packet, (host, port)) #send the packet

	reply, addr = s.recvfrom(MAX_PACKET_SIZE) 
	REPLY_TYPE, REPLY_ID, REPLY_SEQUENCE_NUMBER, REPLY_DATA = extract_packet(reply) 

	# content.pop(0) #assume packet is received in correct order
	SEQUENCE_NUMBER += 1

	done = (REPLY_TYPE == FIN_ACK)

print("lets call it a day")
s.close()