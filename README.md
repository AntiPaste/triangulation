# triangulation

## Start up
On the master node, run the application once as a master and once as a slave.  
On the slave node, run the application once as a slave.

## Running

### Master
```plaintext
$ python -m triangulation --master
```

### Slave
```plaintext
# Basic configuration
$ python -m triangulation --slave --interface wlan0mon --bssid D8:84:66:42:BC:58 --channel 13 --location 1,2

# Without aircrack-ng
$ python -m triangulation --slave --no-aircrack --location 1,2

# With a local master
$ python -m triangulation --slave --no-aircrack --connection localhost:6969 --location 1,2
```
