import socket
import time
import random
import sys
from scapy.all import * 

def receive_ctc_message():
    host = '127.0.0.1'
    port = 5567  # Use the separate port for CTC

    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind((host, port))
    receiver_socket.listen(1)

    print(f"Waiting for the CTC sender to connect on port {port}...")
    conn, addr = receiver_socket.accept()
    print(f"Accepted connection from {addr}")

    binary_message = ""
    prev_time = None
    delay = 0
    initial_packet_received = False
    timeout = 2.0  # Set a timeout of 2 seconds
    #i=1
    while True:
        data = conn.recv(1)
        curr_time = time.time()
    
        if data:
            if not initial_packet_received:
                initial_packet_received = True
                prev_time = curr_time  # Initialize the previous time

            delay = curr_time - prev_time

            if 0.03 <= delay < 0.08:  # Short delay range
                binary_message += '0'
                #print(f"No: {i}, Delay: {delay}, Bit: {binary_message[-1]}")
                #i=i+1
            elif 0.09 <= delay < 0.14:  # Medium delay range
                binary_message += '1'
                #print(f"No: {i}, Delay: {delay}, Bit: {binary_message[-1]}")
                
            else:
                pass

            prev_time = curr_time  # Update previous time
            
        else:
            if initial_packet_received and time.time() - prev_time > timeout:
               print("Timeout reached. Exiting.")
               break  # No more data, and a timeout occurred

    #print("Binary message before conversion:", binary_message)
    if binary_message:
        ASCII_mess = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        reconstructed_ascii_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message) - 8, 8))
        print(f"Received CTC message (Binary): {binary_message}")
        #print(f"Received CTC message (ASCII): {reconstructed_ascii_message}")
        print(f"Received CTC message (ASCII): {ASCII_mess}")

    conn.close()
    receiver_socket.close()

    #print("Binary message before conversion:", binary_message)
    if binary_message:
        ASCII_mess = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        reconstructed_ascii_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message) - 8, 8))
        print(f"Received CTC message (Binary): {binary_message}")
        #print(f"Received CTC message (ASCII): {reconstructed_ascii_message}")
        print(f"Received CTC message (ASCII): {ASCII_mess}")

    conn.close()
    receiver_socket.close()

class MessageReceiver:
    def __init__(self):
        self.output_path = "received_payload.txt"
        self.first_packet = True
        self.cover=''
    def stoplistener(self, packet):
        if packet['TCP'].flags == 'F':
            self.transmission_complete = True
            print("Transmission complete. Connection closing")
            return True
        else:
            return False

    def receive_csc_message(self, packet):
        # Extract character from TCP sport field
        if self.cover == 'sport':
            character = chr(packet['TCP'].sport)
        elif self.cover == 'ipid':
            character = chr(packet['IP'].id)

        mode = 'w' if self.first_packet else 'a'
        with open(self.output_path, mode) as output_file:
            output_file.write(character)

        print("Received Character ", character, "has been saved to", self.output_path)

        self.first_packet = False  # Update state after processing the packet


if __name__ == "__main__":
    user_choice = input("Choose functionality (CTC or CSC): ").strip().lower()
    if user_choice == 'ctc':
        receive_ctc_message()
        #break
    elif user_choice == 'csc':
        while True:
            receiver=MessageReceiver()
            receiver.cover = input("Choose Header field for extraction (Sport, IPID): ").strip().lower()
            print("Listening")
            sniff(iface="Software Loopback Interface 1",filter="tcp and dst host 127.0.0.1 and dst port 5553", prn=receiver.receive_csc_message,stop_filter=receiver.stoplistener)
            break
    else:
        print("Invalid choice. Please enter 'CTC' or 'CSC'.")