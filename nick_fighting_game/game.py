# Imports Libraries
import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700  # Constants
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set window size
pygame.display.set_caption("Fighting Game!")

points = 0

font = pygame.font.SysFont(None, 36)
font = pygame.font.Font('./cool_font.ttf', 36)
label_surface = font.render("Points: " + str(points), True, (0, 0, 0))

# Game variables
PLAYER_SIZE = 50
BULLET_RADIUS = 10
PLAYER_SPEED = 7
ENEMY_SIZE = 50 
ENEMY_SPEED = 2
WHITE = (255, 255, 255)  # RGB
BLACK = (0, 0, 0)  # RGB
RED = (255, 0, 0)  # RGB

# Load images
bomb_image = pygame.image.load("bomb.png").convert_alpha()
resized_bomb_image = pygame.transform.scale(bomb_image, (30, 30))

boom_image = pygame.image.load("boom.png").convert_alpha()
resized_boom_image = pygame.transform.scale(boom_image, (100, 100))


# Game Classes
class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.holding_gun = False
        self.shoot_bullet = False
        self.reloading = False
        self.frames_since_last_shot = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.holding_gun = keys[pygame.K_SPACE]  # Test for space press
        self.shoot_bullet = keys[pygame.K_RCTRL]  # Test for right ctrl press

        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        # Keep player within screen bounds
        self.x = max(0, min(WINDOW_WIDTH - self.size, self.x))
        self.y = max(0, min(WINDOW_HEIGHT - self.size, self.y))

    def shoot(self):
        if self.holding_gun and self.shoot_bullet and not self.reloading:
            self.reloading = True
            self.frames_since_last_shot = 0
            return Bullet(self.x + 20, self.y - 30)
        return None

    def update(self):
        self.frames_since_last_shot += 1
        if self.frames_since_last_shot >= 30:
            self.reloading = False

    def draw(self):
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.size, self.size))
        if self.holding_gun:
            pygame.draw.rect(win, (0, 0, 255), (self.x + 20, self.y - 30, 10, 30))


class Enemy:
    def __init__(self, x=None, y=None, speed=ENEMY_SPEED):
        self.size = ENEMY_SIZE
        self.speed = speed
        self.alive = True
        if x is None or y is None:
            self.random_position()
        else:
            self.x = x
            self.y = y

    def random_position(self):
        self.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.y = random.randint(0, WINDOW_HEIGHT - self.size)

    def moves_towards_player(self, player_x, player_y):
        if self.alive:
            if self.x < player_x:
                self.x += self.speed
            elif self.x > player_x:
                self.x -= self.speed
            if self.y < player_y:
                self.y += self.speed
            elif self.y > player_y:
                self.y -= self.speed
    def check_collision_with_player(self, player_x, player_y):
        return (
            self.alive
            and self.x >= player_x
            and self.x <= player_x + PLAYER_SIZE
            and self.y >= player_y
            and self.y <= player_y + PLAYER_SIZE
        )

    def draw(self):
        if self.alive:
            pygame.draw.rect(win, RED, (self.x, self.y, self.size, self.size))
        else:
            win.blit(resized_bomb_image, (self.x, self.y))


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 30  # Duration to display explosion in frames

    def draw(self):
        if self.timer > 0:
            win.blit(resized_boom_image, (self.x, self.y))
            self.timer -= 1  # Decrease timer


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= 5  # Move bullet up

    def check_collision_with_enemy(self, enemy):
        return (
            enemy.alive
            and self.x >= enemy.x
            and self.x <= enemy.x + enemy.size
            and self.y >= enemy.y
            and self.y <= enemy.y + enemy.size
        )

    def draw(self):
        pygame.draw.circle(win, BLACK, (self.x, self.y), BULLET_RADIUS)


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy()]  # Start with one enemy
        self.bullets = []
        self.explosions = []
        self.running = True
        self.clock = pygame.time.Clock()

    def split_enemy(self, enemy):
        global points
        """Splits the given enemy into two new enemies of the same size."""
        self.explosions.append(Explosion(enemy.x, enemy.y))
        # Spawn two new enemies near the original one
        self.enemies.append(Enemy(enemy.x - enemy.size, enemy.y - enemy.size, enemy.speed * random.random() * 2))
        self.enemies.append(Enemy(enemy.x + enemy.size, enemy.y + enemy.size ,enemy.speed * random.random() * 2))
        # Remove the original enemy
        self.enemies.remove(enemy)
        points+=1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.handle_keys()
        self.player.update()

        for enemy in self.enemies:
            enemy.moves_towards_player(self.player.x, self.player.y)

        for bullet in self.bullets[:]:
            bullet.move()
            for enemy in self.enemies[:]:
                if bullet.check_collision_with_enemy(enemy):
                    self.split_enemy(enemy)  # Split the enemy
                    self.bullets.remove(bullet)
                    break

        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]
        self.explosions = [explosion for explosion in self.explosions if explosion.timer > 0]

        for enemy in self.enemies:
            if enemy.check_collision_with_player(self.player.x, self.player.y):
                self.running = False

        bullet = self.player.shoot()
        if bullet:
            self.bullets.append(bullet)

        

    def draw(self):
        win.fill(WHITE)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for explosion in self.explosions:
            explosion.draw()
        label_surface = font.render(f"Points: {points}", True, (0,0,0))
        win.blit(label_surface, (50, 50))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
