"""
Simple pygame template,
two cirlces with collision and no friction bouncing in a rectangular space

controls:
    - ESC to exit
    - SPACE to pause
"""


import pygame
from pygame.math import Vector2


screen_size = Vector2(800,800)
fps = 144

# Initialize all pygame things
pygame.init()
surface = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Variable to stop the renderign and phisics if True
paused = False


# Ball object
class Ball:
    def __init__(self, pos: Vector2, radius: float, color: pygame.color.Color, init_speed: Vector2, mass: float = 1):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.speed = init_speed
        self.mass = mass
    
    def check_wall_collision(self, screen_size: Vector2) -> bool:
        """
        Change the direction of movment of the ball if a wall is hit.
        Returns True if a wall is hit
        """

        hit = False

        if self.pos.x < self.radius:                   self.pos.x = self.radius;                 self.speed.x *= -1; hit = True # Check top wall
        if self.pos.y < self.radius:                   self.pos.y = self.radius;                 self.speed.y *= -1; hit = True # Check left wall
        if self.pos.x > (screen_size.x - self.radius): self.pos.x = screen_size.x - self.radius; self.speed.x *= -1; hit = True # Check bottom wall
        if self.pos.y > (screen_size.y - self.radius): self.pos.y = screen_size.y - self.radius; self.speed.y *= -1; hit = True # Check right wall

        return hit
    
    def check_ball_collision(self, ball2: "Ball") -> bool:
        """
        Change the direction and speed if it collides with the second ball (also the second balls direction and speed is changed)
        Returns True if a collision is detected
        """

        def collision(ball1: "Ball", ball2: "Ball") -> Vector2:
            """Returns the new speed vector of the ball1"""

            # Applay the angle-free representation of two-dimensional collision with two moving objects formula https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
            return ball1.speed - (((2*ball2.mass)/(ball1.mass+ball2.mass))*(((ball1.speed-ball2.speed)*(ball1.pos-ball2.pos))/(((ball1.pos-ball2.pos).length())**2))*(ball1.pos-ball2.pos))
        
        distance = (self.pos - ball2.pos).length()

        if distance <= (self.radius + ball2.radius):
            speed1 = collision(self, ball2)
            speed2 = collision(ball2, self)

            self.speed = speed1
            ball2.speed = speed2

            # Adjust the position such that they don't overlap and shit
            tv1 = self.pos-ball2.pos
            tv2 = ball2.pos-self.pos

            def clamp(x) -> float:
                if x >= 0: return x
                else: return 0

            self.pos += tv1.normalize() * clamp(tv1.length() - (self.radius + ball2.radius)) / 2
            ball2.pos += tv2.normalize() * clamp(tv2.length() - (self.radius + ball2.radius)) / 2
            
            return True
        
        return False

# Define the istances
BALL1 = Ball(Vector2(30,50),100, "green",Vector2(200,100), 3)
BALL2 = Ball(Vector2(500,250),50, "red",Vector2(-100,-300), 1)


# Main game cicle
while True:

    # Limit the fps to 60
    deltaTime = clock.tick(fps)
    deltaTime /= 1000 # transform from milliseconds to seconds


    # Get pygame events
    for event in pygame.event.get():

        # Quit if the window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Capture the keypress
        elif event.type == pygame.KEYDOWN:

            # Quit if ESC
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            
            # Pause or resume the program
            elif event.key == pygame.K_SPACE:
                paused = not paused

    
    # If paused than skip all the phisics and plotting
    if paused:
        continue


    # Calc objects new positions
    BALL1.pos += BALL1.speed * deltaTime
    BALL2.pos += BALL2.speed * deltaTime

    # Check for collisions with the borders
    BALL1.check_wall_collision(screen_size)
    BALL2.check_wall_collision(screen_size)

    # Check cllision with each other
    BALL1.check_ball_collision(BALL2)

    # Fill the background of the screen
    surface.fill("gray")

    # Plot the ball and the circle
    pygame.draw.circle(surface, BALL1.color, BALL1.pos, BALL1.radius)
    pygame.draw.circle(surface, BALL2.color, BALL2.pos, BALL2.radius)

    # Plot the buffer on the screen
    pygame.display.flip()
