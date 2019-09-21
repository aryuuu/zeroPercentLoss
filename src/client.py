#!/usr/bin/python3
import socket
from packethandler import *



#create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set host, port and message
host = input("host >> ")
port = int(input("port >> "))
filename = input("filename >> ")

#read the file, file is assumed to fit in one packet
content = open(filename).read()

packet = build_packet(FIN, 0x1, 0x1,content) #build the packet

received = False
while (not received):
	s.sendto(packet, (host, port)) #send the packet

	reply, addr = s.recvfrom(MAX_PACKET_SIZE) 
	TYPE, ID, SEQUENCE_NUMBER, DATA = extract_packet(reply) 

	received = (TYPE == FIN_ACK)

print("lets call it a day")