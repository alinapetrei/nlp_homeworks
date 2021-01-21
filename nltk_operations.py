import os
import json
import string
from constants import Constants


def get_files_from_folder(folder_path):
    files = os.listdir(folder_path)
    return [file for file in files if file.startswith('review_page') and file.endswith('.json')]


def parse_jsons_file_reviews_to_binposro_inputuri(list_files_json):
    string_punctuation = r"""!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~👍🏻"""
    translator = str.maketrans(string_punctuation, ' ' * len(string_punctuation))

    for file_json in list_files_json:
        with open(os.path.join(Constants.LAST_REVIEW_PAGES_JSON_CLEAN, file_json), 'r', encoding="utf8") as json_file:
            print(file_json)
            json_data = json.load(json_file)
            for mobile_phone_url in json_data:
                count_reviews = 0
                try:
                    file_txt_name = '_'.join(
                        [s.lower() for s in json_data[mobile_phone_url]['page_1'][0]['mobile_phone_name'].split()]
                    )
                    for page in json_data[mobile_phone_url]:
                        for review in json_data[mobile_phone_url][page]:
                            if int(review['nr_stars']) != 3:
                                review_text = review['review_text'].translate(translator)
                                for i in range(2, 10):
                                    review_text.replace(i * '.', '')
                                with open(
                                        os.path.join(
                                            Constants.BIN_POSRO_INPUTURI_FOLDER,
                                            f'{file_txt_name}_{count_reviews + 1}_{int(review["nr_stars"])}.txt'
                                        ), 'w', encoding="utf8") as txt_file:
                                    txt_file.write(review_text)
                                count_reviews += 1
                except KeyError as e:
                    print(e)


file_jsons = get_files_from_folder(Constants.LAST_REVIEW_PAGES_JSON_CLEAN)
parse_jsons_file_reviews_to_binposro_inputuri(file_jsons)
