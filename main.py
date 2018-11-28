import logging
from threading import Thread

import sys

from src import TaskRunner, StopFetcher, WebServer, SqlWorker

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s %(message)s')

sql_worker = SqlWorker.SqlWorker()
sql_worker.start()

StopFetcher.initStops()

minerThread = Thread(target=TaskRunner.run, args=[sql_worker])
minerThread.start()

webServerThread = Thread(target=WebServer.start, args=[sql_worker])
webServerThread.start()
