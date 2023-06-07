import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Autonomous Agents")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define the autonomous agent class
class Agent:
    def __init__(self, x, y, size, speed, fov_angle):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = random.uniform(0, 2*math.pi)
        self.fov_angle = fov_angle

    def wander(self, agents):
        # Calculate a small random angle change
        angle_change = random.uniform(-0.1, 0.1)

        # Update the angle of movement
        self.angle += angle_change

        # Calculate the velocity components
        velocity_x = math.cos(self.angle) * self.speed
        velocity_y = math.sin(self.angle) * self.speed

        # Initialize the average angle
        average_angle = self.angle

        # Count the neighboring agents
        neighbor_count = 0

        # Calculate the average angle of neighboring agents
        for agent in agents:
            if agent != self:
                distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                if distance < self.size + agent.size + 10:
                    average_angle += agent.angle
                    neighbor_count += 1

        # Calculate the average angle if there are neighbors
        if neighbor_count > 0:
            average_angle /= (neighbor_count + 1)

            # Calculate the angle difference
            angle_diff = average_angle - self.angle

            # Adjust the agent's angle
            self.angle += angle_diff * 0.1

        # Update the position
        self.x += velocity_x
        self.y += velocity_y

        # Wrap around the screen edges
        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height

    def draw(self):
        # Calculate the triangle vertices based on the agent's position and angle
        tip_x = self.x + math.cos(self.angle) * self.size
        tip_y = self.y + math.sin(self.angle) * self.size
        base_x1 = self.x + math.cos(self.angle + self.fov_angle / 2 + math.pi) * self.size / 4
        base_y1 = self.y + math.sin(self.angle + self.fov_angle / 2 + math.pi) * self.size / 4
        base_x2 = self.x + math.cos(self.angle - self.fov_angle / 2 + math.pi) * self.size / 4
        base_y2 = self.y + math.sin(self.angle - self.fov_angle / 2 + math.pi) * self.size / 4

        # Draw the triangle on the screen
        pygame.draw.polygon(screen, WHITE, [(tip_x, tip_y), (base_x1, base_y1), (base_x2, base_y2)], 0)
        pygame.draw.polygon(screen, GREEN, [(tip_x, tip_y), (base_x1, base_y1), (base_x2, base_y2)], 2)

# Create a list to hold the agents
agents = []

# Create a few agents
num_agents = 5
size = 30
speed = 2
fov_angle = math.pi / 2  # 90 degrees

for _ in range(num_agents):
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    agent = Agent(x, y, size, speed, fov_angle)
    agents.append(agent)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Move and draw each agent
    for agent in agents:
        agent.wander(agents)
        agent.draw()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
