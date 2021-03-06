import random

import pygame

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


def drawpixel(surface, color, pos: Point) -> None:
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
    drawpixel(screen, RED, point1)
    drawpixel(screen, RED, point2)
    drawpixel(screen, BLUE, point3)
    drawpixel(screen, WHITE, start)

    return [point1, point2, point3], start


class State:
    screen: pygame.Surface
    fps: Framerate
    vertices: list[Point]
    current: Point


def main():
    state = setup()
    pygame.display.flip()

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    state.fps = Framerate()

    # -------- Main Program Loop -----------
    while not done:
        state, done = event_loop(state, done)

        # --- Game logic goes here
        state.current = halfway(state.current, nextpoint(list(state.vertices)))

        # --- Drawing code goes here
        drawpixel(state.screen, getcolor(state.vertices, state.current), state.current)
        drawfps(state.screen, state.fps)

        # --- Update the screen with what we've drawn
        pygame.display.flip()

        # --- Limit to user-defined frames per second
        # this is a hack, I should be able to use `fps` directly here
        clock.tick(int(f"{state.fps}"))


def setup():
    pygame.init()
    size = (SIZE_X, SIZE_Y)
    state = State
    state.screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Sierpinski Demo")
    state.vertices, state.current = init(state.screen)
    return state


def getcolor(vertices: list[Point], point: Point) -> list[int]:
    mid_point = distance_from_line(vertices, vertices[2]) / 2
    point_distance = distance_from_line(vertices, point)

    if point_distance < 0 or point_distance > 2 * mid_point:
        return WHITE

    if point_distance <= mid_point:
        red_gradient = min(1 - point_distance / mid_point, 1)
        green_gradient = min(point_distance / mid_point, 1)
        blue_gradient = 0
    else:
        red_gradient = 0
        green_gradient = 1 - ((point_distance - mid_point) / mid_point)
        blue_gradient = (point_distance - mid_point) / mid_point

    red = int(red_gradient * 255)
    green = int(green_gradient * 255)
    blue = int(blue_gradient * 255)
    return (red, green, blue)


def distance_from_line(line: list[Point], point: Point) -> float:
    import math

    # calculate the area of the parallelogram described by the line, where
    # A is list[0], B is list[1] and the point, C: |(B-A)*(C-A)|
    area = abs(
        (line[1].x - line[0].x) * (point.y - line[0].y)
        - (line[1].y - line[0].y) * (point.x - line[0].x)
    )
    # calculate the length of the base: sqrt((B-A)^2)
    base = math.sqrt((line[1].x - line[0].x) ** 2 + (line[1].y - line[0].y) ** 2)
    # return the height = area/base
    return area / base


def event_loop(state: State, done: bool):
    for event in pygame.event.get():  # User did something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state.vertices, state.current = init(state.screen)
                pygame.display.flip()
            if event.key == pygame.K_KP_MINUS:
                state.fps.down()
            if event.key == pygame.K_KP_PLUS:
                state.fps.up()
            if event.key == pygame.K_q:
                done = True
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    return state, done


if __name__ == "__main__":
    main()
