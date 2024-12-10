import math

import pygame

from MatterPy.constraint import SpringConstraint
from MatterPy.particle import Particle
from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import CircleRigidBody, BoxRigidBody

WIDTH, HEIGHT = 800, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="SoftBody made with RigidBodies")

FLOOR_HEIGHT = 32
GRAVITY = 9.81

world = World()
world.gravity.y = GRAVITY * 5

floor = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
slope1 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 - 200, 300, 32, static=True, angle=-math.pi / 6)
slope2 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2, 300, 32, static=True, angle=math.pi / 6)
slope3 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 + 200, 300, 32, static=True, angle=-math.pi / 6)
slope4 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2 + 400, 300, 32, static=True, angle=math.pi / 6)
world.add(floor, slope1, slope2, slope3, slope4)


def create_soft_body(x, y, width, height, spacing, stiffness, damping, world):
    bodies = []
    for r in range(height):
        col = []
        for c in range(width):
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                body = CircleRigidBody(
                    x=x + (width / 2 - (c + 0.5)) * spacing,
                    y=y + (height / 2 - (r + 0.5)) * spacing,
                    radius=spacing / 4)
            else:
                body = Particle(
                    x=x + (width / 2 - (c + 0.5)) * spacing,
                    y=y + (height / 2 - (r + 0.5)) * spacing,
                    mass=1)
            col.append(body)
        bodies.append(col)

    for row in bodies:
        for body in row:
            world.add(body)

    for row in range(height):
        for col in range(width):
            if col < width - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row][col + 1],
                                          length=spacing, stiffness=stiffness, damping=damping)
                world.add(spring)
            if row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col],
                                          length=spacing, stiffness=stiffness, damping=damping)
                world.add(spring)
            if col < width - 1 and row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col + 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping)
                world.add(spring)
            if col > 0 and row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col - 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping)
                world.add(spring)


create_soft_body(x=WIDTH // 2 + 192,
                 y=128,
                 width=7,
                 height=7,
                 spacing=32,
                 stiffness=1024,
                 damping=1,
                 world=world)


def update():
    world.step()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("SoftBody basics with Particles, RigidBody Constraints")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
