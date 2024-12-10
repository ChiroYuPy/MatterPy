import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): # Vecteur * Vecteur
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other): # Vecteur - Vecteur
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float): # Vecteur * Scalaire
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, scalar: float) -> 'Vector2':
        return self.__mul__(scalar)

    def __truediv__(self, other: float): # Vecteur / Scalaire
        return Vector2(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: 'Vector2') -> float:
        return self.x * other.y - self.y * other.x

    def rotate(self, angle):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        return Vector2(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta
        )

    def distance(self, other: 'Vector2') -> float:
        return (self - other).length()

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"