class DataPoint:
    def __init__(self, location, station, client, power):
        self.location = location
        self.station = station
        self.client = client
        self.power = power

    def __str__(self):
        return '{0} reports: {1} {2} {3}'.format(
            self.location,
            self.station,
            self.client,
            self.power
        )
