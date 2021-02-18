import socket
import re
import ssl
from threading import *

sem = Semaphore(2)
link = "https://utm.md/"
host = "utm.md"
port = 443


def connections(host, message):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    s_sock = context.wrap_socket(s, server_hostname=host)
    s_sock.connect((host, port))
    s_sock.sendall(message.encode())
    print("Connection made")
    res = b''
    data = s_sock.recv(1024)
    while data:
        try:
            data = s_sock.recv(1024)
            res += data
        except socket.timeout:
            break
    return res


def decode(images):
    decoded_images = []
    for image in images:
        image = image.decode()
        if link in image:
            image = image.split(link)[1]
        decoded_images.append(image)
        print("Images decoded")
    return decoded_images


def devider(l, n):
    avg = len(l) / float(n)
    out = []
    last = 0.0

    while last < len(l):
        out.append(l[int(last):int(last + avg)])
        last += avg

    return out


def download(decoded_images, img_id):
    for decoded_image in decoded_images:
        message = 'GET {} HTTP/1.1\r\nHost: utm.md\r\n\r\n'.format(
            "/" + decoded_image)
        response = connections(host, message)
        with open('utm/'+str(img_id) + '.jpg', 'wb') as f:
            f.write(response)
        print("Image downloaded")
        img_id += 4


def main(t_id):
    sem.acquire()
    initial_message = "GET / HTTP/1.1\r\nHost:utm.md\r\n\r\n"
    initial_response = connections(host, initial_message)
    images = re.findall(
        b'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', initial_response, re.S)
    decoded_images = decode(images)
    decoded_images = list(devider(decoded_images, 4))

    download(decoded_images[t_id-1], t_id)
    sem.release()


t1 = Thread(target=main, args=(1,))
t2 = Thread(target=main, args=(2,))
t3 = Thread(target=main, args=(3,))
t4 = Thread(target=main, args=(4,))

t1.start()
t2.start()
t3.start()
t4.start()
