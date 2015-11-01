#!/usr/bin/env python
import base64
import time
import unittest

from PIL import Image
from StringIO import StringIO

from selenium import webdriver

from page import Page


class TestPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.page = Page(webdriver.Firefox())


    @classmethod
    def tearDownClass(cls):
        cls.page.driver.close()


    def setUp(self):
        self.page.driver.get('https://www.python.org')


    def test_find_with_css(self):
        element = self.page.find('css', '#about > a')
        self.assertEquals(element.text, 'About')


    def test_find_with_xpath(self):
        element = self.page.find('xpath', '//*[@id="downloads"]/a')
        self.assertEquals(element.text, 'Downloads')


    def test_find_with_id(self):
        element = self.page.find('id', 'documentation')
        self.assertEquals(element.text, 'Documentation')


    def test_find_with_name(self):
        element = self.page.find('name', 'q')
        self.assertEquals(element.get_attribute('placeholder'), 'Search')


    def test_find_with_class(self):
        element = self.page.find('class', 'search-button')
        self.assertEquals(element.text, 'GO')


    def test_find_with_tag(self):
        element = self.page.find('tag', 'h1')
        self.assertEquals(element.get_attribute('class'), 'site-headline')


    def test_find_all(self):
        elements = self.page.find_all('tag', 'nav')
        self.assertEqual(len(elements), 2)


    def test_scroll_into_view(self):
        # scroll to element at very bottom of page
        element = self.page.find('css', '#site-map > div.site-base')
        self.page.scroll_into_view(element)

        # get screenshot data
        img = Image.open(
            StringIO(base64.decodestring(
                self.page.driver.get_screenshot_as_base64())))

        # get rgb color of bottom right pixel 
        rgb = img.getpixel((img.size[0]-1, img.size[1]-1))[0:3]

        # compare pixel color to an expected css hex value
        self.assertEquals(''.join(map(chr, rgb)).encode('hex'), '2b5982')


    def test_click(self):
        # click the search button
        self.page.click('css', '#submit')

        # a successful click takes us to the search results page
        self.assertEquals(
            self.page.driver.current_url, 
            'https://www.python.org/search/?q=&submit=')


    def test_double_click(self):
        # click the search button
        self.page.double_click('css', '#submit')

        # a successful click takes us to the search results page
        self.assertEquals(
            self.page.driver.current_url, 
            'https://www.python.org/search/?q=&submit=')


    def test_hover(self):
        # hover over 'downloads' button without clicking
        self.page.hover('css', '#downloads > a')

        # the 'all releases' button should now be visible
        expected = webdriver.support.expected_conditions\
        .visibility_of_element_located((
            'css selector', '#downloads > ul > li.tier-2.element-1 > a'))

        try:
            webdriver.support.ui.WebDriverWait(
                self.page.driver, 10).until(expected)
        except:
            self.fail('element expected to be visible')


    def test_get_active_element(self):
        self.page.click('name', 'q')

        element = self.page.get_active_element()
        self.assertEquals(element.get_attribute('placeholder'), 'Search')


    def test_send_keys(self):
        self.page.send_keys('name', 'q', 'foo')

        element = self.page.find('name', 'q')
        self.assertEquals(element.get_attribute('value'), 'foo')


    def test_send_keys_clear(self):
        self.page.send_keys('name', 'q', 'foo')
        self.page.send_keys('name', 'q', 'bar', clear=True)

        element = self.page.find('name', 'q')
        self.assertEquals(element.get_attribute('value'), 'bar')


    def test_send_keys_noclear(self):
        self.page.send_keys('name', 'q', 'foo')
        self.page.send_keys('name', 'q', 'bar', clear=False)

        element = self.page.find('name', 'q')
        self.assertEquals(element.get_attribute('value'), 'foobar')


    def test_refresh(self):
        element = self.page.driver.find_element_by_name('q')
        element.send_keys('foo')

        self.page.refresh()

        element = self.page.driver.find_element_by_name('q')

        self.assertEquals(
            element.get_attribute('value'), 
            element.get_attribute('placeholder'))


    def test_select(self):
        self.page.driver.get('https://docs.python.org/3/')

        sel = 'body > div:nth-child(1) > ul > li:nth-child(5) > span > select'
        self.page.select('css', sel, '2.7')

        self.page.driver.refresh()

        # a successful select takes us to the python 2.7 docs
        self.assertEquals(
            self.page.driver.current_url, 'https://docs.python.org/2.7/')


    def test_set_checkbox(self):
        self.page.driver.get('https://www.python.org/accounts/login/')

        e = self.page.driver.find_element_by_css_selector('#id_remember')

        self.page.set_checkbox('css', '#id_remember', True)
        self.assertTrue(e.is_selected())

        self.page.set_checkbox('css', '#id_remember', False)
        self.assertFalse(e.is_selected())

        self.page.set_checkbox('css', '#id_remember', True)
        self.assertTrue(e.is_selected())

