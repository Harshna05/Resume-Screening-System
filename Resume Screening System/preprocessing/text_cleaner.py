import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):

    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha()
        and word not in stop_words
    ]

    return " ".join(tokens)