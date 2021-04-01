import socketserver
import http.server
import urllib.request

PORT = 9097


class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path[0] == "/":
            url = self.path[1:]
        else:
            url = self.path
        self.send_response(200)
        self.end_headers()
        self.copyfile(urllib.request.urlopen(url), self.wfile)


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.ForkingTCPServer(('', PORT), MyProxy)
print("Now serving at " + str(PORT))
httpd.serve_forever()