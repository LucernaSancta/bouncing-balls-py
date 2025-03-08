"""
Simple pygame template with 20 balls that bounce off walls and each other, with gravity applied.
controls:
    - ESC to exit
    - SPACE to pause
"""

import pygame
from pygame.math import Vector2
import random

screen_size = Vector2(800, 800)
fps = 144
gravity = Vector2(0, 9.81 * 100)  # Gravity vector, scaled up to make gravity noticeable
walls_b_coff = 0.9 # Add some energy dispersion when hitting the top or bottom of the screen (1 returns all energy, 0 none)

# Initialize all pygame things
pygame.init()
surface = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Variable to stop the rendering and physics if True
paused = False

# Ball object
class Ball:
    def __init__(self, pos: Vector2, radius: float, color: pygame.color.Color, init_speed: Vector2, mass: float = 1):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.speed = init_speed
        self.mass = mass
    
    def apply_gravity(self, deltaTime: float):
        """Apply gravity to the ball's speed."""
        self.speed += gravity * deltaTime  # Update speed with gravity
    
    def check_wall_collision(self, screen_size: Vector2) -> bool:
        """Change the direction of movement if a wall is hit"""
        hit = False
        if self.pos.x < self.radius:                   self.pos.x = self.radius;                 self.speed.x *= -1; hit = True
        if self.pos.y < self.radius:                   self.pos.y = self.radius;                 self.speed.y *= -walls_b_coff; hit = True  # Add slight bounce damping
        if self.pos.x > (screen_size.x - self.radius): self.pos.x = screen_size.x - self.radius; self.speed.x *= -1; hit = True
        if self.pos.y > (screen_size.y - self.radius): self.pos.y = screen_size.y - self.radius; self.speed.y *= -walls_b_coff; hit = True  # Add slight bounce damping
        return hit
    
    def check_ball_collision(self, other: "Ball") -> bool:
        """Change speed if colliding with another ball"""
        def collision(ball1: "Ball", ball2: "Ball") -> Vector2:
            return ball1.speed - (((2 * ball2.mass) / (ball1.mass + ball2.mass)) * 
                                  (((ball1.speed - ball2.speed) * (ball1.pos - ball2.pos)) / 
                                   ((ball1.pos - ball2.pos).length() ** 2)) * 
                                  (ball1.pos - ball2.pos))
        
        distance = (self.pos - other.pos).length()
        if distance <= (self.radius + other.radius):
            self.speed, other.speed = collision(self, other), collision(other, self)
            overlap = self.radius + other.radius - distance
            self.pos += (self.pos - other.pos).normalize() * overlap / 2
            other.pos += (other.pos - self.pos).normalize() * overlap / 2
            return True
        return False

# Create 20 balls with random properties
balls = []
for _ in range(50):
    radius = random.randint(10, 30)
    pos = Vector2(random.randint(radius, int(screen_size.x) - radius),
                  random.randint(radius, int(screen_size.y) - radius))
    color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    speed = Vector2(random.uniform(-200, 200), random.uniform(-200, 200))
    mass = radius  # Assign mass based on radius for variety
    balls.append(Ball(pos, radius, color, speed, mass))

# Main game loop
while True:
    deltaTime = clock.tick(fps) / 1000  # Time in seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                paused = not paused
    
    if paused:
        continue

    # Update ball positions, apply gravity, and check for wall collisions
    for ball in balls:
        ball.apply_gravity(deltaTime)
        ball.pos += ball.speed * deltaTime
        ball.check_wall_collision(screen_size)
    
    # Check ball-to-ball collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].check_ball_collision(balls[j])

    # Draw everything
    surface.fill("gray")
    for ball in balls:
        pygame.draw.circle(surface, ball.color, (int(ball.pos.x), int(ball.pos.y)), ball.radius)
    
    pygame.display.flip()
    