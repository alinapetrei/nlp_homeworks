from Pages.Components.base_component import BaseComponent, driver


class PaginationUL(BaseComponent):
    def __init__(self, locator):
        super().__init__(locator)

    def get_li_nodes(self):
        li_nodes = driver.find_elements_by_xpath(self.locator + '//li')
        return li_nodes

    @staticmethod
    def is_disabled(element):
        return 'disabled' in element.get_attribute("class")

    def click_on_last_next_page_if_not_disabled(self):
        try:
            last_li_node = self.get_li_nodes()[-1]
            if not self.is_disabled(last_li_node):
                last_li_node.click()
                return True
            return False
        except:
            return False
