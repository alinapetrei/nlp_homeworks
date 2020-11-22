from Driver import driver


class BaseComponent:
    def __init__(self, locator):
        self.__locator = locator

    @property
    def locator(self):
        return self.__locator

    @property
    def element(self):
        return driver.find_element_by_xpath(self.__locator)

    @property
    def window_height(self):
        return driver.get_window_size()['height']

    def scroll_to(self):
        driver.execute_script(f"window.scrollTo(0, {self.element.location['y'] - (self.window_height / 2) + 100});")
