import socket
import time
import os
import random
from scapy.all import *

def send_ctc_message(ctc_message):
    host = '127.0.0.1'
    port = 5567  # Separate port for CTC

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((host, port))

    binary_ctc_message = ''.join(format(ord(char), '08b') for char in ctc_message)
    
    short_range = (0.03, 0.06)
    medium_range = (0.09, 0.12)
    data=b'InitialPacket'
    delay=0.005
    bincheck = ""
    addbin = ""
    sender_socket.send(data)
    time.sleep(delay) #send initial packet

    for bit in binary_ctc_message:
        
        if bit == '0':
            delay = random.uniform(short_range[0], short_range[1]) # to signify '0' value, set a short IPD
            
            addbin = '0'
        elif bit == '1':
            delay = random.uniform(medium_range[0], medium_range[1]) #to siginify '1' value, set a longer IPD
            
            addbin = '1'

        data = b'JunkData'
        sender_socket.send(data)
        time.sleep(delay)
        print(f"Delay: {delay}, Bit: {addbin}")
        bincheck = bincheck+addbin
        

    sender_socket.send(data)
    time.sleep(2.5)
    reconstructed_ascii_message = ''.join(chr(int(binary_ctc_message[i:i+8], 2)) for i in range(0, len(binary_ctc_message), 8))
    ASCII_Check = ''.join(chr(int(bincheck[i:i+8], 2)) for i in range(0, len(bincheck), 8))
    print(f"Sent CTC Binary message: {binary_ctc_message}")
    print(f"CTC ASCII Message: {reconstructed_ascii_message}")
    print(f"This is the binary checker: {bincheck}")
    print(f"This is the ASCII checker: {ASCII_Check}")
    sender_socket.close()

def csc_sport(covert_file):
    receiver_ip = '127.0.0.1'  # Receiver's IP address
    
    # Read the covert data from Hidden.txt
    with open(covert_file, 'r') as file:
        covert_data = file.read()

    for character in covert_data:
        char = ord(character) 
        #if option == 'SPort':
        ip_packet = IP(dst=receiver_ip)/TCP(sport=char,dport=5553)
        print(char)
        print(ip_packet.show())
        send(ip_packet)
    
    ip_packet = IP(dst=receiver_ip) / TCP(sport=0, dport=5553, flags="F")
    print(ip_packet.show())
    send(ip_packet)

def csc_ipid(covert_file):
    receiver_ip = '127.0.0.1'  # Receiver's IP address
    
    # Read the covert data from Hidden.txt
    with open(covert_file, 'r') as file:
        covert_data = file.read()

    for character in covert_data:
        char = ord(character) 
        #if option == 'SPort':
        ip_packet = IP(dst=receiver_ip,id=char)/TCP(dport=5553)
        print(ip_packet.show())
        send(ip_packet)
    
    ip_packet = IP(dst=receiver_ip) / TCP(sport=0, dport=5553, flags="F")
    print(ip_packet.show())
    send(ip_packet)

def send_csc_message(covert_file):

# Sender configuration
 receiver_ip = '127.0.0.1'  # Receiver's IP address
 #receiver_port = 5553  # Receiver's port
 # Read the covert data from Hidden.txt
 with open(covert_file, 'r') as file:
        covert_data = file.read()

 print(option)
 for character in covert_data:
    char = ord(character)
    if option == 'Sport':
        ip_packet = IP(dst=receiver_ip)/TCP(sport=char,dport=5553)
    elif option == 'IPID':
        ip_packet = IP(dst=receiver_ip,id=char)/TCP(dport=5553)
    print(ip_packet.show())
    # Send the custom IP packet
    send(ip_packet)

 ip_packet = IP(dst=receiver_ip) / TCP(sport=0, dport=5553, flags="F")
 print(ip_packet.show())
 send(ip_packet)


if __name__ == "__main__":
    while True:
        user_choice = input("Choose functionality (CTC or CSC): ").strip().lower()
        if user_choice == 'ctc':
            ctc_message = "Hello, this is my Inter Packet Delay Channel. Use timing delays for hidden signal"  # Replace with your CTC message
            send_ctc_message(ctc_message)
            break
        elif user_choice == 'csc':
            payload_file = 'Hidden.txt'  # Replace with your file path
            flag_input = input("Choose Header field for modulation (sport, ipid): ").strip().lower()
            print(flag_input)
            if flag_input == 'sport':
                csc_sport(payload_file)
            if flag_input == 'ipid':
                csc_ipid(payload_file)
            #send_csc_message(payload_file, flag_input)
            break
        else:
            print("Invalid choice. Please enter 'CTC' or 'CSC'.")