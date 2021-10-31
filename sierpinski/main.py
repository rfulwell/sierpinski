import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Arbitrarily chosen sizes that fit on my screen
SIZE_X = 1000
SIZE_Y = 1000


class Point:
    x, y = 0, 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def pixel(surface, color, pos: Point):
    surface.fill(color, (pos.x, pos.y, 1, 1))


def nextpoint(one: Point, two: Point, three: Point) -> Point:
    points = [one, two, three]
    random.shuffle(points)
    return points[0]


def halfway(point1: Point, point2: Point) -> Point:
    next_x = (point1.x + point2.x) / 2
    next_y = (point1.y + point2.y) / 2
    return Point(int(next_x), int(next_y))


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


def init(screen: pygame.Surface, size_x: int, size_y: int):
    point1 = Point(random.randrange(size_x), random.randrange(size_y))
    point2 = Point(random.randrange(size_x), random.randrange(size_y))
    point3 = Point(random.randrange(size_x), random.randrange(size_y))
    start = Point(random.randrange(size_x), random.randrange(size_y))

    screen.fill(BLACK)
    pixel(screen, RED, point1)
    pixel(screen, RED, point2)
    pixel(screen, RED, point3)
    pixel(screen, WHITE, start)

    return point1, point2, point3, start


def main():
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
        current = halfway(current, nextpoint(point1, point2, point3))

        # --- Drawing code should go here
        pixel(screen, WHITE, current)
        drawfps(screen, fps)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to user-defined frames per second
        # this is a hack, I should be able to use `fps` directly here
        clock.tick(int(f"{fps}"))


if __name__ == "__main__":
    main()
