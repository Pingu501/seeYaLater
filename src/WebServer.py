from http.server import BaseHTTPRequestHandler, HTTPServer
from src import DataProvider, Logger


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/api/all':
            self.__responseWithJson()
        else:
            self.__printDefaultPage('default page')

    def __printDefaultPage(self, content: str):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'you opened {}'.format(content)
        self.wfile.write(bytes(message, "utf8"))
        return

    def __responseWithJson(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(bytes(DataProvider.getAllDepartures(), "utf8"))
        return


def start():
    server_address = ('127.0.0.1', 8081)
    Logger.createLogEntry('test')
    Logger.createLogEntry('starting web server at 127.0.0.1:8081')
    try:
        httpd = HTTPServer(server_address, WebRequestHandler)
        httpd.serve_forever()
    except:
        print("could not connect to port!")
