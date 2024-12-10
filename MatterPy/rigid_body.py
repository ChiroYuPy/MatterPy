import math

from .AABB import AABB
from .particle import Particle
from .vector2 import Vector2


class RigidBody(Particle):
    def __init__(self, x, y, mass=1, angle=0, friction=0, restitution=1, static=False):
        super().__init__(x, y, mass, static)

        self.angular_velocity = 0
        self.angle = angle

        self.inertia = self.calculate_inertia()
        self.friction = friction
        self.restitution = restitution

        self.AABB = None

    def calculate_inertia(self):
        raise NotImplementedError("This method must be implemented in subclass")

    def get_AABB(self):
        raise NotImplementedError("This method must be implemented in subclass")

    def step(self, dt: float):
        super().step(dt)
        self.AABB = self.get_AABB()
        self.angle += self.angular_velocity * dt


class CircleRigidBody(RigidBody):
    def __init__(self, x, y, radius, mass=1, angle=0, friction=0, restitution=1, static=False):
        self.radius = radius
        super().__init__(x, y, mass, angle, friction, restitution, static)

    def calculate_inertia(self):
        return 0.5 * self.mass * self.radius ** 2

    def get_AABB(self):

        min_x = self.position.x - self.radius
        min_y = self.position.y - self.radius
        max_x = self.position.x + self.radius
        max_y = self.position.y + self.radius

        self.AABB = AABB(min_x, min_y, max_x, max_y)

        return self.AABB


class PolygonRigidBody(RigidBody):
    def __init__(self, x, y, vertices, mass=1, angle=0, friction=0, restitution=1, static=False):
        super().__init__(x, y, mass, angle, friction, restitution, static)
        self._default_vertices = vertices
        self.vertices = self._default_vertices

    def _get_transformed_vertices(self):
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)

        self.transformed_vertices = [self.transform(vector, self.x, self.y, sin, cos) for vector in self._default_vertices]

        return self.transformed_vertices

    def step(self, dt: float):
        super().step(dt)
        self.vertices = self._get_transformed_vertices()

    @staticmethod
    def transform(vector, center_x, center_y, sin, cos):
        x = cos * vector.x - sin * vector.y + center_x
        y = sin * vector.x + cos * vector.y + center_y
        return Vector2(x, y)

    def get_AABB(self):
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for v in self.vertices:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)

        self.AABB = AABB(min_x, min_y, max_x, max_y)

        return self.AABB


class BoxRigidBody(PolygonRigidBody):
    def __init__(self, x, y, width, height, mass=1, angle=0, friction=0, restitution=1, static=False):
        self.width = width
        self.height = height
        super().__init__(x=x, y=y, vertices=self._get_default_vertices(width, height), mass=mass, angle=angle, friction=friction, restitution=restitution, static=static)

    @staticmethod
    def _get_default_vertices(width, height):
        vertices = [Vector2(-width / 2, height / 2),
                    Vector2(width / 2, height / 2),
                    Vector2(width / 2, -height / 2),
                    Vector2(-width / 2, -height / 2)]
        return vertices

    def calculate_inertia(self):
        return (1 / 12) * self.mass * (self.width ** 2 + self.height ** 2)


class RegularPolygonRigidBody(PolygonRigidBody):
    def __init__(self, x, y, num_points, size, mass=1, angle=0, friction=0, restitution=1, static=False):
        super().__init__(x=x, y=y, vertices=self._get_default_vertices(num_points, size), mass=mass, angle=angle, friction=friction, restitution=restitution, static=static)

    def _get_default_vertices(self, num_points, size):
        base_vector = Vector2(1, 0)
        angle = math.radians(360/num_points)
        vertices = [self.transform(base_vector, 0, 0, int(math.sin(angle*i)*size), int(math.cos(angle*i)*size)) for i in range(num_points)]
        return vertices

    def calculate_inertia(self):
        return 0