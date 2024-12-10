import math

import pygame

from MatterPy.composite import CircleComposite, BoxComposite
from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import BoxRigidBody

WIDTH, HEIGHT = 1920, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="SoftBody made with RigidBodies")

FLOOR_HEIGHT = 32
GRAVITY = 9.81

world = World()
world.gravity.y = GRAVITY * 5

floor = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
slope1 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 - 200, WIDTH / 6, 32, static=True, angle=-math.pi / 6)
slope2 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2, WIDTH / 6, 32, static=True, angle=math.pi / 6)
slope3 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 + 200, WIDTH / 6, 32, static=True, angle=-math.pi / 6)
slope4 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2 + 400, WIDTH / 6, 32, static=True, angle=math.pi / 6)
world.add(floor, slope1, slope2, slope3, slope4)


circle_composite = CircleComposite(WIDTH // 2 - 200, 0, 5, 5, 48)
world.add(circle_composite)

box_composite = BoxComposite(WIDTH // 2 + 200, 0, 5, 5, 48)
world.add(box_composite)


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
