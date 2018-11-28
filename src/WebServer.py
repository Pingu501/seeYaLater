import re
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer
from src import DataProvider

logger = logging.getLogger()


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        departure_pattern = re.compile('([\/]?api\/departures[\/]?)(\d*)')
        departure_match = departure_pattern.match(self.path)

        if self.path == '/api':
            self.__printRoutes__()
        elif self.path == '/api/status':
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

    def __printRoutes__(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = '<h1>API</h1>'
        message += '/api - this page <br/>'
        message += '/api/status - current system status <br/>'
        message += '/api/departures - all fetched departures <br/>'
        message += '/api/departures/STATION_ID - all fetched departures by station <br/>'

        self.wfile.write(bytes(message, "utf8"))

    def __printDefaultPage(self):
        self.send_response(404)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = '<h1>path not found</h1> go to <a href="/api">/api</a> for a list of all routes'
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
    logger.log(logging.INFO, 'starting web server at 127.0.0.1:8081')
    try:
        httpd = HTTPServer(server_address, WebRequestHandler)
        httpd.serve_forever()
    except:
        print("could not connect to port!")
