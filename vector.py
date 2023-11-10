import numpy as np


class Vector:
    def __init__(self, v):
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]

    def __repr__(self):
        return str((self.x, self.y, self.z))

    def __array__(self):
        return np.array([self.x, self.y, self.z])

    def __add__(self, other):
        return Vector(np.array(self) + np.array(other))

    def __sub__(self, other):
        return Vector(np.array(self) - np.array(other))

    def __mul__(self, other):
        return Vector(np.array(self) * np.array(other))

    def __rmul__(self, other):
        return self.__mul__(other)
