import math

from renderer import Renderer
from MatterPy.world import World
from MatterPy.particle import Particle
from MatterPy.constraint import SpringConstraint
import pygame


WIDTH, HEIGHT = 1920, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="SoftBody made with particles")

FLOOR_HEIGHT = 32
GRAVITY = 9.81 * 10

ROWS, COLS = 8, 8
SPACING = 48
STIFFNESS = 200


world = World()
world.gravity.y = GRAVITY

def create_soft_body(x, y, width, height, spacing, stiffness, damping, world):

    particles = []
    for r in range(height):
        col = []
        for c in range(width):
            body = Particle(
                x=x + (width / 2 - (c + 0.5)) * spacing,
                y=y + (height / 2 - (r + 0.5)) * spacing,
                mass=1)
            col.append(body)
        particles.append(col)


    for row in particles:
        for body in row:
            world.add(body)


    for row in range(height):
        for col in range(width):
            if col < width - 1:
                spring = SpringConstraint(particles[row][col], particles[row][col + 1],
                                          length=spacing, stiffness=stiffness, damping=damping)
                world.add(spring)
            if row < height - 1:
                spring = SpringConstraint(particles[row][col], particles[row + 1][col],
                                          length=spacing, stiffness=stiffness, damping=damping)
                world.add(spring)
            if col < width - 1 and row < height - 1:
                spring = SpringConstraint(particles[row][col], particles[row + 1][col + 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping)
                world.add(spring)
            if col > 0 and row < height - 1:
                spring = SpringConstraint(particles[row][col], particles[row + 1][col - 1],
                                          length=spacing * math.sqrt(2), stiffness=stiffness, damping=damping)
                world.add(spring)



create_soft_body(x=WIDTH // 2,
                 y=0,
                 width=21,
                 height=11,
                 spacing=48,
                 stiffness=512,
                 damping=8,
                 world=world)


def update():
    world.step()
    floor_limit()

def floor_limit():
    for obj in world.particles:
        if obj.y > HEIGHT - FLOOR_HEIGHT:
            obj.y = HEIGHT - FLOOR_HEIGHT
            obj.velocity.y = 0

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update()
        renderer.add_line("SoftBody basics with particles and constraints")
        renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
        renderer.clear()
        renderer.render_objects(world)
        renderer.render_menu()
        renderer.update()

    renderer.close()

if __name__ == "__main__":
    main()