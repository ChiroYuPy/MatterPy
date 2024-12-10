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
circle = CircleRigidBody(WIDTH // 2, 128, 32, mass=64)
world.add(floor, circle)


def create_soft_body(x, y, width, height, spacing, stiffness, damping, world):

    bodies = []
    for r in range(height):
        col = []
        for c in range(width):
            body = CircleRigidBody(
                x=x + (width / 2 - (c + 0.5)) * spacing,
                y=y + (height / 2 - (r + 0.5)) * spacing,
                radius=spacing / 4, static=True if r==0 and (c==0 or c==width-1) else False)
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



create_soft_body(x=WIDTH // 2,
                 y=HEIGHT - 152,
                 width=15,
                 height=7,
                 spacing=32,
                 stiffness=1024,
                 damping=5,
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
