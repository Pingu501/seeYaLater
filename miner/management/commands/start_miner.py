from django.core.management.base import BaseCommand

from miner.execution.conductor import Conductor


class Command(BaseCommand):
    help = 'start the miner thread'

    def handle(self, *args, **options):
        conductor = Conductor()
        conductor.prepare()
        conductor.start()
