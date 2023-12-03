import matplotlib.pyplot as plt
import numpy as np

from light import Light, compute_intensity
from sphere import Sphere, get_closest_intersection


BACKGROUND_COLOR = [1, 1, 1]


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

    def add_sphere(self, centre, radius, color, specular):
        self.scene.append(Sphere(centre, radius, color, specular))

    def add_light(self, type, intensity, position=None, direction=None):
        self.lights.append(Light(type, intensity, position, direction))

    def canvas_to_viewport(self, x, y):
        vx = x * self.viewport_width / self.width
        vy = y * self.viewport_height / self.height
        vz = self.viewport_distance

        return np.array([vx, vy, vz])

    def trace_ray(self, origin, pixel_coord, t_min, t_max):
        scene = self.scene
        lights = self.lights

        closest_sphere, closest_t = get_closest_intersection(
            scene, origin, pixel_coord, t_min, t_max
        )

        if closest_sphere is None:
            return BACKGROUND_COLOR

        if not lights:
            return closest_sphere.color

        point_on_sphere = origin + closest_t * pixel_coord  # from the eqn, P = O + t(V - O)
        normal = point_on_sphere - closest_sphere.centre
        normal /= np.sqrt(sum(normal ** 2))

        intensity = compute_intensity(
            scene=scene,
            point=pixel_coord,
            normal=normal,
            lights=lights,
            specular=closest_sphere.specular
        )

        return closest_sphere.color * intensity

    def render(self):
        origin = np.array([0, 0, 0])

        for x in range(- self.width // 2, self.width // 2):
            for y in range(- self.height // 2, self.height // 2):
                pixel_coord = self.canvas_to_viewport(x, y)
                color = self.trace_ray(
                    origin=origin,
                    pixel_coord=pixel_coord,
                    t_min=self.viewport_distance,
                    t_max=np.inf
                )
                self.frame[x + self.width // 2, y + self.height // 2] = color

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.imshow(np.clip(np.rot90(self.frame), 0, 1))
        plt.show()


if __name__ == "__main__":
    canvas = Canvas(height=200, width=200)
    canvas.add_sphere(centre=[0, -1, 3], radius=1, color=[1, 0, 0], specular=500)
    canvas.add_sphere(centre=[2, 0, 4], radius=1, color=[0, 1, 0], specular=500)
    canvas.add_sphere(centre=[-2, 0, 4], radius=1, color=[0, 0, 1], specular=10)
    canvas.add_sphere(centre=[0, -5001, 0], radius=5000, color=[1, 1, 0], specular=1000)

    canvas.add_light(type="ambient", intensity=0.2)
    canvas.add_light(type="point", intensity=0.6, position=(2, 1, 0))
    canvas.add_light(type="directinal", intensity=0.2, direction=(1, 4, 4))

    canvas.render()
