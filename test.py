import subprocess
import re

airodump = subprocess.Popen(
    [
        'airodump-ng', 'wlan1mon',
        '--bssid', 'D8:84:66:42:BC:58',
        '--channel', '13'
    ],
    #stdin=subprocess.PIPE,
    #stdout=subprocess.PIPE
    stderr=subprocess.PIPE
)

#o_airodump, unused_stderr = airodump.communicate()
data = ''
escape_chars = ['[2J', '[?25l', '[2J', '[J', chr(27), '[0m', '[1;1H']

while True:
    output = airodump.stderr.readline()
    if output == '' and airodump.poll() is not None:
        break
    if output:
        stripped = output.strip()
        print(stripped)
        #for char in escape_chars:
        #    stripped = stripped.replace(char, '')
        #if not stripped or stripped.startswith('BSSID') or stripped.startswith('CH 13') or stripped.endswith('TaitoUnited'):
        #    continue

        #print(re.findall(r'^(?P<station>[0-9A-F:]+)[ ]+(?P<client>[0-9A-F:]+)[ ]+-(?P<power>[0-9]+)', stripped)[0])
    rc = airodump.poll()

print(data)
# airodump.kill()

