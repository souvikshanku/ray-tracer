import matplotlib.pyplot as plt
import numpy as np

from ray_tracer.light import Light, compute_intensity
from ray_tracer.sphere import Sphere, get_closest_intersection


BACKGROUND_COLOR = np.array([0, 0, 0])


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

    def add_sphere(self, centre, radius, color, specular, reflective):
        self.scene.append(Sphere(centre, radius, color, specular, reflective))

    def add_light(self, type, intensity, position=None, direction=None):
        self.lights.append(Light(type, intensity, position, direction))

    def canvas_to_viewport(self, x, y):
        vx = x * self.viewport_width / self.width
        vy = y * self.viewport_height / self.height
        vz = self.viewport_distance

        return np.array([vx, vy, vz])

    def trace_ray(self, start, end, t_min, t_max, recursion_depth=4):
        scene = self.scene
        lights = self.lights

        closest_sphere, closest_t = get_closest_intersection(scene, start, end, t_min, t_max)

        if closest_sphere is None:
            return BACKGROUND_COLOR

        if not lights:
            return closest_sphere.color

        point_on_sphere = start + closest_t * end  # from the eqn, P = O + t(V - O)
        normal = point_on_sphere - closest_sphere.centre
        normal /= np.sqrt(sum(normal ** 2))

        intensity = compute_intensity(
            scene=scene,
            point_on_sphere=point_on_sphere,
            normal=normal,
            lights=lights,
            specular=closest_sphere.specular
        )

        local_color = closest_sphere.color * intensity

        r = closest_sphere.reflective
        if recursion_depth <= 0 or r <= 0:
            return local_color

        # Same as `Reflected light Vector` from ./light.py
        reflected_ray = 2 * normal * np.dot(normal, - end) - end
        reflected_color = self.trace_ray(
            start=point_on_sphere,
            end=reflected_ray,
            t_min=0.001,
            t_max=np.inf,
            recursion_depth=recursion_depth - 1
        )

        return local_color * (1 - r) + reflected_color * r

    def render(self):
        origin = np.array([0, 0, 0])  # The camera position

        for x in range(- self.width // 2, self.width // 2):
            for y in range(- self.height // 2, self.height // 2):
                pixel_coord = self.canvas_to_viewport(x, y)
                color = self.trace_ray(
                    start=origin,
                    end=pixel_coord,
                    t_min=self.viewport_distance,
                    t_max=np.inf
                )
                self.frame[x + self.width // 2, y + self.height // 2] = color

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.imshow(np.clip(np.rot90(self.frame), 0, 1))
        fig.savefig('scene.png', bbox_inches='tight', pad_inches=0)
        plt.show()
