import matplotlib.pyplot as plt
import numpy as np

from sphere import Sphere, get_intersection_w_sphere


BACKGROUND_COLOR = [1, 1, 1]


def trace_ray(scene, origin, pixel_pos, t_min, t_max):
    closest_t = np.inf
    closest_sphere = None

    for sphere in scene:
        t1, t2 = get_intersection_w_sphere(origin, pixel_pos, sphere)

        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere is None:
        return BACKGROUND_COLOR

    return closest_sphere.color


class Canvas:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        # FOV ~ 53 degree
        self.viewport_width = 1
        self.viewport_height = 1
        self.viewport_distance = 1

        self.scene = []
        self.lights = []
        self.frame = np.zeros(shape=(height, width, 3))

    def add_sphere(self, centre, radius, color):
        self.scene.append(Sphere(centre, radius, color))

    def canvas_to_viewport(self, x, y):
        vx = x * self.viewport_width / self.width
        vy = y * self.viewport_height / self.height
        vz = self.viewport_distance

        return np.array([vx, vy, vz])

    def render(self):
        origin = np.array([0, 0, 0])

        for x in range(- self.width // 2, self.width // 2):
            for y in range(- self.height // 2, self.height // 2):
                pixel_pos = self.canvas_to_viewport(x, y)
                color = trace_ray(
                    scene=self.scene,
                    origin=origin,
                    pixel_pos=pixel_pos,
                    t_min=self.viewport_distance,
                    t_max=np.inf
                )
                self.frame[x + self.width // 2, y + self.height // 2] = color

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.imshow(np.rot90(self.frame))
        plt.show()


if __name__ == "__main__":
    canvas = Canvas(height=200, width=200)
    canvas.add_sphere(centre=[0, -1, 3], radius=1, color=[1, 0, 0])
    canvas.add_sphere(centre=[2, 0, 4], radius=1, color=[0, 1, 0])
    canvas.add_sphere(centre=[-2, 0, 4], radius=1, color=[0, 0, 1])
    canvas.render()
