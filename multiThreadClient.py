# Include Python's Socket Library
from socket import *
import time
import os
# Specify Server Address
serverName = 'localhost'
serverPort = 8000

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket2 = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))
clientSocket2.connect((serverName,serverPort))

# T1: Testing HTTP 200 Response / T2: HTTP 404 Not Found

sentence = 'GET /test.html HTTP/1.1\r\n\r\n'
sentence2 = 'GET /NotReal.html HTTP/1.1\r\n\r\n'

# T1: Testing HTTP 304 Not Modified / T2: Testing HTTP 400 Bad Request

# lastModified = time.ctime(os.path.getmtime('test.html'))
# sentence = 'GET /test.html HTTP/1.1\r\nif-Modified-Since: '
# sentence = sentence + lastModified + '\r\n'
# sentence2 = 'GETT /test.html HTTP/1.1\r\n\r\n'

# Testing HTTP 408 Request Timed Out
# sentence = 'GET /test.html HTTP/1.1\r\n\r\n'
# sentence2 = 'GET /test.html HTTP/1.1\r\n\r\n'
# time.sleep(3)

clientSocket.send(sentence.encode())
clientSocket2.send(sentence2.encode())

# Read reply characters! No need to read address! Why?
modifiedSentence = clientSocket.recv(1024)
modifiedSentence2 = clientSocket2.recv(1024)

# Print out the received string
print ('From Server:', modifiedSentence.decode())
print ('From Server:', modifiedSentence2.decode())

# Close the socket
clientSocket.close()
clientSocket2.close()
