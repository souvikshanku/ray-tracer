import numpy as np


class Sphere:
    def __init__(self, centre, radius, color, specular=None):
        self.centre = np.array(centre)
        self.radius = radius
        self.color = np.array(color)
        self.specular = specular


def get_intersection_w_sphere(origin, pixel_pos, sphere):
    r = sphere.radius
    ray_vector = origin - sphere.centre

    a = (pixel_pos * pixel_pos).sum()
    b = 2 * np.dot(ray_vector,  pixel_pos)
    c = np.dot(ray_vector, ray_vector) - r * r

    discriminant = (b * b - 4 * a * c)

    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    return t1, t2
