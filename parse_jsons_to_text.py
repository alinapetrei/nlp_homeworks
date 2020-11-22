import os
import json
from constants import Constants


def get_files_from_folder(folder_path):
    files = os.listdir(folder_path)
    return [file for file in files if file.startswith('reviews_page') and file.endswith('.json')]


def parse_list_files_json_to_text(list_files_json):
    txt_file = open('reviews_text.txt', 'w', encoding='utf-8')
    for file_json in list_files_json:
        with open(os.path.join(Constants.REVIEWS_FOLDER, file_json), 'r', encoding="utf8") as json_file:
            json_data = json.load(json_file)
            for page in json_data:
                for mobile_phone_url in json_data[page]:
                    for reviews_page in json_data[page][mobile_phone_url]:
                        for review in json_data[page][mobile_phone_url][reviews_page]:
                            txt_file.write(review['review_text'] + '\n')
    txt_file.close()


file_jsons = get_files_from_folder(Constants.REVIEWS_FOLDER)
parse_list_files_json_to_text(file_jsons)
