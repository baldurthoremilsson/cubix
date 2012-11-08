from math import * 

class Vector:
    def __init__(self, v):
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]

    def dot(self, vec):
        return (self.x*vec.x + self.y*vec.y + self.z*vec.z)

    def cross(self, vec):
        return Vector([self.y*vec.z - self.z*vec.y, 
                       self.z*vec.x - self.x*vec.z, 
                       self.x*vec.y - self.y*vec.x])


    def __add__(self, vec):
        return Vector([self.x+vec.x, self.y+vec.y, self.z+vec.z])

    def __sub__(self, vec):
        return Vector([self.x-vec.x, self.y-vec.y, self.z-vec.z])

    "multiply vector with a scalar"
    def __mul__(self, scalar):
        return Vector([self.x*scalar, self.y*scalar, self.z*scalar])

    "divide vector with a scalar"
    def __div__(self, scalar):
        return Vector([self.x/scalar, self.y/scalar, self.z/scalar])

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        len = self.length()
        self = Vector([i / len for i in self.array()])
        return self

    def __str__(self):
        return str((self.x, self.y, self.z))

    def array(self):
        return [self.x, self.y, self.z]


	


	
