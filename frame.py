import numpy as np

from vector import Vector


class Frame:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.frame = np.zeros(shape=(height, width, 3))

    def render(self):
        origin = Vector(0, 0, 0)

        for x in range(- self.width, self.width + 1):
            for y in range(- self.height, self.height + 1):
                coordinate = self.canvas_to_viewport(x, y)
                color = trace_ray(origin, coordinate, 1, np.inf)
                self.frame[x, y] = color

    def canvas_to_viewport(self, x, y):
        canvas_w = 100
        canvas_h = 100
        distance = 1

        return x * self.width / canvas_w, y * self.height / canvas_h, distance


def trace_ray(start, d, end, inf):
    BACKGROUND_COLOR = (0, 0, 0)
    closest_t = np.inf
    closest_sphere = None
    scene = None
    t_min = 0
    t_max = 0

    for sphere in scene:
        t1, t2 = get_intersection(start, d, sphere)

        if t1 in [t_min, t_max] and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t2 in [t_min, t_max] and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

        if closest_sphere == None:
            return BACKGROUND_COLOR

        return closest_sphere.color


def get_intersection(start, D, sphere):
    r = sphere.radius
    CO = start - sphere.center

    a = Vector(D) * Vector(D)
    b = 2 * Vector(CO) * Vector(D)
    c = Vector(CO) * Vector(CO) - r * r

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    return t1, t2
