import math

from .constraint import SpringConstraint
from .particle import Particle
from .rigid_body import CircleRigidBody, BoxRigidBody


class Composite:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.objects = []


class CircleComposite(Composite):
    def __init__(self, x, y, width, height, size, mass=1):
        super().__init__(x, y, width, height)
        local_mass = mass/(width*height)
        for r in range(height):
            col = []
            for c in range(width):
                body = CircleRigidBody(
                    x=x + (width / 2 - (c + 0.5)) * size,
                    y=y + (height / 2 - (r + 0.5)) * size,
                    radius=size / 2, mass=local_mass)
                col.append(body)
                self.objects.append(body)


class BoxComposite(Composite):
    def __init__(self, x, y, width, height, size, mass=1):
        super().__init__(x, y, width, height)
        local_mass = mass / (width * height)
        for r in range(height):
            col = []
            for c in range(width):
                body = BoxRigidBody(
                    x=x + (width / 2 - (c + 0.5)) * size,
                    y=y + (height / 2 - (r + 0.5)) * size,
                    width=size, height=size, mass=local_mass)
                col.append(body)
                self.objects.append(body)


class SoftBody(Composite):
    def __init__(self, x, y, width, height, length, stiffness, damping=1, max_force=0, mass=1):
        super().__init__(x, y, width, height)

        point_mass = mass / (width * height)

        points = []
        for r in range(height):
            col = []
            for c in range(width):
                if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                    body = CircleRigidBody(
                        x=x + (width / 2 - (c + 0.5)) * length,
                        y=y + (height / 2 - (r + 0.5)) * length,
                        radius=length / 4, mass=point_mass)
                else:
                    body = Particle(
                        x=x + (width / 2 - (c + 0.5)) * length,
                        y=y + (height / 2 - (r + 0.5)) * length,
                        mass=point_mass)
                self.objects.append(body)
                col.append(body)
            points.append(col)

        for row in range(height):
            for col in range(width):
                if col < width - 1:
                    spring = SpringConstraint(points[row][col], points[row][col + 1],
                                              length=length, stiffness=stiffness, damping=damping, max_force=max_force)
                    self.objects.append(spring)
                if row < height - 1:
                    spring = SpringConstraint(points[row][col], points[row + 1][col],
                                              length=length, stiffness=stiffness, damping=damping, max_force=max_force)
                    self.objects.append(spring)
                if col < width - 1 and row < height - 1:
                    spring = SpringConstraint(points[row][col], points[row + 1][col + 1],
                                              length=length * math.sqrt(2), stiffness=stiffness, damping=damping, max_force=max_force)
                    self.objects.append(spring)
                if col > 0 and row < height - 1:
                    spring = SpringConstraint(points[row][col], points[row + 1][col - 1],
                                              length=length * math.sqrt(2), stiffness=stiffness, damping=damping, max_force=max_force)
                    self.objects.append(spring)

        print(self.objects)


