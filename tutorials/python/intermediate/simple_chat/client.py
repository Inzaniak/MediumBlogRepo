import socket
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Get the username
username = input("Enter your username: ")

try:
    # Send data
    while True:
        message = input("Enter your message: ")
        if message == "exit":
            break

        # Encode the message as JSON and send it
        message = {"username": username, "message": message}
        message = json.dumps(message).encode()
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)

finally:
    print('closing socket')
    sock.close()
