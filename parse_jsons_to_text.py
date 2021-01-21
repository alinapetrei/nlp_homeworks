import os
import json
import string
from constants import Constants


def get_files_from_folder(folder_path):
    files = os.listdir(folder_path)
    return [file for file in files if file.startswith('review_page') and file.endswith('.json')]


def parse_list_files_json_to_text(list_files_json):
    """
        Preia toate review-urile din fisierele JSON din folderul review_pages_json pentru fiecare telefon mobil
        Si le pune in fisiere text, in folderul 'inputuri' din folderul 'bin_posro' care se ocupa cu tagging-ul
    """
    string_punctuation = r"""!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~👍🏻"""
    translator = str.maketrans(string_punctuation, ' ' * len(string_punctuation))
    if not os.path.isdir(Constants.REVIEWS_PAGES_TEXT):
        os.mkdir(Constants.REVIEWS_PAGES_TEXT)

    for file_json in list_files_json:
        with open(os.path.join(Constants.REVIEWS_CLEAN_FOLDER, file_json), 'r', encoding="utf8") as json_file:
            json_data = json.load(json_file)
            for mobile_phone_url in json_data:
                if 'page_1' in json_data[mobile_phone_url]:
                    file_txt = '_'.join([s.lower() for s in json_data[mobile_phone_url]['page_1'][0]['mobile_phone_name'].split()])
                    list_data = list()
                    for reviews_page in json_data[mobile_phone_url]:
                        for review in json_data[mobile_phone_url][reviews_page]:
                            review_text = review['review_text'].translate(translator)
                            for i in range(2, 10):
                                review_text.replace(i * '.', '')
                            list_data.append(review_text)
                    with open(os.path.join(Constants.BIN_POSRO_INPUTURI_FOLDER, f'{file_txt}.txt'), 'w', encoding="utf8") as txt_file:
                        txt_file.writelines(list_data)


file_jsons = get_files_from_folder(Constants.REVIEWS_FOLDER)
parse_list_files_json_to_text(file_jsons)
