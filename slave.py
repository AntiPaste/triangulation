from triangulation import Connection
from triangulation import DataPoint
import re
import logging


class Slave:
    def __init__(self, queue, location, source, master=None):
        self.queue = queue
        self.location = location
        self.source = source

        self.master = master
        if self.master is None:
            connection = Connection()
            logging.info(
                'No master connection details provided, ' +
                'attempting discovery...'
            )

            self.master = connection.discover()
            if self.master is None:
                raise RuntimeError('Failed to discover a master')

    def scan(self):
        # Block until we get something useful
        while True:
            output = self.source.readline()
            if output == '':
                # Poll returns None while program is still running
                # but we might not have a poll method

                poll = getattr(self.source, 'poll', None)
                if callable(poll) and poll() is None:
                    continue

                return None

            if not output:
                continue

            if type(output) == bytes:
                output = output.decode('utf-8')

            stripped = output.strip()

            # Remove escape sequences
            ansi_escape = re.compile(r'\x1b[^m]*m')
            stripped = ansi_escape.sub('', stripped)

            # Capture interesting data
            data = re.findall(
                r'^(?P<station>[0-9A-F:]+)[ ]+'
                '(?P<client>[0-9A-F:]+)[ ]+'
                '-(?P<power>[0-9]+)',
                stripped
            )

            if not data:
                continue

            data = data[0]
            if not data:
                continue

            return DataPoint(self.location, data[0], data[1], data[2])

    def send(self, datapoint):
        self.master.send(datapoint)
