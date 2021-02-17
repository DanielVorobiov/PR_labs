import socket
import re
from threading import *
import time

link = "http://mib.utm.md/"
host = "me.utm.md"
port = 80


def connection(host, message):
    s = socket.socket()
    s.connect((host, 80))
    s.send(message.encode())
    print("Connection made")
    response = b''
    data = s.recv(1024)

    while data:
        response += data
        data = s.recv(1024)
    print("Data recieved")
    return response


def decode(images):
    decoded_images = []
    for image in images:
        image = image.decode()
        if link in image:
            image = image.split(link)[1]
        decoded_images.append(image)
    return decoded_images


def download(decoded_images, img_id):

    for decoded_image in decoded_images:
        message = 'GET {} HTTP/1.1\r\nHost: me.utm.md\r\n\r\n'.format(
            "/" + decoded_image)
        response = connection(host, message)
        img_content = re.findall(b'\r\n\r\n(.*)', response, re.S)[0]
        with open(str(img_id) + '.jpg', 'wb') as f:
            f.write(img_content)
        img_id += 4


def devider(l, n):
    avg = len(l) / float(n)
    out = []
    last = 0.0

    while last < len(l):
        out.append(l[int(last):int(last + avg)])
        last += avg

    return out


def main(t_id):
    initial_message = 'GET / HTTP/1.1/\r\nHost: me.utm.md \r\n\r\n'
    initial_response = connection(host, initial_message)

    images = re.findall(
        b'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', initial_response, re.S)
    decoded_images = decode(images)
    decoded_images = list(devider(decoded_images, 4))
    print(decoded_images)
    download(decoded_images[t_id-1], t_id)


t1 = Thread(target=main, args=(1,))
t2 = Thread(target=main, args=(2,))
t3 = Thread(target=main, args=(3,))
t4 = Thread(target=main, args=(4,))

t1.start()
t2.start()
t3.start()
t4.start()
