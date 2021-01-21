from web_scrapper import WebScrapper

if __name__ == '__main__':
    web_scrapper = WebScrapper()
    # web_scrapper.get_all_urls()
    web_scrapper.get_reviews(all_pages=True)
