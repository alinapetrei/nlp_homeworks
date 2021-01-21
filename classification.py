import pandas as pd
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score

df = pd.read_csv('reviews_with_scores.csv')

mobile_phones_reviews = dict()

df = df.dropna()

for index, row in df.iterrows():
    if row['mobile phone name'] in mobile_phones_reviews:
        mobile_phones_reviews[row['mobile phone name']]['text review'] += ' ' + str(row['text review'])
        mobile_phones_reviews[row['mobile phone name']]['total reviews'] += 1
        mobile_phones_reviews[row['mobile phone name']]['positive reviews'] += 1 if row['calculated score'] == 1 else 0
        mobile_phones_reviews[row['mobile phone name']]['negative reviews'] += 1 if row['calculated score'] == 0 else 0
    else:
        mobile_phones_reviews[row['mobile phone name']] = {
            'text review': str(row['text review']),
            'total reviews': 1,
            'positive reviews': 1 if row['calculated score'] == 1 else 0,
            'negative reviews': 1 if row['calculated score'] == 0 else 1
        }

independent_var = df['text review']
dependent_var = df['stars score']

IV_train, IV_test, DV_train, DV_test = train_test_split(independent_var, dependent_var, test_size=0.3, random_state=225)

print('IV_train :', len(IV_train))
print('IV_test :', len(IV_test))
print('DV_train :', len(DV_train))
print('DV_test :', len(DV_test))

tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver="lbfgs")

model = Pipeline([('vectorizer', tvec), ('classifier', clf2)])
model.fit(IV_train, DV_train)
predictions = model.predict(IV_test)
confusion_matrix(predictions, DV_test)

print("Accuracy : ", accuracy_score(predictions, DV_test))
print("Precision : ", precision_score(predictions, DV_test, average='weighted'))
print("Recall : ", recall_score(predictions, DV_test, average='weighted'))

predictions = []
for key, value in mobile_phones_reviews.items():
    predictions.append([
        key,
        model.predict([value['text review']])[0],
        value['total reviews'],
        value['positive reviews'],
        value['negative reviews']
    ])

df = pd.DataFrame(predictions, columns=[
    'mobile phone name',
    'classification',
    'total reviews',
    'positive reviews',
    'negative reviews'
])

df.to_csv('classifications.csv', index=False)
