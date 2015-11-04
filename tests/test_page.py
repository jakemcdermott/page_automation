import pytest
from selenium import webdriver

from page import Page


@pytest.fixture(scope='module')
def page(request, driver):
    page = Page(driver)
    request.addfinalizer(driver.close)
    return page


@pytest.fixture(scope='function')
def pyhome(page):
    page.driver.get('https://www.python.org/')
    return page


@pytest.fixture(scope='function')
def pylogin(page):
    page.driver.get('https://www.python.org/accounts/login/')
    return page


@pytest.fixture(scope='function')
def pydocs(page):
    page.driver.get('https://docs.python.org/3/')
    return page


def test_find_with_css(pyhome):
    element = pyhome.find('css', '#about > a')
    assert(element.text == 'About')


def test_find_with_xpath(pyhome):
    element = pyhome.find('xpath', '//*[@id="downloads"]/a')
    assert(element.text == 'Downloads')


def test_find_with_id(pyhome):
    element = pyhome.find('id', 'documentation')
    assert(element.text == 'Documentation')


def test_find_with_name(pyhome):
    element = pyhome.find('name', 'q')
    assert(element.get_attribute('placeholder') == 'Search')


def test_find_with_class(pyhome):
    element = pyhome.find('class', 'search-button')
    assert(element.text == 'GO')


def test_find_with_tag(pyhome):
    element = pyhome.find('tag', 'h1')
    assert(element.get_attribute('class') == 'site-headline')


def test_find_all(pyhome):
    elements = pyhome.find_all('tag', 'nav')
    assert(len(elements) == 2)


def test_click(pyhome):
    # click the search button
    pyhome.click('css', '#submit')

    # a successful click takes us to the search results page
    expected_url = 'https://www.python.org/search/?q=&submit='

    assert(pyhome.driver.current_url == expected_url)


def test_double_click(pyhome):
    # click the search button
    pyhome.double_click('css', '#submit')

    # a successful click takes us to the search results page
    expected_url = 'https://www.python.org/search/?q=&submit='
    
    assert(pyhome.driver.current_url == expected_url)


def test_hover(pyhome):
    # hover over 'downloads' button without clicking
    pyhome.hover('css', '#downloads > a')

    # the 'all releases' button should now be visible
    sel = '#downloads > ul > li.tier-2.element-1 > a'

    expected = webdriver.support.expected_conditions\
    .visibility_of_element_located(('css selector', sel))

    webdriver.support.ui.WebDriverWait(pyhome.driver, 10).until(expected)

    element = pyhome.driver.find_element_by_css_selector(sel)

    assert(element.is_displayed())


def test_get_active_element(pyhome):
    pyhome.click('name', 'q')

    element = pyhome.get_active_element()
    assert(element.get_attribute('placeholder') == 'Search')


def test_send_keys(pyhome):
    pyhome.send_keys('name', 'q', 'foo')

    element = pyhome.find('name', 'q')
    assert(element.get_attribute('value') == 'foo')


def test_send_keys_clear(pyhome):
    pyhome.send_keys('name', 'q', 'foo')
    pyhome.send_keys('name', 'q', 'bar', clear=True)

    element = pyhome.find('name', 'q')
    assert(element.get_attribute('value') == 'bar')


def test_send_keys_noclear(pyhome):
    pyhome.send_keys('name', 'q', 'foo')
    pyhome.send_keys('name', 'q', 'bar', clear=False)

    element = pyhome.find('name', 'q')
    assert(element.get_attribute('value') == 'foobar')


def test_refresh(pyhome):
    e = pyhome.driver.find_element_by_name('q')
    e.send_keys('foo')

    pyhome.refresh()
    e = pyhome.driver.find_element_by_name('q')

    assert(e.get_attribute('value') == e.get_attribute('placeholder'))


def test_select(pydocs):
    sel = 'body > div:nth-child(1) > ul > li:nth-child(5) > span > select'
    pydocs.select('css', sel, '2.7')

    pydocs.driver.refresh()

    # a successful select takes us to the python 2.7 docs
    expected_url = 'https://docs.python.org/2.7/'
    assert(pydocs.driver.current_url == expected_url)


def test_set_checkbox(pylogin):
    e = pylogin.driver.find_element_by_css_selector('#id_remember')

    pylogin.set_checkbox('css', '#id_remember', True)
    assert(e.is_selected())

    pylogin.set_checkbox('css', '#id_remember', False)
    assert(not(e.is_selected()))

    pylogin.set_checkbox('css', '#id_remember', True)
    assert(e.is_selected())
