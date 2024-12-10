import time

from .collision_manager import CollisionManager
from .composite import Composite
from .constraint import Constraint
from .exceptions import NonPhysicalObjectError
from .vector2 import Vector2
from .particle import Particle
from .rigid_body import RigidBody

class World:
    def __init__(self, gravity=Vector2(0, 0)):
        self._particles = []
        self._rigid_bodies = []
        self._constraints = []

        self._aabb_pairs = set()
        self.gravity = gravity
        self.current_time = time.time()
        self.accumulator = 0
        self.time_step = 1 / 120

        self.collision_handlers = {}
        self._to_remove = set()  # For deferring removals

    @property
    def rigid_body_count(self):
        return len(self._rigid_bodies)

    @property
    def rigid_bodies(self):
        return self._rigid_bodies

    @property
    def particles(self):
        return self._particles

    @property
    def constraints(self):
        return self._constraints

    def add_collision_handler(self, typeA, typeB, begin=None, separate=None):
        self.collision_handlers[(typeA, typeB)] = {
            "begin": begin,
            "separate": separate
        }

    def add(self, *objs):
        for obj in objs:
            if isinstance(obj, RigidBody):
                self._rigid_bodies.append(obj)
            elif isinstance(obj, Particle):
                self._particles.append(obj)
            elif isinstance(obj, Constraint):
                self._constraints.append(obj)
            elif isinstance(obj, Composite):
                for body in obj.objects:
                    self.add(body)
            else:
                raise NonPhysicalObjectError

    def remove(self, *objs):
        """Removes the given objects immediately from their respective lists."""
        for obj in objs:
            if isinstance(obj, RigidBody):
                self._remove_from_list(self._rigid_bodies, obj)
            elif isinstance(obj, Particle):
                self._remove_from_list(self._particles, obj)
            elif isinstance(obj, Constraint):
                self._remove_from_list(self._constraints, obj)
            elif isinstance(obj, Composite):
                for body in obj.objects:
                    self.remove(body)
            else:
                print(f"Warning: Object {obj} not found in world.")

    def _remove_from_list(self, lst, obj):
        """Helper function to remove an object from a list with proper error handling."""
        try:
            lst.remove(obj)
        except ValueError:
            print(f"Warning: Object {obj} already removed or not found.")

    def remove_later(self, *objs):
        """Schedule objects for removal at the end of the simulation step."""
        for obj in objs:
            if obj not in self._to_remove:
                self._to_remove.add(obj)

    def _process_removals(self):
        """Process the removals deferred using remove_later."""
        for obj in self._to_remove:
            self.remove(obj)
        self._to_remove.clear()

    def step(self):
        last_time = self.current_time
        self.current_time = time.time()
        dt = self.current_time - last_time
        self.accumulator += dt

        iterations = 0
        total_simulation_time = 0

        while self.accumulator >= self.time_step:
            self.accumulator -= self.time_step
            iterations += 1
            total_simulation_time += self.time_step
            if iterations > 4:
                print("Simulation time exceeded: skipping remaining steps")
                break

            self._step_objects()
            self._broad_phase()
            self._narrow_phase()

        self._process_removals()

    def _step_objects(self):
        """Step through all objects, applying forces and updating positions."""
        for constraint in reversed(self._constraints):
            constraint.step(self.time_step)
            if constraint.broken:
                self._constraints.remove(constraint)

        for obj in self.particles + self.rigid_bodies:
            obj.force += self.gravity * obj.mass
            obj.step(self.time_step)

    def _broad_phase(self):
        """Perform broad phase collision detection."""
        self._aabb_pairs.clear()
        for i in range(self.rigid_body_count - 1):
            objA = self._rigid_bodies[i]

            for j in range(i + 1, self.rigid_body_count):
                objB = self._rigid_bodies[j]

                if objA.static and objB.static:
                    continue  # Skip static vs static checks

                if not CollisionManager.intersect_AABB(objA.AABB, objB.AABB):
                    continue

                self._aabb_pairs.add((objA, objB))

    def _narrow_phase(self):
        """Perform narrow phase collision detection."""
        for objA, objB in self._aabb_pairs:
            collision, normal, depth = CollisionManager.is_collide(objA, objB)

            if collision:
                self._handle_collision(objA, objB, normal, depth)

    def _handle_collision(self, objA, objB, normal, depth):
        """Handle a detected collision."""
        handler_key = (type(objA), type(objB))
        handler = self.collision_handlers.get(handler_key)

        if handler and "begin" in handler and handler["begin"]:
            if not handler["begin"](objA, objB, normal, depth):
                return

        self._separate(objA, objB, normal * depth)
        self._resolve_collision_basic(objA, objB, normal)

        if handler and "separate" in handler and handler["separate"]:
            handler["separate"](objA, objB)

    @staticmethod
    def _separate(objA, objB, normal_dot_depth):
        """Separate colliding objects based on the normal vector."""
        if objB.static:
            objA.position += -normal_dot_depth
        elif objA.static:
            objB.position += normal_dot_depth
        else:
            objA.position += -normal_dot_depth / 2
            objB.position += normal_dot_depth / 2

    @staticmethod
    def _resolve_collision_basic(objA, objB, normal):
        """Resolve the collision by applying impulses to the objects."""
        relative_velocity = objB.velocity - objA.velocity

        if relative_velocity.dot(normal) > 0.0:
            return

        e = min(objA.restitution, objB.restitution)
        j = - (1.0 + e) * relative_velocity.dot(normal)
        j = j / (objA.inv_mass + objB.inv_mass)

        impulse = j * normal

        objA.velocity -= impulse * objA.inv_mass
        objB.velocity += impulse * objB.inv_mass

    @staticmethod
    def _resolve_collision_with_rotation(objA, objB, normal):
        pass