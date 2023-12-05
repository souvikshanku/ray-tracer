import numpy as np

from ray_tracer.sphere import get_closest_intersection


class Light:
    def __init__(self, type, intensity, position=None, direction=None):
        self.type = type
        self.intensity = intensity
        self.position = np.array(position)
        self.direction = np.array(direction)


def length(vector):
    return np.sqrt(sum(vector**2))


def compute_intensity(scene, point_on_sphere, normal, lights, specular):
    intensity = 0

    for light in lights:
        if light.type == "ambient":
            intensity += light.intensity
        else:
            if light.type == "point":
                light_vec = light.position - point_on_sphere
                t_max = 1
            else:
                light_vec = light.direction
                t_max = np.inf

            # Shadow Check
            shadow_sphere, _ = get_closest_intersection(
                scene=scene,
                origin=point_on_sphere,
                pixel_coord=light_vec,
                t_min=0.0001,
                t_max=t_max
            )

            if shadow_sphere is not None:
                continue

            # Diffused reflection
            nl = np.dot(normal, light_vec)
            if nl > 0:
                intensity += light.intensity * nl / (length(normal) * length(light_vec))

            # Specular reflection
            if specular:
                v = - point_on_sphere  # Vector from point to camera
                r = 2 * normal * np.dot(normal, light_vec) - light_vec  # Reflected light Vector
                rv = np.dot(r, v)
                if rv > 0:
                    intensity += light.intensity * np.power(rv / (length(r) * length(v)), specular)

    return intensity
