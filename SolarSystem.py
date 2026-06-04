import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,255, 0)

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()

simulation_speed = 1.0

class Planet:
    def __init__(self, name, orbit_radius, size, color, speed, info):
        self.name = name
        self.orbit_radius = orbit_radius
        self.size = size
        self.color = color
        self.speed = speed
        self.angle = 0
        self.info = info

        self.x = 0
        self.y = 0

    def update(self, speed_multiplier):
        self.angle += self.speed * speed_multiplier
        self.x = CENTER_X + math.cos(self.angle) * self.orbit_radius
        self.y = CENTER_Y + math.sin(self.angle) * self.orbit_radius 

    def draw(self, screen):
        #orbit
        pygame.draw.circle(
            screen, 
            (50,50,50),
            (CENTER_X, CENTER_Y),
            self.orbit_radius,
            1
        )

        #planet
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )
        if self.name == "Saturn":
            pygame.draw.ellipse(
                screen,
                (200, 200, 180),
                (
                    self.x - 25,
                    self.y - 10,
                    50,
                    20
                ),
                2
            )

        label = font.render(self.name, True, WHITE)
        screen.blit(label, (self.x + 10, self.y))
    
    def is_hovered(self, mouse_pos):
        mx, my = mouse_pos

        distance = math.sqrt(
            (mx - self.x) ** 2 +
            (my - self.y) ** 2
        )

        return distance <= self.size

planets = [
    Planet("Mercury", 60, 5, (170, 170, 170), 0.04,
           "Mercury\nDistance: 58M km"),

    Planet("Venus", 90, 8, (255, 180, 50), 0.03,
           "Venus\nDistance: 108M km"),

    Planet("Earth", 130, 9, (50, 100, 255), 0.025,
           """Earth\nDiameter: 12,742 km\nMoons: 1\nOrbit: 365 days\nAverage Temp: 15°C"""),

    Planet("Mars", 170, 7, (255, 80, 50), 0.02,
           "Mars\nDistance: 228M km"),

    Planet("Jupiter", 230, 18, (210, 170, 120), 0.01,
           "Jupiter\nLargest Planet"),

    Planet("Saturn", 300, 16, (220, 200, 140), 0.008,
           "Saturn\nHas Rings"),

    Planet("Uranus", 370, 13, (150, 220, 255), 0.006,
           "Uranus\nIce Giant"),

    Planet("Neptune", 430, 13, (70, 120, 255), 0.005,
           "Neptune\nFarthest Planet")
]

stars = [
    (
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    )
    for _ in range(300)
]

def draw_tooltip(text, x, y):
    lines = text.split("\n")

    width = 200
    height = len(lines) * 25 + 10

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (x, y, width, height)
    )  

    pygame.draw.rect(
        screen,
        WHITE,
        (x,y,width,height),
        2
    )

    for i, line in enumerate(lines):
        rendered = font.render(line, True, WHITE)
        screen.blit(rendered, (x + 10, y + 10 + i * 25))

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #increase speed
            if event.key == pygame.K_UP:
                simulation_speed += 1.25
            #decrease speed
            elif event.key == pygame.K_DOWN:
                simulation_speed /= 1.25
            elif event.key == pygame.K_r:
                simulation_speed = 1.0
    
    screen.fill(BLACK)

    #sun
    pygame.draw.circle(
        screen,
        YELLOW,
        (CENTER_X, CENTER_Y),
        30
    )

    for x, y in stars:
        pygame.draw.circle(screen, WHITE, (x, y), 1)

    hovered_planet = None
    
    for planet in planets:
        planet.update(simulation_speed)
        planet.draw(screen)

        if planet.is_hovered(pygame.mouse.get_pos()):
            hovered_planet= planet

    speed_text = font.render(
        f"Simulation Speed: {simulation_speed:.2f}x   Arrow up to speed up   Arrow down to speed down  R to reset",
        True,
        WHITE
    )

    screen.blit(speed_text, (20, 20))

    if hovered_planet:
        mx, my = pygame.mouse.get_pos()
        draw_tooltip(
            hovered_planet.info,
            mx + 15,
            my + 15
        )
    pygame.display.flip()

pygame.quit()
