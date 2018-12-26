from miner.execution.stop_initializer import StopInitializer


class Conductor:

    @staticmethod
    def prepare():
        initializer = StopInitializer()

        # first we need to fetch all lines from the stops we already know
        print('Fetching all lines ...')
        initializer.fetch_lines_from_initial_stops()

        # then we search for all stops the found line serves
        print('Fetching all stops from lines ...')
        initializer.fetch_stops_from_lines()

        # get the coordinates of the stops
        print('Fetching coordinates of stops ...')
        initializer.fetch_stop_coordinates()

    @staticmethod
    def start():
        pass
