import pygame
import re

from MatterPy.rigid_body import CircleRigidBody, PolygonRigidBody


class Renderer:
    APPLICATION_NAME = "MatterPy"
    APP_VERSION = "0.1.5"

    def __init__(self, width, height, window_name, max_fps=60, text_size=24, background_color=(32, 32, 32), show_AABBs=False):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.window_name = window_name
        self.caption = f"{self.window_name} - {self.APPLICATION_NAME} v{self.APP_VERSION}"
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.SysFont("calibri", text_size)
        self.background_color = background_color
        self.width = width
        self.height = height
        self.max_fps = max_fps
        self.show_AABBs = show_AABBs

        self.clock = pygame.time.Clock()

        self.menu_lines = []

        self.current_fps = 0

    def clear(self):
        self.window.fill(self.background_color)

    def add_line(self, text):
        text_with_placeholders = self.replace_placeholders(text)
        self.menu_lines.append(text_with_placeholders)

    def clear_lines(self):
        self.menu_lines.clear()

    def replace_placeholders(self, text):
        placeholders = {
            "%CURRENT_FPS%": str(self.current_fps),
            "%MAX_FPS%": str(self.max_fps),
            "%WINDOW_NAME%": self.caption
        }

        placeholder_pattern = re.compile(r"%\w+%")
        found_placeholders = placeholder_pattern.findall(text)

        for placeholder in found_placeholders:
            if placeholder in placeholders:
                text = text.replace(placeholder, placeholders[placeholder])
            else:
                raise ValueError(f"Placeholder {placeholder} doesn't exist")

        return text

    def render_menu(self):
        x, y = 6, 0
        for line in self.menu_lines:
            text = self.font.render(line, True, (127, 127, 127))
            self.window.blit(text, (x, y))
            y += self.font.get_height()

    def render_constraints(self, constraints):
        for constraint in constraints:
            pygame.draw.line(self.window,
                             color=(64, 32, 0), width=3,
                             start_pos=(constraint.objA.x, constraint.objA.y),
                             end_pos=(constraint.objB.x, constraint.objB.y)
                             )

    def render_particles(self, particles):
        for particle in particles:
            if particle.static:
                r, g, b = 24, 24, 24
            else:
                r = int(min(max(255 * particle.x // self.width, 0), 255))
                g = int(min(max(255 * particle.y // self.height, 0), 255))
                b = 0
            pygame.draw.circle(self.window, (r, g, b), (int(particle.x), int(particle.y)), 6)

    def render_rigid_bodies(self, rigid_bodies):
        for rigid_body in rigid_bodies:
            if rigid_body.AABB and self.show_AABBs:
                pygame.draw.rect(self.window, (255, 255, 255), (rigid_body.AABB.min.x, rigid_body.AABB.min.y, rigid_body.AABB.max.x - rigid_body.AABB.min.x, rigid_body.AABB.max.y - rigid_body.AABB.min.y), width=1)
            if rigid_body.static:
                r, g, b = 24, 24, 24
            else:
                r = int(min(max(64 + 127 * rigid_body.y // self.height, 0), 255))
                g = int(min(max(192 - 127 * rigid_body.y // self.height, 0), 255))
                b = 0
            if isinstance(rigid_body, CircleRigidBody):
                pygame.draw.circle(self.window, (r, g, b), (rigid_body.x, rigid_body.y), rigid_body.radius)
            if isinstance(rigid_body, PolygonRigidBody):
                vertices = [(v.x, v.y) for v in rigid_body.vertices]
                pygame.draw.polygon(self.window, (r, g, b), vertices)

    def render_objects(self, world):
        self.render_constraints(world.constraints)
        self.render_rigid_bodies(world.rigid_bodies)
        self.render_particles(world.particles)

    def update(self):
        self.current_fps = int(self.clock.get_fps())

        pygame.display.flip()
        self.clear_lines()
        self.clock.tick(self.max_fps)

    def close(self):
        pygame.quit()
