from triangulation import Connection
from triangulation import Coordinates
from triangulation import Master
from triangulation import Slave
from multiprocessing import Queue
from distutils import spawn
import subprocess
import argparse
import logging
import os
import sys

logging.basicConfig(level=20)
path = os.path.dirname(__file__)

parser = argparse.ArgumentParser()
parser.add_argument(
    '--no-aircrack',
    help='force no aircrack',
    dest='disable_aircrack',
    action='store_true'
)

parser.add_argument(
    '--interface',
    help='WLAN monitor interface'
)

parser.add_argument(
    '--bssid',
    help='filter by this bssid'
)

parser.add_argument(
    '--channel',
    help='filter by this channel'
)

parser.add_argument(
    '--location',
    help='location of this instance separated by comma, e.g. 1,2'
)

parser.add_argument(
    '--connection',
    help='master address and port, e.g. localhost:1000'
)

type_group = parser.add_mutually_exclusive_group(required=True)
type_group.add_argument(
    '--master',
    help='start application as master',
    dest='master',
    action='store_true'
)

type_group.add_argument(
    '--slave',
    help='start application as slave',
    dest='master',
    action='store_false'
)

parser.set_defaults(disable_aircrack=False)
args = parser.parse_args()

# Check if aircrack is installed
aircrack_installed = spawn.find_executable('airodump-ng') is not None
if aircrack_installed and not args.disable_aircrack:
    if not args.interface:
        raise RuntimeError('Missing interface flag for aircrack')

    # Open up a handle to the process
    arguments = ['airodump-ng', args.interface]

    if args.bssid:
        arguments += ['--bssid', args.bssid]

    if args.channel:
        arguments += ['--channel', args.channel]

    airodump = subprocess.Popen(arguments, stderr=subprocess.PIPE)

    # Read it boy, read it
    source = airodump.stderr
else:
    # If we have no aircrack or were forced to, use sample data
    source = open(os.path.join(path, 'data.txt'), 'r')

data_queue = Queue()

if args.master:
    logging.info('Starting application as master...')
    app = Master(data_queue)
else:
    logging.info('Starting application as slave...')

    coordinates = args.location.split(',')
    location = Coordinates(int(coordinates[0]), int(coordinates[1]))

    master = None
    if args.connection:
        master_input = args.connection.split(':')
        master = Connection(master_input[0], int(master_input[1]))

    app = Slave(data_queue, location, source, master)

    while True:
        data = app.scan()
        if data is None:
            logging.info('Out of data, exiting...')
            break

        app.send(data)
