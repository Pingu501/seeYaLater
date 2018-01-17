from http.server import BaseHTTPRequestHandler, HTTPServer


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("got get request")
        if self.path == '/api/all':
            self.__responseWithJson('get all')
        else:
            self.__printDefaultPage('default page')

    def __printDefaultPage(self, content: str):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'you opened {}'.format(content)
        self.wfile.write(bytes(message, "utf8"))
        return

    def __responseWithJson(self, json):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(bytes(json, "utf8"))
        return


def start():
    print("starting web server")
    server_address = ('127.0.0.1', 8081)
    try:
        httpd = HTTPServer(server_address, WebRequestHandler)
        httpd.serve_forever()
    except:
        print("could not connect to port!")
