import re
import time
import sys
import json
import requests
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from constants import Constants
from driver import driver
from driver.driver_utils import DriverUtils
from pages.emag_page import EmagPage


class WebScrapper:
    def __init__(self):
        self.__mobile_phones_data = []
        self.__data_frame = None
        self.__emag_page = EmagPage()
        self.__driver_utils = DriverUtils()

    @property
    def mobile_phones_data(self):
        return self.__mobile_phones_data

    @property
    def data_frame(self):
        return self.__data_frame

    @data_frame.setter
    def data_frame(self, data_frame):
        self.__data_frame = data_frame

    @staticmethod
    def get_last_page_number():
        print(f"Se extrag numarul de pagini de la URL-ul {Constants.URL_EMAG_MOBILE_PHONES}...")

        source_code = requests.get(Constants.URL_EMAG_MOBILE_PHONES).text
        soup = BeautifulSoup(source_code, "html.parser")

        pagination = soup.find('ul', attrs={'class': 'pagination'})

        pagination_options = pagination.find_all_next("a", attrs={'class', 'js-change-page hidden-xs hidden-sm'})

        last_pagination_option = pagination_options[-1]

        last_page_number = last_pagination_option.get("data-page")

        return int(last_page_number)

    @staticmethod
    def write_to_json_file(json_path, dict_obj):
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(dict_obj, json_file, indent=4, ensure_ascii=False)

    def get_all_urls(self):
        all_urls_per_page = dict()
        last_page_number = self.get_last_page_number()

        for idx_page in range(1, last_page_number + 1):
            page_url = Constants.URL_EMAG_MOBILE_PHONES_PAGINATION.format(idx_page)

            print(f"Se extrag url-urile telefoanelor mobile de la URL-ul {page_url}...")

            page_source_code = requests.get(page_url).text

            soup = BeautifulSoup(page_source_code, "html.parser")

            mobile_phones_cards = soup.find_all('div', attrs={'class': 'card-item js-product-data'})

            urls = list()

            for mobile_phones_card in mobile_phones_cards:
                urls.append(mobile_phones_card.find('a', attrs={'class': 'js-product-url'}).get('href'))

            all_urls_per_page[page_url] = urls

        self.write_to_json_file(Constants.URLS_JSON_FILE_NAME, all_urls_per_page)

    @staticmethod
    def parse_div_title(div_title):
        title = div_title.replace('\n', '').strip()
        regex_result = re.findall('Telefon mobil ([\\w| ]+),', title)
        return regex_result[0] if regex_result else title

    def parse_p_old_price(self, p_old_price):
        old_price = p_old_price.find('s').find(text=True, recursive=False).replace('.', '')
        discount = self.get_text_if_not_none(p_old_price.find('span', attrs={'class': 'product-this-deal'}))
        if discount:
            for char in ['\n', '(', '-', ')', '%']:
                discount = discount.replace(char, '')
            discount = discount.strip()
        return old_price, discount

    @staticmethod
    def get_text_if_not_none(element):
        return element.text if element is not None else None

    def get_reviews(self, page=1, all_pages=False):
        with open(Constants.UNIQUE_URLS_JSON_FILE_NAME) as json_file:
            all_urls = json.load(json_file)

        with open(Constants.REVIEWS_JSON_FILE_NAME, 'r', encoding="utf8") as json_file:
            all_reviews = json.load(json_file)

        if not all_pages:
            all_urls = all_urls[Constants.URL_EMAG_MOBILE_PHONES_PAGINATION.format(page)]

        for page_url in all_urls:
            if page_url not in all_reviews:
                all_reviews[page_url] = dict()
            for mobile_phone_url in all_urls[page_url]:
                print(f"Se extrag datele de la URL-ul {mobile_phone_url}...")

                driver.get(mobile_phone_url)

                page_source_code = driver.page_source

                soup = BeautifulSoup(page_source_code, "html.parser")

                div_title = soup.find('h1', attrs={'class': 'page-title'})

                mobile_phone_name = WebScrapper.parse_div_title(div_title.text)

                pagination = self.__emag_page.pagination

                all_reviews[page_url][mobile_phone_url] = dict()

                page_nr = 0
                while True:
                    time.sleep(1.5)
                    try:
                        pagination.scroll_to()
                    except NoSuchElementException as e:
                        print(e)
                        break

                    page_source_code = driver.page_source

                    soup = BeautifulSoup(page_source_code, "html.parser")

                    review_items = soup.find_all('div', attrs={'class': 'product-review-item'})

                    print(f"Se extrag review-urile de pe pagina {page_nr + 1}...")

                    reviews = list()
                    for review_item in review_items:
                        div_rating = review_item.find('div', attrs={'class': 'star-rating'})
                        div_rating_classes = div_rating.get('class')

                        result_regex = re.search('rated-(\\d)', ' '.join(div_rating_classes))
                        if result_regex:
                            nr_stars = result_regex.group(1)
                        else:
                            nr_stars = None

                        review_text = review_item.find('div', attrs={'class': 'js-review-body'}).text

                        reviews.append({
                            'mobile_phone_name': mobile_phone_name,
                            'nr_stars': nr_stars,
                            'review_text': review_text
                        })
                    all_reviews[page_url][mobile_phone_url][f"page_{page_nr + 1}"] = reviews
                    try:
                        if not pagination.pagination_ul.click_on_last_next_page_if_not_disabled():
                            break
                    except IndexError as e:
                        print(e)
                        break
                    page_nr += 1
                self.write_to_json_file(Constants.REVIEWS_JSON_FILE_NAME, all_reviews)
