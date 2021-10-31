from typing import Iterable
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
SIZE_Y = SIZE_X


class Point:
    x, y = 0, 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Framerate:
    VALUES = [1, 5, 10, 30, 60, 120, 240, 0]
    __index__ = len(VALUES) - 1

    def __init__(self) -> None:
        self.value = self.VALUES[self.__index__]

    def __str__(self) -> str:
        return str(self.VALUES[self.__index__])

    def __repr__(self) -> int:
        return self.VALUES[self.__index__]

    def up(self) -> None:
        if (self.__index__ + 1) < len(self.VALUES):
            self.__index__ += 1

    def down(self) -> None:
        if self.__index__ > 0:
            self.__index__ -= 1


def pixel(surface, color, pos: Point) -> None:
    surface.fill(color, (pos.x, pos.y, 1, 1))


def nextpoint(points: list[Point]) -> Point:
    random.shuffle(points)
    return points[0]


def halfway(point1: Point, point2: Point) -> Point:
    next_x = (point1.x + point2.x) / 2
    next_y = (point1.y + point2.y) / 2
    return Point(int(next_x), int(next_y))


def drawfps(screen: pygame.Surface, fps: Framerate) -> None:
    OVERLAY_X = 50
    OVERLAY_Y = 50
    FONT_SIZE = 25
    # Erase the previous overlay, I just eyeballed this value to be
    # ~max size of the text to provide an unobstructed background
    screen.fill(BLACK, (OVERLAY_X, OVERLAY_Y, 100, FONT_SIZE))
    font = pygame.font.SysFont("Calibri", FONT_SIZE)
    text = font.render(f"fps: {fps}", True, WHITE)
    screen.blit(text, [OVERLAY_X, OVERLAY_Y])


def init(screen: pygame.Surface) -> tuple[list[Point], Point]:
    point1 = Point(
        random.randrange(screen.get_width()), random.randrange(screen.get_height())
    )
    point2 = Point(
        random.randrange(screen.get_width()), random.randrange(screen.get_height())
    )
    point3 = Point(
        random.randrange(screen.get_width()), random.randrange(screen.get_height())
    )
    start = Point(
        random.randrange(screen.get_width()), random.randrange(screen.get_height())
    )

    screen.fill(BLACK)
    pixel(screen, RED, point1)
    pixel(screen, RED, point2)
    pixel(screen, RED, point3)
    pixel(screen, WHITE, start)

    return [point1, point2, point3], start


def main():
    pygame.init()
    size = (SIZE_X, SIZE_Y)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Sierpinski Demo")
    vertices, current = init(screen)
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
                    vertices, current = init(screen)
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
        current = halfway(current, nextpoint(list(vertices)))

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
