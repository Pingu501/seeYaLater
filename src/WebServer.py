import re
import logging
import os

from http.server import BaseHTTPRequestHandler, HTTPServer

from src.DataProvider import DataProvider

logger = logging.getLogger()
data_provider = None


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        departure_pattern = re.compile('([\/]?api\/departures[\/]?)(\d*)')
        departure_match = departure_pattern.match(self.path)

        if self.path == '/api':
            self.__printRoutes__()
        elif self.path == '/api/status':
            self.__responseWithJson(data_provider.getCurrentStatus())
        elif departure_match:
            stationId = departure_match.group(2)

            if stationId == '':
                response = data_provider.getAllDepartures()
            else:
                response = data_provider.getAllDeparturesByStation(stationId)

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


def start(sql_worker):
    global data_provider
    data_provider = DataProvider(sql_worker)

    port = os.environ["PORT"] if "PORT" in os.environ else 8081
    server_address = ('127.0.0.1', port)
    logger.info('starting web server at 127.0.0.1:{}'.format(port))
    try:
        httpd = HTTPServer(server_address, WebRequestHandler)
        httpd.serve_forever()
    except:
        logger.error("could not connect to port!")
