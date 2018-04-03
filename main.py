from threading import Thread

from src import TaskRunner, StopFetcher, WebServer, SqlWorker

sql_worker = SqlWorker.SqlWorker()
sql_worker.start()

StopFetcher.initStops()

minerThread = Thread(target=TaskRunner.run, args=[sql_worker])
minerThread.start()

webServerThread = Thread(target=WebServer.start)
webServerThread.start()
