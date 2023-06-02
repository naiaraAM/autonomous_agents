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

        for agent in agents:
            if agent != self:
                distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                if distance < self.size + agent.size + 10:
                    target_angle = math.atan2(agent.y - self.y, agent.x - self.x) + math.pi
                    angle_diff = target_angle - self.angle
                    if angle_diff > 0:
                        self.angle += 0.1
                    else:
                        self.angle -= 0.1

                    # Move away from the other agent
                    self.x -= velocity_x
                    self.y -= velocity_y
                    break

        # Check if the mouse is within the window
        if 0 <= mouse_position[0] <= width and 0 <= mouse_position[1] <= height:
            # Calculate the angle to the mouse
            target_angle = math.atan2(mouse_position[1] - self.y, mouse_position[0] - self.x)

            # Calculate the angle difference
            angle_diff = target_angle - self.angle

            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            # Adjust the agent's angle
            self.angle += angle_diff * 0.05

            # Calculate the updated velocity components
            velocity_x = math.cos(self.angle) * self.speed
            velocity_y = math.sin(self.angle) * self.speed

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
num_agents = 1
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

    # Get the mouse position
    mouse_position = pygame.mouse.get_pos()

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
