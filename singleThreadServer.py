# Include Python's Socket Library
from socket import *
import time
import os
# Specify Server Port
serverPort = 8000

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listening for incoming TCP connections
serverSocket.listen(1)
print ('The server is ready to receive')

while True: # Loop forever

    # Server waits on accept for incoming requests.
    # New socket created on return
    connectionSocket, addr = serverSocket.accept()
    print("connected to: " + addr[0] + " " + str(addr[1]))
    connectionSocket.settimeout(2.9)

    try:
        # Read from socket (but not address as in UDP)
        sentence = connectionSocket.recv(1024).decode()

        # Client must send a get request in the form GET /filename HTTP/1.1\r\n
        # Get the Nth word in string: https://www.geeksforgeeks.org/python-get-nth-word-in-given-string/
        header = sentence.split('\r\n')[0]  # request line
        request = header.split(' ')[0]      # GET
        page = header.split(' ')[1]         # filename
        http = header.split(' ')[2]         # HTTP

        if (page.startswith("/")):          # remove the '/' at start
            page = page[1:]

        print("header: " + header + " request: " + request + " page: " + page)

        # Check for bad request
        if (request != "GET" or http != "HTTP/1.1"):
            with open("badRequest.html",'r') as f:
                file = f.read()
            response = 'HTTP/1.1  400 BAD REQUEST\r\nContent-Type: text/html\r\n\r\n'
            response = response + file + '\r\n'
        else:
            try:
                # Check if the page exists, then check if error code is 200 or 304
                with open(page,'r') as f:
                    file = f.read()

                # last modified date of file
                lastModified = time.ctime(os.path.getmtime(page))

                modHeaderExist = 0
                for word in sentence.split("\r\n"):
                    header = word.split(' ')[0]
                    if (header == "if-Modified-Since:"):
                        header_len = len(header) + 1
                        dateReceived = word[header_len:]
                        # if the page has not been updated
                        if (lastModified == dateReceived):
                            modHeaderExist = 1
                
                # if the page has not been updated
                if (modHeaderExist == 1):
                    response = 'HTTP/1.1 304 Not Modified\r\n\r\n\r\n'
                # send 200 if page has not been updated    
                else:
                    # HTTP Response: status line\r\nheader line(s)\r\n\r\nHTML data
                    response = 'HTTP/1.1 200 OK\r\nLast-Modified: ' + lastModified + '\r\n\r\n'
                    response = response + file + '\r\n'
            # Page doesnt exist so send 404
            except FileNotFoundError:   # invalid filename
                with open("notFound.html",'r') as f:
                    file = f.read()
                response = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
                response = response + file + '\r\n'
    # Client took too long to send, send 408 timeout
    except timeout:
        with open("timedOut.html",'r') as f:
            file = f.read()
        response = 'HTTP/1.1 408 Request Timed Out\r\n\r\n'
        response = response + file + '\r\n'

    print("Sending " + response)
    # Send the reply
    connectionSocket.sendall(response.encode())

    # Close connection too client (but not welcoming socket)
    connectionSocket.close()
    print("Closing connection with: " + addr[0] + " " + str(addr[1]))