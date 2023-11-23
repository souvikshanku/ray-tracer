import numpy as np


class Light:
    def __init__(self, type, intensity, position=None, direction=None):
        self.type = type
        self.intensity = intensity
        self.position = position
        self.direction = direction


def length(vector):
    return np.sqrt(sum(vector**2))


def compute_lighting(point, normal, scene):
    intensity = 0

    for light in scene.lights:
        if light.type == "ambient":
            intensity += light.intensity
        else:
            if light.type == "point":
                light_vec = light.position - point
            else:
                light_vec = light.direction

            nl = normal * light_vec
            if nl > 0:
                intensity += light.intensity * nl / (length(normal) * length(light_vec))
