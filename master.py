from triangulation import Connection
from socket import gethostbyname, gethostname
import threading
import logging


class Master:
    service_address = None
    service_port = 6969

    def __init__(self, queue):
        self.queue = queue

        # Get our IP address
        # Careful with multiple interfaces!
        self.service_address = gethostbyname(gethostname())
        self.connection = Connection(self.service_address, self.service_port)

        # Start up an announcer thread
        self.thread(self.announce)

        # Start up a receiving thread
        self.thread(self.receive)

        # Start up a processing thread
        self.thread(self.process)

    def thread(self, function, args=()):
        thread = threading.Thread(target=function, args=args)
        thread.start()

    def announce(self):
        self.connection.announce()

    def receive(self):
        self.connection.receive(self.queue)

    def process(self):
        logging.info('Ready for processing')

        while True:
            data = self.queue.get()
            # Do something interesting with the data!
            print(data)
