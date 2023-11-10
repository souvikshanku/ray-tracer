import numpy as np

from vector import Vector


class Sphere:
    def __init__(self, centre, radius) -> None:
        self.centre = centre
        self.radius = radius


class Frame:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.frame = np.zeros(shape=(height, width, 3))

    def canvas_to_viewport(self, x, y):
        canvas_w = 100
        canvas_h = 100
        distance = 1
        return x * self.width / canvas_w, y * self.height / canvas_h, distance

    def render(self):
        origin = Vector(0, 0, 0)

        for x in range(- self.width, self.width + 1):
            for y in range(- self.height, self.height + 1):
                coordinate = self.canvas_to_viewport(x, y)
                color = trace_ray(origin, coordinate, t_min=1, t_max=np.inf)
                self.frame[x, y] = color


def trace_ray(start, coordinate, t_min, t_max):
    BACKGROUND_COLOR = [0, 0, 0]
    closest_t = np.inf
    closest_sphere = None
    scene = None

    for sphere in scene:
        t1, t2 = get_intersection(start, coordinate, sphere)

        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

        if closest_sphere is None:
            return BACKGROUND_COLOR

        return closest_sphere.color


def get_intersection(start, D, sphere):
    r = sphere.radius
    c_o_vector = start - sphere.center

    a = Vector(D) * Vector(D)
    b = 2 * Vector(c_o_vector) * Vector(D)
    c = Vector(c_o_vector) * Vector(c_o_vector) - r * r

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    return t1, t2
