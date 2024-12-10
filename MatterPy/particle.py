from .vector2 import Vector2

class Particle:
    def __init__(self, x, y, mass=1, static=False):
        self.mass = mass
        self.inv_mass = 1 / mass if mass > 0 else float('inf')
        self._position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.static = static

    def step(self, dt: float):
        if self.static:
            self.velocity *= 0
            self.force *= 0
            return

        if self.mass > 0:
            acceleration = self.force / self.mass
            self.velocity += acceleration * dt
        self._position += self.velocity * dt
        self.force *= 0

    @property
    def position(self):
        return self._position

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @position.setter
    def position(self, value):
        self._position = value

    @x.setter
    def x(self, value):
        self._position.x = value

    @y.setter
    def y(self, value):
        self._position.y = value