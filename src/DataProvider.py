from src import SqlHelper

sqlHelper = SqlHelper('seeYaLater.db')


def getAllDepartures():
    result = sqlHelper.execute('SELECT * FROM departure')
    print(result)

