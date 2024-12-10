import time
from random import randint

import pygame

from renderer import Renderer
from MatterPy.world import World
from MatterPy.rigid_body import CircleRigidBody, BoxRigidBody

WIDTH, HEIGHT = 600, 1080
renderer = Renderer(WIDTH, HEIGHT, window_name="CircleRigidBody")

GRAVITY = 9.81

ROWS, COLS = 8, 8
SPACING = 48
STIFFNESS = 200


world = World()
world.gravity.y = GRAVITY * 100

spacing = 24
floor = BoxRigidBody(WIDTH // 2, HEIGHT - spacing, WIDTH - spacing, spacing, static=True)
wall_left = BoxRigidBody(spacing, HEIGHT // 2, spacing, HEIGHT - spacing, static=True)
wall_right = BoxRigidBody(WIDTH - spacing, HEIGHT // 2, spacing, HEIGHT - spacing, static=True)

world.add(floor, wall_left, wall_right)

def create_fruit(x, y, radius):
    circle = CircleRigidBody(x=x, y=y, radius=radius)
    world.add(circle)


last_time = time.time()
current_time = time.time()
total_time = 0
time_interval = 0.5
def update():
    global last_time, current_time, total_time
    world.step()
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    total_time += dt

    if total_time >= time_interval:
        create_fruit(randint(WIDTH // 2 - 256, WIDTH // 2 + 256), 0, 16)
        total_time -= time_interval


def on_collision_begin(objA, objB, normal, depth):
    if objA.radius == objB.radius:
        world.remove(objA, objB)
        create_fruit(objA.x, objA.y, objA.radius + 16)
        return False
    return True

world.add_collision_handler(CircleRigidBody, CircleRigidBody, begin=on_collision_begin)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    renderer.add_line("Suika Game")
    renderer.add_line("FPS: %CURRENT_FPS%/%MAX_FPS%")
    renderer.clear()
    renderer.render_objects(world)
    renderer.render_menu()
    renderer.update()

renderer.close()
