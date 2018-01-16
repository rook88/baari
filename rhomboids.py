import numpy as np
import cv2

fullAngle = 2 * np.pi
rightAngle = 0.5 * np.pi
origin = 0 + 0j

class line():
    def __init__(self, somePoint = None, directionPoint = None):
        if somePoint <> None and directionPoint <> None:
            self.somePoint = somePoint
            self.direction = directionPoint / abs(directionPoint)
            self.angle = np.imag(np.log(directionPoint))
    def getNormal(self):
        return self.direction / np.exp(rightAngle * 1j)
    def __str__(self):
        return "Line somePoint = {} angle = {} direction = {}".format(self.somePoint, self.angle / fullAngle, self.direction)

#print fullAngle

lines = []
lines.append(line(0 + 0j, 0 + 1j))
lines.append(line(1 + 0j, 0 + 1j))
lines.append(line(0 + 1j, 1 + 0.5j))
lines.append(line(0 + 1.2j, 1 + 0.5j))
lines.append(line(0 + 0j, 1 + 0j))
lines.append(line(0.5 + 0j, 1 + 4j))

#lines.append(line(1 + 1j, -2 + 1j))
#lines.append(line(2 + 1j, -2 - 1j))

lines = []
number = 9
for i in range(number):
    angle = fullAngle * 1.0j * i / number
    lines.append(line(np.exp(angle), np.exp(rightAngle * 1j + angle)))
    lines.append(line(np.exp(angle) * 0.1, np.exp(rightAngle * 1j + angle)))
    lines.append(line(np.exp(angle) * -2, np.exp(rightAngle * 1j + angle)))


lines = []
number = 25
theta1 = (np.sqrt(5) - 1) / 2 * fullAngle
theta2 = 0.25 * fullAngle
angle = 0
for i in range(number):
    angle += theta1 * 1j
    lines.append(line(np.exp(angle) * (1 + 0.00001 * i), np.exp(rightAngle * 1j + angle)))
for i in range(number * 2):
    angle += theta2 * 1j
    lines.append(line(np.exp(angle) * (1 + 0.00001 * i), np.exp(rightAngle * 1j + angle)))
    
def z2xy(z):
    return (np.real(z), np.imag(z))

def intersection(l1, l2):
    (x1, y1) = z2xy(l1.somePoint)
    (x2, y2) = z2xy(l1.somePoint + l1.direction)
    (x3, y3) = z2xy(l2.somePoint)
    (x4, y4) = z2xy(l2.somePoint + l2.direction)
    if ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) == 0:
        return None
    else:
        return ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)) / ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) + ((x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)) / ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) * 1j

def position(l, x):
    if np.imag((x - l.somePoint) / l.direction) >= 0:
        return 0
    else:
        return 1

for l in lines:
    print l
    print position(l, origin)
    print position(l, 3)

def genRhomboidFaceKeys(lines):
    ret = {}
    previousIntersections = []
    for i1 in range(len(lines)):
        for i2 in range(i1 + 1, len(lines)):
            p = intersection(lines[i1], lines[i2])
            if p <> None:
                if p in previousIntersections:
                    raise Error("multiple lines intersect at same point")
                retKey = ""
                for i3 in range(len(lines)):
                    if i3 == i1:
                        retKey += "a"
                    elif i3 == i2:
                        retKey += "b"
                    else:
                        retKey += str(position(lines[i3], p))
                ret[retKey] = (i1, i2, p)
    return ret

def getRhomboidVertices(key, lines):
    (ret1, ret2, ret3, ret4) = (0, 0, 0, 0)
    for i in range(len(lines)):
        position = key[i]
        if position == 'a':
#            ret1 -= lines[i].getNormal()
            ret2 += lines[i].getNormal()
#            ret3 -= lines[i].getNormal()
            ret4 += lines[i].getNormal()
        if position == 'b':
#            ret1 -= lines[i].getNormal()
#            ret2 -= lines[i].getNormal()            
            ret3 += lines[i].getNormal()
            ret4 += lines[i].getNormal()
        if position == '1':
            ret1 += lines[i].getNormal()
            ret2 += lines[i].getNormal()
            ret3 += lines[i].getNormal()
            ret4 += lines[i].getNormal()            
#        if position == '0':
#            ret1 -= lines[i].getNormal()
#            ret2 -= lines[i].getNormal()
#            ret3 -= lines[i].getNormal()
#            ret4 -= lines[i].getNormal()            
    return (ret1, ret2, ret3, ret4)


height = 1000
width = 1000
length = 25

def z2imgPoint(z):
    return (width / 2 + int(np.real(z * length)), height / 2 - int(np.imag(z * length)))

img =  np.zeros((height,width,3), np.uint8)


faceKeys = genRhomboidFaceKeys(lines)

print "------------------------------------------------------------"
for key in faceKeys:
    (v1, v2, v3, v4) = getRhomboidVertices(key, lines)
    print key, faceKeys[key], z2imgPoint(v1), z2imgPoint(v2), z2imgPoint(v3), z2imgPoint(v4)
    cv2.line(img = img, pt1 = z2imgPoint(v1), pt2 = z2imgPoint(v2), color = (255, 255, 255))
    cv2.line(img = img, pt1 = z2imgPoint(v1), pt2 = z2imgPoint(v3), color = (255, 255, 255))
    cv2.line(img = img, pt1 = z2imgPoint(v4), pt2 = z2imgPoint(v2), color = (255, 255, 255))
    cv2.line(img = img, pt1 = z2imgPoint(v4), pt2 = z2imgPoint(v3), color = (255, 255, 255))

cv2.imshow('image',img)
cv2.imwrite('test.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
