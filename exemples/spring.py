import pygame

from MatterPy.composite import CircleComposite
from MatterPy.constraint import SpringConstraint
from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import CircleRigidBody

WIDTH, HEIGHT = 1920, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="Spring made with RigidBodies")

GRAVITY = 9.81

world = World()
world.gravity.y = GRAVITY * 20


SPACING = 16
NUM_CIRCLES = 64
last_particle = None
for i in range(NUM_CIRCLES):
    static = True if i == 0 or i == NUM_CIRCLES - 1 else False
    circle = CircleRigidBody(x=(NUM_CIRCLES/2-i)*SPACING+WIDTH//2, y=256, radius=SPACING/2, static=static, restitution=0)
    world.add(circle)
    if last_particle:
        world.add(SpringConstraint(last_particle, circle, length=SPACING, stiffness=1000, damping=10))
    last_particle = circle



circle_composite = CircleComposite(WIDTH // 2, 0, 12, 12, 24, mass=32)
world.add(circle_composite)


def update():
    world.step()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("A spring with bodies")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
