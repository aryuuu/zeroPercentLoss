#!/usr/bin/python3
import socket
from packethandler import *

#create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set host and port
host = input("host >> ")
port = int(input("port >> "))
filename = input("filename >> ")
# host = '192.168.1.3'
# port = 2000

#bind to the port
server_socket.bind((host,port))
print("server is ready")

#queue up to 5 requests
# server_socket.listen(5)
# packet_buffer = ''
packet_buffer = {} #a buffer for packets, once all the file received, the data from this buffer is written to local file
incomplete_ID = [] #list of file ID that has not completely received

while True:
	# data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	packet, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	print("from :", addr)
	# print("raw packet :", packet.hex())
	# print("checksum from packet :", int(packet.hex()[10:14], 16))
	# print("Message :", data)
	if (is_valid(packet)):
		TYPE, ID, SEQUENCE_NUMBER, DATA = extract_packet(packet) #extract the packet
		# print("TYPE :", TYPE)
		# print("ID :", ID)
		# print("DATA :", end='')
		# for i in range(0,len(DATA), 2):
		# 	print(chr(int(DATA[i:i+2], 16)), end='')
		# print()
		if ID in packet_buffer: #check if this is the first packet of the file
			packet_buffer[ID] += bytes.fromhex(DATA).decode('utf-8') #append to the previous packets of the file with same ID
		else:
			packet_buffer[ID] = bytes.fromhex(DATA).decode('utf-8') #create new key for the file
			incomplete_ID.append(ID)

		#check if that is the last packet for the file
		if (TYPE == FIN):
			REPLY_TYPE = FIN_ACK 
			incomplete_ID.remove(ID) 
		else:
			REPLY_TYPE = ACK 

		#build a reply packet and send it to client
		reply = build_packet(REPLY_TYPE, ID, SEQUENCE_NUMBER)
		server_socket.sendto(reply, addr)
		print("sending response to :", addr)

		if (len(incomplete_ID) == 0): #check if there is no more packet to receive
			break #stop receiving

		# REPLY_TYPE = ACK 
		# if (TYPE == FIN):
		# 	REPLY_TYPE = FIN_ACK
		# 	reply = build_packet(REPLY_TYPE, ID, SEQUENCE_NUMBER) #build an acknowledgment packet
		# 	server_socket.sendto(reply, addr) #send an acknowledment
		# 	break #number of clients is assumed to be one
		# else:
		# 	reply = build_packet(REPLY_TYPE, ID, SEQUENCE_NUMBER) #build an acknowledgment packet
		# 	server_socket.sendto(reply, addr) #send an acknowledment

	else:
		print("packet is loss")

for ID in packet_buffer:
	f = open("received_"+str(ID), 'a')

	f.write(packet_buffer[ID])
	f.close()
	print("saved!")
