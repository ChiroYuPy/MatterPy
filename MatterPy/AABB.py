from .vector2 import Vector2


class AABB:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min = Vector2(min_x, min_y)
        self.max = Vector2(max_x, max_y)