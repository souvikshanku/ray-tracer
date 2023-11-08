import numpy as np


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return str((self.x, self.y, self.z))

    def __array__(self):
        return np.array([self.x, self.y, self.z])

    def __mul__(self, other):
        return np.array(self) * np.array(other)

    def __rmul__(self, other):
        return self.__mul__(other)
