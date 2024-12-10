class Constraint:
    def __init__(self, objA, objB):
        self.objA = objA
        self.objB = objB

    def apply(self, dt):
        raise NotImplementedError("Cette méthode doit être implémentée dans la sous-classe.")

class SpringConstraint(Constraint):
    def __init__(self, objA, objB, length, stiffness, max_force=0, damping=0):
        super().__init__(objA, objB)
        self.length = length
        self.stiffness = stiffness
        self.damping = damping
        self.max_force = max_force
        self.broken = False

    def step(self, dt):
        delta_pos = self.objB.position - self.objA.position
        delta_vel = self.objB.velocity - self.objA.velocity

        direction = delta_pos.normalize()

        distance = delta_pos.length()

        if distance == 0:
            return

        displacement = distance - self.length
        spring_force_magnitude = displacement * self.stiffness

        dot_product = direction.dot(delta_vel)
        damping_force_magnitude = dot_product * self.damping

        total_force_magnitude = spring_force_magnitude + damping_force_magnitude
        if total_force_magnitude > self.max_force and not self.max_force == 0:
            self.broken = True

        force = direction * total_force_magnitude
        self.objA.force += force
        self.objB.force -= force

class BoneConstraint(Constraint):
    def __init__(self, objA, objB, length):
        super().__init__(objA, objB)
        self.length = length

    def step(self, dt):
        delta_pos = self.objB.position - self.objA.position

        distance = delta_pos.length()

        if distance == 0:
            return

        error = (distance - self.length) / distance
        correction = delta_pos * error * 0.5

        self.objA.position += correction
        self.objB.position -= correction