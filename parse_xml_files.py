import os
import json
import pandas as pd
from constants import Constants
from xml.etree.ElementTree import ElementTree

xml_files = os.listdir(Constants.BIN_POSRO_OUTPUTURI_FOLDER)

tree = ElementTree()

stopwords = open('stopwords.txt', 'r', encoding='UTF-8').readlines()
stopwords = [stopword.replace('\n', '') for stopword in stopwords]

dots = [i * '.' for i in range(1, 11)]
data = []
for xml_file in xml_files:
    lemmas = []
    tree.parse(os.path.join(Constants.BIN_POSRO_OUTPUTURI_FOLDER, xml_file))
    sentences = tree.findall('S')
    for sentence in sentences:
        words = sentence.findall('W')
        for word in words:
            if word.text not in dots and word.text not in stopwords:
                lemmas.append(word.get('LEMMA').lower())
    mobile_phone_name = ' '.join(xml_file.split('.')[0].split('_')[:-2])
    score = xml_file.split('.')[0].split('_')[-1]
    data.append([mobile_phone_name, ' '.join(lemmas), 0 if int(score) <= 2 else 1])

df = pd.DataFrame(data, columns=['mobile phone name', 'text review', 'stars score'], )

df.to_csv('reviews.csv', index=False)
