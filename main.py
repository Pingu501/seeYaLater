from threading import Thread

import sys

from src import TaskRunner, StopFetcher
from src import WebServer

StopFetcher.initStops()

minerThread = Thread(target=TaskRunner.run)
minerThread.start()

webServerThread = Thread(target=WebServer.start)
webServerThread.start()
