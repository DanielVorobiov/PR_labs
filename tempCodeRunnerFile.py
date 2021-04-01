import socket
import re
import ssl
from threading import *
img_name = 1
checklist = []
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
target_port = 80
linker = input("Doresti sa introduci linkul de concatenare pentru imagini?: 1 - Da\n 2 - Nu\n\t\t\t")
if (linker == 1):
    link = input("Introdu link de concatenare pentru fotografii(Ex:http://mib.utm.md/)\n\t\t\t")
else:
    print("Linkul a fost setat default pentru laborator: 'http://mib.utm.md/'\n Processing...\n")
    link = "http://mib.utm.md/"
target_host = input("Introdu site-ul:(Ex:'www.me.utm.md')\n\t\t\t")


def con(host, request):
    client = socket.socket()
    client.connect((host, target_port))
    client.sendall(request.encode())
    res = b''
    data = client.recv(1024)
    while data:
        res += data
        data = client.recv(1024)

    return res


def conhttps(host, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    s_sock = context.wrap_socket(s, server_hostname=host)
    s_sock.connect((host, target_port))
    s_sock.sendall(request.encode())
    res = b''
    data = s_sock.recv(1024)
    while data:
        try:
            data = s_sock.recv(1024)
            res += data
        except socket.timeout:
            break
    return res


def devider(l, n):
    med = len(l) / float(n)
    listek = []
    last = 0.0
    while last < len(l):
        listek.append(l[int(last):int(last + med)])
        last += med
    return (listek)


def http(t_id):
    print("Protocol: HTTP ", "Host: ", target_host, "Port: ", target_port)
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
    res = con(target_host, request)
    img_urs = re.findall(r'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', res.decode(), re.S)
    pricol = []
    for img_url in img_urs:
        pricol.append(img_url)
    pricol = list(devider(pricol, 4))
    for img_url in pricol[t_id-1]:
        if link not in img_url:
            img_url = link + img_url
        print(img_url)
        img_host = re.findall(r'//(.*?)/', img_url, re.S)[0]
        img_path = re.findall(r'.md(.*)', img_url, re.S)[-1]
        img_data = 'GET {} HTTP/1.1\r\nHOST:{}\r\nReferer:{}\r\n\r\n'.format(img_path, img_host, target_host)
        img_res = con(img_host, img_data)
        img_content = re.findall(b'\r\n\r\n(.*)', img_res, re.S)[0]
        file_name = str(t_id) + " HTTPImagine" + ".jpg"
        with open(file_name, 'wb') as f:
            f.write(img_content)
        t_id+=4
        



def https():
    target_host = input("Introdu site-ul:(Ex: 'utm.md')\n\t\t\t")

    splitter = target_host.split(".")
    dot = "." + splitter[1]
    print("Protocol: HTTPS ", "Host: ", target_host, "Port: ", target_port)
    request = "GET / HTTP/1.1\r\nHost: %s\r\nConnection: Keep-Alive\r\n\r\n" % target_host

    res = conhttps(target_host, request)
    img_urs = re.findall(r'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', res.decode(), re.S)
    img_name = 1
    for img_url in img_urs:
        print(img_url)
        img_host = re.findall(r'//(.*?)/', img_url, re.S)[0]
        img_path = re.findall(r'{}(.*)'.format(dot), img_url, re.S)[-1]
        if (img_url in checklist):
            continue
        else:
            checklist.append(img_url)
        img_data = 'GET {} HTTP/1.1\r\nHOST:{}\r\nReferer:{}\r\n\r\n'.format(img_path, img_host, target_host)
        img_res = conhttps(img_host, img_data)
        file_name = str(img_name) + " ImagineHTTPS" + ".jpg"
        with open(file_name, 'wb') as f:
            f.write(img_res)
        img_name += 1


def menu():
    selectare = input("Alege protocolul:\n1 - HTTP\n2 - HTTPS\n3 - EXIT\n\t\t\t")
    if (selectare == "1" or selectare == "HTTP" or selectare == "http"):
        t1 = Thread(target=http, args=(1,))
        t2 = Thread(target=http, args=(2,))
        t3 = Thread(target=http, args=(3,))
        t4 = Thread(target=http, args=(4,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()

    elif (selectare == "2" or selectare == "HTTPS" or selectare == "https"):
        https()

    else:
        print("Ati introdus ceva gresit sau ati finalizat programul.")
        exit()


menu()


