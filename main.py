import pygame
import time

pygame.init()

size = (640, 640)
width, height = size
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Thompson")
clock = pygame.time.Clock()

bg_color = (31, 35, 41)

def draw_logo_screen():
    logo = pygame.image.load("sprites/startScreen.png")
    Block.draw_to_screen(logo, (0, 0))
    pygame.display.flip()
    time.sleep(2)

class Block(pygame.sprite.Sprite):
    TEXTURE_SIZE = (64, 64)

    def __init__(self, type="floor1", coords=(0, 0)):
        super().__init__()
        floor1 = pygame.image.load("sprites/fl1.png")
        floor1 = pygame.transform.scale(floor1, self.TEXTURE_SIZE)
        floor2 = pygame.image.load("sprites/fl2.png")
        floor2 = pygame.transform.scale(floor2, self.TEXTURE_SIZE)
        wall = pygame.image.load("sprites/wall.png")
        wall = pygame.transform.scale(wall, self.TEXTURE_SIZE)
        if type == "floor1":
            self.image = floor1
        elif type == "floor2":
            self.image = floor2
        elif type == "wall":
            self.image = wall
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.coords = coords

    @staticmethod
    def draw_to_screen(img: pygame.Surface, coords: tuple):
        screen.blit(img, coords)


obstacle_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()


def setup_bg():
    try:
        with open("pattern", "r") as f:
            rows = f.readlines()
    except FileNotFoundError:
        print("pattern file not found")
        exit(1)

    for i, row in enumerate(rows):
        row = list(row)
        for j, block in enumerate(row):
            if block == "#":
                background_group.add(
                    Block(
                        "floor1", (j * Block.TEXTURE_SIZE[0], i * Block.TEXTURE_SIZE[1])
                    )
                )
            elif block == "@":
                obstacle_group.add(
                    Block(
                        "wall", (j * Block.TEXTURE_SIZE[0], i * Block.TEXTURE_SIZE[1])
                    )
                )
            else:
                background_group.add(
                    Block(
                        "floor2", (j * Block.TEXTURE_SIZE[0], i * Block.TEXTURE_SIZE[1])
                    )
                )


def draw_bg():
    for item in background_group:
        Block.draw_to_screen(item.image, item.coords)
    for item in obstacle_group:
        Block.draw_to_screen(item.image, item.coords)


# sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load all images once
        self.images = {
            "up": pygame.transform.scale(pygame.image.load("sprites/up_idle.png"), (64, 64)),
            "down": pygame.transform.scale(pygame.image.load("sprites/down_idle.png"), (64, 64)),
            "left": pygame.transform.scale(pygame.image.load("sprites/left_idle.png"), (64, 64)),
            "right": pygame.transform.scale(pygame.image.load("sprites/right_idle.png"), (64, 64))
        }
        self.img = self.images["down"]

        self.speed = 5
        self.sprint_speed = 8
        self.velocity = pygame.math.Vector2(0, 0)

        self.rect = pygame.rect.Rect(0,0,64,64)

        self.rect.x = width / 2
        self.rect.y = height / 2

    def draw_to_screen(self):
        screen.blit(self.img, self.rect)

    def move(self, keys):

        if keys[pygame.K_UP]:
            self.velocity.y = self.speed * -1
            self.img = self.images["up"]
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.speed * 1
            self.img = self.images["down"]
        elif keys[pygame.K_LEFT]:
            self.velocity.x = self.speed * -1
            self.img = self.images["left"]
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed * 1
            self.img = self.images["right"]
        if keys[pygame.K_x]:
            self.velocity.x = self.velocity.x / self.speed * self.sprint_speed
            self.velocity.y = self.velocity.y / self.speed * self.sprint_speed

        self.rect.topleft += self.velocity

        self.collision(obstacle_group)
        self.velocity = pygame.math.Vector2(0, 0)

    def collision(self, group):
        collision = pygame.sprite.spritecollideany(self, group)

        if collision:
            if self.velocity.x > 0:
                self.rect.right = collision.rect.left
            elif self.velocity.x < 0:
                self.rect.left = collision.rect.right

            if self.velocity.y > 0:
                self.rect.bottom = collision.rect.top
            elif self.velocity.y < 0:
                self.rect.top = collision.rect.bottom

        return collision


player = Player()

run = True
draw_logo_screen()
setup_bg()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(bg_color)
    draw_bg()
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.draw_to_screen()
    pygame.display.flip()
    clock.tick(60)
