from triangulation import Coordinates
import math


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
        # client: { locationN: (Coordinates, power) }
        locations = client.values()
        locations = (locations[0], locations[1], locations[2])

        origin = None
        axis_point = None
        third_point = None
        for location in locations:
            coordinates = location[0]
            if coordinates.x == 0 and coordinates.y == 0:
                origin = location
            elif coordinates.y == 0:
                axis_point = location
            else:
                third_point = location

        distance = self.distance(origin[0], axis_point[0])

        r1 = self.power_to_meters(origin[1])
        r2 = self.power_to_meters(axis_point[1])
        r3 = self.power_to_meters(third_point[1])

        x = (r1 ** 2 - r2 ** 2 + distance**2) / (2 * distance)
        y = ((r1 ** 2 - r3 ** 2 + third_point[0].x ** 2 + third_point[0].y ** 2) /
            (2 * third_point[0].y) - third_point[0].x / third_point[0].y * x)

        return Coordinates(x, y)

    def distance(self, point1, point2):
        diff_x = point1.x - point2.x
        diff_y = point1.y - point2.y
        return math.sqrt(diff_x ** 2 + diff_y ** 2)

    def power_to_meters(self, power):
        return 9 * power
