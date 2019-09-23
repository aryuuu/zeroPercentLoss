#!/usr/bin/python3
import codecs

#constants
MAX_DATA_SIZE = 32768
MAX_PACKET_SIZE = MAX_DATA_SIZE + 7
DATA = 0x0
ACK = 0x1
FIN = 0x2
FIN_ACK = 0x3



#split num into one byte chunks and turn it into ascii character
#num is an integer
#zero padding is and integer annotating the number of zero to pad in to the result
def int_to_ascii(num, zero_padding=0): #this method contains some weird bug
	
	#get hex value from num
	num = str(hex(num))[2:].zfill(zero_padding)
	
	result = ''
	for i in range(0,len(num), 2):
		result += chr(int(num[i:i+2], 16))


	return result

#this method is just like int_to_ascii, but returns bytes instead of string
#i hope there is no more weird bug
def imp_int_to_ascii(num, zero_padding=2):
	decode_hex = codecs.getdecoder("hex_codec")
	num = str(hex(num))[2:].zfill(zero_padding)

	result = decode_hex(num)[0]
	return result



#this method return int value for a string
def ascii_to_int(stream):
	result = 0
	for i in stream:
		result = result*16 + ord(i)

	return result

#validate a packet by comparing its checksum
#packet is an encoded string
#returns True if packet is valid and False if not valid
def is_valid(packet):
	given_checksum = int(packet.hex()[10:14], 16) #get given checksum
	purged_packet = packet[:5] + packet[7:] #exlude the checksum from the packet
	
	#count the new checksum
	new_checksum = 0x0
	for i in range(0, len(purged_packet), 2):
		chunks = int(purged_packet[i]/16) * (16**3) + (purged_packet[i]%16) * (16**2) 

		if (i+1 < len(purged_packet)):
			chunks += int(purged_packet[i+1]/16) * (16**1) + (purged_packet[i+1]%16) * (16**0)

		new_checksum ^= chunks

	return new_checksum == given_checksum




#build method
#build a packet from TYPE, ID, SEQUENCE_NUMBER, and DATA
#TYPE is an integer, as long as ID and SEQUENCE_NUMBER
#DATA is a string
#this method return an encoded string which is the packet
def build_packet(TYPE, ID, SEQUENCE_NUMBER, DATA=None):
	
	#set the first byte, consist of TYPE and ID
	first_byte = (TYPE << 4) + ID

	#set packet LENGTH
	LENGTH = 7
	if (DATA != None):
		LENGTH += len(DATA)

	temp = imp_int_to_ascii(first_byte) + imp_int_to_ascii(SEQUENCE_NUMBER, 4) + imp_int_to_ascii(LENGTH, 4)
	if (DATA != None):
		temp += DATA
		# temp += DATA.encode()

	checksum = 0x0

	for i in range(0, len(temp), 2):
		chunks = int(temp[i]/16) * (16**3) + (temp[i]%16) * (16**2) 

		if (i+1 < len(temp)):
			chunks += int(temp[i+1]/16) * (16**1) + (temp[i+1]%16) * (16**0)

		checksum ^= chunks	

	#compose the packet
	
	result = imp_int_to_ascii(first_byte) + imp_int_to_ascii(SEQUENCE_NUMBER, 4) + imp_int_to_ascii(LENGTH, 4) + imp_int_to_ascii(checksum, 4)

	if (DATA != None):
		# result += DATA.encode()
		result += DATA
	return result




#extract data from a packet, packet is assumed to be valid
#packet is an encoded string
#this method return TYPE, ID, SEQUENCE_NUMBER and DATA
def extract_packet(packet):

	packet = packet.hex()

	#set value for TYPE, ID and DATA
	TYPE = int(packet[0],16)
	ID = int(packet[1],16)
	SEQUENCE_NUMBER = int(packet[2:6],16)
	DATA = None


	if(TYPE != ACK and TYPE != FIN_ACK):
		DATA = packet[14:]

	return TYPE, ID, SEQUENCE_NUMBER, DATA

