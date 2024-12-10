import math

import pygame

from MatterPy.constraint import SpringConstraint
from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import CircleRigidBody, BoxRigidBody

WIDTH, HEIGHT = 460, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="SoftBody Collapsing")

FLOOR_HEIGHT = 32
GRAVITY = 9.81


world = World()
world.gravity.y = GRAVITY * 10

floor = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
circle = BoxRigidBody(WIDTH // 2, 128, WIDTH, 32, mass=200)
world.add(floor, circle)


def create_soft_body(x, y, width, height, spacing, stiffness, damping, max_force, world):

    bodies = []
    for r in range(height):
        col = []
        for c in range(width):
            body = CircleRigidBody(
                x=x + (width / 2 - (c + 0.5)) * spacing,
                y=y + (height / 2 - (r + 0.5)) * spacing,
                radius=spacing / 4)
            col.append(body)
        bodies.append(col)


    for row in bodies:
        for body in row:
            world.add(body)


    for row in range(height):
        for col in range(width):
            if col < width - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row][col + 1],
                                          length=spacing, stiffness=stiffness, damping=damping, max_force=max_force)
                world.add(spring)
            if row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col],
                                          length=spacing, stiffness=stiffness, damping=damping, max_force=max_force)
                world.add(spring)
            if col < width - 1 and row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col + 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping, max_force=max_force)
                world.add(spring)
            if col > 0 and row < height - 1:
                spring = SpringConstraint(bodies[row][col], bodies[row + 1][col - 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping, max_force=max_force)
                world.add(spring)



create_soft_body(x=WIDTH // 2,
                 y=HEIGHT - 320,
                 width=12,
                 height=6,
                 spacing=32,
                 stiffness=2000,
                 damping=10,
                 max_force=8000,
                 world=world)


def update():
    world.step()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("SoftBody collapsing")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
