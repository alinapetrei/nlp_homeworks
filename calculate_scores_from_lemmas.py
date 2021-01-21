import json
import rowordnet
import pandas as pd
from constants import Constants

wrn = rowordnet.RoWordNet()


def calculate_scores(lemmas):
    scores = [0, 0, 0]
    for i in lemmas:
        ids = wrn.synsets(literal=i)
        if ids:
            for j in range(len(ids)):
                if wrn(ids[j]).sentiwn:
                    scores[0] += wrn(ids[j]).sentiwn[0]
                    scores[1] += wrn(ids[j]).sentiwn[1]
                    scores[2] += wrn(ids[j]).sentiwn[2]
    return scores[0]/len(lemmas), scores[1]/len(lemmas), scores[2]/len(lemmas)


# with open(Constants.LEMMAS_AND_POS_TAGGING, 'r', encoding="utf8") as json_file:
#     mobile_phones_lemmas_pos_tagging = json.load(json_file)

# for mobile_phone in mobile_phones_lemmas_pos_tagging:
#     lemmas_pos_tagging = mobile_phones_lemmas_pos_tagging[mobile_phone]
#     list_lemmas = [lemma_pos_tagging[1] for lemma_pos_tagging in lemmas_pos_tagging]

df_reviews = pd.read_csv('reviews.csv')

# print(df_reviews)

calculated_scores = list()
for _, row in df_reviews.iterrows():
    scores = calculate_scores(str(row['text review']).split())
    calculated_scores.append(1 if scores[0] >= scores[1] else 0)
df_reviews['calculated score'] = calculated_scores

df_reviews.to_csv('reviews_with_scores.csv')
