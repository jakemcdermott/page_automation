#!/usr/bin/env python
import unittest

from selenium import webdriver

from page import Page


class TestPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.page = Page(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def setUp(self):
        self.driver.get('https://www.python.org')


class TestFind(TestPage):

    def test_find_with_css(self):
        e = self.page.find('css', '#about > a')
        self.assertEquals(e.text, 'About')

    def test_find_with_xpath(self):
        e = self.page.find('xpath', '//*[@id="downloads"]/a')
        self.assertEquals(e.text, 'Downloads')

    def test_find_with_id(self):
        e = self.page.find('id', 'documentation')
        self.assertEquals(e.text, 'Documentation')

    def test_find_with_name(self):
        e = self.page.find('name', 'q')
        self.assertEquals(e.get_attribute('placeholder'), 'Search')

    def test_find_with_class(self):
        e = self.page.find('class', 'search-button')
        self.assertEquals(e.text, 'GO')

    def test_find_with_tag(self):
        e = self.page.find('tag', 'h1')
        self.assertEquals(e.get_attribute('class'), 'site-headline')