import re

from http.server import BaseHTTPRequestHandler, HTTPServer
from src import DataProvider, Logger


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        departure_pattern = re.compile('([\/]?api\/departures[\/]?)(\d*)')
        departure_match = departure_pattern.match(self.path)

        if self.path == '/api/status':
            self.__responseWithJson(DataProvider.getCurrentStatus())
        elif departure_match:
            stationId = departure_match.group(2)

            if stationId == '':
                response = DataProvider.getAllDepartures()
            else:
                response = DataProvider.getAllDeparturesByStation(stationId)

            self.__responseWithJson(response)
        else:
            self.__printDefaultPage()

    def __printDefaultPage(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'you opened {}'.format('default page')
        self.wfile.write(bytes(message, "utf8"))
        return

    def __responseWithJson(self, response):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(bytes(response, "utf8"))
        return


def start():
    server_address = ('127.0.0.1', 8081)
    Logger.createLogEntry('starting web server at 127.0.0.1:8081')
    try:
        httpd = HTTPServer(server_address, WebRequestHandler)
        httpd.serve_forever()
    except:
        print("could not connect to port!")
