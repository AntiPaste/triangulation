from distutils import spawn
import subprocess
import re
import sys

escape_chars = ['[2J', '[?25l', '[2J', '[J', chr(27), '[0m', '[1', ';1H']
aircrack_installed = spawn.find_executable('airodump-ng') is not None
if aircrack_installed:
    airodump = subprocess.Popen(
        [
            'airodump-ng', 'wlan1mon',
            '--bssid', 'D8:84:66:42:BC:58',
            '--channel', '13'
        ],
        stderr=subprocess.PIPE
    )

    source = airodump.stderr
else:
    source = open('data.txt', 'r')

while True:
    output = source.readline()
    if output == '' and aircrack_installed and airodump.poll() is not None:
        break

    if output:
        stripped = output.strip()
        for char in escape_chars:
            stripped = stripped.replace(char, '')

        if (
            not stripped or
            stripped.startswith('BSSID') or
            stripped.startswith('CH 13') or
            stripped.endswith('TaitoUnited')
        ):
            continue

        data = re.findall(
            r'^(?P<station>[0-9A-F:]+)[ ]+'
            '(?P<client>[0-9A-F:]+)[ ]'
            '+-(?P<power>[0-9]+)',
            stripped
        )

        if not data:
            print(stripped)

        print(data)
