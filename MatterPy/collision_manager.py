from .rigid_body import CircleRigidBody, PolygonRigidBody
from .vector2 import Vector2


class CollisionManager:

    @staticmethod
    def is_collide(body_a, body_b):
        normal = Vector2(0, 0)
        depth = 0.0

        if isinstance(body_a, PolygonRigidBody):
            if isinstance(body_b, PolygonRigidBody):
                return CollisionManager.intersect_polygons(
                    body_a.position, body_a.vertices,
                    body_b.position, body_b.vertices)
            elif isinstance(body_b, CircleRigidBody):
                result, normal, depth = CollisionManager.intersect_circle_polygon(
                    body_b.position, body_b.radius,
                    body_a.position, body_a.vertices)
                normal = -normal
                return result, normal, depth
        elif isinstance(body_a, CircleRigidBody):
            if isinstance(body_b, PolygonRigidBody):
                return CollisionManager.intersect_circle_polygon(
                    body_a.position, body_a.radius,
                    body_b.position, body_b.vertices)
            elif isinstance(body_b, CircleRigidBody):
                return CollisionManager.intersect_circles(
                    body_a.position, body_a.radius,
                    body_b.position, body_b.radius)

        return False, normal, depth

    @staticmethod
    def intersect_circle_polygon(circle_center, circle_radius, polygon_center, vertices):
        normal = Vector2(0, 0)
        depth = float('inf')

        for i in range(len(vertices)):
            va = vertices[i]
            vb = vertices[(i + 1) % len(vertices)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis = Vector2.normalize(axis)

            min_a, max_a = CollisionManager.project_vertices(vertices, axis)
            min_b, max_b = CollisionManager.project_circle(circle_center, circle_radius, axis)

            if min_a >= max_b or min_b >= max_a:
                return False, normal, depth

            axis_depth = min(max_b - min_a, max_a - min_b)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        cp_index = CollisionManager.find_closest_point_on_polygon(circle_center, vertices)
        cp = vertices[cp_index]

        axis = cp - circle_center
        axis = Vector2.normalize(axis)

        min_a, max_a = CollisionManager.project_vertices(vertices, axis)
        min_b, max_b = CollisionManager.project_circle(circle_center, circle_radius, axis)

        if min_a >= max_b or min_b >= max_a:
            return False, normal, depth

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

        direction = polygon_center - circle_center

        if Vector2.dot(direction, normal) < 0:
            normal = -normal

        return True, normal, depth

    @staticmethod
    def find_closest_point_on_polygon(circle_center, vertices):
        result = -1
        min_distance = float('inf')

        for i in range(len(vertices)):
            v = vertices[i]
            distance = Vector2.distance(v, circle_center)

            if distance < min_distance:
                min_distance = distance
                result = i

        return result

    @staticmethod
    def project_circle(center, radius, axis):
        direction = Vector2.normalize(axis)
        direction_and_radius = direction * radius

        p1 = center + direction_and_radius
        p2 = center - direction_and_radius

        min_proj = Vector2.dot(p1, axis)
        max_proj = Vector2.dot(p2, axis)

        if min_proj > max_proj:
            min_proj, max_proj = max_proj, min_proj

        return min_proj, max_proj

    @staticmethod
    def intersect_polygons(center_a, vertices_a, center_b, vertices_b):
        normal = Vector2(0, 0)
        depth = float('inf')

        for i in range(len(vertices_a)):
            va = vertices_a[i]
            vb = vertices_a[(i + 1) % len(vertices_a)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis = Vector2.normalize(axis)

            min_a, max_a = CollisionManager.project_vertices(vertices_a, axis)
            min_b, max_b = CollisionManager.project_vertices(vertices_b, axis)

            if min_a >= max_b or min_b >= max_a:
                return False, normal, depth

            axis_depth = min(max_b - min_a, max_a - min_b)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        for i in range(len(vertices_b)):
            va = vertices_b[i]
            vb = vertices_b[(i + 1) % len(vertices_b)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis = Vector2.normalize(axis)

            min_a, max_a = CollisionManager.project_vertices(vertices_a, axis)
            min_b, max_b = CollisionManager.project_vertices(vertices_b, axis)

            if min_a >= max_b or min_b >= max_a:
                return False, normal, depth

            axis_depth = min(max_b - min_a, max_a - min_b)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        direction = center_b - center_a

        if Vector2.dot(direction, normal) < 0:
            normal = -normal

        return True, normal, depth

    @staticmethod
    def project_vertices(vertices, axis):
        min_proj = float('inf')
        max_proj = float('-inf')

        for v in vertices:
            proj = Vector2.dot(v, axis)
            if proj < min_proj:
                min_proj = proj
            if proj > max_proj:
                max_proj = proj

        return min_proj, max_proj

    @staticmethod
    def intersect_circles(center_a, radius_a, center_b, radius_b):
        normal = Vector2(0, 0)
        depth = 0.0

        distance = Vector2.distance(center_a, center_b)
        radii = radius_a + radius_b

        if distance >= radii:
            return False, normal, depth

        normal = Vector2.normalize(center_b - center_a)
        depth = radii - distance

        return True, normal, depth

    @staticmethod
    def intersect_AABB(AABB_a, AABB_b):
        if (AABB_a.max.x <= AABB_b.min.x or AABB_b.max.x <= AABB_a.min.x or
                AABB_a.max.y <= AABB_b.min.y or AABB_b.max.y <= AABB_a.min.y):
            return False
        return True