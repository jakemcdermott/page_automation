from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


WAIT_DEFAULT = 5


class Page(object):
    def __init__(self, driver):
        self.driver = driver

        self._find = {}
        self._find['xpath'] = self.driver.find_element_by_xpath
        self._find['class'] = self.driver.find_element_by_class_name
        self._find['css'] = self.driver.find_element_by_css_selector
        self._find['id'] = self.driver.find_element_by_id
        self._find['name'] = self.driver.find_element_by_name
        self._find['tag'] = self.driver.find_element_by_tag_name

        self._find_all = {}
        self._find_all['xpath'] = self.driver.find_elements_by_xpath
        self._find_all['class'] = self.driver.find_elements_by_class_name
        self._find_all['css'] = self.driver.find_elements_by_css_selector
        self._find_all['id'] = self.driver.find_elements_by_id
        self._find_all['name'] = self.driver.find_elements_by_name
        self._find_all['tag'] = self.driver.find_elements_by_tag_name

        self._locators = {}
        self._locators['xpath'] = By.XPATH
        self._locators['class'] = By.CLASS_NAME
        self._locators['css'] = By.CSS_SELECTOR
        self._locators['id'] = By.ID
        self._locators['name'] = By.NAME
        self._locators['tag'] = By.TAG_NAME


    def find(self, locator, value, wait=WAIT_DEFAULT):
        """ Get WebElement  
        """
        if locator == 'element': 
            return value 

        if wait == 0:
            return self._find[locator](value)
        else:
            expected = ec.presence_of_element_located(
                (self._locators[locator], value))
            return WebDriverWait(self.driver, wait).until(expected)
            

    def find_all(self, locator, value):
        """ Get all WebElements of a certain value 
        """
        return list(self._find_all[locator](value))


    def click(self, locator, value):
        """ Single-click on a WebElement
        """
        element = self._find[locator](value)
        
        self.scroll_into_view(element)
        element.click()


    def double_click(self, locator, value):
        """ Double-click on a WebElement
        """
        element = self._find[locator](value)

        self.scroll_into_view(element)

        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.double_click(on_element=element)
        actions.perform()


    def select(self, locator, value, text):
        """ Select text option from a menu WebElement
        """
        element = self._find[locator](value)

        self.scroll_into_view(element)
        Select(element).select_by_visible_text(text)


    def send_keys(self, locator, value, text, clear=True):
        """ Enter text into provided element 
        """
        element = self._find[locator](value)

        self.scroll_into_view(element)

        if clear: 
            element.clear()

        element.send_keys(text)


    def hover(self, locator, value):
        """ Hover mouse cursor over a WebElement
        """
        element = self._find[locator](value)
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()


    def hover_click(self, locator, value):
        """ Move mouse cursor to element then click 
        """
        element = self._find[locator](value)
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.perform()


    def force_click(self, locator, value):
        """ Click location of WebElement 
        """
        element = self._find[locator](value)
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.move_to_element_with_offset(element, 0, 20).click()
        actions.perform()


    def force_double_click(self, locator, value):
        """ Double-click location of WebElement 
        """
        element = self._find[locator](value)
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.move_to_element_with_offset(element, 0, 20)
        actions.double_click(on_element=element)
        actions.perform()


    def get_current_focus(self):
        """ Get the WebElement that has the current focus 
        """
        return self.driver.execute_script("return document.activeElement;")


    def set_checkbox(self, locator, value, state):
        """ Set the state of a checkbox element
        """
        element = self._find[locator](value)

        if state != element.is_selected():
            element.click()


    def scroll_into_view(self, element):
        """ Scroll page until element is in view 
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)


    def get_page_source(self):
        """ Return the raw html source of the current page
        """
        return self.driver.page_source


    def refresh(self):
        """ Refresh the current page
        """
        self.driver.refresh()


    def wait_until_visible(self, locator, value, timeout):
        sel_locator = self._locators[locator]
        expected = ec.visibility_of_element_located((sel_locator, value))

        try:
            WebDriverWait(self.driver, timeout).until(expected)
            return
        except:
            raise ElementNotVisibleException
            

    def wait_until_clickable(self, locator, value, timeout):
        sel_locator = self._locators[locator]
        expected = ec.element_to_be_clickable((sel_locator, value))

        try:
            WebDriverWait(self.driver, timeout).until(expected)
            return
        except:
            raise ElementNotVisibleException
