import socket
import re

link = "http://mib.utm.md/"
host = "me.utm.md"
port = 80
img_id = 1


def connection(host, message):
    s = socket.socket()
    s.connect((host, 80))
    s.send(message.encode())
    response = b''
    data = s.recv(1024)

    while data:
        response += data
        data = s.recv(1024)
    return response


initial_message = 'GET / HTTP/1.1/\r\nHost: me.utm.md \r\n\r\n'
initial_response = connection(host, initial_message)


images = re.findall(
    b'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', initial_response, re.S)

for image in images:
    image = image.decode()
    if link in image:
        image = image.split(link)[1]

    message = 'GET {} HTTP/1.1\r\nHost: me.utm.md\r\n\r\n'.format("/" + image)

    response = connection(host, message)
    img_content = re.findall(b'\r\n\r\n(.*)', response, re.S)[0]
    with open(str(img_id) + '.jpg', 'wb') as f:
        f.write(img_content)
    img_id += 1
