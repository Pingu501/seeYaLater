from miner.execution.stop_initializer import StopInitializer


class Conductor:

    @staticmethod
    def prepare():
        initializer = StopInitializer()

        # first we need to fetch all lines from the stops we already know
        initializer.fetch_lines_from_initial_stops()

        # then we search for all stops the found line serves
        initializer.fetch_stops_from_lines()

    @staticmethod
    def start():
        pass

