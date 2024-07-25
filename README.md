# Network Based Covert Communications Demonstration

## Overview

This project demonstrates two types of covert network communications channels: a Covert Timing Channel (CTC) and a Covert Storage Channel (CSC). The CTC function focuses on using inter-packet delays to codify a hidden message. The CSC function demonstrates TCP/IP steganography - hiding data within TCP/IP header fields. 

The program is designed to be the basis of an attacker or penetration tester's tool(kit) for covert communications. It serves a vision of a command line tool which can perform various methods and techniques of network-based covert communications. 

## Description

### Covert Timing Channel (CTC)

The Timing Channel utilizes delays between sent packets over a socket connection to encode a hidden message. The covert communication does not rely on actual data transfer, but rather signal translation using a dictionary-like cipher approach. 

The hidden message string specified in the code is first converted to binary. Then, iterating through this binary, various interpacket delay values are set.

short_range = (0.03, 0.06)
    - signifies a '0' bit
medium_range = (0.09, 0.12)
    - signifies a '1' bit

The receiver listens on the specified port over loopback, confirming an accepted connection. 

After receiving the initial packet, it begins measuring the timing delay between each received packet. Based on the delay time, the receiver notes either a '0' or a '1' into a binary array. This is ultimately decoded back into plaintext.  

### Covert Storage Chanel (CSC)

The Storage Channel hides encoded characters from a text file into TCP/IP header fields. This covert method manipulates possible values for certain fields, replacing an expected or default value with hidden data.

This implementation utilizes two fields:
    - Source port in TCP protocol
    - ID in IP protocol

The sender code iterates through a specified file's content, converting each character into Unicode. Based on the specified carrier field, that field value is replaced with the Unicode. This crafted packet is sent over the loopback interface to the desired port.

The receiver, sniffing traffic on the loopback interface and specified port, inspects incoming packets. The specified carrier is inspected and the value is converted back to plaintext character. This is then written to an output file.

The sniffing is terminated upon receiving an "F" flag option.

## Requirements
The following files are included in this submission:
    - SepTool_Send.py: The sender/client program
    - SepTool_Rec.py: The receiver/server program
    - Hidden.txt: The sample payload for the Covert Storage Channel

The following Python libraries are used :
  - `socket`: For network communication
  - 'scapy' : For packet crafting and inspection
  - 'time': For implementing timing delays
  - 'random': For variance in the set timing delay

## Usage

1. Open a Command line interface. Run the receiver program first:
    python SepTool_Rec.py

2. When prompted, specify which covert communication method you wish to use from the given options:
    Example: Choose functionality (ctc or csc): csc

3. If choosing CSC, further specify the carrier for the hidden data from the given options:
    Example: Choose Header field for extraction (sport, ipid): sport

4. Open another Command Line interface. Run the sender program:
    python SeptTool_Send.py

5. Repeat steps 2 and 3 when presented with options. Ensure that the chosen options match those chosen at the execution of the receiver

6. Expected outputs:
    - CTC:
        - Sender and receiver will both print the binary and plaintext hidden messages in terminal
    - CSC:
        - Sender will print the packet info in terminal
        - Receiver will print each received character in terminal and confirm writing to specified output path (this path is specified within the code)
        - An output file will be written to in the same directory. The contents of this file should match the payload file 'Hidden.txt'

## Technical Considerations

The code is being run over loopback interface on a Windows endpoint. It also is reliant upon stable network connections. Network issues may cause errors in the program.

The code specifies the ports being used. User may change the ports over which communications are being done, but be wary of ports already in use or which may result in lossy connection.

The covert method and carrier (if CSC scenario) being used must be specified both by the receiver and the sender. These options must match up on both sides, else there will be a communication error.

## Ethical Considerations

This program is meant for academic use only. It is not to be used or shared in any manner which contradicts legal or ethical norms of covert communications.