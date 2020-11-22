from constants import Constants
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import RomanianStemmer


def tokenization(file_input):
    list_tokens = list()
    with open(file_input, 'r', encoding='utf-8') as file_in:
        lines = file_in.readlines()
        for line in lines[:5]:
            list_tokens += word_tokenize(line)
    return list_tokens


def lemmatization(list_tokens):
    wnl = RomanianStemmer()
    list_lemmas = list()
    for token in list_tokens:
        list_lemmas.append(wnl.stem(token))
    return list_lemmas


def parse_punctuation_from_list_tokens(list_tokens):
    return [token for token in list_tokens if token not in ('.', ',', '(', '-', ')', '!', '?')]


list_tokenization = tokenization(Constants.REVIEWS_TEXT)
list_tokenization_without_punctuation = parse_punctuation_from_list_tokens(list_tokenization)
print(list_tokenization_without_punctuation)
# print(lemmatization(list_tokenization_without_punctuation))
