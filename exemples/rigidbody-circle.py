import math
from random import randint

import pygame

from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import CircleRigidBody, BoxRigidBody

WIDTH, HEIGHT = 1920, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="CircleRigidBody")

FLOOR_HEIGHT = 32
GRAVITY = 9.81

world = World()
world.gravity.y = GRAVITY * 10

floor = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
slope1 = BoxRigidBody(WIDTH // 2 + 300, HEIGHT // 2 - 300, WIDTH / 4, 32, static=True, angle=-math.pi / 6)
slope2 = BoxRigidBody(WIDTH // 2 - 300, HEIGHT // 2 - 100, WIDTH / 4, 32, static=True, angle=math.pi / 6)
slope3 = BoxRigidBody(WIDTH // 2 + 300, HEIGHT // 2 + 100, WIDTH / 4, 32, static=True, angle=-math.pi / 6)
slope4 = BoxRigidBody(WIDTH // 2 - 300, HEIGHT // 2 + 300, WIDTH / 4, 32, static=True, angle=math.pi / 6)
celling = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
world.add(floor, slope1, slope2, slope3, slope4, celling)

for _ in range(50):
    circle = CircleRigidBody(x=randint(WIDTH // 2 - 320, WIDTH // 2 + 320),
                             y=randint(50, 100),
                             radius=randint(8, 32))
    world.add(circle)


def update():
    world.step()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("Circle RigidBody simulation basics")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
