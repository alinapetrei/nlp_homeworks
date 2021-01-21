import json
from constants import Constants


def split_big_json_in_json_pages(json_file_path):
    with open(json_file_path, 'r', encoding="utf8") as json_file:
        all_reviews = json.load(json_file)

    count = 1
    for reviews_page in all_reviews:
        with open(f'review_pages_json/review_page_nr{count}.json', 'w', encoding="utf8") as json_file_page:
            json.dump(all_reviews[reviews_page], json_file_page, indent=4, ensure_ascii=False)
        count += 1


split_big_json_in_json_pages(Constants.REVIEWS_JSON_FILE_NAME)
