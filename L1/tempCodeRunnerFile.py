
img_host = re.findall(r'//(.*?)/files/', img_url, re.S)[0]
img_path = re.findall(r'.md(.*)', img_url, re.S)[-1]
img_data = 'GET {} HTTP/1.1\r\nHOST:{}\r\nReferer:{}\r\n\r\n'.format(
    img_path, img_host, target_host)
img_res = con(img_host, img_data)
img_content = re.findall(b'\r\n\r\n(.*)', img_res, re.S)[0]
file_name = str(img_name) + " Imagine" + ".jpg"
with open(file_name, 'wb') as f:
    f.write(img_content)
img_name += 1