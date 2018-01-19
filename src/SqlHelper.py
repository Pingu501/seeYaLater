import sqlite3

__createdOnce = False


def __createConnection():
    connection = sqlite3.connect('seeYaLater.db')
    __prepareDatabase(connection)
    return connection


def __prepareDatabase(connection):
    if __createdOnce:
        return

    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS departure (
            id INT NOT NULL PRIMARY KEY,
            line VARCHAR(4),
            direction VARCHAR(42),
            realTime DATETIME,
            scheduledTime DATETIME,
            station INT
            )
        """)


def execute(sql_command: str):
    connection = __createConnection()

    cursor = connection.cursor()
    cursor.execute(sql_command)
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result


def __arrayToString(array):
    queryString = "("
    isFirst = True
    for entry in array:
        prefix = "" if isFirst else ", "
        queryString += prefix + entry
        isFirst = False
    queryString += ")"
    return queryString


def __dictToString(key_value_pairs: dict):
    string = ""
    for key, value in key_value_pairs.items():
        string += key + " = " + value
    return string


def create(table_name, keys, values):
    queryString = "INSERT INTO {}".format(table_name)
    queryString += __arrayToString(keys)
    queryString += "VALUES "
    queryString += __arrayToString(values)
    return execute(queryString)


def update(table_name, keys_and_values, where):
    queryString = "UPDATE {} SET ".format(table_name)
    queryString += __dictToString(keys_and_values)
    queryString += "WHERE {}".format(where)
    return execute(queryString)
