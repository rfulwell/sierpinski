import pygame
import random


def pixel(surface, color, pos):
    surface.fill(color, (pos, (1, 1)))


def nextpoint(one, two, three, current):
    points = [one, two, three]
    random.shuffle(points)
    target = points[0]
    # return a position halfway between the current point and the target point
    next_x = (current[0] + target[0]) / 2
    next_y = (current[1] + target[1]) / 2
    return (next_x, next_y)


def drawfps(screen, fps):
    # Erase the previous value
    pygame.draw.rect(screen, BLACK, (50, 50, 150, 25))
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont("Calibri", 25)
    text = font.render(f"fps: {fps}", True, WHITE)
    screen.blit(text, [50, 50])


class Framerate:
    VALUES = [1, 5, 10, 30, 60, 120, 240, 0]
    __index__ = len(VALUES) - 1

    def __init__(self):
        self.value = self.VALUES[self.__index__]

    def __str__(self) -> str:
        return str(self.VALUES[self.__index__])

    def __repr__(self) -> int:
        return self.VALUES[self.__index__]

    def up(self):
        if (self.__index__ + 1) < len(self.VALUES):
            self.__index__ += 1

    def down(self):
        if self.__index__ > 0:
            self.__index__ -= 1


def init(screen, SIZE_X, SIZE_Y):
    one_x = random.randrange(SIZE_X)
    two_x = random.randrange(SIZE_X)
    three_x = random.randrange(SIZE_X)
    one_y = random.randrange(SIZE_Y)
    two_y = random.randrange(SIZE_Y)
    three_y = random.randrange(SIZE_Y)
    point1 = (one_x, one_y)
    point2 = (two_x, two_y)
    point3 = (three_x, three_y)

    start_x = random.randrange(SIZE_X)
    start_y = random.randrange(SIZE_Y)
    current = (start_x, start_y)

    screen.fill(BLACK)
    pixel(screen, RED, point1)
    pixel(screen, RED, point2)
    pixel(screen, RED, point3)
    pixel(screen, WHITE, current)

    return point1, point2, point3, current


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE_X = 1000
SIZE_Y = 1000

pygame.init()
size = (SIZE_X, SIZE_Y)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sierpinski Demo")
point1, point2, point3, current = init(screen, SIZE_X, SIZE_Y)
pygame.display.flip()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
fps = Framerate()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                point1, point2, point3, current = init(screen, SIZE_X, SIZE_Y)
                pygame.display.flip()
            if event.key == pygame.K_KP_MINUS:
                fps.down()
            if event.key == pygame.K_KP_PLUS:
                fps.up()
            if event.key == pygame.K_q:
                done = True
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # --- Game logic should go here
    current = nextpoint(point1, point2, point3, current)

    # --- Drawing code should go here
    pixel(screen, WHITE, current)
    drawfps(screen, fps)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to user-defined frames per second
    # this is a hack, I should be able to use `fps` directly here
    clock.tick(int(f"{fps}"))
