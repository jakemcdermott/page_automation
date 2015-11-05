import time

import pytest

from docker import Client
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def pytest_addoption(parser):
    parser.addoption(
        '--browser', 
        action='store', 
        default='firefox', 
        help='browser used to run the tests')


@pytest.fixture(scope='module')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='module')
def driver(request, browser):
    """ Fixture for selenium Webdriver using docker
    """
    if browser == 'firefox':
        browser_image = 'selenium/standalone-firefox'
        browser_dc = DesiredCapabilities.FIREFOX
    elif browser == 'chrome':
        browser_image = 'selenium/standalone-chrome'
        browser_dc= DesiredCapabilities.CHROME

    cli = Client(version='auto')

    port_conf = cli.create_host_config(
        publish_all_ports=True, 
        port_bindings={4444: ('127.0.0.1',)})


    container = cli.create_container(
        image=browser_image, ports=[4444], detach=True, host_config=port_conf)

    cli.start(container.get('Id'))
    request.addfinalizer(lambda: cli.stop(container.get('Id')))

    #import pdb; pdb.set_trace()

    port_info = cli.port(container['Id'], 4444)[0]
    selenium_host = 'http://{}:{}/wd/hub'.format(
        port_info['HostIp'], port_info['HostPort'])

    time.sleep(8) # TODO: Not this

    driver = webdriver.Remote(
        command_executor=selenium_host, desired_capabilities=browser_dc)

    return driver