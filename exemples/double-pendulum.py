import pygame

from MatterPy.constraint import SpringConstraint
from MatterPy.particle import Particle
from MatterPy.world import World

from renderer import Renderer

WIDTH, HEIGHT = 1000, 1000
renderer = Renderer(WIDTH, HEIGHT, window_name="double-pendulum")

world = World()
world.gravity.y = 9.81 * 200

particleA = Particle(WIDTH // 2, HEIGHT // 2, static=True)
particleB = Particle(WIDTH // 2 + 5, HEIGHT // 2 - 200)
particleC = Particle(WIDTH // 2, HEIGHT // 2 - 400)

constraintA = SpringConstraint(particleA, particleB, length=200, stiffness=5000, damping=8)
constraintB = SpringConstraint(particleB, particleC, length=200, stiffness=5000, damping=8)

world.add(particleA, particleB, particleC, constraintA, constraintB)

def update():
    world.step()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("Double Pendulum")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
