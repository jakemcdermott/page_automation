import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False, 
        help="run tests in headlss mode")

    parser.addoption(
        "--size_x", 
        action="store", 
        default=1920, 
        help="headless virtual screen pixel width")

    parser.addoption(
        "--size_y", 
        action="store", 
        default=1080, 
        help="headless virtual screen pixel height")


@pytest.fixture(scope='session')
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture(scope='session')
def size_x(request):
    return request.config.getoption("--size_x")


@pytest.fixture(scope='session')
def size_y(request):
    return request.config.getoption("--size_y")


@pytest.fixture(scope='session')
def display(request, headless, size_x, size_y):
    if headless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(size_x, size_y))
        display.start()
        request.addfinalizer(display.stop)