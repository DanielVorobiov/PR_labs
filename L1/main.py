import socket
import re
link = "http://mib.utm.md/"
target_host = "www.me.utm.md"
target_port = 80


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


request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
res = con(target_host, request)
img_urs = re.findall(
    r'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|jpe?g))["\']', res.decode(), re.S)
img_name = 1


for img_url in img_urs:

    if link not in img_url:
        img_url = link + img_url
    print(img_url)

    img_host = re.findall(r'//(.*?)/', img_url, re.S)[0]
    img_path = re.findall(r'.md(.*)', img_url, re.S)[-1]
    img_data = 'GET {} HTTP/1.1\r\nHOST:{}\r\nReferer:{}\r\n\r\n'.format(
        img_path, img_host, target_host)
    img_res = con(img_host, img_data)
    img_content = re.findall(b'\r\n\r\n(.*)', img_res, re.S)[0]
    file_name = str(img_name) + " Imagine" + ".jpg"
    with open(file_name, 'wb') as f:
        f.write(img_content)
    img_name += 1
