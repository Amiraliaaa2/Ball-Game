# instagram : @amirali.aaa_
import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for rendering text
font_small = pygame.font.SysFont(None, 36)
font_large = pygame.font.SysFont(None, 48)

class BallGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.ball_radius = 15
        self.ball_x = WIDTH // 4
        self.ball_y = HEIGHT - self.ball_radius
        self.ball_speed_y = 0
        self.gravity = 0.5
        self.jump_strength = 15
        self.is_jumping = False
        self.is_falling = False
        self.score = 0
        self.passed_obstacles = 0
        self.obstacle_speed = 10
        self.obstacles = []
        self.obstacle_frequency = 2000

        self.create_obstacle_event()

        self.start_time = time.time()

        # List to track passed obstacles
        self.passed_obstacles_list = []

    def draw_ball(self):
        pygame.draw.circle(screen, BLUE, (self.ball_x, self.ball_y), self.ball_radius)

    def draw_obstacles(self):
        for obs in self.obstacles:
            if obs['type'] == 'circle':
                pygame.draw.circle(screen, RED, (obs['x'], obs['y']), obs['radius'])
            elif obs['type'] == 'rect':
                pygame.draw.rect(screen, RED, obs['rect'])
            elif obs['type'] == 'triangle':
                pygame.draw.polygon(screen, RED, obs['points'])

    def draw_score(self):
        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        timer_text = font_small.render(f"Time: {elapsed_time}", True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 10))

    def draw_obstacle_passed(self):
        passed_text = font_large.render(f"Obstacles Passed: {self.passed_obstacles}", True, GREEN)
        text_rect = passed_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(passed_text, text_rect)

    def create_obstacle_event(self):
        pygame.time.set_timer(pygame.USEREVENT, self.obstacle_frequency)

    def create_obstacle(self):
        num_obstacles = 1 + self.passed_obstacles // 10
        for _ in range(num_obstacles):
            shape_type = random.choice(['circle', 'rect', 'triangle'])
            if shape_type == 'circle':
                x = WIDTH
                y = random.randint(50, HEIGHT - 50)
                radius = random.randint(10, 25)
                obstacle = {'type': 'circle', 'x': x, 'y': y, 'radius': radius}
            elif shape_type == 'rect':
                x = WIDTH
                y = random.randint(50, HEIGHT - 50)
                width = random.randint(20, 50)
                height = random.randint(20, 50)
                obstacle = {'type': 'rect', 'rect': pygame.Rect(x, y, width, height)}
            elif shape_type == 'triangle':
                x = WIDTH
                y = random.randint(50, HEIGHT - 50)
                size = random.randint(20, 50)
                points = [(x, y), (x - size, y + size), (x + size, y + size)]
                obstacle = {'type': 'triangle', 'points': points}
            self.obstacles.append(obstacle)
        self.create_obstacle_event()

    def move_obstacles(self):
        for obs in self.obstacles:
            if obs['type'] == 'circle':
                obs['x'] -= self.obstacle_speed
            elif obs['type'] == 'rect':
                obs['rect'].x -= self.obstacle_speed
            elif obs['type'] == 'triangle':
                for i in range(len(obs['points'])):
                    obs['points'][i] = (obs['points'][i][0] - self.obstacle_speed, obs['points'][i][1])
        self.obstacles = [obs for obs in self.obstacles if obs['type'] == 'circle' and obs['x'] + obs['radius'] > 0 or obs['type'] == 'rect' and obs['rect'].x + obs['rect'].width > 0 or obs['type'] == 'triangle' and obs['points'][1][0] > 0]

    def check_collision(self):
        ball_rect = pygame.Rect(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius, self.ball_radius * 2, self.ball_radius * 2)
        for obs in self.obstacles:
            if obs['type'] == 'circle':
                distance = math.hypot(self.ball_x - obs['x'], self.ball_y - obs['y'])
                if distance < self.ball_radius + obs['radius']:
                    return True
            elif obs['type'] == 'rect':
                if ball_rect.colliderect(obs['rect']):
                    return True
            elif obs['type'] == 'triangle':
                if ball_rect.collidepoint(*obs['points'][0]) or ball_rect.collidepoint(*obs['points'][1]) or ball_rect.collidepoint(*obs['points'][2]):
                    return True
        return False

    def update_passed_obstacles(self):
        for obs in self.obstacles:
            if (obs['type'] == 'circle' and obs['x'] + obs['radius'] < self.ball_x or
                obs['type'] == 'rect' and obs['rect'].x + obs['rect'].width < self.ball_x or
                obs['type'] == 'triangle' and obs['points'][1][0] < self.ball_x) and obs not in self.passed_obstacles_list:
                self.passed_obstacles += 1
                self.passed_obstacles_list.append(obs)
                self.score += 1
                if self.passed_obstacles % 10 == 0:
                    self.obstacle_speed += 2
                    self.obstacle_frequency = max(500, self.obstacle_frequency - 200)

                # Print the obstacle number and shape to the terminal in green
                obstacle_shape = obs['type']
                print(f"\033[92mPassed Obstacle {self.passed_obstacles}: {obstacle_shape}\033[0m")

    def game_over(self):
        screen.fill(BLACK)  # Clear the screen with black color
        game_over_text = font_large.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        restart_text = font_large.render("Play Again", True, BLACK)
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        pygame.draw.rect(screen, GREEN, restart_button)
        screen.blit(restart_text, (WIDTH // 2 - 90, HEIGHT // 2 + 20))

        pygame.display.flip()

        elapsed_time = int(time.time() - self.start_time)
        print(f"Game Over! You passed {self.passed_obstacles} obstacles and played for {elapsed_time} seconds.")

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        waiting_for_restart = False
                        self.reset_game()
                        self.run_game()

    def update_ball(self):
        if self.is_jumping:
            self.ball_speed_y = -self.jump_strength
            self.is_jumping = False
        elif self.is_falling:
            self.ball_speed_y += self.jump_strength
            self.is_falling = False

        self.ball_y += self.ball_speed_y
        self.ball_speed_y += self.gravity

        if self.ball_y >= HEIGHT - self.ball_radius:
            self.ball_y = HEIGHT - self.ball_radius
            self.ball_speed_y = 0

        if self.ball_y <= self.ball_radius:
            self.ball_y = self.ball_radius
            self.ball_speed_y = -self.ball_speed_y * 0.8

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.is_jumping = True
                    elif event.key == pygame.K_DOWN:
                        self.is_falling = True
                elif event.type == pygame.USEREVENT:
                    self.create_obstacle()

            screen.fill(BLACK)  # Clear the screen with black color
            self.update_ball()
            self.move_obstacles()
            self.update_passed_obstacles()

            if self.check_collision():
                self.game_over()
                running = False

            self.draw_ball()
            self.draw_obstacles()
            self.draw_score()
            self.draw_timer()
            self.draw_obstacle_passed()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = BallGame()
    game.run_game()
