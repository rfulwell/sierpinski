import sierpinski
import sierpinski.main


def test_version():
    assert sierpinski.__version__ == "0.1.0"


def test_nextpoint():
    size_x, size_y = 1000, 1000
    point1 = sierpinski.main.Point(size_x, size_y)
    point2 = sierpinski.main.Point(size_x, size_y)
    point3 = sierpinski.main.Point(size_x, size_y)
    next = sierpinski.main.nextpoint([point1, point2, point3])
    assert next in [point1, point2, point3]


def test_halfway_square():
    point1 = sierpinski.main.Point(0, 0)
    point2 = sierpinski.main.Point(10, 10)
    halfway = sierpinski.main.halfway(point1, point2)
    assert halfway.x == 5
    assert halfway.y == 5


def test_halfway_x_axis():
    point1 = sierpinski.main.Point(0, 0)
    point2 = sierpinski.main.Point(10, 0)
    halfway = sierpinski.main.halfway(point1, point2)
    assert halfway.x == 5
    assert halfway.y == 0


def test_halfway_y_axis():
    point1 = sierpinski.main.Point(0, 0)
    point2 = sierpinski.main.Point(0, 10)
    halfway = sierpinski.main.halfway(point1, point2)
    assert halfway.x == 0
    assert halfway.y == 5


def test_first_point_gets_red():
    # verify that the first point is assigned pure red as part of the base of our
    # pretty RGB triangle
    state = sierpinski.main.setup()
    assert sierpinski.main.RED == sierpinski.main.getcolor(
        state.vertices, state.vertices[0]
    )


def test_second_point_gets_red():
    # verify that the second point is assigned pure red as part of the base of our
    # pretty RGB triangle
    state = sierpinski.main.setup()
    assert sierpinski.main.RED == sierpinski.main.getcolor(
        state.vertices, state.vertices[1]
    )


def test_third_point_gets_blue():
    # verify that the third point is assigned pure blue at the top of our
    # pretty RGB triangle
    state = sierpinski.main.setup()
    assert sierpinski.main.BLUE == sierpinski.main.getcolor(
        state.vertices, state.vertices[2]
    )


def test_mid_point_gets_green():
    # verify that the middle point is assigned pure green in our
    # pretty RGB triangle
    state = sierpinski.main.setup()
    assert sierpinski.main.GREEN == sierpinski.main.getcolor(
        state.vertices, sierpinski.main.halfway(state.vertices[0], state.vertices[2])
    )
