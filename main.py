import pygame
import math

# ------- CONFIGURATION AND CONSTANTS -------
pygame.init()

# Screen dimensions
WIDTH: int = 800
HEIGHT: int = 600

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Self-Driving Car Simulation")

# Frame rate
FPS = 60
CLOCK = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

# ------- CLASS DEFINITIONS -------
class Car:
    """Represents a self-driving car with simple AI navigation and sensors."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0

        # Physics parameters
        self.acceleration = 0.15
        self.max_speed = 3
        self.friction = 0.05
        self.turn_rate = 2.5

        # Distance traveled for stats
        self.distance_traveled = 0
        self.last_x = x
        self.last_y = y

        # Car appearance
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, (0, 0, 40, 20))
        pygame.draw.polygon(self.image, WHITE, [(40, 10), (35, 5), (35, 15)])
        self.original_image = self.image

    def update(self):
        """Update car position, rotation, and distance traveled."""
        dx = self.x - self.last_x
        dy = self.y - self.last_y
        self.distance_traveled += math.sqrt(dx * dx + dy * dy)
        self.last_x = self.x
        self.last_y = self.y

        # Apply friction
        if self.speed > 0:
            self.speed = max(self.speed - self.friction, 0)
        elif self.speed < 0:
            self.speed = min(self.speed + self.friction, 0)

        # Move based on angle
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

        # Rotate image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen, obstacles):
        """Draw car and its sensors."""
        screen.blit(self.image, self.rect.topleft)
        sensors = self.get_sensors(obstacles)

        # Draw sensor lines
        for i, offset in enumerate([0, -45, 45]):
            length = sensors[i]
            radians = math.radians(self.angle + offset)
            end_x = self.x + math.cos(radians) * length
            end_y = self.y + math.sin(radians) * length

            # Sensor color based on distance
            if length < 80:
                color = RED   # Very close
            elif length < 120:
                color = YELLOW  # Medium
            else:
                color = GREEN  # Far

            pygame.draw.line(screen, color, (self.x, self.y), (end_x, end_y), 2)

    def ai_navigate(self, sensors):
        """
        Simple AI logic to avoid obstacles using sensor distances.
        Adjusts speed and steering based on proximity.
        """
        forward, left, right = sensors
        safe_distance = 100
        warning_distance = 150

        if forward < safe_distance:
            # Obstacle very close: stop and turn sharply
            self.speed = max(self.speed - self.acceleration * 2, 0)
            if left > right:
                self.angle -= self.turn_rate * 2  # Turn left
            else:
                self.angle += self.turn_rate * 2  # Turn right
        
        elif forward < warning_distance:
            # Obstacle moderately close: slow and steer gently
            self.speed = min(self.speed + self.acceleration * 0.5, self.max_speed * 0.7)
            if left > right + 30:
                self.angle -= self.turn_rate
            elif right > left + 30:
                self.angle += self.turn_rate

        else:
            # Path is clear: accelerate normally
            self.speed = min(self.speed + self.acceleration, self.max_speed)
            # Adjust to stay centered between obstacles
            if left < right - 40:
                self.angle += self.turn_rate * 0.5
            elif right < left - 40:
                self.angle -= self.turn_rate * 0.5

    def cast_ray(self, angle_offset, obstacles, max_length=200):
        """
        Ray-casting sensor to detect distance to obstacles.
        Returns the length to the nearest obstacle in the given direction.
        """
        radians = math.radians(self.angle + angle_offset)
        dx = math.cos(radians)
        dy = math.sin(radians)

        for length in range(1, max_length):
            test_x = int(self.x + dx * length)
            test_y = int(self.y + dy * length)

            # Check screen boundaries
            if test_x < 0 or test_x >= WIDTH or test_y < 0 or test_y >= HEIGHT:
                return length

            test_point = pygame.Rect(test_x, test_y, 1, 1)
            for obs in obstacles:
                if test_point.colliderect(obs):
                    return length

        return max_length

    def get_sensors(self, obstacles):
        """Get distances from car to obstacles in forward, left, and right directions."""
        forward = self.cast_ray(0, obstacles)
        left = self.cast_ray(-45, obstacles)
        right = self.cast_ray(45, obstacles)
        return [forward, left, right]

# ------- HELPER FUNCTIONS -------
def create_track():
    """Create a simple track with walls and obstacles."""
    obstacles = [
        # Outer walls
        pygame.Rect(0, 0, WIDTH, 15),
        pygame.Rect(0, HEIGHT - 15, WIDTH, 15),
        pygame.Rect(0, 0, 15, HEIGHT),
        pygame.Rect(WIDTH - 15, 0, 15, HEIGHT),

        # Inner obstacles
        pygame.Rect(250, 150, 30, 150),
        pygame.Rect(500, 250, 30, 150),
    ]
    return obstacles

def draw_info(screen, car, font):
    """Display car speed on the screen."""
    distance_text = font.render(f"Total Distance Traveled: {car.distance_traveled:.0f}", True, WHITE)
    speed_text = font.render(f"Speed: {car.speed:.1f}", True, WHITE)
    screen.blit(distance_text, (15, 10))
    screen.blit(speed_text, (15, 35))

# ------- MAIN FUNCTION -------
def main():
    """Main loop handling game updates, AI, rendering, and input."""
    obstacles = create_track()
    car = Car(100, 300)
    font = pygame.font.Font(None, 28)

    running = True
    while running:
        CLOCK.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Sensor data and AI decision
        sensors = car.get_sensors(obstacles)
        car.ai_navigate(sensors)
        car.update()

        # Draw everything
        screen.fill(BLACK)
        for obs in obstacles:
            pygame.draw.rect(screen, WHITE, obs)

        car.draw(screen, obstacles)
        draw_info(screen, car, font)

        pygame.display.update()

    pygame.quit()

# -------- Entry Point -------
if __name__ == "__main__":
    main()
