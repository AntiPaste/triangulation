class Coordinates:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return '{0}:{1}'.format(self.x, self.y)
