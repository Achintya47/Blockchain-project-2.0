import socket
import json

node = socket.gethostbyname(socket.gethostname())
def send_message(message):
    print("Entered Sender Code for node:", node)
    host = "192.168.1.255"  # Broadcast address
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use UDP
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.sendto(message.encode(), (host, port))  # Send the string
    client_socket.close()
    print(f"Raw Message Sent : {message}")

    
