from triangulation import Coordinates


class Triangulator:
    def __init__(self):
        pass

    def locatable_clients(self, data):
        clients = {}
        for client in data:
            if len(data[client]) == 3:
                clients[client] = data[client]
        return clients

    def locate_client(self, client):
        # client: {location1: (locationCoord, power)}
        locations = client.values()
        location1 = locations[0][0]
        location2 = locations[1][0]
        location3 = locations[2][0]
        d1 = self.distance(location1, location2)
        # d2 = self.distance(location2, location3)
        # d3 = self.distance(location3, location1)
        r1 = self.power_to_meters(locations[0][1])
        r2 = self.power_to_meters(locations[1][1])
        r3 = self.power_to_meters(locations[2][1])
        #if (r1 + r2 >= d1 and r2 + r3 >= d2 and r3 + r1 >= d3):
        x = (r1 ** 2 - r2 ** 2 + d1**2) / (2 * d1)
        y = ((r1 ** 2 - r3 ** 2 + location3.x ** 2 + location3.y ** 2) /
            (2 * location3.y) - location3.x / location3.y * x)
        return Coordinates(x, y)
        # else:
        #     return self.locate_client({
        #         str(location1): (location1, 1.1*locations[0][1]),
        #         str(location2): (location2, 1.1*locations[1][1]),
        #         str(location3): (location3, 1.1*locations[2][1])
        #     })

    def distance(self, coord1, coord2):
        return ((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2) ** 0.5

    def power_to_meters(self, power):
        return 9*power
