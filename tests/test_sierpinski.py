import sierpinski
import sierpinski.main


def test_version():
    assert sierpinski.__version__ == "0.1.0"


def test_nextpoint():
    size_x, size_y = 1000, 1000
    point1 = sierpinski.main.Point(size_x, size_y)
    point2 = sierpinski.main.Point(size_x, size_y)
    point3 = sierpinski.main.Point(size_x, size_y)
    next = sierpinski.main.nextpoint(point1, point2, point3)
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
