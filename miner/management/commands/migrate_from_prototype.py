import logging
import os.path
import sqlite3

from django.core.management.base import BaseCommand

from miner.execution.conductor import Conductor
from miner.models import Stop

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'migrate database from prototype'

    def handle(self, *args, **options):
        if not os.path.isfile('seeYaLater.db'):
            logger.info('No old database found')
            return

        logger.info('start migration ...')

        old_entries = self.__fetch_results__()

        number_of_entries = len(old_entries)
        done = 0

        for entry in old_entries:
            stop = Stop.objects.get_or_create(id=entry[5])[0]
            try:
                Conductor.create_departure_from_json(departure_json={
                    'LineName': entry[1],
                    'Direction': entry[2],
                    'Id': entry[0],
                    'RealTime': entry[3],
                    'ScheduledTime': entry[4]
                }, stop=stop)
            except Exception as e:
                logger.critical('failed to migrate {}'.format(entry), e)
            done += 1

            # self.__delete_entry__(entry[0], entry[1], stop.id)
            if done % 10000 == 0:
                logger.info('{}% finished'.format((done / number_of_entries) * 100))

    @staticmethod
    def __fetch_results__():
        connection = sqlite3.connect('seeYaLater.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM departure')
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result

    @staticmethod
    def __delete_entry__(departure_id: int, line: str, stop_id: int):
        connection = sqlite3.connect('seeYaLater.db')
        cursor = connection.cursor()

        cursor.execute(
            'DELETE FROM departure WHERE id={} AND line="{}" AND station={}'.format(departure_id, line, stop_id))
        connection.commit()
        connection.close()
