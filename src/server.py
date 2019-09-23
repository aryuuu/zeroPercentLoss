#!/usr/bin/python3
import socket
from packethandler import *
import struct
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 2000))
# wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)
mreq = struct.pack("=4sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("server is ready")

#queue up to 5 requests
# server_socket.listen(5)
# packet_buffer = ''
packet_buffer = {} #a buffer for packets, once all the file received, the data from this buffer is written to local file
incomplete_ID = [] #list of file ID that has not completely received

while True:
	# data, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	packet, addr = server_socket.recvfrom(MAX_PACKET_SIZE)
	
	if (is_valid(packet)):
		TYPE, ID, SEQUENCE_NUMBER, DATA = extract_packet(packet) #extract the packet
		
		if ID in packet_buffer: #check if this is the first packet of the file
			# packet_buffer[ID] += bytes.fromhex(DATA).decode('utf-8') #append to the previous packets of the file with same ID
			packet_buffer[ID] += bytes.fromhex(DATA)
		else:
			# packet_buffer[ID] = bytes.fromhex(DATA).decode('utf-8') #create new key for the file
			packet_buffer[ID] = bytes.fromhex(DATA)
			# incomplete_ID.append(ID)

		#check if that is the last packet for the file
		if (TYPE == FIN):
			REPLY_TYPE = FIN_ACK 
			#once the file received completely, write it to filesystem
			f = open("received_"+str(ID), 'wb') 
			f.write(packet_buffer[ID])
			f.close()
			print("file with ID :", ID,"saved!")
			del packet_buffer[ID]
			# incomplete_ID.remove(ID) 

		else:
			REPLY_TYPE = ACK 

		#build a reply packet and send it to client
		reply = build_packet(REPLY_TYPE, ID, SEQUENCE_NUMBER)
		server_socket.sendto(reply, addr)
		

	else:
		print("packet is loss")

