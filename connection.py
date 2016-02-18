from triangulation import DataPoint
from triangulation import Coordinates
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
import time
import logging


class Connection:
    data_magic = 'da7a1337'
    discovery_magic = '1337b33f'
    discovery_address = '255.255.255.255'
    discovery_port = 50505

    def __init__(self, address=None, port=None):
        self.address = address
        self.port = port

    def send(self, datapoint):
        # Create an UDP socket
        sock = socket(AF_INET, SOCK_DGRAM)
        data = "\x00".join((
            self.data_magic,
            str(datapoint.location.x),
            str(datapoint.location.y),
            datapoint.station,
            datapoint.client,
            datapoint.power
        )).encode('utf-8')  # convert string to bytes

        # And away she goes!
        logging.debug('Sending data: {0}'.format(datapoint))
        sock.sendto(data, (self.address, self.port))

    def receive(self, queue):
        sock = socket(AF_INET, SOCK_DGRAM)

        # Bind the socket to all addresses on a certain port
        sock.bind(('', self.port))

        logging.info('Listening on {0}'.format(self))
        while True:
            body, source_address = sock.recvfrom(4096)
            body = body.decode('utf-8')

            logging.debug('Received {0} bytes from {1}'.format(
                len(body),
                source_address[0]
            ))

            if not body.startswith(self.data_magic):
                logging.warning('Received invalid data from {0}: {1}'.format(
                    source_address[0],
                    repr(body)
                ))

                continue

            data = body.split("\x00")
            coordinates = Coordinates(data[1], data[2])
            datapoint = DataPoint(coordinates, data[3], data[4], data[5])
            logging.debug('Received data point: {0}'.format(datapoint))

            queue.put(datapoint)

    def announce(self):
        # Create an UDP socket
        sock = socket(AF_INET, SOCK_DGRAM)

        # Bind it to all addresses on all ports
        sock.bind(('', 0))

        # This is a broadcast socket
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        while True:
            data = "{0}\x00{1}\x00{2}\x00".format(
                self.discovery_magic,
                self.address,
                self.port
            ).encode('utf-8')  # convert string to bytes

            sock.sendto(data, (self.discovery_address, self.discovery_port))
            logging.debug('Service announcement broadcasted')
            time.sleep(5)

    def discover(self):
        # Create an UDP socket
        sock = socket(AF_INET, SOCK_DGRAM)

        # Listen on all addresses on the specified port
        sock.bind(('', self.discovery_port))

        logging.info('Starting discovery on port {0}...'.format(
            self.discovery_port
        ))

        while True:
            # Wait for a packet
            body, source_address = sock.recvfrom(1024)
            body = body.decode('utf-8')

            if body.startswith(self.discovery_magic):
                data = body.split("\x00")
                address = data[1]
                port = int(data[2])

                if address != source_address[0]:
                    logging.warning((
                        'Mismatch between received address ({0}) and ' +
                        'source address ({1})! Continuing with {0}...'
                    ).format(
                        address,
                        source_address[0]
                    ))

                connection = Connection(address, port)
                logging.info('Discovered master @ {0}'.format(connection))

                return connection

    def __str__(self):
        return '{0}:{1}'.format(self.address, self.port)
