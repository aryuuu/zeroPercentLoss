#!/usr/bin/python3
import socket
from packethandler import *

#create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set host and port
host = '192.168.1.3'
port = 2000

#bind to the port
server_socket.bind((host,port))

#queue up to 5 requests
# server_socket.listen(5)

while True:
	# data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	packet, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	print("from :", addr)
	print("raw packet :", packet.hex())
	print("checksum from packet :", int(packet.hex()[10:14], 16))
	# print("Message :", data)
	if (is_valid(packet)):
		TYPE, ID, SEQUENCE_NUMBER, DATA = extract_packet(packet) #extract the packet
		print("TYPE :", TYPE)
		print("ID :", ID)
		print("DATA :", end='')
		for i in range(0,len(DATA), 2):
			print(chr(int(DATA[i:i+2], 16)), end='')
		print()

		REPLY_TYPE = ACK 
		if (TYPE == FIN):
			REPLY_TYPE = FIN_ACK

		reply = build_packet(REPLY_TYPE, ID, SEQUENCE_NUMBER) #build an acknowledgment packet
		server_socket.sendto(reply, addr) #send an acknowledment
	else:
		print("packet is loss")



