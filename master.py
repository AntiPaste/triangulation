from triangulation import Connection
from triangulation import Triangulator
from socket import gethostbyname, gethostname
import threading
import logging


class Master:
    service_address = None
    service_port = 6969
    data = dict()
    triangulator = Triangulator()

    def __init__(self, queue):
        self.queue = queue

        # Get our IP address
        # Careful with multiple interfaces!
        self.service_address = gethostbyname(gethostname())
        self.connection = Connection(self.service_address, self.service_port)

    def start(self):
        # Start up an announcer thread
        announcer = self.thread(self.announce)

        # Start up a receiving thread
        receiver = self.thread(self.receive)

        # Start up a processing thread
        processer = self.thread(self.process)

        # Wait up
        announcer.join()
        receiver.join()
        processer.join()

    def thread(self, function, args=()):
        thread = threading.Thread(target=function, args=args)
        thread.start()
        return thread

    def announce(self):
        self.connection.announce()

    def receive(self):
        self.connection.receive(self.queue)

    def process(self):
        logging.info('Ready for processing')

        while True:
            datapoint = self.queue.get()
            if datapoint.client not in self.data:
                self.data[datapoint.client] = {}

            key = str(datapoint.location)
            self.data[datapoint.client][key] = (
                datapoint.location,
                datapoint.power
            )

            clients = self.triangulator.locatable_clients(self.data)
            for key, client in clients.iteritems():
                coordinates = self.triangulator.locate_client(client)
                print('Client: {0}, location: {1}'.format(
                    datapoint.client,
                    str(coordinates)
                ))
