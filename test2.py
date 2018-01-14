import numpy as np

fullAngle = 2 * np.pi

class line():
    def __init__(self, somePoint = None, directionPoint = None):
        if somePoint and directionPoint:
            self.somePoint = somePoint
            self.direction = directionPoint / abs(directionPoint)
            self.angle = np.imag(np.log(directionPoint))
    def __str__(self):
        return "Line somePoint = {} angle = {}".format(self.somePoint, self.angle / fullAngle)

#print fullAngle

l = line(2 + 1j, 1 + 1j)

print l


