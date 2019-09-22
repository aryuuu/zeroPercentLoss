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
	# print(num)
	#get hex value from num
	num = str(hex(num))[2:].zfill(zero_padding)
	# print("now num is :", num)
	result = ''
	for i in range(0,len(num), 2):
		result += chr(int(num[i:i+2], 16))
	# 	print("temp result :", result.encode().hex())
	# print("result :", result.encode().hex())
	# print("len result :", len(result))
	# if ()

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
	# packet = packet.decode() #decode packet
	purged_packet = packet[:5] + packet[7:] #exlude the checksum from the packet
	
	# headers = packet[:5] #get TYPE, ID, LENGTH of packet
	# body = packet[7:] #get DATA from packet

	#count the new checksum
	new_checksum = 0x0
	for i in purged_packet:
		new_checksum ^= int(i)
	# for i in range(0,len(purged_packet),2):
	# 	# new_checksum ^= ascii_to_int(purged_packet[i:i+2])
	# 	new_checksum ^= purged_packet[i:i+2]

	print("given checksum :", given_checksum)
	print("new checksum :", new_checksum)
	#compare new_checksum to the given checksum
	return new_checksum == given_checksum




#build method
#build a packet from TYPE, ID, SEQUENCE_NUMBER, and DATA
#TYPE is an integer, as long as ID and SEQUENCE_NUMBER
#DATA is a string
#this method return an encoded string which is the packet
def build_packet(TYPE, ID, SEQUENCE_NUMBER, DATA=None):
	
	#set the first byte, consist of TYPE and ID
	# first_byte = str(hex((TYPE << 4) + ID)).strip('0x')
	first_byte = (TYPE << 4) + ID
	print("first_byte :", int_to_ascii(first_byte))
	print("first_byte in hex :", str(hex(first_byte)))
	print("SEQUENCE_NUMBER :", int_to_ascii(SEQUENCE_NUMBER).encode())
	#set packet LENGTH
	LENGTH = 7
	if (DATA != None):
		LENGTH += len(DATA)
	# print("PACKET LENGTH :", int_to_ascii(LENGTH).encode().hex())

	# temp = chr(first_byte) + chr(SEQUENCE_NUMBER >> 8) + chr(SEQUENCE_NUMBER & 0x00ff) + chr(LENGTH)
	# temp = int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER,4) + int_to_ascii(LENGTH,4)
	temp = imp_int_to_ascii(first_byte) + imp_int_to_ascii(SEQUENCE_NUMBER, 4) + imp_int_to_ascii(LENGTH, 4)
	if (DATA != None):
		# temp += DATA
		temp += DATA.encode()

	checksum = 0x0
	for i in temp:
		checksum ^= i
	# for i in range(0,len(temp),2):
		# checksum ^= ascii_to_int(temp[i:i+2])
		

	print("counted checksum :", hex(checksum))
	# print("converted checksum in ascii :", int_to_ascii(checksum).encode())
	print("converted checksum in ascii :", imp_int_to_ascii(checksum))

	#compose the packet
	# result = int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER,4) + int_to_ascii(LENGTH,4) + int_to_ascii(checksum,4) # this code contain some weird bug
	# print("first byte + SEQUENCE_NUMBER :", (int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER, 4)).encode().hex()) 
	# print("first byte + SEQUENCE_NUMBER + LENGTH", (int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER, 4) + int_to_ascii(LENGTH, 4)).encode().hex())
	# print("first_byte + SEQUENCE_NUMBER + LENGTH + checksum", (int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER, 4) + int_to_ascii(LENGTH, 4) + int_to_ascii(checksum, 4)).encode().hex())
	
	# result = int_to_ascii(first_byte) + int_to_ascii(SEQUENCE_NUMBER, 4) + int_to_ascii(LENGTH, 4) + int_to_ascii(checksum, 4)
	result = imp_int_to_ascii(first_byte) + imp_int_to_ascii(SEQUENCE_NUMBER, 4) + imp_int_to_ascii(LENGTH, 4) + imp_int_to_ascii(checksum, 4)

	print("result :", result.hex())
	# print("result consist of", len(result.hex())/2, "bytes")
	# print("PACKET LENGTH :", imp_int_to_ascii(LENGTH).hex())
	print("converted checksum in ascii :", imp_int_to_ascii(checksum))
	print("checksum from result :", int(result.hex()[10:14], 16))
	print("checksum from result in hex : 0x%s" %result.hex()[10:14])
	if (DATA != None):
		result += DATA.encode()

	# print("result :", result[:100].encode())
	print("result :", result[:100])
	# return result.encode()
	return result




#extract data from a packet, packet is assumed to be valid
#packet is an encoded string
#this method return TYPE, ID, SEQUENCE_NUMBER and DATA
def extract_packet(packet):
	packet = packet.hex()

	#set value for TYPE, ID and DATA
	TYPE = int(packet[0],16)
	ID = int(packet[1],16)
	SEQUENCE_NUMBER = int(packet[2:4])
	DATA = None

	if(TYPE != ACK and TYPE != FIN_ACK):
		DATA = packet[14:]

	return TYPE, ID, SEQUENCE_NUMBER, DATA

#this method returns an ID for a file
def generate_id(filename):
	ID = 0
	for i in filename:
		ID ^= ord(i)
	ID &= 0xf
	return ID