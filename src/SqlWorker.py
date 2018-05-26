import sqlite3
import threading
import time

from src.Helper import Logger


def makeString(arg):
    return "'" + str(arg) + "'"


class SqlWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.q = []
        self.connection = None

    def __prepareDatabase__(self):
        self.execute("""
                    CREATE TABLE IF NOT EXISTS departure (
                    id INT NOT NULL,
                    line VARCHAR(4),
                    direction VARCHAR(42),
                    realTime DATETIME,
                    scheduledTime DATETIME,
                    station INT
                    )
                """)

    def onThread(self, function_to_call, args):
        job = SqlJob(function_to_call, args)
        self.q.append(job)
        return_value = job.fetchResult()
        return return_value

    def run(self):
        self.__prepareDatabase__()

        while True:
            for job in self.q:
                function_to_call, arguments = job.getFunctionAndParameters()
                return_value = function_to_call(*arguments)
                job.updateStatus(return_value)
                self.q.remove(job)

            Logger.verbose('SQL Worker has {} queue entries'.format(len(self.q)))
            if len(self.q) == 0:
                time.sleep(1)

    def createOrUpdate(self, departure):
        """
        :param departure: Departure
        :return: void
        """
        result = self.execute(
            "SELECT COUNT(id) FROM departure WHERE id = '{}' and station = {}".format(departure.id, departure.stop_id))

        if result[0][0] == 0:
            self.create("departure", ["id", "line", "direction", "realTime", "scheduledTime", "station"],
                        [departure.id, makeString(departure.line), makeString(departure.direction),
                         makeString(departure.realTime),
                         makeString(departure.scheduledTime),
                         makeString(departure.stop_id)])
        else:
            self.update("departure", {'scheduledTime': makeString(departure.scheduledTime)},
                        'id = {} and station = {}'.format(departure.id, departure.stop_id))

    def create(self, table_name, keys, values):
        queryString = "INSERT INTO {}".format(table_name)
        queryString += self.__arrayToString(keys)
        queryString += "VALUES "
        queryString += self.__arrayToString(values)
        return self.execute(queryString)

    def select(self, entity_name, parameters, where_statements, order_by=None, order=None, limit=None):
        """
        :param entity_name: the table name to perform
        :param parameters: to fetch
        :param where_statements: Array of Array containing parameter, operator and value
        :param order_by: property to sort by
        :param order: str ASC|DESC
        :param limit: max number of results
        :return: query result
        """

        queryString = 'SELECT ' + parameters + ' FROM ' + entity_name

        count = 0
        for where_statement in where_statements:
            queryString += ' WHERE ' if count == 0 else ' AND '
            queryString += ' '.join(where_statement)
            count += 1

        if order_by is not None and order is not None:
            queryString += ' ORDER BY ' + order_by + ' ' + order

        if limit is not None:
            queryString += ' LIMIT ' + limit

        return self.execute(queryString)

    def count(self, property_to_count):
        queryString = "SELECT COUNT(id) FROM " + property_to_count
        return self.execute(queryString)[0][0]

    def update(self, table_name, keys_and_values, where):
        queryString = "UPDATE {} SET ".format(table_name)
        queryString += self.__dictToString(keys_and_values)
        queryString += "WHERE {}".format(where)
        return self.execute(queryString)

    @staticmethod
    def execute(query):
        connection = sqlite3.connect('seeYaLater.db')
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except sqlite3.IntegrityError as e:
            print(query)
            print(e)
        except Exception as e:
            print(query)
            print(e)

        result = cursor.fetchall()

        connection.commit()
        connection.close()

        return result

    @staticmethod
    def __dictToString(key_value_pairs: dict):
        string = ""
        for key, value in key_value_pairs.items():
            string += key + " = " + value
        return string

    @staticmethod
    def __arrayToString(array):
        queryString = "("
        isFirst = True
        for entry in array:
            prefix = "" if isFirst else ", "
            queryString += prefix + entry
            isFirst = False
        queryString += ")"
        return queryString


class SqlJob:
    def __init__(self, function_to_call, args):
        self.function_to_call = function_to_call
        self.args = args
        self.executed = False
        self.return_value = None

    def getFunctionAndParameters(self):
        return self.function_to_call, self.args

    def updateStatus(self, return_value):
        self.executed = True
        self.return_value = return_value

    def finished(self):
        return self.executed

    def fetchResult(self):
        while True:
            if self.executed:
                return self.return_value
            else:
                time.sleep(0.01)
