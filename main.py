from threading import Thread

from src import TaskRunner
from src import WebServer


minerThread = Thread(target=TaskRunner.run)
minerThread.start()

webServerThread = Thread(target=WebServer.start)
webServerThread.start()
