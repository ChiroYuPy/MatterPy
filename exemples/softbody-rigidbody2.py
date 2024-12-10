import math
import pygame
from MatterPy.composite import SoftBody
from renderer import Renderer
from MatterPy.vector2 import Vector2
from MatterPy.world import World
from MatterPy.rigid_body import BoxRigidBody

WIDTH, HEIGHT = 800, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="SoftBody made with RigidBodies")

FLOOR_HEIGHT = 32
world = World(gravity=Vector2(0, 50))

floor = BoxRigidBody(WIDTH // 2, HEIGHT - FLOOR_HEIGHT, WIDTH, 32, static=True)
slope1 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 - 200, 300, 32, static=True, angle=-math.pi / 6)
slope2 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2, 300, 32, static=True, angle=math.pi / 6)
slope3 = BoxRigidBody(WIDTH // 2 + 200, HEIGHT // 2 + 200, 300, 32, static=True, angle=-math.pi / 6)
slope4 = BoxRigidBody(WIDTH // 2 - 200, HEIGHT // 2 + 400, 300, 32, static=True, angle=math.pi / 6)

soft_body = SoftBody(x=WIDTH // 2 + 192, y=160, width=8, height=8, length=28, stiffness=1024, damping=1, mass=30)

world.add(floor, slope1, slope2, slope3, slope4, soft_body)


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
