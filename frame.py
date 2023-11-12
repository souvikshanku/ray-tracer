import numpy as np

from vector import Vector


class Sphere:
    def __init__(self, centre, radius, color):
        self.centre = Vector(centre)
        self.radius = radius
        self.color = color


class Canvas:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.frame = np.zeros(shape=(height, width, 3))

    def canvas_to_viewport(self, x, y):
        width = 1
        height = 1
        distance = 1
        return Vector([x * width / self.width, y * height / self.height, distance])

    def render(self):
        origin = Vector([0, 0, 0])

        for x in range(- self.width // 2, self.width // 2):
            for y in range(- self.height // 2, self.height // 2):
                pixel_pos = self.canvas_to_viewport(x, y)
                color = trace_ray(origin, pixel_pos, t_min=1, t_max=np.inf)
                self.frame[x + self.width // 2, y + self.height // 2] = color

        return self.frame


def trace_ray(start, pixel_pos, t_min, t_max):
    BACKGROUND_COLOR = [1, 1, 1]
    closest_t = np.inf
    closest_sphere = None
    scene = [
        Sphere([0, -1, 3], 1, [1, 0, 0]),
        Sphere([2, 0, 4], 1, [0, 1, 0])
    ]

    for sphere in scene:
        t1, t2 = get_intersection(start, pixel_pos, sphere)

        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere is None:
        return BACKGROUND_COLOR

    return closest_sphere.color


def get_intersection(start, pixel_pos, sphere):
    r = sphere.radius
    c_o_vector = start - sphere.centre

    a = pixel_pos * pixel_pos
    b = 2 * c_o_vector * pixel_pos
    c = c_o_vector * c_o_vector - r * r

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    return t1, t2
