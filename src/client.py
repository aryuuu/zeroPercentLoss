#!/usr/bin/python3
import socket
from packethandler import *
from bonus import *


#create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set host, port and list of filenames
host = input("host >> ")
port = int(input("port >> "))
filenames = input("filenames >> ").split(' ')

#read the file, than split it into packet sized data
contents = []
for filename in filenames:
	temp = open(filename,'rb').read()
	contents.append([temp[i:i+MAX_DATA_SIZE] for i in range(0, len(temp), MAX_DATA_SIZE)])

print("number of files to be sent :", len(contents))


SEQUENCE_NUMBER = [0 for i in range(len(contents))] #set initial SEQUENCE_NUMBER for each file in list
done_ID = []	#list for file IDs that finished being sent



done = False
while (not done):
	#set the other metadata
	
	
	for ID in range(len(contents)): #iterate through each files
		if (ID not in done_ID): #check if the file is already sent completely

			
			if (SEQUENCE_NUMBER[ID]+1 == len(contents[ID])):
				TYPE = FIN
			else:
				TYPE = DATA
	
			packet = build_packet(TYPE, ID, SEQUENCE_NUMBER[ID], contents[ID][SEQUENCE_NUMBER[ID]]) #build the packet

			s.sendto(packet, (host, port)) #send the packet

			reply, addr = s.recvfrom(MAX_PACKET_SIZE) 
			REPLY_TYPE, REPLY_ID, REPLY_SEQUENCE_NUMBER, REPLY_DATA = extract_packet(reply) 
			print_progress_bar(REPLY_SEQUENCE_NUMBER+1, len(contents[REPLY_ID]), "file with ID" + str(REPLY_ID))
			

			if (REPLY_TYPE == FIN_ACK): #check if all packets of this file sent
				done_ID.append(REPLY_ID) #add the file ID to the done list
				print("file with ID :", ID, "sent!")
			else:
				SEQUENCE_NUMBER[REPLY_ID] = REPLY_SEQUENCE_NUMBER + 1 #get ready for the next packet


	# done = (REPLY_TYPE == FIN_ACK)
	done = len(contents) == len(done_ID)

print("lets call it a day")
s.close()