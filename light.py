import numpy as np


class Light:
    def __init__(self, type, intensity, position=None, direction=None):
        self.type = type
        self.intensity = intensity
        self.position = np.array(position)
        self.direction = np.array(direction)


def length(vector):
    return np.sqrt(sum(vector**2))


def compute_intensity(point, normal, lights, specular):
    intensity = 0

    for light in lights:
        if light.type == "ambient":
            intensity += light.intensity
        else:
            if light.type == "point":
                light_vec = light.position - point
            else:
                light_vec = light.direction

            # Diffused reflection
            nl = np.dot(normal, light_vec)
            if nl > 0:
                intensity += light.intensity * nl / (length(normal) * length(light_vec))

            # Specular reflection
            if specular:
                v = - point  # Vector from point to camera
                r = 2 * normal * np.dot(normal, light_vec) - light_vec  # Reflected light Vector
                rv = np.dot(r, v)
                if rv > 0:
                    intensity += light.intensity * np.power(rv / (length(r) * length(v)), specular)

    return intensity
