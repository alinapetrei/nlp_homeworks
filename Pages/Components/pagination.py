from Pages.Components.base_component import BaseComponent
from Pages.Components.pagination_ul import PaginationUL


class Pagination(BaseComponent):
    def __init__(self, locator):
        super().__init__(locator)

        self.pagination_ul = PaginationUL(self.locator + "//ul")
