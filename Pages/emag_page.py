from Pages.Components.pagination import Pagination
from Pages.constants import PageConstants
from Driver import driver


class EmagPage:
    def __init__(self):
        self.pagination = Pagination(PageConstants.pagination_locator)
