# Include Python's Socket Library
from socket import *
import time
import os
# Specify Server Address
serverName = 'localhost'
serverPort = 8000

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# TEST CASE 1
# Testing HTTP 200 Response

sentence = 'GET /test.html HTTP/1.1\r\n\r\n'

# TEST CASE 2
# Testing HTTP 304 Not Modified

# lastModified = time.ctime(os.path.getmtime('test.html'))
# sentence = 'GET /test.html HTTP/1.1\r\nif-Modified-Since: '
# sentence = sentence + lastModified + '\r\n'


# TEST CASE 3
# Testing HTTP 400 Bad Request

# sentence = 'GETT /test.html HTTP/1.1\r\n\r\n'

# TEST CASE 4
# Testing HTTP 404 Not Found

# sentence = 'GET /NotReal.html HTTP/1.1\r\n\r\n'

# TEST CASE 5
# Testing HTTP 408 Request Timed Out

# sentence = 'GET /test.html HTTP/1.1\r\n\r\n'
# time.sleep(3)

clientSocket.send(sentence.encode())

# Read reply characters! No need to read address! Why?
modifiedSentence = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', modifiedSentence.decode())

# Close the socket
clientSocket.close()
