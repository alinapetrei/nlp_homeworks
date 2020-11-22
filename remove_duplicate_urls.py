import json


def get_len(dictionary):
    list_urls = []
    for key in dictionary:
        list_urls += [u for u in dictionary[key]]
    return len(list_urls)


def get_list_urls_before_key(key):
    list_urls = list()
    for url_key in all_urls:
        if url_key == key:
            break
        else:
            list_urls += [url for url in all_urls[url_key]]
    return list_urls


with open('all_urls.json', 'r', encoding="utf8") as all_urls_json:
    all_urls = json.load(all_urls_json)

unique_urls = {}
for key_url in all_urls:
    for idx, url_value in enumerate(all_urls[key_url]):
        if url_value not in all_urls[key_url][:idx] and url_value not in get_list_urls_before_key(key_url):
            if key_url in unique_urls:
                unique_urls[key_url].append(url_value)
            else:
                unique_urls[key_url] = [url_value]

with open('unique_urls.json', 'w', encoding='utf-8') as json_file:
    json.dump(unique_urls, json_file, indent=4, ensure_ascii=False)

