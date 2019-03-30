from django.core.management.base import BaseCommand

from miner.execution.conductor import Conductor


class Command(BaseCommand):
    help = 'transfer all too old departures in the tmp table into the real table'

    def handle(self, *args, **options):
        conductor = Conductor()
        conductor.__transfer_tmp_departures__()
