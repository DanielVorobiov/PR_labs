import socket
import json

HOST = '127.0.0.1'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data is None:
        continue
    else:
        data = data.decode('utf-8')
        data = json.loads(data)
        print(data)
